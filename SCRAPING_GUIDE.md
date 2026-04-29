# Guide de Scraping - Générateur de Voitures avec Images

## Installation

Les dépendances sont déjà installées:
- `beautifulsoup4` - Pour parser le HTML
- `requests` - Pour les requêtes HTTP
- `Pillow` - Pour la gestion des images

## Utilisation

### Générateur de Voitures avec Images (Recommandé)

```bash
# Depuis le dossier backend
cd backend

# Générer 10 voitures avec images (défaut)
..\venv\Scripts\python.exe manage.py scrape_wandaloo

# Générer un nombre spécifique de voitures
..\venv\Scripts\python.exe manage.py scrape_wandaloo --max-voitures 5
```

## Fonctionnalités

✅ **Génère automatiquement**:
- Marque et modèle des voitures (15 modèles réalistes)
- Année de fabrication (2021-2023)
- Prix par jour réaliste (200-450 DH)
- Kilométrage aléatoire (5000-80000 km)
- Type de carburant (Essence, Diesel, Hybride)
- Transmission (Manuelle, Automatique)
- **Images téléchargées depuis Unsplash (libres de droits)**

✅ **Gestion intelligente**:
- Évite les doublons via immatriculation unique
- Crée automatiquement les catégories par type de carburant
- Génère des immatriculations uniques au format WND-XXXX-XX
- Images stockées dans `media/voitures/`

✅ **Logging complet**:
- Messages détaillés dans la console
- Confirmation du téléchargement des images
- Résumé final de la génération

## Modèles de Voitures Disponibles

- Renault Clio 5, Dacia Sandero Stepway, Peugeot 208
- Volkswagen Golf 8, BMW Série 3, Mercedes Classe A
- Toyota Corolla, Hyundai i20, Kia Rio, Citroën C3
- Audi A3, Nissan Qashqai, Honda Civic, Ford Focus, Seat Ibiza

## Résultats

Les voitures générées sont directement sauvegardées dans la base de données avec:
- Statut: `disponible` (par défaut)
- Catégorie: Essence, Diesel ou Hybride
- Prix: Entre 200 et 450 DH par jour
- Image: Téléchargée depuis Unsplash (libres de droits)

## Exemple de sortie

```
🚗 Génération de voitures avec images libres de droits...
🚗 Génération de 5 voitures avec images libres de droits...
🔍 Génération voiture 1/5: Audi A3
✅ Audi A3 - 380DH/jour
🔍 Génération voiture 2/5: Honda Civic
✅ Honda Civic - 310DH/jour
...
📷 Image téléchargée pour Audi A3
💾 Sauvegardé: Audi A3

✅ Génération terminée!
📊 5 voitures traitées
💾 5 nouvelles voitures sauvegardées
📷 Images téléchargées depuis Unsplash (libres de droits)
```

## Notes

- Les images proviennent d'Unsplash et sont libres de droits
- Le générateur utilise des données réalistes pour le marché marocain
- Les prix sont en Dirhams marocains par jour
- Chaque voiture a une immatriculation unique

## Pourquoi pas de scraping direct?

Le scraping direct de sites comme DiscoverCars, Getaround et Kayak est:
- **Techniquement difficile**: JavaScript dynamique, protections anti-bot
- **Légalement risqué**: Violation des conditions d'utilisation
- **Instable**: Les sites changent souvent leur structure

**Alternatives recommandées**:
- APIs officielles de ces plateformes (partenariat commercial)
- Programmes d'affiliation
- Agrégateurs comme CarTrawler API

