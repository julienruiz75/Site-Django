from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilUtilisateur, ReservationSalle
from django.forms.widgets import SelectDateWidget

# ✅ Formulaire d'inscription personnalisé
class CustomUserForm(UserCreationForm):
    username = forms.CharField(label="Pseudonyme", max_length=30)
    email = forms.EmailField(label="Adresse mail", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ✅ Formulaire de modification du profil utilisateur
class ProfilUtilisateurForm(forms.ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = [
            'prenom', 'nom', 'date_naissance', 'sexe', 'photo',
            'poste', 'societe',
            'show_prenom', 'show_nom', 'show_date_naissance', 'show_sexe', 'show_photo'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'prenom': 'Prénom',
            'nom': 'Nom',
            'date_naissance': 'Date de naissance',
            'sexe': 'Sexe',
            'photo': 'Photo',
            'poste': 'Intitulé du poste',
            'societe': 'Société',
            'show_prenom': 'Afficher le prénom',
            'show_nom': 'Afficher le nom',
            'show_date_naissance': 'Afficher la date de naissance',
            'show_sexe': 'Afficher le sexe',
            'show_photo': 'Afficher la photo',
        }


# ✅ Formulaire pour changer le niveau dans l’admin
class NiveauForm(forms.ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = ['niveau']


# ✅ Formulaire de don de points entre utilisateurs
class DonPointsForm(forms.Form):
    pseudo = forms.CharField(label="Pseudo du destinataire", max_length=100)
    points = forms.IntegerField(label="Nombre de points à donner", min_value=1)


# ✅ Formulaire de réservation de salle
class ReservationSalleForm(forms.ModelForm):
    class Meta:
        model = ReservationSalle
        fields = ['salle', 'date', 'heure']
        widgets = {
            'date': SelectDateWidget(),  # widget calendrier
            'heure': forms.Select(choices=[(str(h).zfill(2), f"{h}h") for h in range(7, 24)]),
        }
