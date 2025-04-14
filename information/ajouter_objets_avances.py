from django.utils import timezone
from information.models import Salle, ObjetConnecte

objets_normaux = [
    {
        "nom": "Éclairage",
        "type": "capteur",
        "description": "Éclairage connecté évolué – Paramètres : Luminosité (%) / Mode / Teinte\n"
                       "Débutant : Lecture seule | Intermédiaire : 50–80 %, mode manuel | "
                       "Avancé : 20–100 %, teinte froide/neutre | Expert : 10–100 %, scénarios prédéfinis",
    },
    {
        "nom": "Thermostat",
        "type": "thermostat",
        "description": "Thermostat multizone – Température cible (°C) / Par zone\n"
                       "Débutant : Lecture seule | Intermédiaire : 21–23 °C | "
                       "Avancé : Zones multiples 19–25 °C | Expert : Programmation avancée 17–27 °C",
    },
    {
        "nom": "Capteur de présence",
        "type": "capteur",
        "description": "Capteur de présence – Sensibilité / Zone ciblée\n"
                       "Débutant : Lecture seule | Intermédiaire : Sensibilité moyenne | "
                       "Avancé : Faible / Moyenne / Élevée | Expert : Détection ciblée + déclenchement éclairage",
    },
    {
        "nom": "Imprimante",
        "type": "imprimante",
        "description": "Imprimante connectée (A3+) – Format / Qualité / Nombre pages\n"
                       "Débutant : A4 recto | Intermédiaire : A4 recto/verso, 10 pages | "
                       "Avancé : A4/A3, 50 pages | Expert : HD, files d’attente, diagnostics",
    },
    {
        "nom": "Casier connecté",
        "type": "distributeur",
        "description": "Casier Bluetooth évolué – Ouverture / Attribution / Horaire\n"
                       "Débutant : Lecture seule | Intermédiaire : Ouverture badge | "
                       "Avancé : Attribution journée | Expert : Attribution horaire, badge invité",
    },
]

objets_specifiques = [
    {
        "nom": "Smart Projecteur HD",
        "type": "projecteur",
        "description": "Smart Projecteur HD – Source / Résolution / Programmation\n"
                       "Débutant : Lecture seule | Intermédiaire : Allumer/éteindre | "
                       "Avancé : HDMI / 1080p | Expert : 4K + auto badge",
    },
    {
        "nom": "Micro directionnel",
        "type": "micro",
        "description": "Micro directionnel – Sensibilité / Zone\n"
                       "Débutant : Lecture | Intermédiaire : Activation simple | "
                       "Avancé : Sensibilité moyenne/forte | Expert : Mode auto",
    },
    {
        "nom": "Caméra visioconférence",
        "type": "camera",
        "description": "Caméra visioconférence – Angle / Zoom / Enregistrement\n"
                       "Débutant : Non autorisé | Intermédiaire : Visio simple | "
                       "Avancé : Zoom + angle | Expert : Streaming, enregistrement",
    },
    {
        "nom": "Assistant vocal",
        "type": "ia",
        "description": "Assistant vocal – Format / Partage\n"
                       "Débutant : Non autorisé | Intermédiaire : Transcription | "
                       "Avancé : Export PDF | Expert : Cloud auto",
    },
    {
        "nom": "Hub mural de contrôle",
        "type": "hub",
        "description": "Hub mural – Température / Lumière / Projecteur\n"
                       "Débutant : Lecture statique | Intermédiaire : Modifier lumière/température | "
                       "Avancé : Visio/projecteur | Expert : Scénarios salle",
    },
]

# Récupère les salles avancées (9 à 13)
salles_avancees = Salle.objects.filter(type="avancee").order_by("id")

for index, salle in enumerate(salles_avancees):
    numero = index + 9
    for obj in objets_normaux:
        ObjetConnecte.objects.create(
            nom=f"{obj['nom']} - Avancée {numero}",
            type=obj['type'],
            description=obj['description'],
            salle_associee=salle,
            niveau_requis="debutant",
            statut="actif",
            date_ajout=timezone.now(),
        )
    for obj in objets_specifiques:
        ObjetConnecte.objects.create(
            nom=f"{obj['nom']} - Avancée {numero}",
            type=obj['type'],
            description=obj['description'],
            salle_associee=salle,
            niveau_requis="avance",
            statut="actif",
            date_ajout=timezone.now(),
        )

print("✅ Objets des salles avancées ajoutés avec succès.")
