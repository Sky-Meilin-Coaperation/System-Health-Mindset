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

---

## 7. Master-Wissensmatrix: Entitäten, Audits, BOS/KRITIS & Ökosystem

Die folgende Matrix enthält sämtliche kuratierte Entitäten, Systempfade, Audits und Open-Source-Bausteine der Wissensdatenbank:

| Entität / Thema | Kategorie | Beschreibung / Key Findings | Status / Details | Quelle |
| :--- | :--- | :--- | :--- | :--- |
| **GitHub Sponsors** | Sponsoring-Plattform | Im Mai 2019 gestarteter Dienst von GitHub, der es der Entwicklercommunity, Einzelpersonen und Organisationen ermöglicht, Spenden und Unterstützung direkt an Open-Source-Software-Entwickler und -Organisationen zu tätigen. GitHub glich im ersten Jahr Beiträge bis zu 5.000 USD ab. Über 5.800 Organisationen sind beteiligt, und es wurden bereits über 100 Mio. USD investiert (über 60 Mio. USD freigeschaltet) für mehr als 70.000 Maintainer/Organisationen mit über 280.000 Sponsoren in 103 Regionen. Inklusive Sub-Sponsoring-Optionen. | Anfänglich in 36 Regionen verfügbar, heute in 103 Regionen. Keine Gebühren für persönliche Konten (100 % an Entwickler); bis zu 6 % Gebühr für Organisationskonten (3 % Kreditkarte, 3 % GitHub-Dienst). Ermöglicht Sponsorship-Tiers, GraphQL-API und Webhooks. | [1], [2], [3], [4] |
| **GitHub Secure Open Source Fund** | Open-Source-Förderprogramm / Sicherheitsinitiative | Kohortenbasiertes Förderprogramm von GitHub und Industriepartnern zur finanziellen und strukturellen Verbesserung der Sicherheit und Nachhaltigkeit von Open-Source-Projekten. Bietet Finanzierung, Cloud-Guthaben (z. B. Azure), Copilot Pro, dreiwöchige Bildungssprints, Mentoring und GitHub Security Lab Office Hours. In Session 4 wurden über 500.000 $ an 50 Projekte verteilt (u. a. Gleam, LangChain, FastAPI, htmx, OpenClaw). Dabei wurden über 1.100 CodeQL-Schwachstellen behoben und 50 neue CVEs verfasst. | Gesamtbudget: 1,25 Mio. USD für 125 Projekte aus 71 Projekten ($10.000 USD Projektmittel + $10.000 Azure-Credits pro Projekt). Anträge/Bewerbungen offen bis 07. Januar bzw. 24. August. 3-wöchiges Sicherheitsprogramm plus Follow-ups nach 6 und 12 Monaten. | [5], [6], [2], [7], [3], [8] |
| **Sky Meilin** | Charakter-Design / Persona-Spezifikation | 25-jährige (bzw. anfangs Anfang 20-jährige) KI-Influencerin, Assistenz von Pascal Weidermann und Head of Automation für SkyOS sowie Vertriebsfigur für SkyOS bei Agency Level Up. Verbindliche Master-Spezifikation: Leuchtend türkisfarbene (oder rosa) geflochtene Zöpfe, feine Sommersprossen über Nase und Wangen, grün-blaue Mandelaugen, 100 % tattoo-freies Gesicht, sympathischer Ausdruck und sportlich-eleganter Look (z. B. Crop-Top und Leggings). Tattoo-Topologie: Florales Muster/Neck-Ornament am Hals, rosa Lotusblüte am Brustbein, 2 schwarze Pfotenabdrücke unterm Schlüsselbein sowie Sleeves an den Armen (keine Cyberpunk-Elemente, Chips, Masken oder Schädel). | Status: ✅ gesetzt / aktiv. Head of Automation \| Creator Systems & AI Workflow. Verknüpft mit Gravatar-Profil skymeilin und WordPress-Heimatseite. | [9], [10], [11] |
| **Audit AUD-2026-SKY-001 / Konzept & Prompt-Spezifikation "Sky Meilin"** | Auditing / Prüfbericht | Forensischer Prüfbericht, der eine Multi-Prompt-Kollision im ursprünglichen Look von Sky Meilin aufdeckte (Optische Variante A "Cyberpunk" vs. Variante B "Türkise Zöpfe/Lotusblüte"). Die Vermischung im Master-Prompt führte zu Prompt-Bleeding. | Prüf-ID: AUD-2026-SKY-001; Status: Bedingt verkehrsfähig / Entwicklungsstand; Konsistenz-Score: 61 / 100. Führte zur Etablierung des Härtungsprotokolls und der verbindlichen Master-Spezifikation. | [9], [12] |
| **Abrollbehälter DIN 14505 / DIN 30722-1** | Spezifikation / Hardware-Norm & BOS | Spezifikation für mobile KRITIS/BOS-Einsatzcontainer und Führungseinheiten (z. B. Führungs- & Stabsraum ELW 2) mit CBRN-Überdruckkapselung, HF-Schirmdämpfung (> 60 dB) und Notstromversorgung (20 kVA Aggregat + LiFePO4). Gesamt-Nutzfläche: 12,70 m² (Brutto ca. 14,5 m²). Sub-Kompartimente umfassen Führungs- & Stabsraum (7,40 m²), Technikzentrale & BOS-Digitalfunk (3,20 m²) und Personenschleuse/ABC-Dekon-Vorraum (2,10 m²). | Abmessungen: Länge 6,90 m, Außenbreite $\le 2,55\text{ m}$ (Container: 2,50 m), Höhe 2,50 m. Aufnahmebeschlag mit Hakenhöhe 1,57 m (DIN 30722-1 Klasse 1). Lichte Durchgangshöhe $\ge 2,10\text{ m}$. Max. Gesamtgewicht: 14.000 kg, Leergewicht: 5.200 kg. | [9], [13] |
| **System-Orchestrator / Six-Verb-Protokoll** | System-Architektur / Core Engine | Übergeordnete Engine, die den Ablauf über eine deterministische State Machine nach dem mathematisch berechenbaren Six-Verb-Protokoll steuert (SEARCH, RESOLVE, PREVIEW, HUMAN-GATE, EXECUTE, VERIFY/RECOVER), um KI-Fehlentscheidungen auszuschließen. Gleichung: $State_{t+1} = T(State_t, Verb, Context)$. | Verwaltet States, setzt Timeouts durch, erzwingt PII-Filterung (DSGVO Art. 25), Secrets-Schutz und Human-in-the-Loop (HITL) Gates. | [9], [14] |
| **DSPy Framework (stanfordnlp/dspy)** | Open-Source-Projekt / Software-Repository | Declarative Self-improving Python Framework zur Programmierung (statt Prompting) von Sprachmodellen. Bietet Werkzeuge zur Prompt- und Gewichtsoptimierung, Assertions und harte Validierungsregeln. | 38.5k Stars, 3.4k Forks, 4.737 Commits, Version 3.4.0, Lizenz: MIT, Hauptsprache: Python (99.7 %). Logo entworfen von Chuyi Zhang. | [15], [16], [17] |
| **langchain-ai/langgraph** | Open-Source-Projekt | Low-Level-Orchestrierungsframework für zyklische, zustandsbehaftete Agenten-Workflows und Multi-Agenten-Pipelines mit expliziter State Machine. | 42.6k Stars, 7.2k Forks, 565 Releases, 7.124 Commits, Lizenz: MIT, Hauptsprache: Python (99.6 %). Ökosystem umfasst LangGraph.js, Deep Agents, LangSmith und LangChain Academy. | [18], [16], [17] |
| **ComfyUI** | Open-Source-Projekt | Modularer KI-Engine und GUI mit Knoten-Graph-Schnittstelle zur Bild-, Video-, 3D-, Audio- und Text-Generierung (z. B. via FLUX.1). Ökosystem umfasst ComfyUI Core, Comfy Desktop, ComfyUI Frontend, Comfy Cloud, ComfyUI-Manager und comfy-cli. | 136k Stars, 16.1k Forks, 6.071 Commits; unterstützt Windows, Linux, macOS. Ordnerstrukturen umfassen models/checkpoints, models/vae und models/vae_approx (TAESD-Decoder). | [19], [16] |
| **n8n-io/n8n** | Open-Source-Projekt | Fair-Code-Workflow-Automatisierungsplattform mit nativen KI-Funktionen zur Verknüpfung von Zahlungen, Datenbanken und Admin-Prozessen. Gründer & CEO: Jan Oberhauser (Name stammt von 'nodemation'). | 207k Stars, 61k Forks, 25.226 Commits, Hauptsprache: TypeScript (92.2 %). Docker Image nutzbar via Port 5678. Lizenzen: Sustainable Use License / Enterprise License. | [20], [16] |
| **gitroomhq/postiz-app** | Open-Source-Projekt / Repository | Agentenbasiertes Tool zur Planung, Automatisierung, Terminierung und Analyse von Social-Media-Inhalten. Verfügbar als gehostete Postiz Cloud und self-hosted Open Source. Gesponsert von Hostinger, Virlo, ChatbotX und RapidProxy. | 36.6k Stars, 7.1k Forks, Lizenz: AGPL-3.0, Hauptsprache: TypeScript (80,3 %). Tech Stack: Pnpm workspaces, NextJS, NestJS, Prisma, Temporal, Resend. | [21], [16] |
| **twentyhq/twenty** | Open-Source-Projekt / CRM | Open-Source-Alternative zu Salesforce, speziell für KI entwickelt. Bietet CRM-Bausteine für Kundendatenbanken, Client-Onboarding und Vertragsverfolgung. Verfügbar via Twenty Cloud, Twenty CLI, Twenty App Skills und Docker Compose. | 57,8k Stars, 9,4k Forks, 16.266 Commits, Hauptsprache: TypeScript (82,6 %), Version v2.44.0. Tech Stack: Nx, NestJS, BullMQ, PostgreSQL, Redis, React, Jotai. | [22], [16] |
| **makeplane/plane** | Open-Source-Projekt / Repository | Modernes Projektmanagement-Tool und Open-Source-Alternative zu Jira, Linear, Monday und ClickUp. Unterstützt Work Items, Cycles, Modules, Views, Pages und Analytics. Bereitstellung via Plane Cloud oder Self-Hosted (Docker/Kubernetes). | 60,3k Stars, 6k Forks, 193 Contributors, Hauptsprachen: TypeScript (69,2 %), Python (27,6 %), Lizenz: GNU AGPL v3.0. Kontakt: security@plane.so. | [23], [16] |
| **docling** | Open-Source-Projekt / Software-Repository | Universelle KI-gestützte Dokumentenverarbeitungs-Engine (LF AI & Data Foundation) zum Parsen heterogener Formate (PDF, DOCX, PPTX, XLSX, HTML, Audio) in strukturierte Formate (DoclingDocument). Nutzt das VLM GraniteDocling (258M) sowie docling-serve und Docling MCP Server. | 68,3k Stars, 5,0k Forks, MIT-Lizenz. Erfordert Python 3.10+. Technischer Bericht veröffentlicht im August 2024 von IBM Research Zurich (DOI: 10.48550/arXiv.2408.09869). | [24], [16], [17] |
| **apache/superset** | Open-Source-Projekt | Data-Visualisierungs- und Data-Exploration-Plattform für Unternehmen mit No-Code Chart Builder, SQL Editor und Semantic Layer. | 75.0k Stars, 18.4k Forks, 23.473 Commits, Hauptsprachen: Python (53.4 %) und TypeScript (43.2 %), Release: 6.1.0. Quellcodeordner: superset-frontend, superset-websocket, superset-embedded-sdk. helm/superset ist veraltet. | [25], [16] |
| **Qwen3-Coder Modellfamilie** | Open-Source-Projekt / Software-Repository | Familie von Code-LLMs und Agentic-Coding-Modellen im offiziellen Repository QwenLM/Qwen3-Coder (16.8k Stars, 1.3k Forks). Umfasst Qwen3-Coder-Next (Open-Weight Hybrid-Architektur, Instruct, 256k Kontext), Qwen3-Coder-Next-Base (80B-A3B-Base) sowie Qwen3-Coder-480B-A35B-Instruct und Qwen3-Coder-30B-A3B-Instruct. | Inferenz-Worker im Hugging Face Space unter sky-meilin/Qwen-Qwen3-Coder-30B-A3B-Instruct eingesetzt. Unterstützt Multi-File-Agents und isolierte Code-Generierung. | [26], [16], [27] |
| **GitHub Copilot & Copilot Autofix** | KI-Software-Tools / Entwickler-Tool | KI-gestützte Entwicklerwerkzeuge zur Unterstützung bei Code-Generierung, Schwachstellen-Triage, Threat Modeling und automatisiertem Code-Scanning. | Positioniert als Leader im Gartner® Magic Quadrant™ for AI Code Assistants (2 Jahre in Folge). Kostenlos bereitgestellt in Förderprogrammen wie dem Secure Open Source Fund. | [2], [3], [8] |
| **Google Distroless Debian 12 Runtime** | System-Pfad / Runtime-Umgebung | Gehärtete Container-Laufzeitumgebung (Hardened OS Image) ohne Shell oder Paketmanager zur Minimierung der Angriffsfläche. | Ausführung unter UID 65532 (non-root) mit Read-Only Filesystem; Multi-Stage musl-x64 Minimal-Container. Eingesetzt im taktischen Air-Gapped Survivor Mode von SkyOS. | [9], [14] |
| **Gravatar API v3 & Gravatar-Integration** | Software-Projekt / API-Schnittstelle | Anbindung der Gravatar Profiles API v3 (Basis-URL https://api.gravatar.com/v3) zur Verifizierung von Systemprofilen (skymeilin). Nutzt Bearer-Token Auth via Environment Secrets (GRAVATAR_API_KEY) und SHA256-Email-Hashing. Inkludiert Android SDK (MPL 2.0) und QR-Code-Endpunkt (/qr-code/{sha256_hash}). | Endpunkt: https://api.gravatar.com/v3/profiles/skymeilin. Profil-URL: https://gravatar.com/skymeilin. | [9], [10] |
| **Taktischer Krisenbetrieb & Sky Os Core Service-Mesh** | KRITIS / BOS Systemansatz | Taktischer Air-Gapped Survivor Mode zur Sicherstellung der Handlungsfähigkeit bei physischem Schock und Netzausfall. Kombiniert Distroless Debian 12 Container, BDBOS PDV 810.3, BSI TR-02102-2 (mTLS), gRPC/Protobuf v3, REST OpenAPI 3.1 und Hands-Free Bedienung (Hori-Fußschalter/PTT, Logitech HID Presenter, offline Vosk Spracherkennung, Brother QL-500 Drucker). | Implementiert in Projekten von System Health Evolution (Pascal Weidermann) in Kooperation mit RWTH Aachen, Kreis Heinsberg (Städt. Krankenhaus) und Bosch Healthcare. | [14] |
| **Forensisches WORM-Ledger** | KRITIS / BOS Systemansatz / Auditing | Revisionssichere Beweisführung und gerichtsfeste Unveränderbarkeit digitaler Spuren nach ISO/IEC 27037 zur Erfüllung der BSI-Nachweispflicht. Nutzt PostgreSQL 16 mit WORM-Triggern (fn_reject_audit_tampering), Stratum-1 PTP Drift $\le 1,2\text{ ms}$ und physische WORM-Medien (HP DVD-R Single-Session). | Blockiert jegliche UPDATE- oder DELETE-Befehle in Zone C nach § 8a BSIG. | [14] |
| **Multi-Agenten-Forensik & 4-Stufen-Laborprinzip** | Labor-Projekt / Auditing | Forensisches Prüflabor („Agency in a Box“) für Audits und Qualitätskontrolle. Besteht aus 4 isolierten Rollen: 1. Dokumenten-Agent (Asservatenaufnahme), 2. Analyst (Spurenanalyse & Mustererkennung), 3. Gutachter-Agent (Fachbegutachtung & Regelprüfung), 4. Neutrale Person/Ombudsstelle (Synthese, Bias-Kontrolle, Finales Urteil). | Vergibt Konsistenz-Scores (0–100) und stellt digitale Validierungs-Zertifikate mit SHA-256 Hash und Ed25519-Signatur aus. Freigabe erfordert Score $\ge 85$. | [9], [28], [17] |
| **OpenSource_V1 bis V8 Datensätze** | Open-Source-Datensatz / Datenbestand | Evaluierte CSV-Datenbestände zur Erfassung von Open-Source-Projekten. Entwicklung von V1 (8 Einträge) über V3 (69 Einträge) bis V8 (91 Einträge in 6 Spalten mit vollständiger Hierarchie). Umfasst Videomodelle, Voice-Cloning, Mobile KI, IDEs, CRMs und Projektplanung. | OpenSource_V8.csv ist die vollständigste Version. OpenSource_V4.csv enthielt teilweise #ERROR!. | [29] |
| **EU Sovereign Tech Fund (EU-STF) & Sovereign Tech Agency** | Öffentliche Förderinitiative | Öffentliche Investitionsinitiativen zur Finanzierung und Härtung kritischer Basis-Open-Source-Technologien. Der deutsche Sovereign Tech Fund (gestartet Oct 2022 unter dem BMWK, 23 Mio. € Investition) dient als Vorbild für den vorgeschlagenen EU-STF (geplantes Budget: min. 350 Mio. € für 2028–2035). | Vorgeschlagen zur Abfederung von Schwachstellen in Lieferketten (z. B. xz backdoor, Log4Shell) und zur Unterstützung des EU Cyber Resilience Acts. | [6] |
| **GitHub Accelerator** | Förderprogramm / Initiative | 10-wöchiges Förderprogramm für Open-Source-Maintainer zur Erreichung nachhaltiger Finanzierung. Erste Kohorte 2023 umfasste 20 Projekte (u. a. AnalogJS, htmx, Dioxus, Formbricks, Nuxt, Datasette, trpc) mit $20.000 Anschubfinanzierung pro Projekt. | Erste Kohorte 2023 mit 32 Teilnehmenden weltweit. | [30] |
| **GitHub Student Developer Pack & Studierenden-Programme** | Förderprogramm für Studierende | Umfangreiche Zusammenstellungen von Entwickler-Tools, Guthaben und Vergünstigungen für Studierende. Beinhaltet das GitHub Student Developer Pack (Wert ca. $10.000), Google AI Pro/Plus, Codex ($100), Firecrawl (10.000 Credits), Kiro (1.000 Credits/Monat), YC AI Student Starter Pack ($25.000) und Azure for Students. | Bietet kostenlosen Zugang zu Premium-Entwicklungsumgebungen, Cloud-Ressourcen und KI-Tools. | [7] |
| **AUD-2026-SKY-10F (10-Finger-Imperium)** | Auditing / Prüfbericht | Forensischer Prüfbericht für den automatisierten Content- & Lead-Funnel 'Sky Meilin 10-Finger Imperium & Molina Hill Fanvue'. Deckte rechnerische Anomalien bei Umsatzprognosen und Lücken in fingers.list auf. | Status: BEDINGT VERKEHRSFÄHIG (Freigabe unter Bereinigungsauflage); Konsistenz-Score: 74 / 100. Deploy-Status: 92 % Deploy-Ready. | [31] |
| **AUD-2026-FNG-008 (Online-Kurs / finger-8-education)** | Auditing / Prüfbericht | Forensischer Prüfbericht für den Online-Kurs 'Sky Meilin KI-Ökosystem mit Hugging Face'. Klärte die Zähldiskrepanz auf: Operativ 9 Kernfinger, während '10-Finger-Imperium' den symbolischen Dachbegriff bildet. | Status: BESTANDEN / ZERTIFIZIERT; Konsistenz-Score: 91 / 100. Didaktisch und architektonisch freigegeben. | [32] |
| **AUD-2026-FNG-006 (finger-6-coding-automation)** | Auditing / Prüfbericht | Forensischer Prüfbericht für das Prüfmodul finger-6-coding-automation (Hugging Face Spaces für Code-Generierung, Simulatoren und Bot-Blueprints). | Status: BESTANDEN / ZERTIFIZIERT; Konsistenz-Score: 92 / 100. Auflage: Isolierte Execution-Sandbox (Docker/WSL) für generierte Skripte erteilt. | [27] |
| **AUD-2026-FNG-007 (YouTube Health Recipes)** | Auditing / Prüfbericht | Forensischer Prüfbericht für das Modul finger-7-youtube-health zur Monetarisierung von Health-Rezepten. | Status: BESTANDEN (mit Compliance-Auflage); Konsistenz-Score: 88 / 100. Auflage: Pflichterklärung eines Health-Disclaimers (EU VO 1924/2006). | [33] |
| **AUD-2026-INF-092 (KI Influencerin & Affiliate Marketing)** | Auditing / Prüfkonzept | Forensische Prüfung eines Konzepts für KI-Influencer-Affiliate-Marketing. Aufdeckung massiver Mängel bezüglich Tool-Eignung (Synthesia/Replika ungeeignet) und Rendertimings. | Status: ABGELEHNT / NICHT VERKEHRSFÄHIG; Konsistenz-Score: 48 / 100. Freigabe verweigert; Hype-Bias festgestellt. | [34] |
| **AUD-2026-METH-008 (DELIBERATE PRACTICE.docx)** | Auditing / Prüfbericht | Prüfbericht zur Deliberate-Practice-Methodik von Nicolas Cole. Validierte das Unbundling von Fertigkeiten sowie das constraint-basierte Template (C-W-D-A-C Framework). | Status: BESTANDEN / HOHE METHODISCHE RELEVANZ; Konsistenz-Score: 94 / 100. Formel: 'When &lt;Character&gt; experiences &lt;Weakness&gt;, they run into &lt;Danger&gt; and must &lt;Action&gt; to &lt;Change&gt;.' | [35] |
| **Sponsorware** | Open-Source-Release-Strategie | Release-Strategie für Open-Source-Software, bei der Software erst freigegeben wird, wenn ein bestimmtes Sponsoring-Ziel erreicht wurde. | Neuartiger Trend im Gegensatz zu rein freiwilligen Wertschätzungs-Spenden. | [1] |
| **Entwickler-Klassifikationsmodell** | Maschinelles Lernen / Statistisches Modell | Mit scikit-learn erstellter Entscheidungsbaum zur Klassifizierung von gesponserten vs. nicht-gesponserten Entwicklern. Wichtigste Features: num_repos_top_contributing, num_repos_top_co_contributing und highest_stars. | Trainiert auf 9.363 Entwicklern im Rahmen der GitHub-Sponsors-Studie. | [1] |
| **Netzwerk der Sponsoring-Beziehungen** | Soziales Netzwerk / Graphmodell | Graphmodell der Sponsoring-Beziehungen zwischen Entwicklern auf GitHub. Zeigt, dass 22 % (809 von 3.697) der gesponserten Entwickler selbst als Sponsoren agieren. | Stärkstes Cluster bilden PHP-Entwickler. | [1] |
| **Eigener Datensatz der Studie (GitHub-Repositories)** | Forschungsdaten | Sammlung von 1.209.654 GitHub-Repositories (2008–2020, $\ge 10$ Stars) und 1.695.015 Top-Contributors zur Analyse von Sponsoring-Dynamiken. | Identifizierte 3.697 gesponserte und 5.666 nicht-gesponserte Entwickler. | [1] |
| **GitHut (GitHut 2.0)** | Web-Service / Datenanalyse | Web-Service zur Analyse von GitHub-Daten über Google BigQuery zwecks Visualisierung von Programmiersprachen-Trends. | Verwendet zur Ermittlung des Pull-Request-Volumens pro Sprache im Q4 2020. | [1] |
| **RepoReapers** | Open-Source-Datensatz / Kurations-Tool | Datensatz und Tool zur Kuration echter Software-Repositories auf GitHub. | Untersuchte 1.857.423 Repositories zur Identifizierung von Projekten mit geringer Star-Anzahl. | [1] |
| **Bountysource** | Bounty-Plattform | Plattform für Open-Source-Bounties zur Entlohnung von Bugfixes und Feature-Implementierungen. | In Literatur bezüglich Lösungsraten und Backer-Verhalten untersucht. | [1] |
| **PayPal / Patreon** | Spenden-Plattformen | Plattformen zur finanziellen Abwicklung von Spenden an Open-Source-Entwickler vor GitHub Sponsors. | In Studien als historische Spendenkanäle analysiert. | [1] |
| **Planer-Agent** | Software-Projekt / Agenten-Rolle | Nimmt Anforderungen entgegen, zerlegt Aufgaben strukturiert (Dekomposition) und definiert Parameter/Ablaufpläne nach Vor-/Nachbedingungen. | Berücksichtigt spezielle Direktiven (z. B. Startzeiten nach 10:00 Uhr). | [9] |
| **Sicherheits-Agent** | Auditing / Security | Überwacht Systemgrenzen, führt Sandbox-Prüfungen durch und blockiert unbefugte Befehle oder Ausbruchsversuche. | Fokus auf PII-Filterung (DSGVO Art. 25), Secrets-Schutz (GRAVATAR_API_KEY, Stripe, HF-Keys) und Container-Isolation. | [9] |
| **Anwalts-Agent** | Compliance / Recht | Begutachtet Artefakte und Pläne auf Rechtmäßigkeit (EU AI Act, Health-Claims-Verordnung, Urheberrecht, UWG, Impressum/AGB). | Erzwingt KI-Kennzeichnungspflichten und Rechtstexte. | [9] |
| **Validierungs-Agent** | Auditing / Qualitätskontrolle | Prüft auf logische/mathematische Widersprüche gemäß 4-Stufen-Laborprinzip und vergibt Konsistenz-Scores. | Blockiert Freigaben bei Scores $< 85$. | [9] |
| **Support-Agent** | Kundenkommunikation / Ticketing | Schnittstelle zu Anwendern für Intake, Statusberichte und Ergebnisübergabe. | Kommuniziert professionell, deeskalierend und strikt in der Du-Form. | [9] |
| **Joy AI Orchester** | Open-Source-Projekt / Inferenz-Engine | Generative Multimodal Execution Engine als Worker-Pool für Text-, Bild-, Audio- und Skript-Generierung (Hugging Face Spaces, Qwen, FLUX, SD LoRA). | Untersteht der Kontrolle des Orchestrators und der Prüf-Gates. | [9] |
| **Dreischichten-Architektur (3-Layer-IP-Protection)** | System-Architektur / Security | Schutzmodell für geistiges Eigentum: Layer 1 (Public UI) $\rightarrow$ Layer 2 (Gateway/Firebase) $\rightarrow$ Layer 3 (Gehärteter Core IP Kern). | Verhindert Prompt-Bleeding und Schlüssel-Exposition. | [9] |
| **sky_os_agent_dashboard** | Software-Projekt / Flutter-App | Flutter/Dart Controller Dashboard mit Riverpod State Management, Material 3 UI, nativer MCP-Anbindung und Secure Storage. | Inkludiert interaktiven DIN 14505 Container-Planer. | [9] |
| **Jan Oberhauser** | Personenspezifikation | Gründer und CEO von n8n.io. | Founder and CEO, n8n.io. | [20] |
| **GitHub Secure Open Source Fund gehärtete Projekte** | Open-Source-Software / Security | Gruppe von Open-Source-Tools, die ihre Sicherheitsarchitektur im Rahmen des GitHub Fund ausgebaut haben (Ollama, GravitasML, shadcn/ui, Node.js, Turborepo, Log4j, Charset-Normalizer, nvm, JUnit, Matplotlib). | Führten Threat Modeling durch, integrierten CodeQL in CI/CD, aktivierten Private Vulnerability Reporting und verfassten Incident Response Pläne. | [5] |
| **OpenUK & Amanda Brock** | Organisation / Person | Branchenverband im VK und dessen CEO, die Empfehlungen und Analysen für eine nachhaltige Open-Source-Förderung erarbeiten. | Kooperation mit dem öffentlichen Sektor; Veröffentlichungen im Herbst angekündigt. | [6] |
| **Fit 4 Start (#16)** | Startup-Förderprogramm | Luxinnovations Unterstützungsprogramm für europäische Startups. | Befindet sich in der 16. Ausgabe; Bewerbungen geöffnet. | [6] |
| **Open-Source-Sicherheitsvorfälle (xz backdoor & Log4Shell)** | Sicherheitsvorfall / Schwachstelle | Kritische Sicherheitslücken in Open-Source-Lieferketten, die Risiken durch überlastete Maintainer und unzureichende Wartung aufzeigten. | Dienen als Fallbeispiele für die Notwendigkeit von Förderfonds und den EU Cyber Resilience Act. | [6] |
| **Open-Source-Sponsoren & Partner** | Unternehmen / Sponsor | Unternehmen, die Open-Source-Projekte und -Entwickler finanziell unterstützen oder als Partner auftreten (Hostinger, Virlo, ChatbotX, RapidProxy, Shopify, Mercedes-Benz Tech Innovation). | Investieren via direkte Sponsorships oder Sponsoring-Plattformen. | [21], [3] |
| **Open Source Funding Survey 2024** | Forschungsstudie / Open-Source-Finanzierung | Studie von GitHub, Linux Foundation und LISH über Finanzierungsströme in Open Source. | Schätzt jährliche Gesamtinvestitionen auf 7,7 Mrd. USD. Nur 6 % der Mittel fließen direkt in umfassende Audits. | [2] |
| **EU Cyber Resilience Act & Secure by Design** | Gesetzgebung / Richtlinie | EU-Regulierung und Sicherheitsrichtlinie zur Durchsetzung von Cybersicherheitsanforderungen über den gesamten Produktlebenszyklus. | Bestandsbestandteile der Policy-Schulungen im Secure Open Source Fund. | [2] |
| **GitHub Security Lab** | Sicherheitsorganisation / Expertenteam | Sicherheitsteam von GitHub zur Schwachstellenforschung und Unterstützung von Maintainern. | Bietet Sprechstunden, Mentoring und unterstützt Incident-Management. | [2] |
| **GitHub Accelerator Kohorte 2023 Projekte** | Open-Source-Projekte | Sammlung von 20 geförderten Projekten der 10-wöchigen GitHub Accelerator Kohorte 2023: AnalogJS, Atri-Labs, htmx, Code Hike, Dioxus, BioDrop, Seamly2D, nbdev, Formbricks, Sniffnet, pypandoc, Mockoon, Nuxt, Responsively App, Datasette, Spyder, Strawberry GraphQL, Termux, Poly, tRPC. | Erhielten je $20.000 Anschubfinanzierung zur Erreichung finanzieller Nachhaltigkeit. | [30] |
| **Open-Source- & Startup-Förderprogramme** | Förderprogramm / Kredit-Programm | Kuratierte Förderinitiativen für Studierende, Open-Source-Maintainer und Early-Stage Startups (Catalyst, Claude/OpenAI/Capy/Kilo/Upstash for OSS, AWS Activate, Cloudflare/Google/Microsoft for Startups, Y Combinator, etc.). | Bieten Cloud-Guthaben (bis $350k), API-Credits, Mentoring und kostenfreie Enterprise-Pläne. | [7] |
| **Lime Networks, Livewire & Alpine.js, tiangolo (Sebastián Ramírez)** | Open-Source-Projekte / Entwickler | Maintainer und Projekte, die sich über GitHub Sponsors finanzieren oder Einnahmen reinvestieren. | Caleb Porzio arbeitet dank Sponsors in Vollzeit an Livewire/Alpine.js; Sebastián Ramírez betreibt Sub-Sponsoring. | [3] |
| **Git 2.56** | Open-Source-Software / Versionskontrolle | Major Release des verteilten Versionskontrollsystems Git. | Highlights und Performance-Verbesserungen im GitHub Blog veröffentlicht. | [3] |
| **OpenClaw** | Open-Source-Projekt | Das am schnellsten wachsende Open-Source-Projekt in der Geschichte von GitHub (Maintainer: Peter Steinberger u. a.). | Gefördert in Session 4 des GitHub Secure Open Source Fund. | [3], [8] |
| **Interaktives Sound-ASCII-Art-Tool** | Software-Projekt | Canvas-basiertes Zeichen-Tool mit Maus-/Touch-Support, das beim Erzeugen von ASCII-Zeichen passende Töne abspielt. | Enthält Pattern-Switcher und Reset-Button. | [26] |
| **Pflanzen vs. Zombies Web-Spiel** | Charakter-Design / Spezifikation | Reverse-Tower-Defense-Webspiel mit 5x9 Feld, 120s Limit, Zombietypen (Standard, Kegel, Eimer, Sprint) und Ressourcen-Loop. | Ausgearbeitete Spielmechanik-Spezifikation. | [26] |
| **Echtzeit-Partikelsystem (Parkour Game)** | Software-Projekt | HTML5-Canvas-Partikelsystem mit physikbasierter Anziehung/Abstoßung und FPS-Anzeige. | Verarbeitet 800–1200 Partikel via requestAnimationFrame. | [26] |
| **SkyOS & Agency Level Up Infrastruktur** | Projekt-Infrastruktur / Software | Vernetzte Infrastruktur zur Automatisierung von Content, Verteilung und Dokumentenverwaltung. Umfasst Notion DB, Stripe Checkout, Telegram Bot, WordPress, Make.com Webhooks und Google Sheets Wissensdatenbank. | URL-Wissensdatenbank speichert Entscheidungen, Links und Checklisten. | [10], [31] |
| **M12 GitHub Fund & CodeSee** | Investmentfonds / Plattform | Gemeinsamer Venture-Fonds von M12 (Microsoft) und GitHub für Open-Source-Startups. Erster Investment-Empfänger: CodeSee (Tool zur visuellen Codebase-Analyse). | Angekündigt im November 2022 von Priyanka Mitra, Michelle Gonzalez und Thomas Dohmke. | [36] |
| **OpenSourceArchitectureApp & ArchitecturalSpace** | Open-Source-Projekt / App | Flutter-Anwendung und Datenmodell zur Verwaltung architektonischer Räume (z. B. Büro A: 24,5 m², Flur Nord: 18,0 m²). Umfasst PlannerAgent zum Testen von Layouts. | Bietet Paywall via PremiumServicesController für Profi-Erweiterungen (NormenAgent ab 14,99 €, FlaechenAgent ab 19,99 €). | [13] |
| **BosContainerPlannerAgent** | Auditing / Agent | Controller im PlannerAgent zur Validierung von BOS/KRITIS-Containern nach DIN 14505 / DIN 30722-1. | Generiert complianceLog und prüft Hakenhöhe, Breite, lichte Höhe und CBRN-Schutz. | [13] |
| **Multi-Agenten-Orchestrierungs-Tools (CrewAI, AutoGen)** | Open-Source-Projekte | Open-Source-Frameworks für rollenbasierte Agenten-Automatisierung und konversationsgetriebene Group-Chats mit Moderation. | Werden in Multi-Agenten-Pipelines und Marketing-Workflows genutzt. | [16], [17] |
| **Dokumentenextraktions-Tools (Marker, Nougat, PyMuPDF)** | Software-Tools | Hochpräzise Konverter für PDFs, Scans und Tabellen in strukturiertes Markdown/JSON ohne Formatierungsverlust. | Verhindern OCR-Halluzinationen in Asservatenaufnahmen. | [17] |
| **RAG & Evaluation Frameworks (Ragas, TruLens)** | Open-Source-Projekte | Evaluierungstools zur mathematischen Bewertung von LLM-Antworten hinsichtlich Faithfulness, Answer Relevance und Context Recall. | Genutzt zur automatisierten Berechnung von Konsistenz-Scores. | [16], [17] |
| **Zertifikats- & Kryptografie-Tools (WeasyPrint, ReportLab, PyCryptodome)** | Software-Bibliotheken | Werkzeuge zur Headless-PDF-Generierung und kryptografischen Absicherung (SHA-256 Hashing, Ed25519/RSA Signaturen). | Werden zur Erstellung fälschungssicherer Validierungs-Zertifikate eingesetzt. | [17] |
| **Marketing-, SEO- & Operations-Tools** | Open-Source-Projekte | Software-Ökosystem für automatisierte Marketing-, Admin- und Operations-Pipelines (CrewAI & Ghost CMS, Crawl4AI, Instructor, Listmonk & Mautic, Discord.py, Activepieces). | Integriert in erweiterte Workflow-Pipelines. | [16] |
| **B2B-Validierungsdienstleistungen** | B2B-Dienstleistung | Professionelle Prüfdienste auf Basis des 4-Stufen-Laborprinzips: Data & Content Audit (Korrekturprotokoll), Logic & Process Check (Schwachstellen-Report) und Full Compliance Seal (Validierungs-Zertifikat mit Prüf-ID). | Zertifikate enthalten Prüf-ID, Zeitstempel, SHA-256 Hash und Konsistenz-Score. | [28] |
| **Social Media & Content Marketing Strategie** | Marketing / Strategie | Multi-Kanal-Strategie (LinkedIn, TikTok, Instagram, X, Discord, Fanvue) für KI-Systeme, Finanz-Souveränität, Business-Elegance und Lifestyle. | Nutzt zielgerichtete Skripte und Calls-to-Action zur Community-Aktivierung. | [12], [37] |
| **Workspace System-Pfade (sky-os-workspace)** | System-Pfad | Lokale und vernetzte Pfadangaben für den Haupt-Arbeitsordner des SkyOS-Workspaces unter WSL (/home/openclaw/sky-os-workspace bzw. \\\\wsl$\\OpenClawGateway\\...) sowie Windows Host (C:\sky-os-workspace). | Basis-Entwicklungsumgebung: Ubuntu / WSL2 (Distribution OpenClawGateway). | [38] |
| **Repository-Systempfade (Superset, n8n, Postiz, Twenty, DSPy, LangGraph, Qwen3)** | System-Pfad | Interne Konfigurations- und Quellcodeordner in Repositories (z. B. .agents, .claude, .devcontainer, packages, libs, docs, scripts, tests, pyproject.toml, uv.lock, CLAUDE.md, AGENTS.md, SECURITY.md). | Dienen der CI/CD-Steuerung, Agenten-Instruktion, Abgabe von Code-Scanning-Regeln und Paketverwaltung. | [25], [20], [21], [22], [26], [15], [18] |

---

## 8. Quellen- und Referenzverzeichnis

- **[1]** *GitHub Sponsors: Exploring a New Way to Contribute to Open Source* – arXiv
- **[2]** *Announcing GitHub Secure Open Source Fund: Help secure the open source ecosystem for everyone* – The GitHub Blog
- **[3]** *$100 million for open source: A milestone built by the community* – The GitHub Blog
- **[4]** *Über GitHub Sponsoren* – GitHub Dokumente
- **[5]** *Securing the supply chain at scale: Starting with 71 important open source projects*
- **[6]** *Chronic underfunding of open source software poses strategic risk to Europe's digital sovereignty* – Tech.eu / OpenUK
- **[7]** *GitHub - doanbactam/awesome-builder-programs: A curated list of programs, credits, grants, and perks for students, startups, and open-source builders.*
- **[8]** *Inside GitHub's Secure Open Source Fund: what maintainers actually got out of it* – daily.dev
- **[9]** *Workflow der Agenten-Kollaboration*
- **[10]** *Sky Meilin – Gravatar Datenbank*
- **[11]** *Bereinigter Master-Prompt: Sky Meilin (Original-Identität)*
- **[12]** *Prüfbericht & Audit: Sky Meilin Spezifikation*
- **[13]** *Planer Agent & BOS DIN 14505 Container (Code-Export)*
- **[14]** *KRITIS & BOS Systemansätze: Synthese und Konzeptvergleich*
- **[15]** *DSPy: Programmatic Prompt Optimization*
- **[16]** *Research report: Open Source Zuweisung 15 Abteilungen*
- **[17]** *Open-Source Frameworks & Forensik-Tools*
- **[18]** *LangGraph: Cyclical Multi-Agent Orchestration*
- **[19]** *ComfyUI: Modular Stable Diffusion & FLUX GUI*
- **[20]** *n8n: Workflow Automation Platform*
- **[21]** *Postiz: Open Source Social Media Management*
- **[22]** *Twenty: #1 Open Source CRM*
- **[23]** *Plane: Open Source Project Management Platform*
- **[24]** *Docling: Document Processing Engine*
- **[25]** *Apache Superset: Enterprise Data Exploration & BI*
- **[26]** *Qwen2.5-Coder: Code LLM & Agent Stack*
- **[27]** *Audit & Prüfbericht: Finger 6 Coding & Automation (HF Spaces)*
- **[28]** *Labor-Architektur, Agenten & B2B-Zertifikate*
- **[29]** *daten analysieren - daten analysieren*
- **[30]** *GitHub Accelerator: our first cohort and what's next*
- **[31]** *Audit & Prüfbericht: 10 Finger Masterplan (Feb 2026)*
- **[32]** *Audit & Prüfbericht: Finger 8 Online-Kurs (door-one)*
- **[33]** *Audit & Prüfbericht: Finger 7 YouTube Health-Recipes*
- **[34]** *Prüfbericht & Beweis-Audit: KI Influencerin Konzept*
- **[35]** *Audit & Methoden-Dossier: Deliberate Practice & Story Seeds*
- **[36]** *Announcing the M12 GitHub Fund* – Microsoft Ventures
- **[37]** *Agency level up Content-Datenbank*
- **[38]** *und du schreibst mir das jetzt in eine tabelle we...*
