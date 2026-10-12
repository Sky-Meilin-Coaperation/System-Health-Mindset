import hashlib
import json
from typing import Any
from uuid import uuid4

from system_health.worm import append_event


class AuditInputError(ValueError):
    """Raised when a forensic audit request does not meet the input contract."""


def _document_agent(evidence: Any) -> dict[str, Any]:
    if not isinstance(evidence, list) or not evidence:
        raise AuditInputError("evidence must be a non-empty list.")
    if len(evidence) > 100:
        raise AuditInputError("evidence may contain at most 100 items.")

    captured = []
    seen_ids: set[str] = set()
    total_content_bytes = 0
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            raise AuditInputError(f"evidence[{index}] must be an object.")
        evidence_id = item.get("id")
        source = item.get("source")
        content = item.get("content")
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            raise AuditInputError(f"evidence[{index}].id is required.")
        if evidence_id in seen_ids:
            raise AuditInputError(f"Duplicate evidence id: {evidence_id}.")
        if not isinstance(source, str) or not source.strip():
            raise AuditInputError(f"evidence[{index}].source is required.")
        if not isinstance(content, str) or not content:
            raise AuditInputError(f"evidence[{index}].content must be a non-empty string.")
        content_bytes = content.encode("utf-8")
        if len(content_bytes) > 65536:
            raise AuditInputError(f"evidence[{index}].content exceeds 64 KiB.")
        total_content_bytes += len(content_bytes)
        if total_content_bytes > 1_048_576:
            raise AuditInputError("Combined evidence content exceeds 1 MiB.")
        facts = item.get("facts", [])
        if not isinstance(facts, list):
            raise AuditInputError(f"evidence[{index}].facts must be a list.")
        try:
            json.dumps(facts, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise AuditInputError(f"evidence[{index}].facts must contain valid JSON values.") from exc

        seen_ids.add(evidence_id)
        content_hash = hashlib.sha256(content_bytes).hexdigest()
        supplied_hash = item.get("sha256")
        hash_matches = supplied_hash is None or supplied_hash == content_hash
        captured.append(
            {
                "id": evidence_id,
                "source": source,
                "content_sha256": content_hash,
                "provided_sha256_matches": hash_matches,
                "facts": facts,
            }
        )

    return {
        "agent": "document-custodian",
        "status": "completed",
        "evidence_count": len(captured),
        "evidence": captured,
        "findings": [
            {
                "severity": "high",
                "code": "evidence-hash-mismatch",
                "evidence_id": item["id"],
                "message": "The supplied SHA-256 does not match the submitted content.",
            }
            for item in captured
            if not item["provided_sha256_matches"]
        ],
    }


def _analyst_agent(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    values_by_key: dict[str, list[dict[str, Any]]] = {}
    findings = []
    for item in evidence:
        for fact in item["facts"]:
            if not isinstance(fact, dict):
                findings.append(
                    {
                        "severity": "medium",
                        "code": "invalid-fact",
                        "evidence_id": item["id"],
                        "message": "A fact must be an object with fact_key and value.",
                    }
                )
                continue
            fact_key = fact.get("fact_key")
            if not isinstance(fact_key, str) or not fact_key.strip() or "value" not in fact:
                findings.append(
                    {
                        "severity": "medium",
                        "code": "invalid-fact",
                        "evidence_id": item["id"],
                        "message": "A fact must include a non-empty fact_key and a value.",
                    }
                )
                continue
            values_by_key.setdefault(fact_key, []).append(
                {"evidence_id": item["id"], "value": fact["value"]}
            )

    for fact_key, values in values_by_key.items():
        distinct_values = {repr(item["value"]) for item in values}
        if len(distinct_values) > 1:
            findings.append(
                {
                    "severity": "high",
                    "code": "conflicting-facts",
                    "fact_key": fact_key,
                    "evidence": values,
                    "message": "Evidence contains different values for the same fact.",
                }
            )

    return {
        "agent": "evidence-analyst",
        "status": "completed",
        "findings": findings,
    }


def _expert_agent(
    document_result: dict[str, Any], analyst_result: dict[str, Any]
) -> dict[str, Any]:
    findings = [
        {
            "severity": "medium",
            "code": "source-not-authenticated",
            "message": "Evidence source identity and publication time have not been independently verified.",
        },
        {
            "severity": "medium",
            "code": "no-external-trust-anchor",
            "message": "The local WORM hash chain has no external signature or trusted timestamp configured.",
        },
        {
            "severity": "low",
            "code": "content-not-retained",
            "message": "Only evidence fingerprints and declared facts are retained in the audit event; keep original files separately.",
        },
    ]
    if document_result["findings"] or analyst_result["findings"]:
        findings.append(
            {
                "severity": "high",
                "code": "evidence-quality-issues",
                "message": "The document or analyst stage reported evidence-quality issues.",
            }
        )
    return {
        "agent": "technical-reviewer",
        "status": "completed",
        "scope": "Deterministic provenance and consistency checks; not legal advice or certification.",
        "findings": findings,
    }


def _ombuds_agent(
    document_result: dict[str, Any],
    analyst_result: dict[str, Any],
    expert_result: dict[str, Any],
) -> dict[str, Any]:
    evidence_findings = document_result["findings"] + analyst_result["findings"]
    if any(item["severity"] == "high" for item in evidence_findings):
        status = "hold"
        rationale = "Resolve high-severity evidence-integrity or consistency findings before relying on this audit."
        actions = [
            "Correct or explain every high-severity evidence finding.",
            "Retain the original evidence files and verify their fingerprints.",
            "Obtain independent source and timestamp verification.",
        ]
    else:
        status = "conditional"
        rationale = "No high-severity internal inconsistency was found, but source authenticity and trusted time are unverified."
        actions = [
            "Have a human reviewer confirm the sources and facts.",
            "Retain the original evidence files.",
            "Configure an external signature or trusted timestamp before treating the record as independently anchored.",
        ]

    return {
        "agent": "ombuds-reviewer",
        "status": "completed",
        "decision": status,
        "rationale": rationale,
        "required_actions": actions,
        "limitations": expert_result["findings"],
    }


def run_forensic_audit(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise AuditInputError("Audit request must be an object.")
    case_id = payload.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip() or len(case_id) > 120:
        raise AuditInputError("case_id must be a non-empty string up to 120 characters.")

    document_result = _document_agent(payload.get("evidence"))
    analyst_result = _analyst_agent(document_result["evidence"])
    expert_result = _expert_agent(document_result, analyst_result)
    decision = _ombuds_agent(document_result, analyst_result, expert_result)
    report = {
        "audit_id": str(uuid4()),
        "case_id": case_id,
        "status": decision["decision"],
        "agents": [
            document_result,
            analyst_result,
            expert_result,
            decision,
        ],
    }
    audit_entry = append_event(
        {
            "event_type": "forensic.audit.completed",
            "audit_id": report["audit_id"],
            "case_id": case_id,
            "status": report["status"],
            "report": report,
        }
    )
    report["worm_audit"] = {
        "sequence": audit_entry["sequence"],
        "hash": audit_entry["hash"],
    }
    return report
