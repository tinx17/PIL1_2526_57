from django.contrib import admin
from .models import UserProfile, Competence, Lacune, Offre, Demande, Conversation, Message

# Enregistrement des modèles pour l'interface graphique
admin.site.register(UserProfile)
admin.site.register(Competence)
admin.site.register(Lacune)
admin.site.register(Offre)
admin.site.register(Demande)
admin.site.register(Conversation)
admin.site.register(Message)

# Register your models here.
