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

3. **WORM Security Agent & Prioritätsnachweis:**
   - Fälschungssichere Append-Only SHA-256 Hash-Chain (`data/L4_organized/worm_ledger.jsonl`).
   - Mathematischer **Proof of Prior Art** zur rechtlichen Absicherung gegen Fremd-Claiming.

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

---

## 📜 Lizenz
Dieses Projekt steht unter der **SkyOS Sustainable Use License v1.0** (siehe `LICENSE`). Freie interne Nutzung und Entwicklung gestattet; kommerzieller SaaS-Dienstbetrieb für Dritte ist eingeschränkt.
