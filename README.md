# System Health Evolution - Technische Architektur & Dokumentation

Diese zweite README-Datei dient als technische Ergänzung und Entwickler-Dokumentation für die dezentrale Infrastruktur unter dem Namen **System Health Evolution**.

---

## 1. Systemarchitektur & Komponenten

Die Architektur ist strikt modular und lokal/dezentral aufgebaut, um maximale Datensouveränität und Isolierung zu gewährleisten.

* **Open-Source WordPress (`wordpress.org`):** Dient als Content-Management- und Publikations-Backend, betrieben in einer isolierten Docker-Umgebung[cite: 1].
* **MariaDB:** Stellt die relationale Datenbank für das WordPress-System bereit.
* **Ollama (Lokale KI):** Fungiert als lokaler Microservice für die dezentrale Generierung von Texten und Inhalten, vollständig entkoppelt von externen Cloud-APIs.
* **Ökosystem-Anbindung (Automattic):** Integration von **Gravatar** für Profilbilder und **Jetpack** für Statistiken und Sicherheitsfunktionen (unter Berücksichtigung der entsprechenden Datenübertragungen in die USA)[cite: 1].

---

## 2. Kommunikations- & Plattform-Integration

* **Messaging & Community:** Direkter Austausch und Benachrichtigungen über **Discord** und **ICQ** (vollständig ohne Telegram oder proprietäre Alternativen).
* **Creator-Plattform:** Anbindung an **Fanvue** für Abonnements, digitale Inhalte und die strikte Einhaltung von Creator-Richtlinien sowie Jugendschutzstandards[cite: 1].

---

## 3. Compliance, Datenschutz & KI-Kennzeichnung

* **EU AI Act & Transparenz:** Alle automatisiert oder durch KI erstellten Inhalte (sowie virtuelle Profile) sind direkt am Content als solche zu kennzeichnen.
* **Datenschutz (DSGVO):** Transparente Offenlegung aller verwendeten Automattic-Dienste (Jetpack, Gravatar) sowie der lokalen Verarbeitungsprozesse.
