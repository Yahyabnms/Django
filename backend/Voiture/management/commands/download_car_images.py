from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db.models import Q
from django.conf import settings
import requests
import re
from pathlib import Path
from Voiture.models import Voiture


class Command(BaseCommand):
    help = "Télécharge des images de voitures (Unsplash) et les assigne au catalogue"

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='unsplash',
            choices=['unsplash', 'pexels'],
            help='Source des images: unsplash ou pexels'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help="Nombre max de voitures à traiter (0 = toutes)"
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Remplacer les images existantes'
        )
        parser.add_argument(
            '--timeout',
            type=int,
            default=20,
            help="Timeout (secondes) pour chaque téléchargement"
        )
        parser.add_argument(
            '--local-first',
            action='store_true',
            help="Assigner d'abord des images locales deja presentes dans MEDIA_ROOT/voitures/ si disponibles"
        )

    def handle(self, *args, **options):
        source = options['source']
        force = options['force']
        limit = options['limit']
        timeout = options['timeout']
        local_first = options['local_first']

        self.stdout.write(self.style.SUCCESS("Telechargement d'images pour le catalogue..."))

        local_pool = self._collect_local_images()
        if local_pool and local_first:
            self.stdout.write(self.style.SUCCESS(f"Images locales detectees: {len(local_pool)} fichier(s)"))

        voitures = Voiture.objects.all().order_by('id')
        if not force:
            voitures = voitures.filter(Q(image__isnull=True) | Q(image=''))
        if limit and limit > 0:
            voitures = voitures[:limit]

        count = 0
        for voiture in voitures:
            try:
                if local_pool and local_first:
                    self.assign_from_local_pool(voiture, local_pool)
                else:
                    if source == 'unsplash':
                        self.download_from_unsplash(voiture, timeout=timeout)
                    elif source == 'pexels':
                        self.download_from_pexels(voiture, timeout=timeout)

                count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"OK: {voiture.marque} {voiture.modele}"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"ERREUR: {voiture.marque} {voiture.modele}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"\nTERMINE: {count} images de voitures telechargees!")
        )

    def download_from_unsplash(self, voiture, timeout: int = 20):
        """Télécharge une image de voiture depuis Unsplash."""
        car_images = [
            # Note: les URLs "auto=format" peuvent 404 selon le réseau/CDN.
            # On garde des liens qui fonctionnent généralement avec ixlib + w.
            'https://images.unsplash.com/photo-1619405399517-d4dc2500eaa0?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1566023967268-70fbd8ac6e84?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1552832860-cfb67165eaf0?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1598643881987-93f70ea41f40?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1527814050087-3793815479db?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1549399542-7e3f8b83ad38?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1542282088-fe8426682b8f?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1609034227505-5876f6aa4e90?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1611707267537-b85faf00021e?ixlib=rb-4.0.3&w=1400',
            'https://images.unsplash.com/photo-1605559424843-9e4c3ff86b90?ixlib=rb-4.0.3&w=1400',
        ]
        
        image_url = car_images[voiture.id % len(car_images)]
        content = self._download_image_bytes_with_fallbacks(image_url, timeout=timeout)
        filename = self._safe_filename(voiture)
        voiture.image.save(filename, ContentFile(content), save=True)

    def download_from_pexels(self, voiture, timeout: int = 20):
        """Pexels nécessite une API key: fallback Unsplash."""
        self.download_from_unsplash(voiture, timeout=timeout)

    def assign_from_local_pool(self, voiture, local_pool: list[Path]):
        """
        Assigne une image existante dans MEDIA_ROOT/voitures/ au vehicule.
        Utile quand tu as deja des images (scraping/demo) et tu veux remplir le catalogue vite.
        """
        img_path = local_pool[voiture.id % len(local_pool)]
        content = img_path.read_bytes()
        filename = self._safe_filename(voiture)
        voiture.image.save(filename, ContentFile(content), save=True)

    def _collect_local_images(self) -> list[Path]:
        """
        Cherche des images deja presentes localement.
        - Priorite: MEDIA_ROOT/voitures/
        - Fallback: ./media/voitures/ (au niveau du projet)
        """
        candidates: list[Path] = []
        media_root = Path(getattr(settings, "MEDIA_ROOT", "")) if getattr(settings, "MEDIA_ROOT", "") else None
        if media_root:
            candidates.append(media_root / "voitures")
        candidates.append(Path.cwd() / "media" / "voitures")

        exts = {".jpg", ".jpeg", ".png", ".webp"}
        found: list[Path] = []
        for folder in candidates:
            if folder and folder.exists() and folder.is_dir():
                for p in folder.iterdir():
                    if p.is_file() and p.suffix.lower() in exts:
                        found.append(p)
        # deterministe
        found.sort(key=lambda p: p.name.lower())
        return found

    def _download_image_bytes(self, url: str, timeout: int = 20) -> bytes:
        headers = {
            "User-Agent": "AutoLocationBot/1.0 (+local dev)",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        }
        r = requests.get(url, timeout=timeout, headers=headers)
        r.raise_for_status()
        content_type = (r.headers.get("Content-Type") or "").lower()
        if "image" not in content_type:
            raise ValueError(f"URL ne renvoie pas une image (content-type={content_type})")
        return r.content

    def _download_image_bytes_with_fallbacks(self, url: str, timeout: int = 20) -> bytes:
        candidates = [url]
        if "ixlib=" in url and "&w=" in url:
            candidates.append(re.sub(r"&w=\\d+", "&w=800", url))
        if "?" in url:
            candidates.append(url.split("?")[0] + "?ixlib=rb-4.0.3&w=1200")

        last_err = None
        for candidate in candidates:
            try:
                return self._download_image_bytes(candidate, timeout=timeout)
            except Exception as e:
                last_err = e
        raise last_err

    def _safe_filename(self, voiture) -> str:
        base = voiture.immatriculation or f"voiture-{voiture.id}"
        base = re.sub(r"[^a-zA-Z0-9_-]+", "_", base).strip("_")
        if not base:
            base = f"voiture-{voiture.id}"
        return f"{base}.jpg"
