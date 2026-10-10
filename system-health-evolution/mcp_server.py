from mcp.server.fastmcp import FastMCP
import os
import requests

mcp = FastMCP("System Health Evolution")

@mcp.tool()
def ask_ollama(prompt: str, model: str = "deepseek-r1-0528-qwen3-8b") -> str:
    """Sendet einen Prompt an die lokale Ollama-Instanz."""
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    try:
        response = requests.post(
            f"{ollama_host}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        return response.json().get("response", "Keine Antwort erhalten.")
    except Exception as e:
        return f"Fehler bei Verbindung zu Ollama: {str(e)}"

if __name__ == "__main__":