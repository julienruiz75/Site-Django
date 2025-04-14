from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta

from django.contrib.auth.models import User

from .models import Evenement, ProfilUtilisateur, ObjetConnecte, Salle, ReservationSalle
from .forms import CustomUserForm, ProfilUtilisateurForm, NiveauForm, DonPointsForm

# ✅ Mise à jour automatique du niveau
def mettre_a_jour_niveau(profil):
    if profil.points >= 100:
        profil.niveau = 'expert'
    elif profil.points >= 50:
        profil.niveau = 'avance'
    elif profil.points >= 15:
        profil.niveau = 'intermediaire'
    else:
        profil.niveau = 'debutant'
    profil.save()

# 🏠 Accueil
def home(request):
    return render(request, 'information/home.html')

# 🔍 Recherche
def recherche(request):
    return render(request, 'information/recherche.html')

# 📝 Inscription
def inscription(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            destinataire = form.cleaned_data.get('email')
            send_mail(
                subject='Bienvenue chez Cowork Connect',
                message="Bonjour,\n\nMerci pour votre inscription sur Cowork Connect.",
                from_email='coworkconnect2025@gmail.com',
                recipient_list=[destinataire],
                fail_silently=False,
            )
            return redirect('connexion')
    else:
        form = CustomUserForm()
    return render(request, 'information/inscription.html', {'form': form})

# 🌍 Découvrir les événements
def decouvrir(request):
    domaine = request.GET.get('domaine')
    mois = request.GET.get('mois')
    evenements = Evenement.objects.all()
    if domaine and domaine != "tous":
        evenements = evenements.filter(domaine=domaine)
    if mois and mois != "tous":
        evenements = evenements.filter(date__month=int(mois))
    return render(request, 'information/decouvrir.html', {
        'evenements': evenements,
        'mois_actuel': datetime.now().month,
    })

# 🔐 Connexion
def connexion(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            profil, _ = ProfilUtilisateur.objects.get_or_create(user=user)
            profil.points += 1
            mettre_a_jour_niveau(profil)
            return redirect('home')
        else:
            message = "Identifiants incorrects"
    return render(request, 'information/connexion.html', {'message': message})

# 🚪 Déconnexion
def deconnexion(request):
    logout(request)
    return redirect('home')

# 👤 Profil
@login_required
def profil(request):
    profil, _ = ProfilUtilisateur.objects.get_or_create(user=request.user)
    message = ""
    if request.method == 'POST':
        form = ProfilUtilisateurForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            message = "Profil mis à jour ✅"
        else:
            message = "Erreur dans le formulaire ❌"
    else:
        form = ProfilUtilisateurForm(instance=profil)
    return render(request, 'information/profil.html', {
        'form': form,
        'message': message,
        'pseudo': request.user.username,
        'niveau': profil.niveau,
        'points': profil.points,
    })

# 👥 Membres
@login_required
def membres(request):
    societe_filtre = request.GET.get('societe')
    profils = ProfilUtilisateur.objects.select_related('user').all()
    if societe_filtre:
        profils = profils.filter(societe__icontains=societe_filtre)
    return render(request, 'information/membres.html', {
        'profils': profils,
        'societe_filtre': societe_filtre or '',
    })

# 🛠 Admin – niveaux
@user_passes_test(lambda u: u.is_superuser)
def gestion_niveaux(request):
    profils = ProfilUtilisateur.objects.all()
    if request.method == "POST":
        profil_id = request.POST.get("profil_id")
        profil = get_object_or_404(ProfilUtilisateur, id=profil_id)
        form = NiveauForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
        return redirect('gestion_niveaux')
    return render(request, "information/gestion_niveaux.html", {
        'profils': profils,
        'form': NiveauForm()
    })

# 📡 Objets connectés
@login_required
def liste_objets_connectes(request):
    profil = ProfilUtilisateur.objects.get(user=request.user)
    niveaux_ordre = ['debutant', 'intermediaire', 'avance', 'expert']
    index_niveau = niveaux_ordre.index(profil.niveau)
    niveaux_autorises = niveaux_ordre[:index_niveau + 1]

    type_filtre = request.GET.get('type')
    salle_filtre = request.GET.get('salle')

    objets = ObjetConnecte.objects.all()
    if type_filtre and type_filtre != 'tous':
        objets = objets.filter(type=type_filtre)
    if salle_filtre and salle_filtre != 'tous':
        objets = objets.filter(salle_associee__id=salle_filtre)

    return render(request, 'information/liste_objets.html', {
        'objets': objets,
        'pseudo': request.user.username,
        'niveau': profil.niveau,
        'niveaux_autorises': niveaux_autorises,
        'toutes_salles': Salle.objects.all(),
        'tous_types': ObjetConnecte.TYPES_OBJETS,
        'type_selectionne': type_filtre or 'tous',
        'salle_selectionnee': salle_filtre or 'tous',
    })

# 🔄 Activer/Désactiver objet
@require_POST
@login_required
def changer_statut_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    profil = ProfilUtilisateur.objects.get(user=request.user)
    niveaux = ['debutant', 'intermediaire', 'avance', 'expert']
    if niveaux.index(profil.niveau) >= niveaux.index(objet.niveau_requis):
        objet.statut = 'inactif' if objet.statut == 'actif' else 'actif'
        objet.save()
    return redirect('liste_objets_connectes')

# 🌟 Mes points + don
@login_required
def mes_points(request):
    profil = ProfilUtilisateur.objects.get(user=request.user)
    paliers = [('Débutant', 0), ('Intermédiaire', 15), ('Avancé', 50), ('Expert', 100)]
    prochain_palier = next(((nom, seuil) for nom, seuil in paliers if profil.points < seuil), None)
    message_don = ""
    if request.method == 'POST':
        form = DonPointsForm(request.POST)
        if form.is_valid():
            pseudo = form.cleaned_data['pseudo']
            nb_points = form.cleaned_data['points']
            try:
                destinataire = User.objects.get(username=pseudo)
                profil_dest = ProfilUtilisateur.objects.get(user=destinataire)
                niveaux = ['debutant', 'intermediaire', 'avance', 'expert']
                if niveaux.index(profil_dest.niveau) < niveaux.index(profil.niveau):
                    profil_dest.points += nb_points
                    mettre_a_jour_niveau(profil_dest)
                    profil_dest.save()
                    message_don = f"✅ {nb_points} point(s) donné(s) à {pseudo}."
                else:
                    message_don = "❌ Vous ne pouvez donner des points qu'à un membre de niveau inférieur."
            except User.DoesNotExist:
                message_don = "❌ Pseudo introuvable."
    else:
        form = DonPointsForm()
    return render(request, 'information/mes_points.html', {
        'points': profil.points,
        'niveau': profil.niveau,
        'prochain_palier': prochain_palier,
        'form': form,
        'message_don': message_don,
    })

# 🔘 Choix type réservation
@login_required
def reservation_choix(request):
    return render(request, 'information/reservation_choix.html')

# 🎫 Réservation événement
@login_required
def reservation_evenement(request):
    profil = ProfilUtilisateur.objects.get(user=request.user)
    evenements = Evenement.objects.all()
    message = ""

    if request.method == 'POST':
        event_id = request.POST.get("event_id")
        event = get_object_or_404(Evenement, id=event_id)

        if request.user in event.participants.all():
            message = "❌ Vous êtes déjà inscrit à cet événement."
        else:
            event.participants.add(request.user)
            profil.points += 10
            mettre_a_jour_niveau(profil)
            profil.save()
            message = "✅ Réservation confirmée !"

    return render(request, 'information/reservation_evenement.html', {
        'evenements': evenements,
        'message': message,
    })

# 🗓️ Planning des salles
@login_required
def reservation_salle(request):
    profil = ProfilUtilisateur.objects.get(user=request.user)

    niveaux_autorises = {
        'debutant': ['Salle Normale 1'],
        'intermediaire': ['Salle Normale 1'],
        'avance': ['Salle Normale 1', 'Salle Avancée 1'],
        'expert': ['Salle Normale 1', 'Salle Avancée 1', 'Salle Premium 1'],
    }

    noms_autorises = niveaux_autorises.get(profil.niveau, [])
    salles_disponibles = Salle.objects.filter(nom__in=noms_autorises)

    today = timezone.now().date()
    jours, dates = [], {}
    jours_fr = {
        'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi', 'Friday': 'Vendredi'
    }

    compteur, i = 0, 0
    while compteur < 5:
        jour = today + timedelta(days=i)
        if jour.weekday() < 5:
            nom_jour = jours_fr[jour.strftime("%A")]
            jours.append(nom_jour)
            dates[nom_jour] = jour
            compteur += 1
        i += 1

    heures = [f"{h:02d}" for h in range(7, 24)]  # Ex: ['07', '08', ..., '23']

    reservations = ReservationSalle.objects.filter(salle__in=salles_disponibles)
    reservations_dict = {}
    for resa in reservations:
        heure_str = resa.heure if isinstance(resa.heure, str) else resa.heure.strftime('%H')
        cle = f"{resa.salle.id}_{resa.date}_{heure_str}"
        reservations_dict[cle] = resa

    return render(request, 'information/reservation_salle.html', {
        'salles_autorisees': salles_disponibles,
        'niveau': profil.niveau,
        'jours': jours,
        'dates': dates,
        'heures': heures,
        'reservations_dict': reservations_dict,
        'user': request.user,
    })

# ✅ Réserver un créneau
@login_required
def reserver_creneau_direct(request, salle_id, date, heure):
    profil = ProfilUtilisateur.objects.get(user=request.user)
    salle = get_object_or_404(Salle, id=salle_id)
    date_obj = parse_date(date)

    if not ReservationSalle.objects.filter(salle=salle, date=date_obj, heure=heure).exists():
        ReservationSalle.objects.create(utilisateur=request.user, salle=salle, date=date_obj, heure=heure)
        profil.points += 1
        mettre_a_jour_niveau(profil)
        profil.save()

    return redirect('reservation_salle')

# ❌ Annuler un créneau
@login_required
def annuler_creneau(request, reservation_id):
    reservation = get_object_or_404(ReservationSalle, id=reservation_id)
    if reservation.utilisateur == request.user:
        reservation.delete()
        messages.success(request, "✅ Réservation annulée.")
    else:
        messages.error(request, "❌ Vous ne pouvez annuler que vos propres réservations.")
    return redirect('reservation_salle')

from django.shortcuts import redirect

@login_required
def reservation_evenement(request):
    profil = ProfilUtilisateur.objects.get(user=request.user)
    evenements = Evenement.objects.all()
    if request.method == 'POST':
        event_id = request.POST.get("event_id")
        event = get_object_or_404(Evenement, id=event_id)
        if request.user not in event.participants.all():
            event.participants.add(request.user)
            profil.points += 10
            mettre_a_jour_niveau(profil)
            profil.save()
        return redirect('confirmation_evenement', event_id=event.id)

    return render(request, 'information/reservation_evenement.html', {
        'evenements': evenements,
    })

@login_required
def confirmation_evenement(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)
    participants = event.participants.all()
    return render(request, 'information/confirmation_evenement.html', {
        'event': event,
        'participants': participants,
    })