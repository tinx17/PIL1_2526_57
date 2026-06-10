"""
Configuration de l'administration Django pour l'application messaging.
"""

from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation')
    filter_horizontal = ('participants',)
    ordering = ('-date_creation',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'conversation', 'contenu_court', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('contenu', 'auteur__nom')
    ordering = ('-date_envoi',)

    def contenu_court(self, obj):
        return obj.contenu[:50] + '...' if len(obj.contenu) > 50 else obj.contenu
    contenu_court.short_description = 'Contenu'
