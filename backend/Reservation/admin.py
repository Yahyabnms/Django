from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'voiture', 'date_debut', 'date_fin', 'statut', 'prix_estime')
    list_filter = ('statut', 'date_reservation', 'date_debut')
    search_fields = ('client__nom', 'voiture__immatriculation')
    ordering = ('-date_reservation',)
