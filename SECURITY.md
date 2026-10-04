# Sicherheitsrichtlinien (Security Policy)

Sicherheit bei lokaler KI-Entwicklung bedeutet: Volle Kontrolle über die eigenen Daten, keine Datenlecks nach außen und ein transparenter Umgang mit Schwachstellen.

## 1. Grundprinzipien für lokale KI-Umgebungen

- **Lokale Isolation (Air-Gap / Localhost):** Das Modell und der Server laufen standardmäßig auf `localhost:1234`. Es fließen keine Daten ungewollt an externe Dritte oder Web-Portale.
- **Keine Secrets im Quellcode:** API-Keys, Zugangsdaten oder private Pfade gehören niemals in Dateien, die in öffentliche Repositories synchronisiert werden.
- **Transparenz vor Komplexität:** Jeder Schritt und jedes Modul muss architektonisch nachvollziehbar sein.

## 2. Sicherheitslücke melden (Responsible Disclosure)

Falls du eine Sicherheitslücke oder ein potenzielles Datenleck findest:

1. Bitte eröffne **kein öffentliches GitHub-Issue**.
2. Kontaktiere die Maintainer vertraulich per E-Mail (`agencylevelup2025@gmail.com`).
3. Beschreibe die Schritte zur Reproduktion und das mögliche Schadensausmaß.
4. Wir prüfen die Meldung und stellen vor Veröffentlichung eine bereinigte Version bereit.