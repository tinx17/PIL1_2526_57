from django.contrib import admin
from .models import UserProfile, PointFort, Lacune, Offre, UserCreneau,Demande, CreneauDemande, CreneauOffre, Conversation, Message

# Enregistrement des modèles pour l'interface graphique
admin.site.register(UserProfile)
admin.site.register(PointFort)
admin.site.register(Lacune)
admin.site.register(Offre)
admin.site.register(Demande)
admin.site.register(UserCreneau)
admin.site.register(CreneauOffre)
admin.site.register(CreneauDemande)
admin.site.register(Conversation)
admin.site.register(Message)

# Register your models here.
