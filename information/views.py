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
from django.shortcuts import render, redirect
from django.core.mail import send_mail

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
            # Récupération de l'email saisi
            destinataire = form.cleaned_data.get('email')
            # Envoi de l'e-mail
            send_mail(
                subject='Bienvenue chez Cowork Connect',
                message=(
                    "Bonjour,\n\n"
                    "Nous vous remercions pour votre inscription sur le site de Cowork Connect.\n"
                    "Nous serions ravis de vous accueillir bientôt au sein de nos locaux.\n"
                    "Afin de mieux faire connaissance, nous vous invitons à bien vouloir compléter votre profil utilisateur en vous connectant à votre compte.\n"
                    "Pour toute question, n'hésitez pas à nous contacter.\n\n"
                    "À bientôt,\n"
                    "L'équipe Cowork Connect"),
                from_email='coworkconnect2025@gmail.com',  # Mets ici l'email de ton application
                recipient_list=[destinataire],
                fail_silently=False,
            )

            return redirect('connexion') 

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

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProfilUtilisateur
from .forms import NiveauForm

def est_superuser(user):
    return user.is_superuser

@user_passes_test(est_superuser)
def gestion_niveaux(request):
    profils = ProfilUtilisateur.objects.all()

    if request.method == "POST":
        profil_id = request.POST.get("profil_id")
        profil = get_object_or_404(ProfilUtilisateur, id=profil_id)
        form = NiveauForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
        return redirect('gestion_niveaux')

    context = {
        'profils': profils,
        'form': NiveauForm()
    }
    return render(request, "information/gestion_niveaux.html", context)

