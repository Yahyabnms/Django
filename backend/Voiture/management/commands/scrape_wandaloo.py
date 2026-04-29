from django.core.management.base import BaseCommand
import requests
from Voiture.models import Voiture, CategorieVoiture


class Command(BaseCommand):
    help = 'Générateur de voitures avec images libres de droits (Unsplash)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--max-voitures',
            type=int,
            default=10,
            help='Nombre maximum de voitures à générer (défaut: 10)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚗 Génération de voitures avec images libres de droits...'))
        
        scraper = SimpleWandalooScraper()
        
        # Générer les voitures
        voitures_data = scraper.generate_voitures(max_voitures=options['max_voitures'])
        
        if voitures_data:
            # Sauvegarder
            saved_count = scraper.save_voitures(voitures_data)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Génération terminée!\n'
                    f'📊 {len(voitures_data)} voitures traitées\n'
                    f'💾 {saved_count} nouvelles voitures sauvegardées\n'
                    f'📷 Images téléchargées depuis Unsplash (libres de droits)'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Aucune voiture générée.')
            )
