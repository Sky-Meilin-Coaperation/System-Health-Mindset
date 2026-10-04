import json
import urllib.request
import urllib.error

API_URL = "http://localhost:1234/v1/chat/completions"

def test_lm_studio():
    print("Pruefe Verbindung zu LM Studio auf Port 1234...")
    payload = {
        "messages": [
            {"role": "system", "content": "Antworte praezise und kurz."},
            {"role": "user", "content": "Antworte genau mit drei Worten: LM Studio laeuft."}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            answer = result["choices"][0]["message"]["content"]
            print("\n[ERFOLG] Antwort von LM Studio:")
            print(answer)
    except urllib.error.URLError as e:
        print("\n[FEHLER] Verbindung fehlgeschlagen.")
        print("Stelle sicher, dass LM Studio laeuft und der Server auf Port 1234 gestartet ist.")
        print(f"Details: {e}")

if __name__ == "__main__":
    test_lm_studio()
