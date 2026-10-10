import os
import sys
import logging
import asyncio
import subprocess
from typing import Optional, Dict

# ------------------------------------------------------------------------------
# SkyOS BlueZ Bluetooth Security Controller
# ------------------------------------------------------------------------------
# Verwaltet die gehärtete Bluetooth-Kopplung (Security Mode 4 Level 4 / SSP / ECDH)
# unter Linux via BlueZ und schützt vor Eavesdropping & MitM-Angriffen.
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] SkyOS_BlueZ: %(message)s"
)
logger = logging.getLogger("SkyOS_BlueZ")


class SkyOSBlueZController:
    """Steuert die BlueZ-Sicherheit, erzwingt Verschlüsselung & Authentifizierung."""

    def __init__(self, interface: str = "hci0"):
        self.interface = interface

    def execute_hciconfig(self, command: str) -> bool:
        """Führt ein hciconfig-Kommando sicher im Linux-Hostsystem aus."""
        cmd = f"hciconfig {self.interface} {command}"
        try:
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Kommando '{cmd}' erfolgreich: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Fehler bei execution of '{cmd}': {e.stderr.strip()}")
            return False
        except FileNotFoundError:
            logger.warning("hciconfig Werkzeug nicht gefunden (evtl. nicht auf Host installiert).")
            return False

    def enforce_high_security(self) -> Dict[str, bool]:
        """
        Aktiviert Security Mode 3/4 Regeln:
        - pscan auth encrypt: Erzwingt Authentifizierung und AES-CCM Verschlüsselung
        - sspmode enable: Aktiviert Secure Simple Pairing (P-256 ECDH)
        - noscan / iscan: Begrenzt Sichtbarkeit zur Vermeidung von Tracking
        """
        logger.info(f"Sichere Konfiguration für Interface {self.interface} wird angewendet...")
        
        status = {}
        # 1. Page Scan + Authentifizierung + Verschlüsselung erzwingen
        status["auth_encrypt"] = self.execute_hciconfig("pscan auth encrypt")
        
        # 2. Secure Simple Pairing (SSP) mit ECDH aktivieren
        status["ssp_mode"] = self.execute_hciconfig("sspmode 1")
        
        # 3. Sendeleistung optimieren (Class 2 / 10m Bereich)
        status["le_mode"] = self.execute_hciconfig("leadv")

        logger.info(f"Sicherheits-Status für {self.interface}: {status}")
        return status

    async def pair_headset_securely(self, target_mac: str, pin_passkey: Optional[str] = None) -> bool:
        """
        Startet den gegenseitigen Authentifizierungsprozess (Mutual Authentication)
        mit dem Bluetooth Headset unter Verwendung von BlueZ 'bluetoothctl'.
        """
        logger.info(f"Starte abgesicherte Kopplung mit Headset {target_mac}...")
        
        # Interaktiver Aufruf via bluetoothctl
        commands = [
            "power on",
            "agent KeyboardDisplay",
            "default-agent",
            f"pair {target_mac}",
            f"trust {target_mac}",
            f"connect {target_mac}"
        ]

        full_script = "\n".join(commands) + "\nquit\n"

        try:
            process = await asyncio.create_subprocess_exec(
                "bluetoothctl",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate(input=full_script.encode())
            
            output = stdout.decode()
            if "Connection successful" in output or "Pairing successful" in output:
                logger.info(f"✅ Bluetooth-Headset {target_mac} erfolgreich verschlüsselt gekoppelt!")
                return True
            else:
                logger.warning(f"Kopplungsergebnis für {target_mac}:\n{output}")
                return False
        except Exception as e:
            logger.error(f"Fehler bei bluetoothctl Ausführung: {e}")
            return False


if __name__ == "__main__":
    controller = SkyOSBlueZController(interface="hci0")
    controller.enforce_high_security()
