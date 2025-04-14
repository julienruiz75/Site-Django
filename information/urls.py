from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('decouvrir/', views.decouvrir, name='decouvrir'),
    path('recherche/', views.recherche, name='recherche'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='logout'),

    # Authentification : réinitialisation de mot de passe
    path("mot-de-passe-oublie/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("mot-de-passe-oublie/envoye/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reinitialiser/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("mot-de-passe-complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # Pages connectées
    path('profil/', views.profil, name='profil'),
    path('membres/', views.membres, name='membres'),

    # Administration
    path("admin-niveaux/", views.gestion_niveaux, name="gestion_niveaux"),

    # Objets connectés
    path('objets/', views.liste_objets_connectes, name='liste_objets'),
    path('changer-statut-objet/<int:objet_id>/', views.changer_statut_objet, name='changer_statut_objet'),
    path('objets/', views.liste_objets_connectes, name='liste_objets_connectes'),

    # Points utilisateur
    path('mes-points/', views.mes_points, name='mes_points'),

    # Réservations
    path('reservation/', views.reservation_choix, name='reservation_choix'),
    path('reservation/salles/', views.reservation_salle, name='reservation_salle'),
    path('reservation/evenements/', views.reservation_evenement, name='reservation_evenement'),
    path('reserver/<int:salle_id>/<str:date>/<str:heure>/', views.reserver_creneau_direct, name='reserver_creneau_direct'),
    path('annuler/<int:reservation_id>/', views.annuler_creneau, name='annuler_creneau'),

    # ✅ Confirmation d'inscription à un événement (NOUVEAU)
    path('reservation/confirmation/<int:event_id>/', views.confirmation_evenement, name='confirmation_evenement'),
]

# 📂 Pour les fichiers médias (ex: photos de profil)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
