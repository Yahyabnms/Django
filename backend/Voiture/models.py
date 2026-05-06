from django.db import models
from django.utils import timezone
from datetime import timedelta


class CategorieVoiture(models.Model):
    """Modèle représentant une catégorie de voiture."""
    
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    capacite_passagers = models.IntegerField(default=5)
    nombre_portes = models.IntegerField(default=4)
    type_carburant = models.CharField(max_length=50, null=True, blank=True)
    transmission = models.CharField(max_length=50, null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie Voiture"
        verbose_name_plural = "Catégories Voitures"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Voiture(models.Model):
    """Modèle représentant une voiture."""
    
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('louee', 'Louée'),
        ('maintenance', 'Maintenance'),
    ]
    
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    categorie = models.ForeignKey(CategorieVoiture, on_delete=models.PROTECT, related_name='voitures')
    immatriculation = models.CharField(max_length=20, unique=True)
    annee = models.IntegerField()
    prix_par_jour = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')
    kilométrage = models.IntegerField(default=0)
    image = models.ImageField(upload_to='voitures/', null=True, blank=True)
    
    # Champs pour le suivi GPS
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude actuelle")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude actuelle")
    derniere_mise_a_jour_gps = models.DateTimeField(null=True, blank=True, help_text="Dernière mise à jour de la position")
    
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"
        ordering = ['marque', 'modele']

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"
    
    def details_voiture(self):
        """Retourne les détails de la voiture."""
        return (f"Marque: {self.marque}\n"
                f"Modèle: {self.modele}\n"
                f"Catégorie: {self.categorie}\n"
                f"Immatriculation: {self.immatriculation}\n"
                f"Année: {self.annee}\n"
                f"Prix/jour: {self.prix_par_jour}DH\n"
                f"Kilométrage: {self.kilométrage} km\n"
                f"Statut: {self.get_statut_display()}")
    
    def is_available(self):
        """Vérifie si la voiture est disponible."""
        return self.statut == 'disponible'
    
    def is_available_for_dates(self, date_debut, date_fin):
        """
        Vérifie si la voiture est disponible pour une période donnée.
        Prend en compte les locations en cours et les réservations confirmées.
        """
        from Location.models import Location
        from Reservation.models import Reservation
        
        # Vérifier si la voiture est marquée comme disponible
        if self.statut != 'disponible':
            return False
        
        # Vérifier les locations en cours ou à venir qui chevauchent la période
        locations_chevauchantes = Location.objects.filter(
            voiture=self,
            statut='en_cours'
        ).filter(
            models.Q(date_debut__lte=date_fin) & models.Q(date_fin__gte=date_debut)
        )
        
        if locations_chevauchantes.exists():
            return False
        
        # Vérifier les réservations confirmées ou activées qui chevauchent la période
        reservations_chevauchantes = Reservation.objects.filter(
            voiture=self,
            statut__in=['confirmee', 'activee']
        ).filter(
            models.Q(date_debut__lte=date_fin) & models.Q(date_fin__gte=date_debut)
        )
        
        if reservations_chevauchantes.exists():
            return False
        
        return True
