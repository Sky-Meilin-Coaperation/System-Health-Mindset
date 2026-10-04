import os
import asyncio
import lmstudio as lms

API_HOST = "localhost:1234"
# Falls du in LM Studio explizit ein Token aktiviert hast:
API_TOKEN = "sk-lm-WeLRcE1N:pHNCHI0G1Ia3lc8wnh4N"
PROMPT = "Antworte kurz mit genau drei Worten: LM Studio laeuft."

def check_server():
    print("Pruefe Verbindung zu LM Studio...")
    # Token-Umgebungsvariable standardmaessig bereinigen, um Fehler zu vermeiden
    os.environ.pop("LM_API_TOKEN", None)

def test_convenience():
    print("--- 1. Test: Convenience API ---")
    lms.configure_default_client(API_HOST)
    # Erstes geladenes Modell abgreifen
    model = lms.llm()
    result = model.respond(PROMPT)
    print(f"Antwort:\n{result}\n")

def test_scoped():
    print("--- 2. Test: Scoped Resource API ---")
    with lms.Client(api_host=API_HOST) as client:
        model = client.llm.model()
        result = model.respond(PROMPT)
        print(f"Antwort:\n{result}\n")

async def test_async():
    print("--- 3. Test: Asynchronous API ---")
    async with lms.AsyncClient(api_host=API_HOST) as client:
        model = await client.llm.model()
        result = await model.respond(PROMPT)
        print(f"Antwort:\n{result}\n")

if __name__ == "__main__":
    check_server()
    try:
        test_convenience()
        test_scoped()
        asyncio.run(test_async())
        print("Alle drei API-Tests erfolgreich abgeschlossen!")
    except Exception as e:
        print(f"\nHinweis: Falls Authentication verlangt wird, setze den Token in LM Studio Server Settings.")
        print(f"Fehler: {e}")
