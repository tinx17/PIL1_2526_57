"""
Configuration des URLs principales du projet IFRI_MentorLink.
Regroupe les URLs de toutes les applications.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def accueil(request):
    """Redirige la page d'accueil vers le dashboard ou la page de connexion."""
    if request.user.is_authenticated:
        return redirect('matching:dashboard')
    return redirect('accounts:login')


urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),

    # Page d'accueil — redirige selon l'état de connexion
    path('', accueil, name='accueil'),

    # Applications
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('matching/', include('matching.urls', namespace='matching')),
    path('messaging/', include('messaging.urls', namespace='messaging')),
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
