# Richtlinien für Beiträge (CONTRIBUTING)

Vielen Dank für dein Interesse am **SkyOS Workspace Setup**! Um die Code-Integrität, Sicherheit und Urheberschaft im Ökosystem zu gewährleisten, befolge bitte die folgenden Richtlinien.

---

## 📐 Architektur- &amp; Code-Standards

1. **Clean Architecture &amp; State Management:**

  * Flutter-Komponenten folgen strikt der Trennung in *Presentation*, *Domain* und *Data* (BLoC-Pattern).
  * Python-Services nutzen typisierte DTOs für Datentransfers zwischen den Ebenen L0 bis L4.
2. **Security First (Kein Plaintext):**

  * API-Schlüssel, Passwörter oder persönliche Daten dürfen **niemals** im Quellcode gehardcodet werden.
  * Nutze stets `.env` oder den nativen Tresor (`flutter_secure_storage`).
3. **WORM Protocol &amp; Asset-Signierung:**

  * Jede wesentliche Code-Änderung oder neue Paketinstallation muss über den Security Agent signiert werden:
