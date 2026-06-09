from django.apps import AppConfig


class IfriMentorlinkConfig(AppConfig):
    name = 'IFRI_MentorLink'
def ready(self):
        import IFRI_MentorLink.signals  # ← charge les signaux au démarrage