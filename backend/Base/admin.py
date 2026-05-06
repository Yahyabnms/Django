from django.contrib import admin
from .models import Agence


@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'telephone', 'est_principale', 'active']
    list_filter = ['ville', 'est_principale', 'active']
    search_fields = ['nom', 'adresse', 'ville']
