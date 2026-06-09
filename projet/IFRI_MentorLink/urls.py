from django.urls import path
from . import views

urlpatterns = [

    # ── Profil ────────────────────────────────────────────
    path('profil/',           views.get_profil,      name='get_profil'),
    path('profil/modifier/',  views.modifier_profil, name='modifier_profil'),

    # ── Offres ────────────────────────────────────────────
    path('offres/',                        views.liste_offres,   name='liste_offres'),
    path('offres/creer/',                  views.creer_offre,    name='creer_offre'),
    path('offres/<int:offre_id>/',         views.detail_offre,   name='detail_offre'),
    path('offres/<int:offre_id>/modifier/', views.modifier_offre, name='modifier_offre'),
    path('offres/<int:offre_id>/supprimer/', views.supprimer_offre, name='supprimer_offre'),

    # ── Demandes ──────────────────────────────────────────
    path('demandes/',                            views.liste_demandes,   name='liste_demandes'),
    path('demandes/creer/',                      views.creer_demande,    name='creer_demande'),
    path('demandes/<int:demande_id>/',           views.detail_demande,   name='detail_demande'),
    path('demandes/<int:demande_id>/modifier/',  views.modifier_demande, name='modifier_demande'),
    path('demandes/<int:demande_id>/supprimer/', views.supprimer_demande, name='supprimer_demande'),

    # ── Matching ──────────────────────────────────────────
    path('matching/demande/<int:demande_id>/', views.matching_demande, name='matching_demande'),
    path('matching/offre/<int:offre_id>/',     views.matching_offre,   name='matching_offre'),
]
