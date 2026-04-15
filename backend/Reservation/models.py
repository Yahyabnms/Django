from django.db import models
from django.utils import timezone
from Client.models import Client
from Voiture.models import Voiture


class Reservation(models.Model):
    """Modèle représentant une réservation de voiture."""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('activee', 'Activée'),
        ('annulee', 'Annulée'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.PROTECT)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    nombre_jours = models.IntegerField()
    prix_estime = models.DecimalField(max_digits=10, decimal_places=2)
    date_reservation = models.DateTimeField(auto_now_add=True)
    commentaires = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_reservation']

    def __str__(self):
        return f"Reservation {self.id} - {self.client} ({self.voiture})"
    
    def details_reservation(self):
        """Retourne les détails de la réservation."""
        return (f"ID: {self.id}\n"
                f"Client: {self.client}\n"
                f"Voiture: {self.voiture}\n"
                f"Début: {self.date_debut.strftime('%d/%m/%Y %H:%M')}\n"
                f"Fin: {self.date_fin.strftime('%d/%m/%Y %H:%M')}\n"
                f"Nombre de jours: {self.nombre_jours}\n"
                f"Prix estimé: {self.prix_estime}€\n"
                f"Statut: {self.get_statut_display()}")
    
    def is_confirmed(self):
        """Vérifie si la réservation est confirmée."""
        return self.statut == 'confirmee'
    
    def is_pending(self):
        """Vérifie si la réservation est en attente."""
        return self.statut == 'en_attente'
    
    def is_upcoming(self):
        """Vérifie si la réservation est à venir."""
        return self.date_debut > timezone.now() and self.statut in ['confirmee', 'activee']
