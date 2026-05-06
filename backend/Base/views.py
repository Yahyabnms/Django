from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from Voiture.models import Voiture
from Reservation.models import Reservation
from Contrat.models import Contrat
from Client.models import Client
from Paiement.models import Paiement
from Location.models import Location


class HomeView(View):
    def get(self, request):
        voitures = Voiture.objects.all().order_by('-date_ajout')[:6]
        total_voitures = Voiture.objects.count()
        
        context = {
            'voitures': voitures,
            'total_voitures': total_voitures,
        }
        return render(request, 'base/home.html', context)


class SignUpView(CreateView):
    """Vue d'inscription pour les nouveaux utilisateurs."""
    form_class = UserCreationForm
    template_name = 'base/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Inscription réussie! Vous pouvez maintenant vous connecter.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de l\'inscription. Veuillez vérifier les données.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'S\'inscrire'
        return context


class LoginView(View):
    """Vue de connexion pour les utilisateurs."""
    def get(self, request):
        return render(request, 'base/login.html', {'title': 'Se connecter'})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return render(request, 'base/login.html', {
                'title': 'Se connecter',
                'username': username
            })


class ProfileView(View):
    """Vue du profil utilisateur."""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'base/profile.html', {'user': request.user})


class MesReservationsView(View):
    """Afficher les réservations de l'utilisateur connecté."""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            client = Client.objects.get(email=request.user.email)
            reservations = Reservation.objects.filter(client=client).select_related('voiture').order_by('-date_reservation')
            
            # Associer les paiements aux réservations via les locations
            for res in reservations:
                try:
                    location = Location.objects.filter(
                        client=client, voiture=res.voiture,
                        date_debut=res.date_debut, date_fin=res.date_fin
                    ).first()
                    if location:
                        res.paiement = Paiement.objects.filter(location=location).first()
                    else:
                        res.paiement = None
                except Exception:
                    res.paiement = None
        except Client.DoesNotExist:
            reservations = []
        
        context = {
            'reservations': reservations,
        }
        return render(request, 'base/mes_reservations.html', context)


class MesContratsView(View):
    """Afficher les contrats de l'utilisateur connecté."""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            client = Client.objects.get(email=request.user.email)
            contrats = Contrat.objects.filter(client=client).select_related('location', 'reservation').order_by('-date_signature')
        except Client.DoesNotExist:
            contrats = []
        
        context = {
            'contrats': contrats,
        }
        return render(request, 'base/mes_contrats.html', context)


class CustomLogoutView(View):
    """Vue de déconnexion personnalisée (supporte GET)."""
    def get(self, request):
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
        return redirect('home')
    
    def post(self, request):
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
        return redirect('home')