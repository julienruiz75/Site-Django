from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilUtilisateur

class CustomUserForm(UserCreationForm):
    username = forms.CharField(label="Pseudonyme", max_length=30)
    email = forms.EmailField(label="Adresse mail", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfilUtilisateurForm(forms.ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = [
            'prenom', 'nom', 'date_naissance', 'sexe', 'photo',
            'poste', 'societe',  # ✅ ici on utilise le bon champ
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
            'poste': 'Intitulé du poste',  # ✅ le bon label
            'societe': 'Société',
            'show_prenom': 'Afficher le prénom',
            'show_nom': 'Afficher le nom',
            'show_date_naissance': 'Afficher la date de naissance',
            'show_sexe': 'Afficher le sexe',
            'show_photo': 'Afficher la photo',
        }

from django import forms
from .models import ProfilUtilisateur

class NiveauForm(forms.ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = ['niveau']
