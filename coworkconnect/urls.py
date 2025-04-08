from django.contrib import admin
from django.urls import path, include

# ✅ Ajout pour servir les fichiers médias
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("information.urls")),
]

# ✅ Permet d’accéder aux fichiers médias (comme les photos) en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

