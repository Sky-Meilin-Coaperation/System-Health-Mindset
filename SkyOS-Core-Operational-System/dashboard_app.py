import json
import gradio as gr
from pathlib import Path

manifest_file = Path("manifest.json")
data = json.loads(manifest_file.read_text(encoding="utf-8")) if manifest_file.exists() else {}

with gr.Blocks(title="Sky Meilin | Operational Dashboard") as demo:
    gr.Markdown("# 🛸 Sky Meilin – Operationales System-Dashboard")
    gr.Markdown("Zentrale Leitstelle: Strategie, Säulen, Budget und operative Roadmap.")

    with gr.Tab("Strategische Säulen"):
        gr.Markdown("### Säule 3: TECHNOLOGIE\n* Platform Architecture, API Integration, Security & Compliance, Scalability Design, DevOps Infrastructure\n* **Ziel:** Enterprise-Grade System")
        gr.Markdown("### Säule 4: MEDIA\n* Programmatic Advertising, Predictive Targeting, Cross-Channel Orchestration, Content Distribution\n* **Ziel:** Wachstumsförderung")
        gr.Markdown("### Säule 5: PERFORMANCE\n* Real-time Analytics, Multi-Touch Attribution, Predictive Forecasting, ROI Optimization\n* **Ziel:** Echtzeit-Optimierung")

    with gr.Tab("Budget & Allokation"):
        gr.Markdown("### Budget-Struktur (€2.5M Gesamtvolumen)")
        gr.DataFrame(
            headers=["Bereich", "Budget", "Anteil"],
            value=[
                ["Team", "€1.200.000", "48%"],
                ["Marketing", "€800.000", "32%"],
                ["Technologie", "€300.000", "12%"],
                ["Operations", "€200.000", "8%"]
            ]
        )
        gr.Markdown("**Infrastruktur-Status:** €0 Hostingkosten via lokaler ThinkPad-Inferenz & Free-Tier Hugging Face Spaces.")

    with gr.Tab("Roadmap (Q1 - Q4)"):
        gr.DataFrame(
            headers=["Quartal", "Monat / Fokus", "Zielgröße"],
            value=[
                ["Q1: Foundation & MVP", "Monat 1: Product Strategy & MVP Design", "€20K MRR"],
                ["Q1: Foundation & MVP", "Monat 2: MVP Development & Alpha Testing", "Product-Market Fit"],
                ["Q1: Foundation & MVP", "Monat 3: Beta Launch & Erste 3 Kunden", "3 Kunden"],
                ["Q2: Validation", "Monat 4: Refine Product & Customer Interviews", "€50K MRR"],
                ["Q2: Validation", "Monat 5: Sales Process & Marketing Start", "20 Kunden"],
                ["Q2: Validation", "Monat 6: First 10 Customers & Pilots", "10 Enterprise Pilots"],
                ["Q3: Scaling", "Monat 7: Team Hiring (2-3 Personen)", "€150K MRR"],
                ["Q3: Scaling", "Monat 8: Sales Acceleration & Enhancement", "50+ Kunden"],
                ["Q3: Scaling", "Monat 9: Channel Partnerships & Expansion", "Globale Präsenz"],
                ["Q4: Profitability", "Monat 10: Enterprise Sales & Upsell", "€1.5M ARR"],
                ["Q4: Profitability", "Monat 11: Market Expansion & Series A", "150+ Kunden"],
                ["Q4: Profitability", "Monat 12: Profitability & Series A Raise", "Profitabel"]
            ]
        )

if __name__ == "__main__":
    demo.launch(server_port=7860)
