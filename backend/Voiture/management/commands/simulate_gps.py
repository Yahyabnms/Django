from django.core.management.base import BaseCommand
from django.utils import timezone
import random
import time
from Voiture.models import Voiture

class Command(BaseCommand):
    help = 'Simule le mouvement des voitures en mettant à jour leurs coordonnées GPS'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=5,
            help='Intervalle entre les mises à jour en secondes (défaut: 5)'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Nombre de mises à jour à effectuer (défaut: 10, 0 pour infini)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        count = options['count']
        
        self.stdout.write(self.style.SUCCESS(f'🚀 Démarrage de la simulation GPS (intervalle: {interval}s)...'))
        
        iteration = 0
        try:
            while count == 0 or iteration < count:
                iteration += 1
                # On ne bouge que les voitures "louee" ou on bouge tout pour la démo ?
                # Pour la démo, on bouge toutes les voitures qui ont des coordonnées
                voitures = Voiture.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
                
                if not voitures.exists():
                    self.stdout.write(self.style.WARNING("Aucune voiture avec des coordonnées GPS n'a été trouvée."))
                    break
                
                for voiture in voitures:
                    # Simulation d'un petit mouvement (environ 10-50 mètres)
                    # 0.0001 degré de latitude est environ 11 mètres
                    delta_lat = random.uniform(-0.0005, 0.0005)
                    delta_lng = random.uniform(-0.0005, 0.0005)
                    
                    voiture.latitude += delta_lat
                    voiture.longitude += delta_lng
                    voiture.derniere_mise_a_jour_gps = timezone.now()
                    voiture.save()
                    
                    self.stdout.write(f"  📍 {voiture.marque} {voiture.modele} ({voiture.immatriculation}) -> {voiture.latitude:.6f}, {voiture.longitude:.6f}")
                
                self.stdout.write(self.style.SUCCESS(f"✅ Mise à jour #{iteration} effectuée. Attente de {interval}s..."))
                if count == 0 or iteration < count:
                    time.sleep(interval)
                    
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n🛑 Simulation arrêtée par l'utilisateur."))
            
        self.stdout.write(self.style.SUCCESS('🏁 Simulation terminée.'))
