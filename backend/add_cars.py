# -*- coding: utf-8 -*-
from Voiture.models import Voiture, CategorieVoiture

# 1. Get or create category
cat_compacte, _ = CategorieVoiture.objects.get_or_create(
    nom='Compacte',
    defaults={
        'capacite_passagers': 5,
        'nombre_portes': 5,
        'type_carburant': 'Diesel',
        'transmission': 'Automatique'
    }
)

cat_hybride, _ = CategorieVoiture.objects.get_or_create(
    nom='Berline Hybride',
    defaults={
        'capacite_passagers': 5,
        'nombre_portes': 4,
        'type_carburant': 'Hybride',
        'transmission': 'Automatique'
    }
)

# 2. Add Volkswagen Golf
vw, created_vw = Voiture.objects.get_or_create(
    immatriculation='12345-A-8',
    defaults={
        'marque': 'Volkswagen',
        'modele': 'Golf 8',
        'categorie': cat_compacte,
        'annee': 2023,
        'prix_par_jour': 450.00,
        'statut': 'disponible',
        'kilométrage': 15000
    }
)

# 3. Add Toyota (Corolla)
toyota, created_toyota = Voiture.objects.get_or_create(
    immatriculation='54321-B-6',
    defaults={
        'marque': 'Toyota',
        'modele': 'Corolla',
        'categorie': cat_hybride,
        'annee': 2024,
        'prix_par_jour': 400.00,
        'statut': 'disponible',
        'kilométrage': 5000
    }
)

print("Voitures ajoutées avec succès !")
print(f"- {vw.marque} {vw.modele} ({vw.immatriculation})")
print(f"- {toyota.marque} {toyota.modele} ({toyota.immatriculation})")