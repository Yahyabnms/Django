from django.core.management.base import BaseCommand
from scrapers.demo_data_generator_fixed import DemoDataGenerator
import time

class Command(BaseCommand):
    help = 'Génère des données de démonstration sans images externes pour AutoLocation'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=15,
            help='Nombre de voitures à générer (défaut: 15)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚗 Génération des données de démonstration (Version corrigée)...')
        )
        
        start_time = time.time()
        
        try:
            generator = DemoDataGenerator()
            saved_count = generator.generate_demo_data(max_voitures=options['count'])
            
            end_time = time.time()
            duration = end_time - start_time
            
            if saved_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Données de démonstration générées en {duration:.2f} secondes\n'
                        f'📈 {saved_count} nouvelles voitures ajoutées\n'
                        f'🎨 Thème jaune appliqué\n'
                        f'📋 Données complètes (prix, km, carburant, transmission)'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️ Aucune voiture ajoutée (peut-être déjà existantes)')
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de la génération: {e}')
            )
            raise
