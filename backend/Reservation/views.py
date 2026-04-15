from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Reservation
from Contrat.models import Contrat
from Client.models import Client
from Voiture.models import Voiture
from Location.models import Location
from django.utils import timezone
from datetime import datetime
import uuid


class ListReservationView(ListView):
    """Afficher la liste des réservations."""
    model = Reservation
    template_name = 'reservation/list_reservation.html'
    context_object_name = 'reservations'
    paginate_by = 10

    def get_queryset(self):
        return Reservation.objects.select_related('client', 'voiture', 'contrat').order_by('-date_reservation')


class DetailReservationView(DetailView):
    """Afficher les détails d'une réservation."""
    model = Reservation
    template_name = 'reservation/detail_reservation.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.get_object()
        context['contrat'] = reservation.contrat
        context['paiements'] = reservation.contrat.paiements.all() if reservation.contrat else []
        return context


class CreateReservationView(CreateView):
    """Créer une réservation avec génération automatique d'un contrat."""
    model = Reservation
    template_name = 'reservation/create_reservation.html'
    fields = ['client', 'voiture', 'date_debut', 'date_fin', 'nombre_jours', 'prix_estime', 'commentaires']
    success_url = reverse_lazy('reservation-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        reservation = self.object
        
        # Créer la location
        location = Location.objects.create(
            client=reservation.client,
            voiture=reservation.voiture,
            date_debut=reservation.date_debut,
            date_fin=reservation.date_fin,
            prix_journalier=reservation.prix_estime / reservation.nombre_jours
        )
        
        # Créer le contrat associé
        contrat = Contrat.objects.create(
            numero_contrat=f"CONTRAT-{uuid.uuid4().hex[:8].upper()}",
            location=location,
            client=reservation.client,
            date_expiration=reservation.date_fin,
            conditions="Conditions standard de location.",
            statut='actif'
        )
        
        # Lier le contrat à la réservation
        reservation.contrat = contrat
        reservation.save()
        
        return response
