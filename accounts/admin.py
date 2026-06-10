"""
Configuration de l'administration Django pour l'application accounts.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Matiere


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    """Administration du modèle Matière."""
    list_display = ('id', 'nom')
    search_fields = ('nom',)
    ordering = ('nom',)


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    """Administration du modèle UserProfile."""
    list_display = ('email', 'nom', 'prenom', 'filiere', 'niveau', 'date_inscription')
    list_filter = ('filiere', 'niveau', 'is_active')
    search_fields = ('email', 'nom', 'prenom', 'telephone')
    ordering = ('-date_inscription',)

    # Champs affichés dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations IFRI', {
            'fields': (
                'nom', 'prenom', 'telephone', 'photo_profil',
                'filiere', 'niveau', 'competences', 'lacunes',
                'disponibilites', 'bio'
            )
        }),
    )

    # Champs affichés lors de la création
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations IFRI', {
            'fields': (
                'nom', 'prenom', 'email', 'telephone',
                'filiere', 'niveau'
            )
        }),
    )
