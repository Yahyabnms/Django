from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reservation
from Contrat.models import Contrat
from Client.models import Client
from Voiture.models import Voiture
from Location.models import Location
from Assurance.models import Assurance
from Paiement.models import Paiement
from django.utils import timezone
from datetime import datetime, timedelta
import uuid
import json


class ListReservationView(ListView):
    """Afficher la liste des réservations."""
    model = Reservation
    template_name = 'reservation/list_reservation.html'
    context_object_name = 'reservations'
    paginate_by = 10

    def get_queryset(self):
        return Reservation.objects.select_related('client', 'voiture').order_by('-date_reservation')


class DetailReservationView(DetailView):
    """Afficher les détails d'une réservation."""
    model = Reservation
    template_name = 'reservation/detail_reservation.html'
    context_object_name = 'reservation'


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
            prix_total=reservation.prix_estime,
            statut='en_cours'
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
        
        return response


class ReserverVoitureView(View):
    """Vue pour réserver une voiture spécifique"""
    
    def get(self, request, voiture_id):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        
        voiture = get_object_or_404(Voiture, id=voiture_id)
        assurances = Assurance.objects.all()
        
        if voiture.statut != 'disponible':
            return render(request, 'reservation/reserver_voiture.html', {
                'voiture': voiture,
                'assurances': assurances,
                'error': 'Cette voiture n\'est pas disponible'
            })
        
        return render(request, 'reservation/reserver_voiture.html', {
            'voiture': voiture,
            'assurances': assurances
        })


@csrf_exempt
def check_availability(request, voiture_id):
    """API pour vérifier la disponibilité d'une voiture"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d')
            date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d')
            
            voiture = get_object_or_404(Voiture, id=voiture_id)
            
            # Vérifier si la voiture est disponible pour ces dates
            existing_reservations = Reservation.objects.filter(
                voiture=voiture,
                statut__in=['en_attente', 'confirmee', 'activee']
            ).filter(
                date_debut__lte=date_fin,
                date_fin__gte=date_debut
            )
            
            is_available = not existing_reservations.exists()
            
            return JsonResponse({'available': is_available})
        except Exception as e:
            return JsonResponse({'available': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'available': False}, status=405)


@csrf_exempt
def create_reservation(request):
    """API pour créer une réservation"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Vous devez être connecté'}, status=401)
        
        try:
            voiture_id = request.POST.get('voiture_id')
            date_debut_str = request.POST.get('date_debut')
            date_fin_str = request.POST.get('date_fin')
            
            voiture = get_object_or_404(Voiture, id=voiture_id)
            
            if voiture.statut != 'disponible':
                return JsonResponse({'success': False, 'message': 'Cette voiture n\'est pas disponible'})
            
            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d')
            date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d')
            
            if date_fin <= date_debut:
                return JsonResponse({'success': False, 'message': 'La date de fin doit être après la date de début'})
            
            # Vérifier la disponibilité
            existing_reservations = Reservation.objects.filter(
                voiture=voiture,
                statut__in=['en_attente', 'confirmee', 'activee']
            ).filter(
                date_debut__lte=date_fin,
                date_fin__gte=date_debut
            )
            
            if existing_reservations.exists():
                return JsonResponse({'success': False, 'message': 'Cette voiture n\'est pas disponible pour ces dates'})
            
            # Récupérer ou créer le client
            telephone = request.POST.get('telephone', '')[:15]
            client, created = Client.objects.get_or_create(
                email=request.user.email if hasattr(request.user, 'email') else f"{request.user.username}@example.com",
                defaults={
                    'nom': request.user.last_name or request.user.username,
                    'prenom': request.user.first_name or '',
                    'telephone': telephone,
                    'adresse': ''
                }
            )
            
            # Mettre à jour le téléphone si existant
            if not created and telephone:
                client.telephone = telephone
                client.save()
            
            # Calculer le nombre de jours et le prix
            nombre_jours = (date_fin - date_debut).days
            prix_estime = nombre_jours * float(voiture.prix_par_jour)
            
            # Récupérer l'assurance choisie
            assurance_id = request.POST.get('assurance_id')
            assurance_choisie = get_object_or_404(Assurance, idAssurance=assurance_id) if assurance_id else None
            
            # Créer la réservation
            reservation = Reservation.objects.create(
                client=client,
                voiture=voiture,
                assurance=assurance_choisie,
                date_debut=date_debut,
                date_fin=date_fin,
                nombre_jours=nombre_jours,
                prix_estime=prix_estime,
                statut='en_attente'
            )
            
            # Créer la location
            location = Location.objects.create(
                client=client,
                voiture=voiture,
                date_debut=date_debut,
                date_fin=date_fin,
                prix_total=prix_estime,
                statut='en_cours'
            )
            
            # Créer le paiement
            methode_paiement = request.POST.get('methode_paiement', 'carte')
            montant_total = prix_estime + (assurance_choisie.prix if assurance_choisie else 0)
            
            paiement = Paiement.objects.create(
                client=client,
                location=location,
                montant=montant_total,
                methode_paiement=methode_paiement,
                statut='en_attente',
                numero_transaction=f"TRANS-{reservation.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )
            
            # Créer le contrat
            contrat = Contrat.objects.create(
                numero_contrat=f"CONTRAT-{uuid.uuid4().hex[:8].upper()}",
                location=location,
                client=client,
                assurance=assurance_choisie,
                date_expiration=date_fin,
                conditions=f"Location de {voiture.marque} {voiture.modele} du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}. Assurance: {assurance_choisie.nomAssurance if assurance_choisie else 'N/A'}. Paiement total: {montant_total} DH."
            )
            
            return JsonResponse({
                'success': True,
                'reservation_id': reservation.id,
                'message': 'Réservation créée avec succès. Contrat, assurance et paiement générés automatiquement.',
                'details': {
                    'location_id': location.id,
                    'assurance_id': assurance_choisie.idAssurance if assurance_choisie else None,
                    'paiement_id': paiement.id,
                    'contrat_id': contrat.id,
                    'contrat_number': contrat.numero_contrat,
                    'total_price': float(paiement.montant),
                    'methode_paiement': paiement.get_methode_paiement_display()
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False}, status=405)
