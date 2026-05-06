from django.core.management.base import BaseCommand
from Voiture.models import CategorieVoiture, Voiture
from Client.models import Client
from Location.models import Location
from Reservation.models import Reservation
from Contrat.models import Contrat
from Paiement.models import Paiement


class Command(BaseCommand):
    help = 'Supprime toutes les données fake de la base de données'

    def handle(self, *args, **kwargs):
        self.stdout.write('Suppression des données fake...')
        
        # Compter les enregistrements avant suppression
        count_contrats = Contrat.objects.count()
        count_paiements = Paiement.objects.count()
        count_reservations = Reservation.objects.count()
        count_locations = Location.objects.count()
        count_voitures = Voiture.objects.count()
        count_clients = Client.objects.count()
        count_categories = CategorieVoiture.objects.count()
        
        # Supprimer dans l'ordre pour respecter les contraintes de clés étrangères
        Contrat.objects.all().delete()
        Paiement.objects.all().delete()
        Reservation.objects.all().delete()
        Location.objects.all().delete()
        Voiture.objects.all().delete()
        Client.objects.all().delete()
        CategorieVoiture.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ Données supprimées avec succès!'))
        self.stdout.write(f'  - {count_contrats} contrats')
        self.stdout.write(f'  - {count_paiements} paiements')
        self.stdout.write(f'  - {count_reservations} réservations')
        self.stdout.write(f'  - {count_locations} locations')
        self.stdout.write(f'  - {count_voitures} voitures')
        self.stdout.write(f'  - {count_clients} clients')
        self.stdout.write(f'  - {count_categories} catégories de voitures')
