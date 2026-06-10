"""
Modèles de l'application messaging.
Définit les conversations et les messages.
"""

from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """
    Représente une conversation entre deux ou plusieurs utilisateurs.
    Créée automatiquement lors d'un match ou d'une réponse à une offre.
    """

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name='Participants'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-date_creation']

    def __str__(self):
        noms = ', '.join([p.get_full_name() for p in self.participants.all()[:3]])
        return f"Conversation: {noms}"

    @property
    def dernier_message(self):
        """Retourne le dernier message de la conversation."""
        return self.messages.order_by('-date_envoi').first()

    def messages_non_lus(self, utilisateur):
        """Retourne le nombre de messages non lus pour un utilisateur donné."""
        return self.messages.filter(lu=False).exclude(auteur=utilisateur).count()

    def autre_participant(self, utilisateur):
        """Retourne l'autre participant de la conversation (pour les conversations à 2)."""
        return self.participants.exclude(pk=utilisateur.pk).first()


class Message(models.Model):
    """
    Représente un message dans une conversation.
    Stocké en base de données pour conserver l'historique.
    """

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversation'
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_envoyes',
        verbose_name='Auteur'
    )
    contenu = models.TextField(
        verbose_name='Contenu du message'
    )
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date d\'envoi'
    )
    lu = models.BooleanField(
        default=False,
        verbose_name='Lu'
    )

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['date_envoi']

    def __str__(self):
        contenu_court = self.contenu[:50] + '...' if len(self.contenu) > 50 else self.contenu
        return f"{self.auteur.get_short_name()}: {contenu_court}"
