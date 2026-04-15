from django.contrib import admin
from .models import Contrat

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = ('numero_contrat', 'client', 'location', 'date_signature', 'date_expiration', 'statut')
    list_filter = ('statut', 'date_signature')
    search_fields = ('numero_contrat', 'client__nom')
    ordering = ('-date_signature',)
