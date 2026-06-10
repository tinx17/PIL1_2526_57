"""
Configuration des URLs de l'application accounts.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Inscription
    path('register/', views.inscription_view, name='register'),

    # Connexion et déconnexion
    path('login/', views.connexion_view, name='login'),
    path('logout/', views.deconnexion_view, name='logout'),

    # Profil
    path('profile/<int:user_id>/', views.profil_view, name='profil'),
    path('edit-profile/', views.editer_profil_view, name='edit_profil'),

    # Réinitialisation du mot de passe
    path('reset-password/', views.reinitialiser_mdp_view, name='reset_password'),
]
