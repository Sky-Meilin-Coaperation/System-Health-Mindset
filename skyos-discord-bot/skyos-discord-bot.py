import os
import sys
import logging
import asyncio
import httpx
import discord
from discord.ext import commands

# ------------------------------------------------------------------------------
# SkyOS Discord Bot - Native Python Implementation
# ------------------------------------------------------------------------------
# Dieser Bot ersetzt n8n vollkommen und kommuniziert direkt über den FastAPI Core
# Gateway (:8000) mit dem Joy AI Orchestrator, der Telemetrie und der arXiv-Engine.
# ------------------------------------------------------------------------------

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SkyOSDiscordBot")

# Environment Variables & Configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")
HF_TOKEN = os.getenv("HF_TOKEN")

if not DISCORD_BOT_TOKEN:
    logger.warning("DISCORD_BOT_TOKEN Umgebungsvariable ist aktuell nicht gesetzt!")

# Bot Setup mit benötigten Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Async HTTP Client für FastAPI Kommunikation
http_client = httpx.AsyncClient(base_url=FASTAPI_BASE_URL, timeout=30.0)


@bot.event
async def on_ready():
    """Event-Handler beim erfolgreichen Start des Bots."""
    logger.info(f"SkyOS Discord Bot erfolgreich eingeloggt als: {bot.user} (ID: {bot.user.id})")
    logger.info(f"Verbunden mit FastAPI Core Gateway unter: {FASTAPI_BASE_URL}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!status | SkyOS Command Center"
        )
    )


@bot.command(name="status", help="Ruft die aktuelle SkyOS System-Telemetrie ab")
async def get_status(ctx):
    """Holt Echtzeit-Telemetriedaten aus der FastAPI Core Engine."""
    await ctx.typing()
    try:
        response = await http_client.get("/api/v1/telemetry")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="⚙️ SkyOS System Telemetrie",
                color=discord.Color.blue()
            )
            embed.add_field(name="Status", value=data.get("status", "Online"), inline=True)
            embed.add_field(name="Fehlerrate", value=f"{data.get('error_rate', 0.0)}%", inline=True)
            embed.add_field(name="Zeitstempel", value=data.get("timestamp", "N/A"), inline=False)
            embed.add_field(name="Metrics", value=data.get("metrics", "ThinkPad / HF Spaces OK"), inline=False)
            embed.set_footer(text="SkyOS Core Engine | ErrorTracker")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Fehler beim Abfragen der Telemetrie (Status: {response.status_code})")
    except Exception as e:
        logger.error(f"Fehler in !status: {e}")
        await ctx.send(f"⚠️ Verbindung zum FastAPI Backend fehlgeschlagen: {e}")


@bot.command(name="ask", help="Fragt den Joy AI Orchestrator & das Knowledge System (L0-L4)")
async def ask_skyos(ctx, *, query: str):
    """Sendet eine Wissensabfrage an das SkyAI Knowledge System."""
    await ctx.typing()
    try:
        payload = {"query": query, "tier": "L4_Organized"}
        response = await http_client.post("/api/v1/knowledge/query", json=payload)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            answer_text = "\n".join([str(r) for r in results]) if results else "Keine direkten Treffer in der Knowledge Base gefunden."
            
            # Formatierung für Discord Maximallänge (2000 Zeichen Limit)
            if len(answer_text) > 1900:
                answer_text = answer_text[:1900] + "\n\n*(Antwort aufgrund von Zeichenlimit gekürzt)*"
                
            embed = discord.Embed(
                title="🧠 Joy AI Knowledge Response",
                description=answer_text,
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Context Tier: {data.get('tier', 'L4_Organized')} | SkyOS Assistant")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Fehler bei der Knowledge-Abfrage: {response.text}")
    except Exception as e:
        logger.error(f"Fehler in !ask: {e}")
        await ctx.send(f"⚠️ Backend-Fehler: {e}")


@bot.command(name="papersync", help="Startet die automatische arXiv-Paper-Synchronisation")
async def trigger_paper_sync(ctx):
    """Startet das arxiv_paper_sync.py Skript über FastAPI BackgroundTasks."""
    await ctx.typing()
    try:
        response = await http_client.post("/api/v1/workflows/paper-sync/trigger", json={})
        if response.status_code in [200, 202]:
            embed = discord.Embed(
                title="📚 arXiv Paper-Synchronisation",
                description="Das Skript `arxiv_paper_sync.py` wurde gestartet. Neue Arbeiten aus Hugging Face Collections werden jetzt verarbeitet.",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Synchronisation konnte nicht gestartet werden: {response.text}")
    except Exception as e:
        logger.error(f"Fehler in !papersync: {e}")
        await ctx.send(f"⚠️ Trigger-Fehler: {e}")


@bot.command(name="voice_join", help="Tritt dem aktuellen Voice Channel des Nutzers bei")
async def voice_join(ctx):
    """Verbindet den Bot mit dem Sprachkanal für zukünftiges Audio/Speech-Streaming."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎙️ **SkyOS Assistant** ist dem Sprachkanal `{channel.name}` beigetreten.")
    else:
        await ctx.send("⚠️ Du musst dich in einem Sprachkanal befinden, um diesen Befehl zu nutzen.")


@bot.command(name="voice_leave", help="Verlässt den aktuellen Voice Channel")
async def voice_leave(ctx):
    """Trennt die Sprachverbindung."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Sprachverbindung getrennt.")
    else:
        await ctx.send("⚠️ Der Bot befindet sich in keinem Sprachkanal.")


def main():
    token = DISCORD_BOT_TOKEN
    if not token:
        print("CRITICAL ERROR: 'DISCORD_BOT_TOKEN' ist nicht als Umgebungsvariable gesetzt.")
        print("Bitte setze das Secret vor dem Start: export DISCORD_BOT_TOKEN='dein_token'")
        sys.exit(1)
    
    bot.run(token)


if __name__ == "__main__":
    main()
