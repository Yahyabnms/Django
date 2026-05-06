from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

from Voiture.models import Voiture, CategorieVoiture
from Client.models import Client
from Reservation.models import Reservation
from Location.models import Location
from Paiement.models import Paiement
from Contrat.models import Contrat

try:
    from faker import Faker
except ImportError:
    raise ImportError("Veuillez installer faker: pip install faker")

fake = Faker('fr_FR')


class Command(BaseCommand):
    help = 'Génère des données de test (fake data) pour le projet AutoLocation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clients',
            type=int,
            default=10,
            help='Nombre de clients à créer (défaut: 10)'
        )
        parser.add_argument(
            '--voitures',
            type=int,
            default=15,
            help='Nombre de voitures à créer (défaut: 15)'
        )
        parser.add_argument(
            '--reservations',
            type=int,
            default=20,
            help='Nombre de réservations à créer (défaut: 20)'
        )
        parser.add_argument(
            '--locations',
            type=int,
            default=15,
            help='Nombre de locations à créer (défaut: 15)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprimer toutes les données existantes avant de générer'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Génération des données de test...'))

        # Optionnel: supprimer les données existantes
        if options['clear']:
            self.clear_data()

        # Générer les catégories
        self.generate_categories()

        # Générer les clients
        clients = self.generate_clients(options['clients'])

        # Générer les voitures
        voitures = self.generate_voitures(options['voitures'])

        # Générer les locations
        locations = self.generate_locations(clients, voitures, options['locations'])

        # Générer les réservations
        self.generate_reservations(clients, voitures, options['reservations'])

        # Générer les paiements
        self.generate_paiements(clients, locations)

        # Générer les contrats
        self.generate_contrats(clients, locations)

        self.stdout.write(self.style.SUCCESS('✅ Données de test générées avec succès!'))
        self.print_summary(options)

    def clear_data(self):
        """Supprime toutes les données existantes."""
        self.stdout.write(self.style.WARNING('⚠️ Suppression des données existantes...'))
        Contrat.objects.all().delete()
        Paiement.objects.all().delete()
        Reservation.objects.all().delete()
        Location.objects.all().delete()
        Voiture.objects.all().delete()
        Client.objects.all().delete()
        CategorieVoiture.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✅ Données supprimées'))

    def generate_categories(self):
        """Génère les catégories de voiture."""
        categories_data = [
            {
                'nom': 'Économique',
                'description': 'Voitures petites et économes en carburant',
                'capacite_passagers': 5,
                'nombre_portes': 4,
                'type_carburant': 'Essence',
                'transmission': 'Manuelle'
            },
            {
                'nom': 'Confort',
                'description': 'Voitures confortables pour famille',
                'capacite_passagers': 5,
                'nombre_portes': 4,
                'type_carburant': 'Essence',
                'transmission': 'Automatique'
            },
            {
                'nom': 'Premium',
                'description': 'Voitures haut de gamme',
                'capacite_passagers': 5,
                'nombre_portes': 4,
                'type_carburant': 'Essence',
                'transmission': 'Automatique'
            },
            {
                'nom': 'SUV',
                'description': 'Véhicules utilitaires spacieux',
                'capacite_passagers': 7,
                'nombre_portes': 5,
                'type_carburant': 'Diesel',
                'transmission': 'Automatique'
            },
            {
                'nom': 'Électrique',
                'description': 'Voitures électriques écologiques',
                'capacite_passagers': 5,
                'nombre_portes': 4,
                'type_carburant': 'Électrique',
                'transmission': 'Automatique'
            }
        ]

        for cat_data in categories_data:
            category, created = CategorieVoiture.objects.get_or_create(
                nom=cat_data['nom'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f"✅ Catégorie créée: {category.nom}")

    def generate_clients(self, count):
        """Génère des clients."""
        self.stdout.write(self.style.WARNING(f'👥 Génération de {count} clients...'))
        clients = []

        for _ in range(count):
            client = Client.objects.create(
                nom=fake.last_name(),
                prenom=fake.first_name(),
                email=fake.email(),
                telephone=fake.phone_number()[:15],
                adresse=fake.address().replace('\n', ', '),
                actif=random.choice([True, True, True, False])  # 75% actifs
            )
            clients.append(client)
            self.stdout.write(f"  ✓ {client.get_full_name()}")

        return clients

    def generate_voitures(self, count):
        """Génère des voitures."""
        self.stdout.write(self.style.WARNING(f'🚗 Génération de {count} voitures...'))
        
        marques = ['Renault', 'Peugeot', 'Citroën', 'Toyota', 'Honda', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Ford']
        modeles = {
            'Renault': ['Clio', 'Megane', 'Scenic', 'Kangoo'],
            'Peugeot': ['208', '308', '3008', '5008'],
            'Citroën': ['C3', 'C4', 'C5', 'Berlingo'],
            'Toyota': ['Corolla', 'Yaris', 'RAV4', 'Prius'],
            'Honda': ['Civic', 'Accord', 'CR-V', 'Jazz'],
            'BMW': ['Serie 3', 'Serie 5', 'X1', 'X3'],
            'Mercedes': ['Classe A', 'Classe C', 'GLA', 'GLC'],
            'Audi': ['A3', 'A4', 'Q3', 'Q5'],
            'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Polo'],
            'Ford': ['Focus', 'Mondeo', 'EcoSport', 'Ranger']
        }
        
        categories = list(CategorieVoiture.objects.all())
        voitures = []

        for i in range(count):
            marque = random.choice(marques)
            modele = random.choice(modeles[marque])
            categorie = random.choice(categories)

            voiture = Voiture.objects.create(
                marque=marque,
                modele=modele,
                categorie=categorie,
                immatriculation=f"WND-{random.randint(1000, 9999)}-{random.randint(10, 99)}",
                annee=random.randint(2019, 2024),
                prix_par_jour=Decimal(random.randint(250, 800)),
                statut='disponible',  # Toujours disponible comme demandé
                kilométrage=random.randint(5000, 150000),
                # Ajouter des coordonnées GPS (autour de Casablanca, Maroc)
                latitude=random.uniform(33.5, 33.6),
                longitude=random.uniform(-7.65, -7.5),
                derniere_mise_a_jour_gps=timezone.now()
            )
            voitures.append(voiture)
            self.stdout.write(f"  ✓ {voiture.marque} {voiture.modele} - {voiture.immatriculation}")

        return voitures

    def generate_locations(self, clients, voitures, count):
        """Génère des locations."""
        self.stdout.write(self.style.WARNING(f'📝 Génération de {count} locations...'))
        locations = []

        for _ in range(count):
            client = random.choice(clients)
            voiture = random.choice(voitures)
            
            date_debut = fake.date_time_this_month(before_now=True, after_now=False)
            date_fin = date_debut + timedelta(days=random.randint(1, 14))
            
            duree = (date_fin - date_debut).days
            prix_total = Decimal(duree) * voiture.prix_par_jour
            
            location = Location.objects.create(
                client=client,
                voiture=voiture,
                date_debut=date_debut,
                date_fin=date_fin,
                statut=random.choice(['en_cours', 'terminee', 'terminee', 'terminee']),
                prix_total=prix_total
            )
            locations.append(location)
            self.stdout.write(f"  ✓ Location {location.id}: {client.get_full_name()} - {voiture.marque} {voiture.modele}")

        return locations

    def generate_reservations(self, clients, voitures, count):
        """Génère des réservations."""
        self.stdout.write(self.style.WARNING(f'📅 Génération de {count} réservations...'))

        for _ in range(count):
            client = random.choice(clients)
            voiture = random.choice(voitures)
            
            date_debut = timezone.now() + timedelta(days=random.randint(1, 30))
            date_fin = date_debut + timedelta(days=random.randint(1, 14))
            
            nombre_jours = (date_fin - date_debut).days
            prix_estime = Decimal(nombre_jours) * voiture.prix_par_jour
            
            reservation = Reservation.objects.create(
                client=client,
                voiture=voiture,
                date_debut=date_debut,
                date_fin=date_fin,
                statut=random.choice(['en_attente', 'confirmee', 'confirmee', 'confirmee']),
                nombre_jours=nombre_jours,
                prix_estime=prix_estime,
                commentaires=fake.sentence() if random.random() > 0.5 else None
            )
            self.stdout.write(f"  ✓ Réservation {reservation.id}: {client.get_full_name()}")

    def generate_paiements(self, clients, locations):
        """Génère des paiements."""
        self.stdout.write(self.style.WARNING(f'💳 Génération de paiements...'))

        for location in locations:
            if location.statut == 'terminee' or random.random() > 0.5:
                paiement = Paiement.objects.create(
                    location=location,
                    client=location.client,
                    montant=location.prix_total,
                    methode_paiement=random.choice(['carte', 'espece', 'cheque', 'virement']),
                    statut=random.choice(['confirme', 'confirme', 'confirme', 'en_attente']),
                    numero_transaction=f"TRX-{fake.numerify('############')}" if random.random() > 0.3 else None,
                    remarques=fake.sentence() if random.random() > 0.7 else None
                )
                self.stdout.write(f"  ✓ Paiement {paiement.id}: {paiement.montant} DH")

    def generate_contrats(self, clients, locations):
        """Génère des contrats."""
        self.stdout.write(self.style.WARNING(f'📜 Génération de contrats...'))

        for i, location in enumerate(locations):
            numero_contrat = f"CONT-{timezone.now().year}-{i+1:06d}"
            
            contrat = Contrat.objects.create(
                numero_contrat=numero_contrat,
                location=location,
                client=location.client,
                date_expiration=location.date_fin + timedelta(days=30),
                conditions="Conditions standard de location:\n- Conducteur doit avoir au moins 21 ans\n- Permis valide obligatoire\n- Assurance responsabilité civile obligatoire",
                statut=random.choice(['actif', 'actif', 'expire'])
            )
            self.stdout.write(f"  ✓ Contrat {contrat.numero_contrat}")

    def print_summary(self, options):
        """Affiche un résumé des données générées."""
        self.stdout.write(self.style.SUCCESS('\n📊 Résumé:'))
        self.stdout.write(f'  👥 Clients: {Client.objects.count()}')
        self.stdout.write(f'  🚗 Voitures: {Voiture.objects.count()}')
        self.stdout.write(f'  🏷️ Catégories: {CategorieVoiture.objects.count()}')
        self.stdout.write(f'  📝 Locations: {Location.objects.count()}')
        self.stdout.write(f'  📅 Réservations: {Reservation.objects.count()}')
        self.stdout.write(f'  💳 Paiements: {Paiement.objects.count()}')
        self.stdout.write(f'  📜 Contrats: {Contrat.objects.count()}')
        self.stdout.write(self.style.WARNING('\n💡 Conseil: Utilisez --clear pour réinitialiser les données à chaque test'))
