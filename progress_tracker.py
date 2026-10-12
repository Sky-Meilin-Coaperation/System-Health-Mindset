import os
import sys
import sqlite3
import json
import hashlib
import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_DIR = Path(__file__).resolve().parent
DB_PATH = WORKSPACE_DIR / "data" / "L4_organized" / "progress_tracker.db"
LEDGER_PATH = WORKSPACE_DIR / "data" / "L4_organized" / "worm_ledger.jsonl"

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS progress_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_number INTEGER UNIQUE,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        file_path TEXT NOT NULL,
        action_type TEXT NOT NULL,
        status TEXT DEFAULT 'PENDING',
        description TEXT NOT NULL,
        code_snippet TEXT NOT NULL,
        updated_at TEXT
    )
    ''')

    cards = [
        (0, 'System- & WSL-Umgebung initialisieren', 'Setup', '.', 'EXECUTE', 'DONE', 'Pruefung des Arbeitsverzeichnisses unter Windows & WSL Ubuntu.', 'cd "C:\\Workspace LM studio"'),
        (1, 'GitHub Konto & SSH-Schluessel', 'Security', '~/.ssh/id_ed25519', 'CONFIG', 'DONE', 'Erstellung des SSH-Keys und Hinterlegen auf GitHub', 'ssh-keygen -t ed25519 && cat ~/.ssh/id_ed25519.pub'),
        (2, 'Git Repository Init & Branch Main', 'Git', '.git', 'GIT', 'DONE', 'Git-Repository lokal initialisieren und Hauptbranch festlegen', 'git init && git branch -M main'),
        (3, 'Passwort & Secret-Schutz (.gitignore)', 'Security', '.gitignore', 'FILE', 'DONE', 'Sperren von .env, Logs und temporaeren Daten fuer Git-Commits', 'cat .gitignore'),
        (4, 'Umgebungsvariablen (.env)', 'Config', '.env', 'FILE', 'DONE', 'API-Endpunkte fuer LM Studio (Port 1234) und Ollama (Port 11434)', 'cat .env'),
        (5, 'VS Code Terminal-Profile (.vscode/settings.json)', 'VS Code', '.vscode/settings.json', 'FILE', 'DONE', 'Fixieren des Startordners fuer PowerShell & Ubuntu Terminal', 'cat .vscode/settings.json'),
        (6, 'Lizenzdatei (LICENSE - Sustainable Use)', 'Legal', 'LICENSE', 'FILE', 'DONE', 'Schutz vor kommerzieller SaaS-Ausbeutung durch Dritte (v1.0)', 'cat LICENSE'),
        (7, 'L4 Organized Master Manifest', 'Data Level L4', 'data/L4_organized/skyos_manifest.json', 'FILE', 'DONE', 'System-Manifest mit WORM-Status und Endpunkt-Verzeichnis', 'cat data/L4_organized/skyos_manifest.json'),
        (8, 'WORM Security Agent (Prioritaetsnachweis)', 'Security Agent', 'security_agent.py', 'PYTHON', 'DONE', 'SHA-256 Hash-Chain Guard fuer Proof of Prior Art', 'python security_agent.py'),
        (9, 'Lokale Inferenz-Server (LM Studio & Ollama)', 'Monitoring', 'LM Studio / Ollama', 'SERVER', 'DONE', 'Validierung der lokalen KI-Server auf Port 1234 und 11434', 'lms status && ollama list'),
        (10, 'Fortschritts- & Checklisten DB', 'Core DB', 'progress_tracker.py', 'PYTHON', 'DONE', 'Interaktiver Fortschritts-Tracker verknuepft mit SQLite & WORM', 'python progress_tracker.py list'),
        (11, 'Git Commit & GitHub Remote Sync', 'Deployment', 'Git Remote', 'GIT', 'PENDING', 'Sichern und Hochladen aller initialisierten Komponenten auf GitHub', 'git add . && git commit -m "SkyOS Setup" && git push')
    ]

    for c in cards:
        cur.execute('''
        INSERT OR REPLACE INTO progress_cards 
        (card_number, title, category, file_path, action_type, status, description, code_snippet, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], datetime.datetime.now(datetime.timezone.utc).isoformat()))

    conn.commit()
    conn.close()
    print("[SUCCESS] Progress Database initialisiert unter:", str(DB_PATH))

def list_cards():
    if not DB_PATH.exists():
        init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT card_number, title, category, status, file_path FROM progress_cards ORDER BY card_number ASC")
    rows = cur.fetchall()
    conn.close()

    print("\n==========================================================================")
    print(" [i] SKYOS SETUP PROGRESS CHECKLIST (SQLITE & WORM INTEGRATED)")
    print("==========================================================================")
    for r in rows:
        symbol = "[x] DONE   " if r[3] == "DONE" else "[ ] PENDING"
        print(f"Karte {r[0]:02d} | {symbol} | [{r[2]}] {r[1]}")
        print(f"         +-- Zielpfad: {r[4]}")
    print("==========================================================================\n")

def complete_card(card_num):
    if not DB_PATH.exists():
        init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cur.execute("UPDATE progress_cards SET status = 'DONE', updated_at = ? WHERE card_number = ?", (timestamp, card_num))
    conn.commit()

    cur.execute("SELECT card_number, title, file_path FROM progress_cards WHERE card_number = ?", (card_num,))
    card = cur.fetchone()
    conn.close()

    if card:
        log_entry = {
            "timestamp_utc": timestamp,
            "event_type": "CARD_COMPLETED",
            "card_number": card[0],
            "title": card[1],
            "target_file": card[2]
        }
        current_hash = hashlib.sha256(json.dumps(log_entry, sort_keys=True).encode('utf-8')).hexdigest()
        log_entry["current_hash"] = current_hash

        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(str(LEDGER_PATH), "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        print(f"[COMPLETED] Karte {card_num:02d} ({card[1]}) als ERLEDIGT markiert.")
        print(f"             +-- WORM SHA-256 Hash: {current_hash[:16]}...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "init":
            init_db()
        elif cmd == "list":
            list_cards()
        elif cmd == "complete" and len(sys.argv) > 2:
            complete_card(int(sys.argv[2]))
        else:
            print("Nutzung: python progress_tracker.py [init|list|complete <nr>]")
    else:
        list_cards()
