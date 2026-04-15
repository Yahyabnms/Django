from django.shortcuts import render
from .models import Assurance


def assurance_list(request):
    """Affiche la liste de toutes les assurances."""
    assurances = Assurance.objects.all()
    return render(request, 'assurance/list.html', {'assurances': assurances})


def assurance_detail(request, pk):
    """Affiche les détails d'une assurance spécifique."""
    assurance = Assurance.objects.get(pk=pk)
    return render(request, 'assurance/detail.html', {'assurance': assurance})
