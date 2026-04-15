from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'actif', 'date_inscription')
    list_filter = ('actif', 'date_inscription')
    search_fields = ('nom', 'prenom', 'email')
    ordering = ('-date_inscription',)
