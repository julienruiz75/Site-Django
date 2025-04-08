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

    def __str__(self):
        return f"{self.titre} ({self.domaine})"


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

    # Champs personnels
    prenom = models.CharField(max_length=100, blank=True)
    nom = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXES, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    societe = models.CharField(max_length=100, blank=True)  # 🏢 Société
    poste = models.CharField("Intitulé du poste", max_length=100, blank=True)  # 💼 Poste

    # Visibilité des données personnelles
    show_prenom = models.BooleanField(default=True)
    show_nom = models.BooleanField(default=False)
    show_date_naissance = models.BooleanField(default=True)
    show_sexe = models.BooleanField(default=True)
    show_photo = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username