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
        queryset = Voiture.objects.filter(statut='disponible').select_related('categorie')
        
        # Filtre par lieu (ville)
        lieu_depart = self.request.GET.get('lieu_depart')
        if lieu_depart:
            queryset = queryset.filter(ville=lieu_depart)
            
        # Filtre par dates de disponibilité
        date_debut_str = self.request.GET.get('date_depart')
        date_fin_str = self.request.GET.get('date_retour')
        
        if date_debut_str and date_fin_str:
            try:
                from Location.models import Location
                from Reservation.models import Reservation
                from django.db.models import Q
                
                date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d')
                date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d')
                
                # Trouver les IDs des voitures occupées pendant cette période
                voitures_occupees_loc = Location.objects.filter(
                    statut='en_cours'
                ).filter(
                    Q(date_debut__lte=date_fin) & Q(date_fin__gte=date_debut)
                ).values_list('voiture_id', flat=True)
                
                voitures_occupees_res = Reservation.objects.filter(
                    statut__in=['confirmee', 'activee']
                ).filter(
                    Q(date_debut__lte=date_fin) & Q(date_fin__gte=date_debut)
                ).values_list('voiture_id', flat=True)
                
                # Exclure ces voitures du queryset
                queryset = queryset.exclude(id__in=voitures_occupees_loc).exclude(id__in=voitures_occupees_res)
                
            except (ValueError, TypeError):
                # En cas de format de date invalide, on ignore le filtre
                pass
            
        return queryset.order_by('marque', 'modele')


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

class DashboardGPSView(UserPassesTestMixin, View):
    """Affiche une carte avec toutes les voitures suivies"""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return HttpResponseForbidden("<h1>403 Interdit</h1><p>Seuls les administrateurs peuvent accéder au dashboard GPS.</p>")

    def get(self, request):
        voitures = Voiture.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
        return render(request, 'voiture/dashboard_gps.html', {
            'voitures': voitures
        })

class APIAllCarsGPS(UserPassesTestMixin, View):
    """API pour récupérer les coordonnées GPS de toutes les voitures"""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return JsonResponse({'success': False, 'error': 'Accès non autorisé.'}, status=403)

    def get(self, request):
        voitures = Voiture.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
        data = []
        for v in voitures:
            data.append({
                'id': v.id,
                'marque': v.marque,
                'modele': v.modele,
                'immatriculation': v.immatriculation,
                'latitude': v.latitude,
                'longitude': v.longitude,
                'statut': v.statut,
                'derniere_mise_a_jour': v.derniere_mise_a_jour_gps.isoformat() if v.derniere_mise_a_jour_gps else None
            })
        return JsonResponse({'success': True, 'voitures': data})
