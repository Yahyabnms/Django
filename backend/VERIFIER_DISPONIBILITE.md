# Vérification de Disponibilité des Voitures

## Description
Ce module permet de vérifier la disponibilité d'une voiture pour une période donnée en tenant compte des locations en cours et des réservations confirmées.

## Méthode du Modèle

### `is_available_for_dates(date_debut, date_fin)`
Vérifie si la voiture est disponible pour une période spécifique.

**Paramètres:**
- `date_debut`: Date de début de la période (datetime)
- `date_fin`: Date de fin de la période (datetime)

**Retourne:**
- `True` si la voiture est disponible
- `False` si la voiture n'est pas disponible

**Exemple d'utilisation (Python):**
```python
from Voiture.models import Voiture
from datetime import datetime

voiture = Voiture.objects.get(id=1)
date_debut = datetime(2026, 5, 10)
date_fin = datetime(2026, 5, 15)

if voiture.is_available_for_dates(date_debut, date_fin):
    print("La voiture est disponible")
else:
    print("La voiture n'est pas disponible")
```

## API HTTP

### Endpoint
`GET /voiture/<voiture_id>/verifier-disponibilite/`

### Paramètres de requête
- `date_debut` (requis): Date de début au format YYYY-MM-DD
- `date_fin` (requis): Date de fin au format YYYY-MM-DD

### Réponse JSON

**Succès:**
```json
{
    "success": true,
    "disponible": true,
    "voiture": {
        "id": 1,
        "marque": "Dacia",
        "modele": "Duster",
        "immatriculation": "12345-A-1"
    },
    "date_debut": "2026-05-10",
    "date_fin": "2026-05-15"
}
```

**Erreur (dates manquantes):**
```json
{
    "success": false,
    "error": "Les dates de début et de fin sont requises"
}
```

**Erreur (format invalide):**
```json
{
    "success": false,
    "error": "Format de date invalide. Utilisez YYYY-MM-DD"
}
```

**Erreur (voiture non trouvée):**
```json
{
    "success": false,
    "error": "Voiture non trouvée"
}
```

### Exemple d'utilisation (cURL)
```bash
curl "http://localhost:8000/voiture/1/verifier-disponibilite/?date_debut=2026-05-10&date_fin=2026-05-15"
```

### Exemple d'utilisation (JavaScript/Fetch)
```javascript
async function verifierDisponibilite(voitureId, dateDebut, dateFin) {
    const response = await fetch(
        `/voiture/${voitureId}/verifier-disponibilite/?date_debut=${dateDebut}&date_fin=${dateFin}`
    );
    const data = await response.json();
    
    if (data.success) {
        if (data.disponible) {
            console.log('La voiture est disponible');
        } else {
            console.log('La voiture n\'est pas disponible pour ces dates');
        }
    } else {
        console.error('Erreur:', data.error);
    }
}

// Utilisation
verifierDisponibilite(1, '2026-05-10', '2026-05-15');
```

## Logique de Vérification

La méthode vérifie:
1. Si la voiture a le statut 'disponible'
2. Si aucune location en cours ne chevauche la période demandée
3. Si aucune réservation confirmée ou activée ne chevauche la période demandée

Une période est considérée comme chevauchante si:
- La location/réservation commence avant la fin de la période demandée ET
- La location/réservation finit après le début de la période demandée
