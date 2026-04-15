from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Paiement
from Contrat.models import Contrat
from Reservation.models import Reservation
from Client.models import Client
from Location.models import Location
from django.utils import timezone
import uuid


class ListPaiementView(ListView):
    """Afficher la liste des paiements."""
    model = Paiement
    template_name = 'paiement/list_paiement.html'
    context_object_name = 'paiements'
    paginate_by = 10

    def get_queryset(self):
        return Paiement.objects.select_related('client', 'location', 'contrat', 'reservation').order_by('-date_paiement')


class DetailPaiementView(DetailView):
    """Afficher les détails d'un paiement."""
    model = Paiement
    template_name = 'paiement/detail_paiement.html'
    context_object_name = 'paiement'


class CreatePaiementView(CreateView):
    """Créer un paiement pour une réservation/contrat."""
    model = Paiement
    template_name = 'paiement/create_paiement.html'
    fields = ['montant', 'methode_paiement', 'numero_transaction', 'remarques']
    success_url = reverse_lazy('paiement-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrat_id = self.kwargs.get('contrat_id')
        reservation_id = self.kwargs.get('reservation_id')
        
        if contrat_id:
            context['contrat'] = get_object_or_404(Contrat, id=contrat_id)
        if reservation_id:
            context['reservation'] = get_object_or_404(Reservation, id=reservation_id)
        
        return context

    def form_valid(self, form):
        contrat_id = self.kwargs.get('contrat_id')
        reservation_id = self.kwargs.get('reservation_id')
        
        contrat = get_object_or_404(Contrat, id=contrat_id) if contrat_id else None
        reservation = get_object_or_404(Reservation, id=reservation_id) if reservation_id else None
        
        paiement = form.save(commit=False)
        
        if contrat:
            paiement.contrat = contrat
            paiement.client = contrat.client
            paiement.location = contrat.location
        
        if reservation:
            if not paiement.contrat:
                paiement.contrat = reservation.contrat
            paiement.reservation = reservation
            if not paiement.client:
                paiement.client = reservation.client
        
        paiement.statut = 'confirme'
        paiement.save()
        
        return super().form_valid(form)


class ConfirmerPaiementView(View):
    """Confirmer/valider un paiement."""
    
    def post(self, request, pk):
        paiement = get_object_or_404(Paiement, id=pk)
        paiement.statut = 'confirme'
        paiement.numero_transaction = paiement.numero_transaction or f"TXN-{uuid.uuid4().hex[:8].upper()}"
        paiement.save()
        return redirect('paiement-detail', pk=paiement.id)


class AnnulerPaiementView(View):
    """Annuler/refuser un paiement."""
    
    def post(self, request, pk):
        paiement = get_object_or_404(Paiement, id=pk)
        paiement.statut = 'refuse'
        paiement.save()
        return redirect('paiement-detail', pk=paiement.id)
