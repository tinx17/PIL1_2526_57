"""
Configuration de l'application messaging.
"""

from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """Configuration de l'application de messagerie."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
    verbose_name = 'Messagerie instantanée'
