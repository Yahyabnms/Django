from django.shortcuts import render
from django.views.generic import ListView
from .models import Voiture


class ListeVoituresView(ListView):
    """Afficher la liste des voitures disponibles"""
    model = Voiture
    template_name = 'voiture/liste_voitures.html'
    context_object_name = 'voitures'
    paginate_by = 12

    def get_queryset(self):
        return Voiture.objects.filter(statut='disponible').select_related('categorie').order_by('marque', 'modele')
