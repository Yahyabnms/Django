from django.core.management.base import BaseCommand
from Voiture.models import Voiture
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Associe les images du dossier static/images/voitures aux voitures'

    def handle(self, *args, **options):
        images_dir = 'Base/static/images/voitures'
        base_path = os.path.join(os.getcwd(), images_dir)
        
        if not os.path.exists(base_path):
            self.stdout.write(self.style.ERROR(f'Dossier non trouvé: {base_path}'))
            return
        
        # Mapping nom de fichier -> (marque, modele)
        image_mapping = {
            'Audi Q3.jpg': ('Audi', 'Q3'),
            'BMW Série 1.jpeg': ('BMW', 'Série 1'),
            'Citroen C5.jpg': ('Citroën', 'C5'),
            'Dacia_Lodgy_1.png': ('Dacia', 'Lodgy'),
            'honda CIVIC.jpeg': ('Honda', 'Civic'),
            'Honda CR-V.jpg': ('Honda', 'CR-V'),
            'Kia Picanto.jpeg': ('Kia', 'Picanto'),
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
