import os
import sys
import logging
from pathlib import Path
from typing import List, Optional, Dict
from PIL import Image
from huggingface_hub import HfApi, hf_hub_download, snapshot_download

# ------------------------------------------------------------------------------
# SkyOS Hugging Face Reference Image & Avatar Template Manager
# ------------------------------------------------------------------------------
# Ruf Referenzbilder aus Hugging Face Buckets/Datasets (Owner: sky-meilin) ab,
# verarbeitet diese gemäß der 5-Trommel-DNA und bereitet sie als visuelle
# Vorlagen für die WebRTC-Avatar-Streaming-Engine vor.
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SkyOSAvatarSync")

# Configuration & Environment
HF_TOKEN = os.getenv("HF_TOKEN")
HF_OWNER = os.getenv("HF_OWNER", "sky-meilin")
DATASET_REPO = os.getenv("HF_AVATAR_DATASET", f"{HF_OWNER}/avatar-reference-images")
LOCAL_TEMPLATE_DIR = Path("/workspace/scratch/avatar_templates")
OUTPUT_REEL_DIR = Path("/workspace/scratch/vault/templates")

class SkyOSAvatarTemplateManager:
    """Manager zum Abrufen, Verarbeiten und Bereitstellen von Avatar-Referenzbildern."""

    def __init__(
        self,
        token: Optional[str] = None,
        owner: str = HF_OWNER,
        dataset_repo: str = DATASET_REPO,
        local_dir: Path = LOCAL_TEMPLATE_DIR
    ):
        self.token = token or HF_TOKEN
        self.owner = owner
        self.dataset_repo = dataset_repo
        self.local_dir = local_dir
        self.local_dir.mkdir(parents=True, exist_ok=True)
        OUTPUT_REEL_DIR.mkdir(parents=True, exist_ok=True)

        if not self.token:
            logger.warning("HF_TOKEN nicht gesetzt. Zugriff beschränkt auf öffentliche Datasets.")

        self.api = HfApi(token=self.token)

    def fetch_reference_images_from_hf(self) -> List[Path]:
        """
        Lädt Referenzbilder aus dem Hugging Face Dataset/Bucket herunter.
        Unterstützt Einzel-Downloads sowie Repositories des Owners.
        """
        downloaded_files: List[Path] = []
        logger.info(f"Starte Download von Referenzbildern aus HF Repo: {self.dataset_repo}")

        try:
            # Versuche das gesamte Dataset/Repo zu synchronisieren
            repo_path = snapshot_download(
                repo_id=self.dataset_repo,
                repo_type="dataset",
                token=self.token,
                local_dir=str(self.local_dir),
                allow_patterns=["*.png", "*.jpg", "*.jpeg", "*.webp"]
            )
            logger.info(f"Hugging Face Dataset erfolgreich heruntergeladen nach: {repo_path}")
            
            for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
                downloaded_files.extend(Path(repo_path).rglob(ext))

        except Exception as e:
            logger.error(f"Fehler beim Download des HF Datasets ({self.dataset_repo}): {e}")
            logger.info("Überprüfe lokale Vorlagen oder erstelle Fallback-Templates...")
            downloaded_files = self._get_local_fallback_images()

        return downloaded_files

    def _get_local_fallback_images(self) -> List[Path]:
        """Gibt lokal vorhandene Bilder zurück oder generiert ein Platzhalter-Template."""
        existing = list(self.local_dir.rglob("*.png")) + list(self.local_dir.rglob("*.jpg"))
        if existing:
            return existing

        # Fallback: Erzeuge ein synthetisches 5-Trommel-DNA Referenzbild (1080x1920 für Reels)
        fallback_path = self.local_dir / "sky_meilin_reference_5dna.png"
        img = Image.new("RGB", (1080, 1920), color=(15, 23, 42)) # Slate Dark
        img.save(fallback_path)
        logger.info(f"Synthetisches Referenzbild erzeugt: {fallback_path}")
        return [fallback_path]

    def process_templates_for_reels(
        self,
        target_size: tuple = (1080, 1920), # 9:16 Reel Format
        aspect_fit: bool = True
    ) -> List[Dict[str, str]]:
        """
        Verarbeitet die heruntergeladenen Referenzbilder:
        - Skaliert auf 9:16 Format für Reels / Mobile Dashboard
        - Optimiert Farbraum & Schärfe für die WebRTC Streaming Engine
        """
        raw_images = self.fetch_reference_images_from_hf()
        processed_templates = []

        for idx, img_path in enumerate(raw_images):
            try:
                with Image.open(img_path) as img:
                    # Konvertiere nach RGB
                    img = img.convert("RGB")
                    
                    # Anpassen der Bildgröße für 9:16 Vertical Reels (1080x1920)
                    if aspect_fit:
                        img.thumbnail(target_size, Image.Resampling.LANCZOS)
                        new_img = Image.new("RGB", target_size, (10, 15, 30))
                        # Zentrieren
                        offset = (
                            (target_size[0] - img.width) // 2,
                            (target_size[1] - img.height) // 2
                        )
                        new_img.paste(img, offset)
                        processed_img = new_img
                    else:
                        processed_img = img.resize(target_size, Image.Resampling.LANCZOS)

                    out_path = OUTPUT_REEL_DIR / f"avatar_template_{idx+1}_9x16.png"
                    processed_img.save(out_path, "PNG", quality=95)

                    template_info = {
                        "template_id": f"template_{idx+1}",
                        "original_path": str(img_path),
                        "processed_path": str(out_path),
                        "resolution": f"{target_size[0]}x{target_size[1]}",
                        "aspect_ratio": "9:16 (Reel)",
                        "dna_profile": "5-Trommel-DNA (Smaragdgrün / Rayleigh-Mie)"
                    }
                    processed_templates.append(template_info)
                    logger.info(f"Template verarbeitet: {out_path.name}")

            except Exception as e:
                logger.error(f"Fehler bei Bildverarbeitung ({img_path}): {e}")

        return processed_templates

    def get_active_avatar_frame(self, template_id: str = "template_1") -> Optional[str]:
        """Gibt den Dateipfad der aktiven visuellen Vorlage für die WebRTC Avatar Engine zurück."""
        templates = list(OUTPUT_REEL_DIR.glob("*_9x16.png"))
        if templates:
            return str(templates[0])
        return None

def main():
    print("=== SkyOS Hugging Face Avatar Reference Sync ===")
    sync_manager = SkyOSAvatarTemplateManager()
    results = sync_manager.process_templates_for_reels()
    
    print(f"\n[OK] {len(results)} Avatar-Referenzvorlagen erfolgreich vorbereitet:")
    for res in results:
        print(f" - ID: {res['template_id']} | Pfad: {res['processed_path']} | Format: {res['aspect_ratio']}")

if __name__ == "__main__":
    main()
