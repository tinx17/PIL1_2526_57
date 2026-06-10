from django.apps import AppConfig


class IfriMentoratConfig(AppConfig):
    name = 'ifri_mentorat'
    def ready(self):
        import ifri_mentorat.signals  # ← active les signals