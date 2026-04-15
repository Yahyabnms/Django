from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm


class HomeView(View):
    def get(self, request):
        return render(request, 'base/home.html', {})


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