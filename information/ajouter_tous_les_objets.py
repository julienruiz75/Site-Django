from information.models import ObjetConnecte, Salle
from django.utils import timezone

def get_salle(nom, type_salle, niveau_min):
    return Salle.objects.get_or_create(
        nom=nom,
        defaults={'type': type_salle, 'niveau_min': niveau_min}
    )[0]

def creer_objets_pour_salles(liste_salles, objets, niveau_defaut):
    for salle in liste_salles:
        for objet in objets:
            ObjetConnecte.objects.create(
                nom=f"{objet['nom']} - {salle.nom}",
                type=objet["type"],
                description=objet["description"] + f"\nSalle assignée : {salle.nom}",
                salle_associee=salle,
                niveau_requis=niveau_defaut,
                statut='actif'
            )

# Objets par salle
objets_normaux = [
    {"nom": "Éclairage", "type": "capteur", "description": "Éclairage connecté (manuel ou auto)..."},
    {"nom": "Thermostat", "type": "thermostat", "description": "Thermostat standard..."},
    {"nom": "Capteur de présence", "type": "capteur", "description": "Capteur de présence..."},
    {"nom": "Capteur d’ouverture", "type": "capteur", "description": "Capteur d’ouverture..."},
    {"nom": "Imprimante", "type": "imprimante", "description": "Imprimante A4..."},
    {"nom": "Casier connecté", "type": "distributeur", "description": "Casier Bluetooth..."},
    {"nom": "Badgeuse", "type": "badgeuse", "description": "Badgeuse simple..."},
    {"nom": "Table connectée", "type": "table", "description": "Table réglable..."},
    {"nom": "Capteur de bruit", "type": "capteur", "description": "Capteur de bruit..."},
    {"nom": "Prise intelligente", "type": "prise", "description": "Prise intelligente..."},
    {"nom": "Horloge connectée", "type": "autre", "description": "Horloge..."},
    {"nom": "Multiprise USB", "type": "prise", "description": "Multiprise USB..."},
    {"nom": "Station météo", "type": "autre", "description": "Station météo..."},
]

nouveaux_avances = [
    {"nom": "Smart Projecteur HD", "type": "projecteur", "description": "Smart projecteur..."},
    {"nom": "Micro directionnel", "type": "micro", "description": "Micro de table..."},
]

nouveaux_premium = [
    {"nom": "Diffuseur d’odeurs", "type": "diffuseur", "description": "Diffuseur..."},
    {"nom": "Mur LED", "type": "led", "description": "Mur LED dynamique..."},
]

# Création des salles
salles_normales = [get_salle(f"Salle Normale {i}", "normale", "debutant") for i in range(1, 9)]
salles_avancees = [get_salle(f"Salle Avancée {i}", "avancee", "avance") for i in range(9, 13)]
salles_premium = [get_salle(f"Salle Premium {i}", "premium", "expert") for i in range(13, 16)]

# Ajout des objets
creer_objets_pour_salles(salles_normales, objets_normaux, "debutant")
creer_objets_pour_salles(salles_avancees, objets_normaux, "debutant")
creer_objets_pour_salles(salles_avancees, nouveaux_avances, "avance")
creer_objets_pour_salles(salles_premium, objets_normaux, "debutant")
creer_objets_pour_salles(salles_premium, nouveaux_avances, "avance")
creer_objets_pour_salles(salles_premium, nouveaux_premium, "expert")

print("✅ Objets créés avec succès dans les 15 salles.")
