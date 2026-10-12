# Sky Meilin – Allgemeine Wissensdatenbank Pascal
**Projekt:** SkyOS & Sky Meilin Ecosystem  
**Version:** v16.0 / L4 Organized  
**Urheber & Copyright:** (c) 2026 SkyOS / Pascal / Sky-Meilin-Coaperation  
**Klassifizierung:** L4 Master Knowledge Base & Revisionssicherer Prioritätsnachweis  

---

## 1. Executive Summary & Ökosystem-DNA

Die **Allgemeine Wissensdatenbank Pascal** bildet das zentrale Wissensfundament des **SkyOS & Sky Meilin Ökosystems**. Sie verbindet:
1. **Autonome KI-Agenten & Creator-Persona (Sky Meilin):**  
   Synthetische 25-jährige Automation-Lead-Persona bei *Agency Level Up*, transmediale Wachstums- und Content-Workflows, deterministische Visual DNA (`--cw 100`, MolinaEngine / MiniMax-M3) sowie dezentrale Abteilungs-Orchestratoren.
2. **KRITIS-Maschinenraum & BOS-Standards (*Das Duisburg-Protokoll*):**  
   Härtung nach BSI § 8a BSIG, hydrodynamische Personenstrom-Analyse nach HBS 2001/2009, DIN 14505 und DIN 30722-1 für Einsatzleitcontainer mit autarkem Notbetrieb.
3. **Revisionssichere WORM-Governance:**  
   Write-Once-Read-Many SHA-256 Hashchains (`data/L4_organized/worm_ledger.jsonl`) zur mathematischen Sicherung von Prioritätsnachweisen (*Proof of Prior Art*) bei jeder Datei- und Statusänderung.
4. **100 % Lokale Inferenz (Zero Data-Leakage):**  
   Vollständige Unabhängigkeit von externen Cloud-APIs (kein OpenAI-Zwang). Primäre Inferenz über lokale Server:
   - **LM Studio:** Port `1234` (`http://localhost:1234/v1`)
   - **Ollama:** Port `11434` (`http://localhost:11434/v1`)

---

## 2. Lizenz- und Schutzarchitektur

Das Gesamtsystem operiert unter einer mehrstufigen Schutzarchitektur:

```
+-----------------------------------------------------------------------------------+
|                        1. SKYOS SUSTAINABLE USE LICENSE v1.0                      |
|                  (Fair-Core / Primäre Arbeitsplatz- & Core-Lizenz)                 |
|                                                                                   |
|  * PERMITTED USE: Freie Nutzung, Modifikation und Deployment für private,         |
|    pädagogische, gemeinnützige und interne Unternehmenszwecke.                    |
|  * COMMERCIAL SERVICE LIMITATION: Verbot der gewerblichen Bereitstellung als      |
|    Managed Service, SaaS oder Weiterverkauf ohne gesonderte Lizenz von Pascal.   |
+-----------------------------------------+-----------------------------------------+
                                          |
                        KOMPLEMENTÄRE COPYLEFT-OPTION
                                          |
+-----------------------------------------v-----------------------------------------+
|                  2. GNU AFFERO GENERAL PUBLIC LICENSE v3 (AGPLv3)                 |
|              (Netzwerk-Transparenz für ausgewählte Open-Source Module)             |
|                                                                                   |
|  * Garantiert, dass Netzwerk-Server-Modifikationen der Community als Source-Code  |
|    bereitgestellt werden müssen (§ 13 AGPLv3).                                    |
+-----------------------------------------+-----------------------------------------+
                                          |
                         PROPRIETÄRES GESCHÄFTSGEHEIMNIS
                                          |
+-----------------------------------------v-----------------------------------------+
|                     3. § 2 GeschGehG (Trade Secrets / Enterprise IP)              |
|                                                                                   |
|  * Schutz proprietärer WORM-Salts, Lead-Closing-Cutoffs (75/40 Triage),           |
|    Visual-DNA-Seeds und Zero-Day Failover-Schaltungen.                            |
+-----------------------------------------------------------------------------------+
```

---

## 3. Tiered Data Management (L0 bis L4)

Gemäß dem Forschungsparadigma der *Data-Model Co-Evolution* (arXiv:2602.09003) ist sämtliches Wissen strukturiert in:

