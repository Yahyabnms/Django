# Guide d'Utilisation - Interface de Réservation

## Vue d'ensemble

Une interface moderne et intuitive pour réserver des voitures a été créée avec:
- **Bootstrap 5** pour le design responsive
- **Font Awesome** pour les icônes
- **JavaScript** pour le calcul automatique du prix
- **API Django** pour la vérification de disponibilité en temps réel

## Fonctionnalités

### 1. Page de Listing des Voitures
**URL**: `http://127.0.0.1:8000/voitures/`

Affiche toutes les voitures disponibles avec:
- Image de la voiture
- Marque et modèle
- Prix par jour
- Année, carburant, transmission
- Statut (disponible/indisponible)
- Bouton "Réserver maintenant"

### 2. Page de Réservation
**URL**: `http://127.0.0.1:8000/reservation/reserver/<voiture_id>/`

#### Section Voiture Sélectionnée
- Image de la voiture avec effet hover
- Badge de statut (vert = disponible, rouge = indisponible)
- Informations détaillées (marque, modèle, prix, année, carburant, transmission, kilométrage)

#### Formulaire de Réservation
- **Date de début**: Date picker avec icône calendrier
- **Date de fin**: Date picker avec icône calendrier
- **Calcul automatique**:
  - Nombre de jours affiché en temps réel
  - Prix total calculé automatiquement (jours × prix/jour)
  - Animation pulse sur le prix

#### Vérification de Disponibilité
- Vérification automatique quand les dates sont sélectionnées
- Message vert: "Disponible pour ces dates"
- Message rouge: "Non disponible pour ces dates"
- Le bouton de confirmation est désactivé si indisponible

#### Bouton de Confirmation
- "Confirmer la réservation"
- Désactivé si la voiture n'est pas disponible
- Active uniquement si toutes les conditions sont remplies

#### Feedback Utilisateur
- **Succès**: "Réservation envoyée, en attente de validation" (vert)
- **Erreur**: Message d'erreur spécifique (rouge)
- Redirection automatique vers le profil après 2 secondes

## Comment Utiliser

### 1. Démarrer le Serveur
```bash
cd backend
..\venv\Scripts\python.exe manage.py runserver
```

### 2. Accéder aux Voitures
Ouvrez votre navigateur sur: `http://127.0.0.1:8000/voitures/`

### 3. Choisir une Voiture
- Parcourez la liste des voitures disponibles
- Cliquez sur "Réserver maintenant" sur une voiture

### 4. Remplir le Formulaire
- Sélectionnez la date de début
- Sélectionnez la date de fin
- Le prix total se calcule automatiquement
- La disponibilité est vérifiée en temps réel

### 5. Confirmer la Réservation
- Si disponible, cliquez sur "Confirmer la réservation"
- Attendez le message de confirmation
- Vous serez redirigé vers votre profil

## Caractéristiques Techniques

### Design
- **Gradient violet** pour le thème principal
- **Cartes avec ombre** et arrondis
- **Animations fluides** (hover, pulse)
- **Responsive** sur mobile et desktop
- **Icônes Font Awesome** pour une meilleure UX

### JavaScript
- Calcul automatique du nombre de jours
- Calcul du prix total en temps réel
- Vérification de disponibilité via API
- Gestion des erreurs
- Animation du prix

### API Endpoints
- `POST /api/check-availability/<voiture_id>/` - Vérifie la disponibilité
- `POST /api/create-reservation/` - Crée une réservation

### Sécurité
- Authentification requise pour réserver
- Protection CSRF
- Vérification des dates (fin > début)
- Vérification de disponibilité avant création

## Personnalisation

### Changer les Couleurs
Dans `reservation/templates/reservation/reserver_voiture.html`:
```css
.car-image-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Modifier le Prix
Les prix sont définis dans le modèle `Voiture` et générés par le scraper.

### Ajouter des Champs
Modifiez le formulaire HTML et la vue `create_reservation` dans `views.py`.

## Dépannage

### Le bouton "Réserver" est désactivé
- Vérifiez que la voiture a le statut "disponible"
- Connectez-vous à votre compte

### Le prix ne se calcule pas
- Vérifiez que JavaScript est activé
- Sélectionnez les deux dates

### Erreur de disponibilité
- La voiture est déjà réservée pour ces dates
- Choisissez d'autres dates

### Erreur d'authentification
- Connectez-vous avant de réserver
- Créez un compte si nécessaire

## Structure des Fichiers

```
backend/
├── Reservation/
│   ├── templates/
│   │   └── reservation/
│   │       └── reserver_voiture.html
│   ├── urls.py
│   └── views.py
├── Voiture/
│   ├── templates/
│   │   └── voiture/
│   │       └── liste_voitures.html
│   └── views.py
└── Base/
    └── templates/
        └── base/
            └── base.html
```

## Prochaines Améliorations Possibles

- [ ] Filtres par marque, prix, année
- [ ] Recherche de voitures
- [ ] Calendrier visuel des disponibilités
- [ ] Comparaison de voitures
- [ ] Avis et notes des clients
- [ ] Système de favoris
- [ ] Notifications par email
- [ ] Paiement en ligne
