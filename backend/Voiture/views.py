from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from datetime import datetime
from .models import Voiture


class ListeVoituresView(ListView):
    """Afficher la liste des voitures disponibles"""
    model = Voiture
    template_name = 'voiture/liste_voitures.html'
    context_object_name = 'voitures'
    paginate_by = 12

    def get_queryset(self):
        return Voiture.objects.filter(statut='disponible').select_related('categorie').order_by('marque', 'modele')


class VerifierDisponibiliteView(View):
    """Vérifier la disponibilité d'une voiture pour des dates données"""
    
    def get(self, request, voiture_id):
        try:
            voiture = Voiture.objects.get(id=voiture_id)
            
            date_debut_str = request.GET.get('date_debut')
            date_fin_str = request.GET.get('date_fin')
            
            if not date_debut_str or not date_fin_str:
                return JsonResponse({
                    'success': False,
                    'error': 'Les dates de début et de fin sont requises'
                }, status=400)
            
            try:
                date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d')
                date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Format de date invalide. Utilisez YYYY-MM-DD'
                }, status=400)
            
            if date_debut >= date_fin:
                return JsonResponse({
                    'success': False,
                    'error': 'La date de fin doit être après la date de début'
                }, status=400)
            
            disponible = voiture.is_available_for_dates(date_debut, date_fin)
            
            return JsonResponse({
                'success': True,
                'disponible': disponible,
                'voiture': {
                    'id': voiture.id,
                    'marque': voiture.marque,
                    'modele': voiture.modele,
                    'immatriculation': voiture.immatriculation
                },
                'date_debut': date_debut_str,
                'date_fin': date_fin_str
            })
            
        except Voiture.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Voiture non trouvée'
            }, status=404)

class SuiviGPSView(UserPassesTestMixin, View):
    """Affiche la carte de suivi GPS d'une voiture"""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return HttpResponseForbidden("<h1>403 Interdit</h1><p>Seuls les administrateurs peuvent accéder au suivi GPS.</p>")

    def get(self, request, voiture_id):
        try:
            voiture = Voiture.objects.get(id=voiture_id)
            return render(request, 'voiture/suivi_gps.html', {
                'voiture': voiture
            })
        except Voiture.DoesNotExist:
            return render(request, '404.html', status=404)

class APIGPSVoiture(UserPassesTestMixin, View):
    """API pour récupérer les coordonnées GPS d'une voiture (pour rafraîchissement AJAX)"""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return JsonResponse({'success': False, 'error': 'Accès non autorisé. Réservé aux administrateurs.'}, status=403)

    def get(self, request, voiture_id):
        try:
            voiture = Voiture.objects.get(id=voiture_id)
            
            # Si la voiture n'a pas de coordonnées, on peut simuler ou renvoyer null
            # Dans un cas réel, ces données viendraient d'un tracker IoT
            return JsonResponse({
                'success': True,
                'latitude': voiture.latitude,
                'longitude': voiture.longitude,
                'derniere_mise_a_jour': voiture.derniere_mise_a_jour_gps.isoformat() if voiture.derniere_mise_a_jour_gps else None
            })
        except Voiture.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Voiture non trouvée'
            }, status=404)
