from django.db import models
from django.utils import timezone
from datetime import timedelta
from Client.models import Client
from Voiture.models import Voiture


class Location(models.Model):
    """Modèle représentant une location de voiture."""
    
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    voiture = models.ForeignKey(Voiture, on_delete=models.PROTECT)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Location {self.id} - {self.client} ({self.voiture})"
    
    def details_location(self):
        """Retourne les détails de la location."""
        duree = (self.date_fin - self.date_debut).days
        return (f"ID: {self.id}\n"
                f"Client: {self.client}\n"
                f"Voiture: {self.voiture}\n"
                f"Début: {self.date_debut.strftime('%d/%m/%Y %H:%M')}\n"
                f"Fin: {self.date_fin.strftime('%d/%m/%Y %H:%M')}\n"
                f"Durée: {duree} jours\n"
                f"Prix total: {self.prix_total}€\n"
                f"Statut: {self.get_statut_display()}")
    
    def get_duree_days(self):
        """Retourne la durée de la location en jours."""
        return (self.date_fin - self.date_debut).days
    
    def is_active(self):
        """Vérifie si la location est actuellement active."""
        now = timezone.now()
        return self.date_debut <= now <= self.date_fin and self.statut == 'en_cours'
