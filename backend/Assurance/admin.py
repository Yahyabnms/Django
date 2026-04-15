from django.contrib import admin
from .models import Assurance


@admin.register(Assurance)
class AssuranceAdmin(admin.ModelAdmin):
    list_display = ('idAssurance', 'nomAssurance', 'typeAssurance', 'prix', 'dateDebut', 'dateFin')
    search_fields = ('nomAssurance', 'typeAssurance')
    list_filter = ('typeAssurance', 'dateDebut', 'dateFin')
    ordering = ('-dateDebut',)
