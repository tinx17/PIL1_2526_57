"""
Configuration ASGI pour le projet IFRI_MentorLink.
Intègre Django Channels pour le support WebSocket
(messagerie en temps réel).
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorlink.settings')

# Initialiser l'application Django d'abord
django_asgi_app = get_asgi_application()

# Importer le routing WebSocket après l'initialisation de Django
from messaging.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # Requêtes HTTP classiques
    'http': django_asgi_app,

    # Connexions WebSocket avec authentification
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
