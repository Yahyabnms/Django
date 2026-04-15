from django.db import models
from django.utils import timezone
from Client.models import Client
from Location.models import Location


class Contrat(models.Model):
    """Modèle représentant un contrat de location."""
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('expire', 'Expiré'),
        ('annule', 'Annulé'),
    ]
    
    numero_contrat = models.CharField(max_length=50, unique=True)
    location = models.OneToOneField(Location, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_signature = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField()
    conditions = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    document = models.FileField(upload_to='contrats/', null=True, blank=True)

    class Meta:
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats"
        ordering = ['-date_signature']

    def __str__(self):
        return f"Contrat {self.numero_contrat} - {self.client}"
    
    def details_contrat(self):
        """Retourne les détails du contrat."""
        return (f"Numéro: {self.numero_contrat}\n"
                f"Client: {self.client}\n"
                f"Location: {self.location}\n"
                f"Date signature: {self.date_signature.strftime('%d/%m/%Y')}\n"
                f"Date expiration: {self.date_expiration.strftime('%d/%m/%Y')}\n"
                f"Statut: {self.get_statut_display()}\n"
                f"Conditions: {self.conditions[:100]}...")
    
    def is_valid(self):
        """Vérifie si le contrat est valide."""
        return self.statut == 'actif' and timezone.now() <= self.date_expiration
    
    def is_expired(self):
        """Vérifie si le contrat est expiré."""
        return timezone.now() > self.date_expiration
