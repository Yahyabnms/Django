from django.db import models


class Client(models.Model):
    """Modèle représentant un client."""
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def details_client(self):
        """Retourne les détails du client."""
        return (f"Nom: {self.nom}\n"
                f"Prénom: {self.prenom}\n"
                f"Email: {self.email}\n"
                f"Téléphone: {self.telephone}\n"
                f"Adresse: {self.adresse}\n"
                f"Inscription: {self.date_inscription.strftime('%d/%m/%Y')}\n"
                f"Statut: {'Actif' if self.actif else 'Inactif'}")
    
    def get_full_name(self):
        """Retourne le nom complet du client."""
        return f"{self.prenom} {self.nom}"
