"""
Configuration du routing WebSocket pour l'application messaging.
Définit les URLs WebSocket pour le chat et les notifications.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket pour le chat d'une conversation spécifique
    re_path(
        r'ws/chat/(?P<conversation_id>\d+)/$',
        consumers.ChatConsumer.as_asgi()
    ),

    # WebSocket pour les notifications en temps réel
    re_path(
        r'ws/notifications/$',
        consumers.NotificationConsumer.as_asgi()
    ),
]
