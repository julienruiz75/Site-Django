from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recherche/', views.recherche, name='recherche'),
    path('inscription/', views.inscription, name='inscription'),
    path('decouvrir/', views.decouvrir, name='decouvrir'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='logout'),  # 👈 on garde cette ligne et on lui donne le nom 'logout'
    path('profil/', views.profil, name='profil'),
    path('membres/', views.membres, name='membres'),
    path("admin-niveaux/", views.gestion_niveaux, name="gestion_niveaux"),
    
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.auth import views as auth_views

urlpatterns += [
    path("mot-de-passe-oublie/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("mot-de-passe-oublie/envoye/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reinitialiser/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("mot-de-passe-complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]


