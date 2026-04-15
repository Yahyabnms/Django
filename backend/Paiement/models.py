from django.db import models
from Location.models import Location
from Client.models import Client


class Paiement(models.Model):
    """Modèle représentant un paiement de location."""
    
    METHODE_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('espece', 'Espèce'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('refuse', 'Refusé'),
        ('remboursé', 'Remboursé'),
    ]
    
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode_paiement = models.CharField(max_length=20, choices=METHODE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_paiement = models.DateTimeField(auto_now_add=True)
    numero_transaction = models.CharField(max_length=100, unique=True, null=True, blank=True)
    remarques = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_paiement']

    def __str__(self):
        return f"Paiement {self.id} - {self.montant}€ ({self.statut})"
    
    def details_paiement(self):
        """Retourne les détails du paiement."""
        return (f"ID: {self.id}\n"
                f"Client: {self.client}\n"
                f"Montant: {self.montant}€\n"
                f"Méthode: {self.get_methode_paiement_display()}\n"
                f"Statut: {self.get_statut_display()}\n"
                f"Date: {self.date_paiement.strftime('%d/%m/%Y %H:%M')}\n"
                f"Transaction: {self.numero_transaction or 'N/A'}")
    
    def is_confirmed(self):
        """Vérifie si le paiement est confirmé."""
        return self.statut == 'confirme'
    
    def is_pending(self):
        """Vérifie si le paiement est en attente."""
        return self.statut == 'en_attente'
