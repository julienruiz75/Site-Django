from django.shortcuts import render
from .models import Evenement
from datetime import datetime
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilUtilisateurForm
from .models import ProfilUtilisateur
from django.contrib.auth.models import User

# Vue pour la page d'accueil
def home(request):
    return render(request, 'information/home.html')

# Vue pour la page de recherche (pas utilisée pour l’instant)
def recherche(request):
    return render(request, 'information/recherche.html')

# Vue pour la page d'inscription
def inscription(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ crée l’utilisateur dans la base
            return redirect('home')  # redirige vers la page d’accueil après inscription
    else:
        form = CustomUserForm()

    return render(request, 'information/inscription.html', {'form': form})

# Vue pour la page Découvrir (photo, description, filtres, événements)
def decouvrir(request):
    domaine = request.GET.get('domaine')
    mois = request.GET.get('mois')

    evenements = Evenement.objects.all()

    if domaine and domaine != "tous":
        evenements = evenements.filter(domaine=domaine)

    if mois and mois != "tous":
        evenements = evenements.filter(date__month=int(mois))

    context = {
        'evenements': evenements,
        'mois_actuel': datetime.now().month,
    }

    return render(request, 'information/decouvrir.html', context)

def connexion(request):
    message = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = "Identifiants incorrects"

    return render(request, 'information/connexion.html', {'message': message})

def deconnexion(request):
    logout(request)
    return redirect('home')

@login_required
def profil(request):
    # ✅ On récupère ou crée le profil lié à l’utilisateur connecté
    profil, created = ProfilUtilisateur.objects.get_or_create(user=request.user)

    message = ""

    if request.method == 'POST':
        # Formulaire envoyé : on traite la mise à jour
        form = ProfilUtilisateurForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            message = "Profil mis à jour avec succès ✅"
        else:
            message = "Erreur dans le formulaire ❌"
    else:
        # Première visite de la page : on pré-remplit le formulaire
        form = ProfilUtilisateurForm(instance=profil)

    context = {
        'form': form,
        'message': message,
        'pseudo': request.user.username,
        'niveau': profil.niveau,
        'points': profil.points,
    }
    return render(request, 'information/profil.html', context)

@login_required
def membres(request):
    societe_filtre = request.GET.get('societe')
    
    profils = ProfilUtilisateur.objects.all().select_related('user')

    if societe_filtre:
        profils = profils.filter(societe__icontains=societe_filtre)

    context = {
        'profils': profils,
        'societe_filtre': societe_filtre or '',
    }

    return render(request, 'information/membres.html', context)