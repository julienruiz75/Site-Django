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
    
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)