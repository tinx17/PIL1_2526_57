"""
Consumer WebSocket pour la messagerie en temps réel.
Gère les connexions WebSocket, l'envoi et la réception
de messages via Django Channels.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket pour le chat en temps réel.
    
    Protocole :
    - Connexion : ws://domain/ws/chat/<conversation_id>/
    - Envoi : {"message": "contenu du message"}
    - Réception : {"type": "chat_message", "message": "...", "auteur": "...", "auteur_id": ..., "date": "..."}
    """

    async def connect(self):
        """
        Gère la connexion WebSocket.
        Vérifie que l'utilisateur est authentifié et participant
        à la conversation.
        """
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']

        # Vérifier que l'utilisateur est authentifié
        if self.user.is_anonymous:
            await self.close()
            return

        # Vérifier que l'utilisateur est participant à la conversation
        est_participant = await self.verifier_participant()
        if not est_participant:
            await self.close()
            return

        # Rejoindre le groupe de la conversation
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Gère la déconnexion WebSocket."""
        # Quitter le groupe de la conversation
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Reçoit un message du client WebSocket.
        Sauvegarde le message en BDD et le diffuse au groupe.
        """
        try:
            text_data_json = json.loads(text_data)
            message_contenu = text_data_json.get('message', '').strip()
        except json.JSONDecodeError:
            return

        if not message_contenu:
            return

        # Sauvegarder le message en base de données
        message = await self.sauvegarder_message(message_contenu)

        if message:
            # Diffuser le message à tous les participants du groupe
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_contenu,
                    'auteur': self.user.get_full_name(),
                    'auteur_id': self.user.pk,
                    'date': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'message_id': message.pk,
                }
            )

    async def chat_message(self, event):
        """
        Reçoit un message du groupe et l'envoie au client WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'auteur': event['auteur'],
            'auteur_id': event['auteur_id'],
            'date': event['date'],
            'message_id': event['message_id'],
        }))

    @database_sync_to_async
    def verifier_participant(self):
        """Vérifie que l'utilisateur est participant à la conversation."""
        from messaging.models import Conversation
        try:
            conversation = Conversation.objects.get(pk=self.conversation_id)
            return conversation.participants.filter(pk=self.user.pk).exists()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def sauvegarder_message(self, contenu):
        """
        Sauvegarde un message dans la base de données.
        
        Args:
            contenu: Le texte du message
            
        Returns:
            L'objet Message créé ou None en cas d'erreur
        """
        from messaging.models import Conversation, Message
        try:
            conversation = Conversation.objects.get(pk=self.conversation_id)
            message = Message.objects.create(
                conversation=conversation,
                auteur=self.user,
                contenu=contenu
            )
            return message
        except Conversation.DoesNotExist:
            return None


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket pour les notifications en temps réel.
    Envoie des notifications de nouveaux messages à l'utilisateur.
    
    Connexion : ws://domain/ws/notifications/
    """

    async def connect(self):
        """Connexion au canal de notifications de l'utilisateur."""
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        self.notification_group = f'notifications_{self.user.pk}'

        await self.channel_layer.group_add(
            self.notification_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Déconnexion du canal de notifications."""
        if hasattr(self, 'notification_group'):
            await self.channel_layer.group_discard(
                self.notification_group,
                self.channel_name
            )

    async def nouvelle_notification(self, event):
        """Envoie une notification au client."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event.get('message', ''),
            'conversation_id': event.get('conversation_id', ''),
            'auteur': event.get('auteur', ''),
            'count': event.get('count', 0),
        }))
