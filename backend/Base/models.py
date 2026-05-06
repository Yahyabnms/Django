from django.db import models


class Agence(models.Model):
    """Modèle représentant une agence de location avec coordonnées GPS."""

    nom = models.CharField(max_length=200)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    heures_ouverture = models.TextField(blank=True, help_text="Ex: Lun-Ven: 8h-18h, Sam: 9h-12h")
    est_principale = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agence"
        verbose_name_plural = "Agences"
        ordering = ['-est_principale', 'ville', 'nom']

    def __str__(self):
        return f"{self.nom} - {self.ville}"
