# 1. Aktuelles Debian-Derivat als Basis nutzen (Schließt viele bekannte OS-Lücken)
FROM python:3.11-slim-bookworm

WORKDIR /app

# 2. System-Pakete aktualisieren, um CVEs in System-Bibliotheken zu patchen
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Nicht-Root-Benutzer anlegen (Verhindert Root-Zugriff bei Kompromittierung)
RUN useradd -m -u 1000 appuser

# 4. Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Anwendungscode kopieren
COPY . .

# 6. Dateiberechtigungen an den neuen User übergeben
RUN chown -R appuser:appuser /app

# 7. Zu diesem User wechseln
USER appuser

# Standardbefehl zum Starten des MCP-Servers
CMD ["python", "mcp_server.py"]