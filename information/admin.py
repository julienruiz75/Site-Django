from django.contrib import admin
from .models import Evenement  # on importe le modèle

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'domaine', 'date')  # colonnes visibles dans l'admin
    list_filter = ('domaine', 'date')  # filtres dans la sidebar
    search_fields = ('titre', 'description')  # champ de recherche rapide