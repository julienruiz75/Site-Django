from information.models import Salle, ObjetConnecte
from django.db import transaction

@transaction.atomic
def run():
    objets_normaux = [
        ("Éclairage", "capteur", "debutant"),
        ("Thermostat", "thermostat", "debutant"),
        ("Capteur de présence", "capteur", "debutant"),
        ("Imprimante", "imprimante", "debutant"),
        ("Casier connecté", "distributeur", "debutant"),
        ("Table connectée", "table", "debutant"),
        ("Badgeuse", "badgeuse", "debutant"),
        ("Capteur de bruit", "capteur", "debutant"),
    ]

    objets_avances = [
        ("Smart Projecteur HD", "projecteur", "avance"),
        ("Micro directionnel", "micro", "avance"),
        ("Caméra visioconférence", "camera", "avance"),
        ("Assistant vocal", "vocal", "avance"),
        ("Détecteur de CO₂", "capteur", "avance"),
    ]

    objets_premium = [
        ("Diffuseur d’odeurs", "diffuseur", "expert"),
        ("Table tactile collaborative", "table", "expert"),
        ("Capteur de stress biométrique", "capteur", "expert"),
        ("IA prédictive de salle", "ia", "expert"),
        ("Mur LED dynamique", "led", "expert"),
    ]

    print("🛠 Création des salles normales...")
    for i in range(1, 9):
        salle = Salle.objects.create(
            nom=f"Salle Normale {i}",
            type="normale",
            niveau_min="debutant"
        )
        for nom, type_objet, niveau in objets_normaux:
            ObjetConnecte.objects.create(
                nom=f"{nom} - Normale {i}",
                type=type_objet,
                description=f"{nom} installé dans {salle.nom}",
                salle_associee=salle,
                niveau_requis=niveau,
                statut="actif"
            )

    print("🛠 Création des salles avancées...")
    for i in range(1, 6):
        salle = Salle.objects.create(
            nom=f"Salle Avancée {i}",
            type="avancee",
            niveau_min="avance"
        )
        for nom, type_objet, niveau in objets_normaux + objets_avances:
            ObjetConnecte.objects.create(
                nom=f"{nom} - Avancée {i}",
                type=type_objet,
                description=f"{nom} installé dans {salle.nom}",
                salle_associee=salle,
                niveau_requis=niveau,
                statut="actif"
            )

    print("🛠 Création des salles premium...")
    for i in range(1, 4):
        salle = Salle.objects.create(
            nom=f"Salle Premium {i}",
            type="premium",
            niveau_min="expert"
        )
        for nom, type_objet, niveau in objets_normaux + objets_avances + objets_premium:
            ObjetConnecte.objects.create(
                nom=f"{nom} - Premium {i}",
                type=type_objet,
                description=f"{nom} installé dans {salle.nom}",
                salle_associee=salle,
                niveau_requis=niveau,
                statut="actif"
            )

    print("Toutes les salles et objets ont été créés avec succès !")
