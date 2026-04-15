from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'voiture', 'date_debut', 'date_fin', 'statut', 'prix_total')
    list_filter = ('statut', 'date_creation', 'date_debut')
    search_fields = ('client__nom', 'voiture__immatriculation')
    ordering = ('-date_creation',)
