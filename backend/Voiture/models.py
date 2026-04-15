from django.db import models


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
                f"Prix/jour: {self.prix_par_jour}€\n"
                f"Kilométrage: {self.kilométrage} km\n"
                f"Statut: {self.get_statut_display()}")
    
    def is_available(self):
        """Vérifie si la voiture est disponible."""
        return self.statut == 'disponible'
