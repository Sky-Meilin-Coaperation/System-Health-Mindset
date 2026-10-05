class ErrorTracker {
  constructor(endpoint) {
    this.endpoint = endpoint || "/api/telemetry";
  }

  captureException(error, context = {}) {
    const payload = {
      timestamp: new Date().toISOString(),
      name: error.name || "RuntimeError",
      message: error.message || String(error),
      stack: error.stack || null,
      context: context
    };
    
    console.error("[SkyOS Telemetry] Kritischer Fehler registriert:", payload);
    
    if (typeof fetch !== "undefined") {
      fetch(this.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).catch(err => console.warn("[SkyOS Telemetry] Offline-Puffer aktiv:", err));
    }
  }
}

if (typeof module !== "undefined") {
  module.exports = { ErrorTracker };
}
