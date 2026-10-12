import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app
from system_health import workflows
from system_health.worm import LedgerIntegrityError, append_event, verify_ledger


class WormLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ledger_path = Path(self.temp_dir.name) / "worm_ledger.jsonl"
        self.path_patcher = patch.dict(os.environ, {"WORM_LEDGER_PATH": str(self.ledger_path)})
        self.path_patcher.start()

    def tearDown(self) -> None:
        self.path_patcher.stop()
        self.temp_dir.cleanup()

    def test_appends_linked_entries_and_verifies(self) -> None:
        first = append_event({"event_type": "test.created", "value": 1})
        second = append_event({"event_type": "test.updated", "value": 2})

        self.assertEqual(first["sequence"], 1)
        self.assertEqual(second["sequence"], 2)
        self.assertEqual(second["previous_hash"], first["hash"])
        self.assertEqual(len(first["hash"]), 64)
        self.assertEqual(
            verify_ledger(),
            {"valid": True, "entry_count": 2, "head_hash": second["hash"]},
        )

    def test_detects_modified_entry(self) -> None:
        append_event({"event_type": "test.created", "value": 1})
        raw_entry = json.loads(self.ledger_path.read_text(encoding="utf-8"))
        raw_entry["event"]["value"] = 999
        self.ledger_path.write_text(json.dumps(raw_entry) + "\n", encoding="utf-8")

        report = verify_ledger()
        self.assertFalse(report["valid"])
        with self.assertRaises(LedgerIntegrityError):
            append_event({"event_type": "test.append"})

    def test_rejects_incomplete_trailing_entry(self) -> None:
        append_event({"event_type": "test.created"})
        with self.ledger_path.open("ab") as ledger_file:
            ledger_file.write(b'{"sequence":2}')

        self.assertFalse(verify_ledger()["valid"])

    def test_concurrent_appends_keep_a_contiguous_chain(self) -> None:
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(
                executor.map(
                    lambda value: append_event({"event_type": "test.concurrent", "value": value}),
                    range(32),
                )
            )

        report = verify_ledger()
        self.assertTrue(report["valid"])
        self.assertEqual(report["entry_count"], 32)

    def test_workflow_logs_start_and_result_hash(self) -> None:
        action = lambda payload: {"answer": payload["question"]}
        workflow = ("Test", "Test workflow audit.", action)
        with patch.dict(workflows._WORKFLOWS, {"test-audit": workflow}):
            result = workflows.run_workflow("test-audit", {"question": "ok"})

        lines = self.ledger_path.read_text(encoding="utf-8").splitlines()
        entries = [json.loads(line) for line in lines]
        self.assertEqual([entry["event"]["event_type"] for entry in entries], [
            "workflow.started",
            "workflow.completed",
        ])
        result_hash = hashlib.sha256(
            json.dumps(
                result["result"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(entries[-1]["event"]["result_sha256"], result_hash)
        self.assertEqual(result["audit"]["hash"], entries[-1]["hash"])

    def test_failed_workflow_is_audited_without_logging_error_text(self) -> None:
        def fail(_payload):
            raise RuntimeError("sensitive message")

        with patch.dict(workflows._WORKFLOWS, {"test-failure": ("Test", "Failure", fail)}):
            with self.assertRaisesRegex(RuntimeError, "sensitive message"):
                workflows.run_workflow("test-failure", {})

        entries = [json.loads(line) for line in self.ledger_path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(
            [entry["event"]["event_type"] for entry in entries],
            ["workflow.started", "workflow.failed"],
        )
        self.assertEqual(entries[-1]["event"]["error_type"], "RuntimeError")
        self.assertNotIn("sensitive message", self.ledger_path.read_text(encoding="utf-8"))

    def test_audit_endpoint_reports_ledger_status(self) -> None:
        append_event({"event_type": "test.endpoint"})
        response = TestClient(app).get("/api/v1/audit/worm")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["valid"])
        self.assertEqual(response.json()["entry_count"], 1)


if __name__ == "__main__":
    unittest.main()
