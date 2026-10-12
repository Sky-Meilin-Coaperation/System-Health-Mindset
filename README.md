# SkyOS Workspace Setup & Architecture

Das **SkyOS-Ökosystem** ist eine modulare, containerbasierte und sicherheitszentrierte Plattform für KI-gestützte Workflow-Orchestrierung, plattformübergreifende Visualisierung (Flutter) und fälschungssichere WORM-Governance.

---

## 🏗️ Hauptkomponenten

1. **Planer Agent & Multi-Model Router:**
   - Dynamisches Routing von Prompts an **LM Studio** (Port 1234, schweres Reasoning) und **Ollama** (Port 11434, schnelle Klassifikation).
   - Normen- & Compliance-Prüfung nach **DIN 14505** und **DIN 30722-1** für BOS/KRITIS-Abrollbehälter.

2. **WISSENSSTUFEN (L0–L4 Tiered Data Management):**
   - Basierend auf *Data-Model Co-Evolution* (arXiv 2602.09003).
   - Transformation von Rohdaten (L0) zu verifiziertem, strukturiertem Wissen (L4 Master-Manifest).

3. **WORM-Audit-Ledger:**
   - Append-only JSONL-Ledger mit SHA-256-Hash-Chain unter `data/L4_organized/worm_ledger.jsonl`.
   - Workflow-Start, Abschluss und Fehler werden protokolliert; abgeschlossene Ergebnisse werden über ihren SHA-256-Hash referenziert.
   - `GET /api/v1/audit/worm` prüft Sequenz, Verkettung und Eintragshashes; `WORM_LEDGER_PATH` kann den Ledger-Pfad überschreiben.
   - Das Ledger ist manipulations-erkennbar, aber ohne extern verankerte Signatur oder unveränderlichen Speicher kein kryptografischer Beweis gegen privilegierte Änderungen an der gesamten Datei.

4. **Fortschritts-Tracker & Telemetrie:**
   - Interaktive SQLite-Datenbank (`progress_tracker.db`) gekoppelt mit WORM-Events.
   - Offline-Pufferung (FIFO) von Telemetrie- und Fehlerdaten.

---

## 🚀 Schnelleinstieg (WSL / Ubuntu)

```bash
# 1. In das Arbeitsverzeichnis wechseln
cd "/mnt/c/Workspace LM studio"

# 2. Fortschritts-Datenbank initialisieren
python3 [verdächtiger Link entfernt] init

# 3. Aktuellen Setup-Status anzeigen
python3 [verdächtiger Link entfernt] list
```

## System Health Evolution – The Box

The repository includes a runnable FastAPI operations core with a browser dashboard, live runtime telemetry, and an extensible workflow registry. The built-in `system-diagnostic` workflow captures a fresh telemetry snapshot; new workflow actions can be registered in `system_health/workflows.py`.

Run locally with Python:

```bash
pip install -r REQUIREMENTS.txt
uvicorn app:app --reload
```

Open `http://localhost:8000` for the dashboard, `http://localhost:8000/docs` for the API, and `http://localhost:8000/health` for the container health check. Build and run the same core with `docker compose up --build`.

The telemetry endpoint reports the core process uptime, filesystem usage, processor count and load average where supported, and memory usage. It prefers a configured container memory limit and otherwise reports host memory on Linux; unavailable metrics are reported as unavailable rather than inferred.

Run the WORM ledger and workflow audit tests with `python -m unittest discover -v`.

---

## 📜 Lizenz
Dieses Projekt steht unter der **SkyOS Sustainable Use License v1.0** (siehe `LICENSE`). Freie interne Nutzung und Entwicklung gestattet; kommerzieller SaaS-Dienstbetrieb für Dritte ist eingeschränkt.
