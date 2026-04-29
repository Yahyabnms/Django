from django.core.management.base import BaseCommand
from scrapers.professional_scraper import ProfessionalScraper
import time
import os

class Command(BaseCommand):
    help = 'Scraping professionnel avec ScrapingBee pour données automobiles fiables'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--max-voitures',
            type=int,
            default=20,
            help='Nombre maximum de voitures à scraper (défaut: 20)'
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='Mode test - vérifie la configuration seulement'
        )
        parser.add_argument(
            '--setup-api-key',
            type=str,
            help='Configure votre clé API ScrapingBee'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚗 Scraping Professionnel avec ScrapingBee...')
        )
        
        # Configuration de la clé API
        if options['setup_api_key']:
            self.setup_api_key(options['setup_api_key'])
            return
        
        # Vérifier la clé API
        api_key = os.getenv('SCRAPINGBEE_API_KEY')
        if not api_key or api_key == 'YOUR_SCRAPINGBEE_API_KEY':
            self.stdout.write(
                self.style.ERROR('❌ Clé API ScrapingBee non configurée!')
            )
            self.stdout.write(
                self.style.WARNING('📋 Configuration requise:')
            )
            self.stdout.write(
                self.style.WARNING('1. Créez un compte: https://www.scrapingbee.com/')
            )
            self.stdout.write(
                self.style.WARNING('2. Obtenez votre clé API gratuite')
            )
            self.stdout.write(
                self.style.WARNING('3. Configurez: python manage.py scrape_professional --setup-api-key VOTRE_CLÉ')
            )
            return
        
        # Mode test
        if options['test']:
            self.test_configuration()
            return
        
        start_time = time.time()
        
        try:
            scraper = ProfessionalScraper()
            
            self.stdout.write(
                self.style.WARNING(f'📊 Scraping de {options["max_voitures"]} voitures...')
            )
            
            # Scraper les données
            voitures_data = scraper.scrape_all_sites(max_voitures=options['max_voitures'])
            
            if voitures_data:
                # Sauvegarder
                saved_count = scraper.save_voitures(voitures_data)
                
                end_time = time.time()
                duration = end_time - start_time
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Scraping professionnel terminé en {duration:.2f} secondes\n'
                        f'📈 {len(voitures_data)} voitures traitées\n'
                        f'💾 {saved_count} nouvelles voitures sauvegardées\n'
                        f'🌐 Source: ScrapingBee API\n'
                        f'🎨 Intégration thème jaune'
                    )
                )
                
                # Afficher les voitures
                if saved_count > 0:
                    self.stdout.write(
                        self.style.SUCCESS('🚗 Voitures ajoutées:')
                    )
                    for voiture in voitures_data[:5]:
                        self.stdout.write(
                            self.style.SUCCESS(f'   • {voiture.get("marque")} {voiture.get("modele")} - {voiture.get("prix_par_jour")}DH/jour ({voiture.get("source")})')
                        )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️ Aucune voiture trouvée. Vérifiez la configuration API.')
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur scraping professionnel: {e}')
            )
            raise
    
    def setup_api_key(self, api_key):
        """Configure la clé API ScrapingBee"""
        try:
            # Ajouter au fichier .env ou settings
            env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
            
            with open(env_file, 'a') as f:
                f.write(f'\nSCRAPINGBEE_API_KEY={api_key}\n')
            
            self.stdout.write(
                self.style.SUCCESS('✅ Clé API ScrapingBee configurée!')
            )
            self.stdout.write(
                self.style.WARNING('📝 Redémarrez votre serveur pour appliquer les changements.')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur configuration clé API: {e}')
            )
    
    def test_configuration(self):
        """Test la configuration ScrapingBee"""
        self.stdout.write(
            self.style.WARNING('🧪 Test de configuration ScrapingBee...')
        )
        
        try:
            scraper = ProfessionalScraper()
            
            # Test simple
            test_url = 'https://httpbin.org/get'
            html_content = scraper.scrape_with_scrapingbee(test_url)
            
            if html_content:
                self.stdout.write(
                    self.style.SUCCESS('✅ Configuration ScrapingBee valide!')
                )
                self.stdout.write(
                    self.style.SUCCESS('🚀 Prêt à scraper des sites automobiles.')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Échec du test. Vérifiez votre clé API.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur test: {e}')
            )
