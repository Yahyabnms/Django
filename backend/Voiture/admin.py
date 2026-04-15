from django.contrib import admin
from .models import Voiture, CategorieVoiture

@admin.register(CategorieVoiture)
class CategorieVoitureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite_passagers', 'nombre_portes', 'type_carburant', 'transmission')
    search_fields = ('nom',)
    ordering = ('nom',)

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'categorie', 'immatriculation', 'statut', 'prix_par_jour', 'kilométrage')
    list_filter = ('statut', 'categorie', 'marque', 'annee')
    search_fields = ('marque', 'modele', 'immatriculation')
    ordering = ('marque',)
