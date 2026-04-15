from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Contrat
from Paiement.models import Paiement
from Reservation.models import Reservation
from django.utils import timezone


class ListContratView(ListView):
    """Afficher la liste des contrats."""
    model = Contrat
    template_name = 'contrat/list_contrat.html'
    context_object_name = 'contrats'
    paginate_by = 10

    def get_queryset(self):
        return Contrat.objects.select_related('client', 'location').order_by('-date_signature')


class DetailContratView(DetailView):
    """Afficher les détails d'un contrat avec sa réservation et paiements."""
    model = Contrat
    template_name = 'contrat/detail_contrat.html'
    context_object_name = 'contrat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrat = self.get_object()
        
        # Récupérer la réservation associée
        context['reservation'] = Reservation.objects.filter(contrat=contrat).first()
        
        # Récupérer les paiements associés au contrat
        context['paiements'] = Paiement.objects.filter(contrat=contrat).order_by('-date_paiement')
        
        # Calculer les statistiques
        total_paye = sum([p.montant for p in context['paiements'] if p.statut == 'confirme'])
        context['total_paye'] = total_paye
        context['montant_restant'] = (context['reservation'].prix_estime - total_paye) if context['reservation'] else 0
        
        return context


class RenouvelerContratView(View):
    """Renouveler un contrat expiré."""
    
    def post(self, request, pk):
        contrat = get_object_or_404(Contrat, id=pk)
        
        if contrat.is_expired():
            from datetime import timedelta
            new_contrat = Contrat.objects.create(
                numero_contrat=f"{contrat.numero_contrat}-RENEW",
                location=contrat.location,
                client=contrat.client,
                date_expiration=timezone.now() + timedelta(days=365),
                conditions=contrat.conditions,
                statut='actif'
            )
            return redirect('contrat-detail', pk=new_contrat.id)
        
        return redirect('contrat-detail', pk=contrat.id)


class AnnulerContratView(View):
    """Annuler un contrat."""
    
    def post(self, request, pk):
        contrat = get_object_or_404(Contrat, id=pk)
        contrat.statut = 'annule'
        contrat.save()
        return redirect('contrat-detail', pk=contrat.id)
