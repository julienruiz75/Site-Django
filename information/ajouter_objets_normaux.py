# information/scripts/ajouter_objets_normaux.py

from information.models import ObjetConnecte, Salle
from django.utils import timezone

objets_normaux = [
    ("Éclairage", "capteur", "Éclairage connecté (manuel ou auto) – Paramètres : Luminosité (%) / Mode\nDébutant : Lecture seule | Intermédiaire : 50–80 % (manuel) | Avancé : 20–100 %, auto | Expert : 10–100 %, scénarios"),
    ("Thermostat", "thermostat", "Thermostat standard – Température cible (°C)\nDébutant : lecture seule | Intermédiaire : 21–23°C | Avancé : 19–25°C | Expert : 17–27°C + météo"),
    ("Capteur de présence", "capteur", "Capteur de présence – Paramètres : Sensibilité\nDébutant : lecture seule | Intermédiaire : moyenne | Avancé : faible/moyenne/élevée | Expert : zones + actions"),
    ("Capteur d’ouverture", "capteur", "Capteur d’ouverture de porte – Logs et alertes\nDébutant : état actuel | Intermédiaire : journal 24h | Avancé : 7j + alertes | Expert : logs + badge/caméra"),
    ("Imprimante", "imprimante", "Imprimante standard A4 – Type impression, format, pages\nDébutant : 1 A4 recto | Intermédiaire : recto/verso max 10p | Avancé : A3, 50p | Expert : suivi cartouches + cloud"),
    ("Casier connecté", "distributeur", "Casier connecté Bluetooth – Ouverture et réservation\nDébutant : lecture état | Intermédiaire : badge | Avancé : temp journalier | Expert : attribution avancée"),
    ("Badgeuse", "badgeuse", "Badgeuse simple – Fréquentation et historique\nDébutant : présence auto | Intermédiaire : consultation perso | Avancé : fréquentation jour | Expert : export CSV"),
    ("Table connectée", "table", "Table réglable manuellement – Hauteur (cm)\nDébutant : manuel | Intermédiaire : 100–120 cm | Avancé : 90–125 cm + 1 profil | Expert : 85–130 cm + multi-profils"),
    ("Capteur de bruit", "capteur", "Capteur de bruit basique – Seuil (dB)\nDébutant : lecture seule | Intermédiaire : 75–85 dB | Avancé : 65–85 dB | Expert : 60–90 dB + lumière rouge"),
    ("Prise intelligente", "prise", "Prise connectée – État / conso\nDébutant : lecture seule | Intermédiaire : on/off manuel | Avancé : minuterie | Expert : stats mensuelles"),
    ("Horloge connectée", "autre", "Horloge – Planning synchronisé\nDébutant : lecture | Intermédiaire : planning fixe | Avancé : dynamique selon utilisateur | Expert : synchro Outlook"),
    ("Multiprise USB", "prise", "Multiprise USB – Ports et sécurité\nDébutant : toujours actif | Intermédiaire : on/off manuel | Avancé : horaire | Expert : analyse + verrou auto"),
    ("Station météo", "autre", "Station météo intérieure – Température / humidité\nDébutant : lecture seule | Intermédiaire : historique 24h | Avancé : graphique 7j | Expert : aération auto"),
]

# Ajout pour les 8 salles normales
for i in range(1, 9):
    try:
        salle = Salle.objects.get(nom=f"Salle Normale {i}")
        for nom_base, type_objet, description in objets_normaux:
            ObjetConnecte.objects.create(
                nom=f"{nom_base} - Normale {i}",
                type=type_objet,
                description=f"{description}\nSalle assignée : {salle.nom}",
                salle_associee=salle,
                niveau_requis='debutant',
                statut='actif'
            )
        print(f"Objets ajoutés à {salle.nom}")
    except Salle.DoesNotExist:
        print(f"Salle Normale {i} introuvable.")
