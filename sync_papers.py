import os
import re
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from huggingface_hub import HfApi

BASE_DIR = Path(__file__).resolve().parent

# SSL-Kontext fuer Windows einrichten (nutzt certifi falls vorhanden, sonst unverified fallback)
try:
    import certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
except Exception:
    ssl_context = ssl._create_unverified_context()

TARGET_DIR = BASE_DIR / "papers"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

api = HfApi(token=os.getenv("HF_TOKEN"))
owner = "sky-meilin"

print(f"Lese Sammlungen fuer {owner} aus...")
paper_ids = set()

default_papers = {
    "2604.06392", "2603.24517", "2605.10988", "2605.25624",
    "2605.19633", "2605.14386", "2602.09146", "2601.21459",
    "2602.02276", "2310.07321", "2302.04844", "2311.05556",
    "2309.09400", "2305.06161", "2302.14534", "2303.11408",
    "2310.03739", "2310.18840"
}
paper_ids.update(default_papers)

try:
    cols = list(api.list_collections(owner=owner))
    for c in cols:
        full = api.get_collection(c.slug)
        for item in full.items:
            if item.item_type == "paper":
                paper_ids.add(item.item_id)
except Exception as e:
    print(f"Hinweis: Nutze Standardliste ({e})")

print(f"Gefundene arXiv-Papiere: {len(paper_ids)}")

def fetch_arxiv_meta(arxiv_id):
    clean_id = re.sub(r"v\d+$", "", arxiv_id)
    url = f"https://export.arxiv.org/api/query?id_list={clean_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "SkyOS-PaperSync/1.0"})
    
    try:
        with urllib.request.urlopen(req, context=ssl_context) as resp:
            tree = ET.fromstring(resp.read())
    except Exception as e:
        print(f"   [FEHLER] Abruf fuer {clean_id}: {e}")
        return None
    
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entry = tree.find("atom:entry", ns)
    if entry is None or entry.find("atom:title", ns) is None:
        return None
    
    title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
    summary = entry.find("atom:summary", ns).text.strip()
    authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
    published = entry.find("atom:published", ns).text[:10] if entry.find("atom:published", ns) is not None else ""
    
    return {
        "id": clean_id,
        "title": title,
        "authors": authors,
        "summary": summary,
        "published": published,
        "pdf_url": f"https://arxiv.org/pdf/{clean_id}.pdf",
        "abs_url": f"https://arxiv.org/abs/{clean_id}"
    }

index_rows = []

for pid in sorted(paper_ids):
    print(f" - Verarbeite arXiv:{pid}...")
    meta = fetch_arxiv_meta(pid)
    if not meta:
        continue
    
    filename = f"arxiv_{meta['id'].replace('.', '_')}.md"
    filepath = TARGET_DIR / filename
    
    content = f"""# {meta['title']}

- **arXiv ID:** [{meta['id']}]({meta['abs_url']})
- **PDF:** [Direktlink]({meta['pdf_url']})
- **Veroeffentlicht:** {meta['published']}
- **Autoren:** {', '.join(meta['authors'])}

---

## Zusammenfassung / Abstract

{meta['summary']}

---
*Automatisch synchronisiert via SkyOS Repository Sync.*
"""
    filepath.write_text(content, encoding="utf-8")
    index_rows.append(f"| [{meta['id']}]({meta['abs_url']}) | [{meta['title']}]({filename}) | {meta['published']} | [PDF]({meta['pdf_url']}) |")

readme_path = TARGET_DIR / "README.md"
readme_content = f"""# arXiv Forschungsbibliothek (SkyOS)

Uebersicht aller in den Hugging Face Collections archivierten Paper.

| arXiv ID | Titel | Datum | PDF |
| :--- | :--- | :--- | :--- |
""" + "\n".join(index_rows) + "\n"

readme_path.write_text(readme_content, encoding="utf-8")
print("\n[ERFOLG] Alle Paper wurden im Ordner 'papers/' als Markdown abgelegt.")
