from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'montant', 'methode_paiement', 'statut', 'date_paiement')
    list_filter = ('statut', 'methode_paiement', 'date_paiement')
    search_fields = ('numero_transaction', 'client__nom')
    ordering = ('-date_paiement',)
