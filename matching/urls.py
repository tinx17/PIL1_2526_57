"""
Configuration des URLs de l'application matching.
"""

from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    # Tableau de bord
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Création d'offres et demandes
    path('create-offer/', views.creer_offre_view, name='create_offer'),
    path('create-request/', views.creer_demande_view, name='create_request'),

    # Recherche
    path('search/', views.recherche_view, name='search'),
    path('results/', views.resultats_view, name='results'),

    # Actions
    path('contact/<int:user_id>/', views.contacter_view, name='contact'),
    path('close/<int:offre_id>/', views.fermer_offre_view, name='close_offer'),
]
