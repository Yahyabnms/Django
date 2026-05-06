from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
import random
from Voiture.models import CategorieVoiture, Voiture
from Client.models import Client
from Location.models import Location
from Reservation.models import Reservation
from Paiement.models import Paiement
from Contrat.models import Contrat


class Command(BaseCommand):
    help = 'Génère des données fake marocaines pour la base de données'

    def handle(self, *args, **kwargs):
        self.stdout.write('Génération des données fake marocaines...')
        
        # Données marocaines
        noms_marocains = [
            'Alami', 'Benali', 'Chadli', 'Drissi', 'Fassi', 'Gharbi', 'Hammadi', 'Idrissi',
            'Jazouli', 'Kabbaj', 'Lahbabi', 'Mansouri', 'Naciri', 'Ouazzani', 'Rafiq', 'Sahli',
            'Tazi', 'Zahraoui', 'Bennani', 'Bouazza', 'Chraibi', 'El Fassi', 'El Idrissi',
            'El Mansouri', 'El Ouardi', 'Filali', 'Guennoun', 'Hilali', 'Jellouli'
        ]
        
        prenoms_marocains = [
            'Mohammed', 'Ahmed', 'Youssef', 'Omar', 'Ali', 'Hassan', 'Karim', 'Saïd',
            'Abdelkader', 'Abdelaziz', 'Moustapha', 'Ibrahim', 'Ismail', 'Khalid', 'Nabil',
            'Rachid', 'Tariq', 'Walid', 'Zakaria', 'Fatima', 'Amina', 'Khadija', 'Samira',
            'Latifa', 'Nadia', 'Sanaa', 'Yasmine', 'Sara', 'Hajar', 'Imane', 'Lina'
        ]
        
        villes_marocaines = [
            'Casablanca', 'Rabat', 'Fès', 'Marrakech', 'Tanger', 'Agadir', 'Meknès',
            'Oujda', 'Kenitra', 'Tétouan', 'Safi', 'El Jadida', 'Beni Mellal', 'Nador'
        ]
        
        quartiers_casablanca = [
            'Maârif', 'Centre-ville', 'Habbous', 'Old Medina', 'Ain Diab', 'Corniche',
            'Technopark', 'Sidi Maarouf', 'California', 'Les Roches'
        ]
        
        marques_voitures = [
            'Dacia', 'Renault', 'Peugeot', 'Citroën', 'Volkswagen', 'Toyota', 'Hyundai',
            'Kia', 'Ford', 'Fiat', 'Honda', 'Nissan', 'Mercedes', 'BMW', 'Audi'
        ]
        
        modeles_par_marque = {
            'Dacia': ['Logan', 'Sandero', 'Duster', 'Lodgy'],
            'Renault': ['Clio', 'Megane', 'Captur', 'Kadjar', 'Dacia'],
            'Peugeot': ['208', '308', '2008', '3008', '508'],
            'Citroën': ['C3', 'C4', 'C5 Aircross', 'Berlingo'],
            'Volkswagen': ['Polo', 'Golf', 'Tiguan', 'T-Roc'],
            'Toyota': ['Yaris', 'Corolla', 'RAV4', 'C-HR'],
            'Hyundai': ['i20', 'i30', 'Tucson', 'Santa Fe'],
            'Kia': ['Picanto', 'Rio', 'Sportage', 'Sorento'],
            'Ford': ['Fiesta', 'Focus', 'Puma', 'Kuga'],
            'Fiat': ['500', 'Panda', 'Tipo', '500X'],
            'Honda': ['Jazz', 'Civic', 'HR-V', 'CR-V'],
            'Nissan': ['Micra', 'Note', 'Qashqai', 'X-Trail'],
            'Mercedes': ['Classe A', 'Classe C', 'GLA', 'GLC'],
            'BMW': ['Série 1', 'Série 3', 'X1', 'X3'],
            'Audi': ['A1', 'A3', 'Q2', 'Q3']
        }
        
        # Créer des catégories de voitures
        self.stdout.write('Création des catégories de voitures...')
        categories_data = [
            {
                'nom': 'Économique',
                'description': 'Voitures économiques parfaites pour la ville',
                'capacite_passagers': 5,
                'nombre_portes': 4,
                'type_carburant': 'Essence',
                'transmission': 'Manuelle'
            },
            {
                'nom': 'Compacte',
                'description': 'Voitures compactes idéales pour les petites familles',
                'capacite_passagers': 5,
                'nombre_portes': 5,
                'type_carburant': 'Diesel',
                'transmission': 'Manuelle'
            },
            {
                'nom': 'SUV',
                'description': 'SUV spacieux pour les longs trajets',
                'capacite_passagers': 5,
                'nombre_portes': 5,
                'type_carburant': 'Diesel',
                'transmission': 'Automatique'
            },
            {
                'nom': 'Luxe',
                'description': 'Voitures de luxe pour un confort optimal',
                'capacite_passagers': 5,
                'nombre_portes': 4,
                'type_carburant': 'Essence',
                'transmission': 'Automatique'
            },
            {
                'nom': 'Utilitaire',
                'description': 'Véhicules utilitaires pour le transport de marchandises',
                'capacite_passagers': 2,
                'nombre_portes': 4,
                'type_carburant': 'Diesel',
                'transmission': 'Manuelle'
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            categorie, created = CategorieVoiture.objects.get_or_create(
                nom=cat_data['nom'],
                defaults=cat_data
            )
            if created:
                categories.append(categorie)
                self.stdout.write(f'  - Catégorie créée: {categorie.nom}')
            else:
                categories.append(categorie)
        
        # Créer des voitures
        self.stdout.write('Création des voitures...')
        voitures = []
        for i in range(20):
            marque = random.choice(marques_voitures)
            modele = random.choice(modeles_par_marque[marque])
            categorie = random.choice(categories)
            
            # Génération d'immatriculation marocaine: 12345-A-1
            numero = random.randint(10000, 99999)
            lettre = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
            region = random.randint(1, 99)
            immatriculation = f'{numero}-{lettre}-{region}'
            
            # Prix en Dirhams marocains
            prix_par_jour = random.uniform(200, 1500)
            
            voiture = Voiture.objects.create(
                marque=marque,
                modele=modele,
                categorie=categorie,
                immatriculation=immatriculation,
                annee=random.randint(2015, 2024),
                prix_par_jour=prix_par_jour,
                statut=random.choice(['disponible', 'disponible', 'disponible', 'louee', 'maintenance']),
                kilométrage=random.randint(5000, 120000)
            )
            voitures.append(voiture)
            self.stdout.write(f'  - Voiture créée: {voiture.marque} {voiture.modele} ({voiture.immatriculation})')
        
        # Créer des clients
        self.stdout.write('Création des clients...')
        clients = []
        for i in range(15):
            nom = random.choice(noms_marocains)
            prenom = random.choice(prenoms_marocains)
            ville = random.choice(villes_marocaines)
            
            if ville == 'Casablanca':
                quartier = random.choice(quartiers_casablanca)
                adresse = f'{quartier}, {ville}, Maroc'
            else:
                adresse = f'Centre-ville, {ville}, Maroc'
            
            # Numéro de téléphone marocain: 06XXXXXXXX ou 07XXXXXXXX
            prefixe = random.choice(['06', '07'])
            numero_tel = f'{prefixe}{random.randint(10000000, 99999999)}'
            
            email = f'{prenom.lower()}.{nom.lower()}@{random.choice(["gmail.com", "yahoo.fr", "hotmail.com", "outlook.ma"])}'
            
            client = Client.objects.create(
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=numero_tel,
                adresse=adresse,
                actif=random.choice([True, True, True, False])
            )
            clients.append(client)
            self.stdout.write(f'  - Client créé: {client.prenom} {client.nom}')
        
        # Créer des locations
        self.stdout.write('Création des locations...')
        for i in range(10):
            client = random.choice(clients)
            voiture = random.choice(voitures)
            
            date_debut = timezone.now() - timedelta(days=random.randint(1, 60))
            duree_jours = random.randint(1, 14)
            date_fin = date_debut + timedelta(days=duree_jours)
            
            prix_total = voiture.prix_par_jour * duree_jours
            
            statut = random.choice(['en_cours', 'terminee', 'terminee', 'annulee'])
            
            location = Location.objects.create(
                client=client,
                voiture=voiture,
                date_debut=date_debut,
                date_fin=date_fin,
                statut=statut,
                prix_total=prix_total
            )
            self.stdout.write(f'  - Location créée: {client} - {voiture} ({duree_jours} jours)')
        
        # Créer des réservations
        self.stdout.write('Création des réservations...')
        for i in range(8):
            client = random.choice(clients)
            voiture = random.choice(voitures)
            
            date_debut = timezone.now() + timedelta(days=random.randint(1, 30))
            duree_jours = random.randint(1, 10)
            date_fin = date_debut + timedelta(days=duree_jours)
            
            prix_estime = voiture.prix_par_jour * duree_jours
            
            statut = random.choice(['en_attente', 'confirmee', 'confirmee', 'activee', 'annulee'])
            
            reservation = Reservation.objects.create(
                client=client,
                voiture=voiture,
                date_debut=date_debut,
                date_fin=date_fin,
                statut=statut,
                nombre_jours=duree_jours,
                prix_estime=prix_estime,
                commentaires=random.choice([
                    'Réservation pour vacances',
                    'Déplacement professionnel',
                    'Location pour week-end',
                    'Besoin urgent',
                    'Réservation pour famille',
                    ''
                ]) if random.random() > 0.3 else ''
            )
            self.stdout.write(f'  - Réservation créée: {client} - {voiture} ({duree_jours} jours)')
        
        # Créer des paiements
        self.stdout.write('Création des paiements...')
        methode_paiement_marocain = [
            'carte', 'espece', 'virement'
        ]
        
        locations = list(Location.objects.all())
        for i in range(12):
            location = random.choice(locations)
            methode = random.choice(methode_paiement_marocain)
            
            # Générer un numéro de transaction marocain
            if methode == 'carte':
                numero_transaction = f"MAR-{random.randint(100000, 999999)}-{random.randint(1000, 9999)}"
            elif methode == 'virement':
                numero_transaction = f"VIR-{random.randint(100000, 999999)}-{random.randint(1000, 9999)}"
            else:
                numero_transaction = None
            
            statut = random.choice(['confirme', 'confirme', 'confirme', 'en_attente', 'refuse'])
            
            paiement = Paiement.objects.create(
                location=location,
                client=location.client,
                montant=location.prix_total,
                methode_paiement=methode,
                statut=statut,
                numero_transaction=numero_transaction,
                remarques=random.choice([
                    'Paiement effectué à l\'agence',
                    'Paiement en ligne',
                    'Paiement par virement bancaire',
                    'Espèces remises au chauffeur',
                    ''
                ]) if random.random() > 0.4 else ''
            )
            self.stdout.write(f'  - Paiement créé: {location.client} - {paiement.montant}DH ({paiement.get_methode_paiement_display()})')
        
        # Créer des contrats pour les locations
        self.stdout.write('Création des contrats pour les locations...')
        locations_with_contrat = random.sample(locations, min(6, len(locations)))
        for i, location in enumerate(locations_with_contrat, 1):
            # Générer un numéro de contrat marocain
            annee = timezone.now().year
            numero_contrat = f"CONT-{annee}-LOC-{str(i).zfill(4)}"
            
            date_signature = location.date_creation
            duree_contrat = random.randint(30, 365)
            date_expiration = date_signature + timedelta(days=duree_contrat)
            
            statut = random.choice(['actif', 'actif', 'actif', 'expire', 'annule'])
            
            conditions = random.choice([
                'Location conforme à la législation marocaine. Assurance incluse. Kilométrage illimité.',
                'Contrat de location standard. Caution requise. Assurance tous risques incluse.',
                'Location avec chauffeur optionnel. Assurance incluse. Frais de carburant non inclus.',
                'Contrat longue durée. Maintenance incluse. Assistance 24/7 sur tout le territoire marocain.'
            ])
            
            contrat = Contrat.objects.create(
                numero_contrat=numero_contrat,
                location=location,
                client=location.client,
                date_signature=date_signature,
                date_expiration=date_expiration,
                conditions=conditions,
                statut=statut
            )
            self.stdout.write(f'  - Contrat location créé: {contrat.numero_contrat} - {location.client}')
        
        # Créer des contrats pour toutes les réservations
        self.stdout.write('Création des contrats pour les réservations...')
        reservations = list(Reservation.objects.all())
        for i, reservation in enumerate(reservations, 1):
            # Générer un numéro de contrat marocain
            annee = timezone.now().year
            numero_contrat = f"CONT-{annee}-RES-{str(i).zfill(4)}"
            
            date_signature = reservation.date_reservation
            duree_contrat = random.randint(30, 365)
            date_expiration = date_signature + timedelta(days=duree_contrat)
            
            statut = random.choice(['actif', 'actif', 'actif', 'expire', 'annule'])
            
            conditions = random.choice([
                'Réservation confirmée conforme à la législation marocaine. Assurance incluse.',
                'Contrat de réservation standard. Caution requise. Assurance tous risques incluse.',
                'Réservation avec option chauffeur disponible. Assurance incluse.',
                'Contrat réservation longue durée. Maintenance incluse. Assistance 24/7.'
            ])
            
            contrat = Contrat.objects.create(
                numero_contrat=numero_contrat,
                reservation=reservation,
                client=reservation.client,
                date_signature=date_signature,
                date_expiration=date_expiration,
                conditions=conditions,
                statut=statut
            )
            self.stdout.write(f'  - Contrat réservation créé: {contrat.numero_contrat} - {reservation.client}')
        
        self.stdout.write(self.style.SUCCESS('✓ Données fake marocaines générées avec succès!'))
        self.stdout.write(f'  - {len(categories)} catégories de voitures')
        self.stdout.write(f'  - {len(voitures)} voitures')
        self.stdout.write(f'  - {len(clients)} clients')
        self.stdout.write(f'  - {Location.objects.count()} locations')
        self.stdout.write(f'  - {Reservation.objects.count()} réservations')
        self.stdout.write(f'  - {Paiement.objects.count()} paiements')
        self.stdout.write(f'  - {Contrat.objects.count()} contrats')