| Stufe | Bezeichnung | Beschreibung & Speicherort |
| :--- | :--- | :--- |
| **L0** | Raw Data | Ungefilterte Eingaben, Roh-Logs, initiale Mitschnitte (`logs/`, Chat-Dumps) |
| **L1** | Filtered Data | Bereinigte, deduplizierte Datensätze ohne syntaktischen Ballast |
| **L2** | Selected Data | Hochwertige Extrakte mit hoher fachlicher Informationsdichte |
| **L3** | Refined Data | Ausformulierte Standard Operating Procedures (SOPs), Playbooks & Skripte |
| **L4** | Organized Data | Verifiziertes Master-Wissen: `skyos_manifest.json`, `progress_tracker.db`, `worm_ledger.jsonl` |

---

## 4. Die 12-Karten Setup-Matrix (Fortschritts-Tracker)

Verwaltet über `progress_tracker.py` und persistiert in `data/L4_organized/progress_tracker.db`:

- **Karte 00 [DONE]:** System- & WSL-Umgebung (`C:\Workspace LM studio` / `/mnt/c/Workspace LM studio`)
- **Karte 01 [DONE]:** GitHub Konto & SSH-Schlüssel (`~/.ssh/id_ed25519`)
- **Karte 02 [DONE]:** Git Repository Initialisierung (`git init`, Branch `main`)
- **Karte 03 [DONE]:** Passwort- & Secret-Schutz (`.gitignore`)
- **Karte 04 [DONE]:** Umgebungsvariablen (`.env` mit lokalen Endpunkten)
- **Karte 05 [DONE]:** VS Code Terminal-Profile (`.vscode/settings.json`)
- **Karte 06 [DONE]:** Lizenzdatei (`LICENSE` – SkyOS Sustainable Use License v1.0)
- **Karte 07 [DONE]:** L4 Master Manifest (`data/L4_organized/skyos_manifest.json`)
- **Karte 08 [DONE]:** WORM Security Agent (`security_agent.py` mit SHA-256 Ledger)
- **Karte 09 [DONE]:** Lokale Inferenz-Server (`LM Studio` Port 1234 & `Ollama` Port 11434)
- **Karte 10 [DONE]:** Fortschritts- & Checklisten DB (`progress_tracker.py` initialisiert)
- **Karte 11 [PENDING]:** Git Commit & GitHub Remote Sync (`git push -u origin main`)

---

## 5. Operative Anleitung: Lokale KI-Inferenz

### 5.1 LM Studio lokal starten
1. **Via Grafischer Benutzeroberfläche (GUI):**
   - Öffne LM Studio.
   - Wähle in der linken Leiste das Entwickler-Symbol (`<->` / *Local Server*).
   - Lade ein Modell (z. B. `google/gemma-4-e4b` oder `DeepSeek-R1-0528-Qwen3-8B-GGUF`).
   - Klicke auf **"Start Server"** (Port standardmäßig `1234`).
   - **Authentifizierung:** Unter *API Token*:
     - Falls ohne Token gewünscht: Schalter *"Require API Token"* auf **OFF**.
     - Falls mit Token: Den Token kopieren und in der `.env` als `LM_API_TOKEN` hinterlegen.
2. **Via Terminal (CLI `lms`):**
   ```powershell
   # Server starten
   lms server start --port 1234
   
   # Modell in Speicher laden
   lms load google/gemma-4-e4b
   
   # Status prüfen
   lms status
   ```

### 5.2 Server-Endpoints testen

#### LM Studio Test (Port 1234)
```powershell
# PowerShell Test (ohne Token bzw. mit Token falls aktiviert)
$headers = @{ "Authorization" = "Bearer $env:LM_API_TOKEN" }
Invoke-RestMethod -Uri "http://localhost:1234/v1/models" -Headers $headers
```

#### Ollama Test (Port 11434)
```powershell
# Modellliste abrufen
Invoke-RestMethod -Uri "http://localhost:11434/api/tags"

# Lokale Prompt-Generierung testen
$body = @{ model = "qwen2.5-coder:3b"; prompt = "Hallo Sky Meilin"; stream = $false } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json"
```

---

## 6. Revisionssicherer WORM-Prioritätsnachweis

Jede neu erstellte Komponente wird mit dem Security Agenten unveränderlich verkettet:

```powershell
python security_agent.py PRIOR_ART_PROOF "docs/ALLGEMEINE_WISSENSDATENBANK_PASCAL.md" "Zentrale Wissensdatenbank Verifikation"
```

Der resultierende SHA-256 Hashblock bildet zusammen mit Vorgänger-Hash und Zeitstempel den unumstößlichen mathematischen Nachweis der Schöpfungshöhe und Erstentwicklung.
