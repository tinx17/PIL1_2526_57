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

    # API endpoints
    path('api/login/', views.api_login_view, name='api_login'),
    path('api/register/', views.api_register_view, name='api_register'),
    path('api/logout/', views.api_logout_view, name='api_logout'),
    path('api/user/', views.api_user_view, name='api_user'),
    path('api/user/update/', views.api_update_profile_view, name='api_user_update'),
    path('api/matieres/', views.api_matieres_view, name='api_matieres'),
    path('api/reset-password/', views.api_reset_password_view, name='api_reset_password'),
]
