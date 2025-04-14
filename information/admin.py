from django.contrib import admin
from .models import Evenement, ProfilUtilisateur, ObjetConnecte

# 🎟️ Admin Événements
@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'domaine', 'date')
    list_filter = ('domaine', 'date')
    search_fields = ('titre', 'description')

# 👤 Admin Profils utilisateurs
@admin.register(ProfilUtilisateur)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'prenom', 'nom', 'societe', 'poste', 'niveau', 'points')  # ✅ ajout points
    list_editable = ('niveau', 'points')  # ✅ modifiables directement dans la liste
    search_fields = ('user__username', 'prenom', 'nom', 'societe')
    list_filter = ('niveau',)

# 🧠 Admin Objets connectés
@admin.register(ObjetConnecte)
class ObjetConnecteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'salle_associee', 'statut', 'niveau_requis', 'date_ajout')
    list_filter = ('type', 'statut', 'niveau_requis', 'salle_associee')