# Governance des SkyOS-Projekts

Das SkyOS-Agentic-Framework arbeitet nach einem offenen Governance-Modell, das von den Charta-Prinzipien der Node.js- und OpenJS-Foundation inspiriert ist. Dieses Dokument beschreibt die konsensbasierte Entscheidungsfindung, die Rollen der Beitragenden und den Entscheidungsrahmen des Projekts.

---

## 1. Technische Steuerung und Leitung

Das Projekt wird von den Core Maintainers geleitet, die die technische Ausrichtung, die Sicherheitskonformität (KRITIS-/Air-Gap-Standards) und die architektonische Integrität der SkyOS-Agentic-Runtime überwachen.

### Verantwortlichkeiten:
* Überwachung architektonischer Entscheidungen, Protokoll-Definitionen (MCP, WebSocket-Spezifikationen) und der Stabilität der Core-APIs.
* Verwaltung von Repository-Releases, Continuous-Integration-Pipelines und CodeQL-Sicherheitsgates.
* Schlichtung von RFCs (Request for Comments) und technischen Meinungsverschiedenheiten durch konsensorientierte Entscheidungsfindung.
* Wahrung des Vulnerability-Disclosure-Prozesses in Abstimmung mit den zuständigen CVE-Programmen.

---

## 2. Rollen der Beitragenden

### Beitragende
Jede Person, die Code, Issues, Dokumentation oder Reviews einreicht. Alle Beiträge unterliegen streng den architektonischen Richtlinien und den Anforderungen an die Domänenunabhängigkeit des Projekts.

### Mitarbeiter / Maintainer
Personen, denen Zugriff auf die Hauptbranches und Triage-Rechte gewährt wurden. Mitarbeiter:
* Prüfen und mergen Pull Requests nach Qualitäts- und Sicherheitskriterien, die durch automatisierte Scans validiert wurden.
* Stellen sicher, dass keine proprietären Domänenzuordnungen in öffentliche Vektor-Interfaces gelangen.
* Verantwortlich für Issue-Triage und den Lebenszyklus von RFCs.

---

## 3. Entscheidungsfindung und RFC-Prozess

Änderungen an der Core-Runtime, an öffentlichen Vektorschemata oder an FastMCP-Tool-Definitionen erfolgen nach einem konsensorientierten Verfahren:

1. **Vorschlag (RFC):** Für Breaking Changes oder neue Subsystem-Module muss ein Issue im RFC-Template eröffnet werden.
2. **Review-Fenster:** Vorschläge bleiben für mindestens 72 Stunden offen, damit Maintainer und Beitragende sie prüfen können.
3. **Konsens:** Wesentliche Entscheidungen erfordern einen allgemeinen oder breiten Konsens unter den Core Maintainers. Wenn kein Konsens erreicht werden kann, besitzt der Lead Maintainer die endgültige Entscheidungshoheit.

---

## 4. Interessenkonflikte und Sicherheitsgrenzen

Zur Wahrung strenger IP-Schutz- und Sicherheitsanforderungen gilt:
* Öffentliche Beiträge sind strikt auf verallgemeinerte mathematische Graphenmechaniken, deterministische Vektorevaluatoren und Protokoll-Gateways begrenzt.
* Proprietäre Rechenmodule bleiben als optionale, geschlossene Binär-Plugins segregiert und sind ausdrücklich aus den öffentlichen Governance-Bereichen ausgeschlossen.
