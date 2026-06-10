"""
Configuration de l'application matching.
"""

from django.apps import AppConfig


class MatchingConfig(AppConfig):
    """Configuration de l'application de mise en correspondance."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matching'
    verbose_name = 'Mise en correspondance'
