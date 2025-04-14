from django.db import models
from django.contrib.auth.models import User

class Evenement(models.Model):
    DOMAINE_CHOICES = [
        ('science', 'Science'),
        ('art', 'Art'),
        ('finance', 'Finance'),
        ('business', 'Business'),
        ('cinema', 'Cinéma'),
        ('maths', 'Maths'),
        ('informatique', 'Informatique'),
        ('ia', 'Intelligence Artificielle'),
    ]

    titre = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    domaine = models.CharField(max_length=30, choices=DOMAINE_CHOICES)
    lieu = models.CharField(max_length=100, blank=True, null=True)
    participants = models.ManyToManyField(User, blank=True, related_name='evenements_participes')

    def __str__(self):
        return f"{self.titre} ({self.get_domaine_display()})"


class ProfilUtilisateur(models.Model):
    NIVEAUX = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]

    SEXES = [
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=20, choices=NIVEAUX, default='debutant')
    points = models.FloatField(default=0.0)

    # Informations personnelles
    prenom = models.CharField(max_length=100, blank=True)
    nom = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXES, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    societe = models.CharField(max_length=100, blank=True)
    poste = models.CharField("Intitulé du poste", max_length=100, blank=True)

    # Visibilité des infos
    show_prenom = models.BooleanField(default=True)
    show_nom = models.BooleanField(default=False)
    show_date_naissance = models.BooleanField(default=True)
    show_sexe = models.BooleanField(default=True)
    show_photo = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Salle(models.Model):
    TYPES = [
        ('normale', 'Salle normale'),
        ('avancee', 'Salle avancée'),
        ('premium', 'Salle premium'),
        ('commune', 'Salle commune'),
    ]
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPES)
    niveau_min = models.CharField(max_length=20, choices=ProfilUtilisateur.NIVEAUX)

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"


class ObjetConnecte(models.Model):
    TYPES_OBJETS = [
        ('capteur', 'Capteur'),
        ('imprimante', 'Imprimante'),
        ('thermostat', 'Thermostat'),
        ('camera', 'Caméra'),
        ('badgeuse', 'Badgeuse'),
        ('distributeur', 'Distributeur'),
        ('table', 'Table connectée'),
        ('projecteur', 'Projecteur'),
        ('micro', 'Micro'),
        ('station', 'Station de recharge'),
        ('hub', 'Hub de contrôle'),
        ('diffuseur', 'Diffuseur d’odeurs'),
        ('led', 'Mur LED'),
        ('tapis', 'Tapis connecté'),
        ('ia', 'IA prédictive'),
        ('vocal', 'Commande vocale'),
        ('autre', 'Autre'),
    ]

    STATUTS = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('maintenance', 'Maintenance'),
    ]

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=TYPES_OBJETS)
    description = models.TextField(blank=True)
    salle_associee = models.ForeignKey(Salle, on_delete=models.CASCADE)
    niveau_requis = models.CharField(max_length=20, choices=ProfilUtilisateur.NIVEAUX, default='debutant')
    statut = models.CharField(max_length=20, choices=STATUTS, default='actif')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"

from django.utils import timezone

class ReservationSalle(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    heure = models.CharField(max_length=5)  # Exemples : "07", "13", etc.


    def __str__(self):
        return f"{self.utilisateur.username} - {self.salle.nom} à {self.heure} le {self.date}"