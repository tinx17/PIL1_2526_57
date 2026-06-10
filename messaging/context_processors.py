"""
Processeur de contexte pour la messagerie.
Ajoute le compteur de messages non lus à tous les templates.
"""

from .models import Message


def unread_messages_count(request):
    """
    Ajoute le nombre total de messages non lus au contexte
    de chaque template. Utilisé pour le badge de notification
    dans la navbar.
    """
    if request.user.is_authenticated:
        count = Message.objects.filter(
            conversation__participants=request.user,
            lu=False
        ).exclude(auteur=request.user).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
