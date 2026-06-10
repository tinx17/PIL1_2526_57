from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Offre, Demande,
    OffreCreneau, DemandeCreneau,
    UserCreneau, PointFort, Lacune,User,Conversation
)

# Configuration personnalisée de l'affichage de votre table User
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Liste des colonnes qui s'afficheront dans le tableau de l'interface admin
    list_display = ('id', 'email', 'nom', 'prenom', 'filiere', 'niveau')
    
    # Barre de recherche pour retrouver un utilisateur
    search_fields = ('email', 'nom', 'prenom')
    
    # Tri par défaut dans le tableau (par ID)
    ordering = ('id',)

# 🔌 Enregistrement sécurisé par boucle pour toutes les autres tables du projet
modeles = [ Offre, Demande, OffreCreneau, DemandeCreneau, UserCreneau, PointFort, Lacune, Conversation]

for modele in modeles:
    if not admin.site.is_registered(modele):
        admin.site.register(modele)

