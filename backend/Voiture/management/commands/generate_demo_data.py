from django.core.management.base import BaseCommand
from Voiture.models import Voiture, CategorieVoiture
import requests
import time
import uuid
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Génère des données de démonstration avec images pour AutoLocation'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=15,
            help='Nombre de voitures à générer (défaut: 15)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚗 Génération des données de démonstration...')
        )
        
        start_time = time.time()
        
        try:
            saved_count = self.generate_demo_data(max_voitures=options['count'])
            
            end_time = time.time()
            duration = end_time - start_time
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Données de démonstration générées en {duration:.2f} secondes\n'
                    f'📈 {saved_count} nouvelles voitures ajoutées\n'
                    f'🖼️ Images téléchargées avec succès'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de la génération: {e}')
            )
            raise
    
    def generate_demo_data(self, max_voitures=15):
        """Génère des données de démonstration"""
        
        # Données de voitures
        car_data = [
            {"marque": "Toyota", "modele": "Corolla", "annee": 2023, "prix": 450},
            {"marque": "Honda", "modele": "Civic", "annee": 2023, "prix": 480},
            {"marque": "Nissan", "modele": "Sentra", "annee": 2023, "prix": 420},
            {"marque": "Mazda", "modele": "Mazda3", "annee": 2023, "prix": 460},
            {"marque": "Hyundai", "modele": "Elantra", "annee": 2023, "prix": 380},
            {"marque": "Kia", "modele": "Forte", "annee": 2023, "prix": 370},
            {"marque": "Volkswagen", "modele": "Jetta", "annee": 2023, "prix": 440},
            {"marque": "Ford", "modele": "Focus", "annee": 2023, "prix": 390},
            {"marque": "Chevrolet", "modele": "Cruze", "annee": 2023, "prix": 400},
            {"marque": "BMW", "modele": "Série 3", "annee": 2023, "prix": 850},
            {"marque": "Mercedes", "modele": "Classe C", "annee": 2023, "prix": 900},
            {"marque": "Audi", "modele": "A4", "annee": 2023, "prix": 780},
            {"marque": "Tesla", "modele": "Model 3", "annee": 2023, "prix": 1200},
            {"marque": "Porsche", "modele": "Macan", "annee": 2023, "prix": 1500},
            {"marque": "Lexus", "modele": "ES", "annee": 2023, "prix": 950},
        ]
        
        # Catégorie par défaut
        categorie, _ = CategorieVoiture.objects.get_or_create(
            nom="Standard",
            defaults={
                "type_carburant": "Essence",
                "transmission": "Automatique",
                "capacite_passagers": 5,
                "nombre_portes": 4,
            }
        )
        
        saved_count = 0
        
        for i, car in enumerate(car_data[:max_voitures]):
            try:
                # Télécharger une image aléatoire
                image_url = f"https://picsum.photos/seed/{car['marque']}_{car['modele']}_{uuid.uuid4().hex[:8]}/400/300.jpg"
                response = requests.get(image_url)
                
                # Créer la voiture
                voiture = Voiture.objects.create(
                    marque=car["marque"],
                    modele=car["modele"],
                    annee=car["annee"],
                    prix_par_jour=car["prix"],
                    kilométrage=15000 + (i * 2000),
                    statut="disponible",
                    categorie=categorie,
                    immatriculation=f"123-ABC-{i+1:03d}"
                )
                
                # Sauvegarder l'image
                if response.status_code == 200:
                    image_name = f"{car['marque']}_{car['modele']}_{uuid.uuid4().hex[:8]}.jpg"
                    voiture.image.save(image_name, ContentFile(response.content))
                
                saved_count += 1
                self.stdout.write(f"✅ {car['marque']} {car['modele']} créée")
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Erreur avec {car['marque']} {car['modele']}: {e}")
                )
        
        return saved_count
