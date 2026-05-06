from django.core.management.base import BaseCommand
from Voiture.models import Voiture
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Associe les images du dossier static/images/voitures aux voitures'

    def handle(self, *args, **options):
        # Utiliser un chemin relatif correct par rapport à la racine du projet Django (le dossier backend)
        images_dir = 'Base/static/images/voitures'
        base_path = os.path.join(os.getcwd(), 'backend', images_dir)
        
        if not os.path.exists(base_path):
            self.stdout.write(self.style.ERROR(f'Dossier non trouvé: {base_path}'))
            return
        
        # Mapping nom de fichier -> (marque, modele)
        image_mapping = {
            'Audi A3.jpg': ('Audi', 'A3'),
            'Audi Q3.jpg': ('Audi', 'Q3'),
            'Audi Q5.png': ('Audi', 'Q5'),
            'BMW Série 1.jpeg': ('BMW', 'Série 1'),
            'Citroen C5.jpg': ('Citroën', 'C5'),
            'Citroën Berlingo.jpeg': ('Citroën', 'Berlingo'),
            'Citroën C4.jpg': ('Citroën', 'C4'),
            'Dacia_Lodgy_1.png': ('Dacia', 'Lodgy'),
            'Ford Puma.jpg': ('Ford', 'Puma'),
            'honda CIVIC.jpeg': ('Honda', 'Civic'),
            'Honda CR-V.jpg': ('Honda', 'CR-V'),
            'Hyundai-santafe.webp': ('Hyundai', 'Santa Fe'),
            'Kia Picanto.jpeg': ('Kia', 'Picanto'),
            'Kia Sportage.jpg': ('Kia', 'Sportage'),
            'Nissan Micra.jpg': ('Nissan', 'Micra'),
            'Peugeot 2008.jpg': ('Peugeot', '2008'),
            'Renault Captur.png': ('Renault', 'Captur'),
            'Renault Clio.jpg': ('Renault', 'Clio'),
            'Renault Kangoo.jpg': ('Renault', 'Kangoo'),
            'Renault Megane.jpg': ('Renault', 'Megane'),
            'Toyota Corolla.png': ('Toyota', 'Corolla'),
            'Toyota Yaris.jpg': ('Toyota', 'Yaris'),
            'Volkswagen Golf 8.png': ('Volkswagen', 'Golf 8'),
            'Volkswagen Golf.jpg': ('Volkswagen', 'Golf'),
            'Volkswagen Tiguan.png': ('Volkswagen', 'Tiguan'),
        }
        
        assigned = 0
        
        for filename, (marque, modele) in image_mapping.items():
            filepath = os.path.join(base_path, filename)
            
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'Fichier non trouvé: {filename}'))
                continue
            
            # Chercher la voiture correspondante
            try:
                voiture = Voiture.objects.get(marque__iexact=marque, modele__iexact=modele)
                
                # Sauvegarder l'image
                with open(filepath, 'rb') as f:
                    voiture.image.save(filename, File(f), save=True)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Image assignée: {filename} -> {voiture.marque} {voiture.modele}'
                    )
                )
                assigned += 1
                
            except Voiture.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Voiture non trouvée: {marque} {modele}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nTotal: {assigned} image(s) assignée(s)'
            )
        )
