"""
Configuration de l'administration Django pour l'application matching.
"""

from django.contrib import admin
from .models import OffreMentorat, Matching


@admin.register(OffreMentorat)
class OffreMentoratAdmin(admin.ModelAdmin):
    """Administration des offres de mentorat."""
    list_display = ('auteur', 'type', 'format', 'statut', 'date_creation')
    list_filter = ('type', 'statut', 'format')
    search_fields = ('auteur__nom', 'auteur__prenom', 'matieres__nom')
    ordering = ('-date_creation',)
    filter_horizontal = ('matieres',)


@admin.register(Matching)
class MatchingAdmin(admin.ModelAdmin):
    """Administration des matchings."""
    list_display = ('mentor', 'mentore', 'score_compatibilite', 'date_creation')
    list_filter = ('score_compatibilite',)
    search_fields = ('mentor__nom', 'mentore__nom')
    ordering = ('-score_compatibilite',)
    filter_horizontal = ('matieres_communes',)
