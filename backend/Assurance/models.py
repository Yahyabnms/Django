from django.db import models


class Assurance(models.Model):
    """Modèle représentant une assurance."""
    
    idAssurance = models.AutoField(primary_key=True)
    nomAssurance = models.CharField(max_length=100)
    typeAssurance = models.CharField(
        max_length=100,
        help_text="Type d'assurance (ex. tous risques, responsabilité civile)"
    )
    prix = models.FloatField()
    dateDebut = models.DateField()
    dateFin = models.DateField()
    
    class Meta:
        verbose_name = "Assurance"
        verbose_name_plural = "Assurances"
    
    def detailsAssurance(self):
        """Retourne les détails complets de l'assurance."""
        return (f"ID: {self.idAssurance}\n"
                f"Nom: {self.nomAssurance}\n"
                f"Type: {self.typeAssurance}\n"
                f"Prix: {self.prix}€\n"
                f"Date début: {self.dateDebut}\n"
                f"Date fin: {self.dateFin}")
    
    def __str__(self):
        return f"{self.nomAssurance} ({self.typeAssurance})"
