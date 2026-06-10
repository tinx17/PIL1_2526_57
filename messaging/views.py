"""
Vues de l'application messaging.
Gère la boîte de réception et l'affichage des conversations.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.contrib.auth import get_user_model
from .models import Conversation, Message

UserProfile = get_user_model()


@login_required
def inbox_view(request):
    """
    Boîte de réception : liste toutes les conversations
    de l'utilisateur connecté avec le dernier message.
    """
    user = request.user

    # Récupérer toutes les conversations de l'utilisateur
    conversations = Conversation.objects.filter(
        participants=user
    ).prefetch_related('participants', 'messages').order_by('-date_creation')

    # Préparer les données pour chaque conversation
    conversations_data = []
    for conv in conversations:
        dernier_msg = conv.dernier_message
        non_lus = conv.messages_non_lus(user)
        autre = conv.autre_participant(user)

        conversations_data.append({
            'conversation': conv,
            'autre_participant': autre,
            'dernier_message': dernier_msg,
            'non_lus': non_lus,
        })

    # Trier par date du dernier message (plus récent en premier)
    conversations_data.sort(
        key=lambda x: x['dernier_message'].date_envoi if x['dernier_message'] else x['conversation'].date_creation,
        reverse=True
    )

    context = {
        'conversations': conversations_data,
    }
    return render(request, 'messaging/inbox.html', context)


@login_required
def conversation_view(request, conversation_id):
    """
    Affiche une conversation avec l'historique des messages
    et l'interface de chat en temps réel.
    """
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    # Vérifier que l'utilisateur est participant
    if not conversation.participants.filter(pk=request.user.pk).exists():
        django_messages.error(request, 'Vous n\'avez pas accès à cette conversation.')
        return redirect('messaging:inbox')

    # Marquer les messages non lus comme lus
    Message.objects.filter(
        conversation=conversation,
        lu=False
    ).exclude(
        auteur=request.user
    ).update(lu=True)

    # Récupérer tous les messages
    messages_list = conversation.messages.select_related('auteur').all()

    # Récupérer l'autre participant
    autre_participant = conversation.autre_participant(request.user)

    context = {
        'conversation': conversation,
        'messages_list': messages_list,
        'autre_participant': autre_participant,
        'user_id': request.user.pk,
    }
    return render(request, 'messaging/conversation.html', context)


@login_required
def demarrer_conversation_view(request, user_id):
    """
    Démarre une nouvelle conversation avec un utilisateur
    ou redirige vers une conversation existante.
    """
    autre = get_object_or_404(UserProfile, pk=user_id)

    if autre == request.user:
        django_messages.warning(request, 'Vous ne pouvez pas démarrer une conversation avec vous-même.')
        return redirect('messaging:inbox')

    # Chercher une conversation existante
    conversations = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=autre
    )

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, autre)

    return redirect('messaging:conversation', conversation_id=conversation.pk)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def api_conversations_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'ok': False, 'message': 'Non authentifié.'}, status=401)
        
    user = request.user
    # Récupérer toutes les conversations de l'utilisateur
    conversations = Conversation.objects.filter(
        participants=user
    ).prefetch_related('participants', 'messages').order_by('-date_creation')
    
    conversations_data = []
    for conv in conversations:
        dernier_msg = conv.dernier_message
        non_lus = conv.messages_non_lus(user)
        autre = conv.autre_participant(user)
        
        conversations_data.append({
            'id': conv.pk,
            'autre_participant': {
                'id': autre.pk,
                'nom': autre.nom,
                'prenom': autre.prenom,
                'email': autre.email,
                'telephone': autre.telephone,
            },
            'dernier_message': {
                'contenu': dernier_msg.contenu if dernier_msg else None,
                'auteur_id': dernier_msg.auteur.pk if dernier_msg else None,
                'date': dernier_msg.date_envoi.strftime('%d/%m %H:%M') if dernier_msg else None,
            } if dernier_msg else None,
            'non_lus': non_lus,
        })
        
    # Trier par date du dernier message (plus récent en premier)
    conversations_data.sort(
        key=lambda x: x['dernier_message']['date'] if x['dernier_message'] else '',
        reverse=True
    )
    
    return JsonResponse({'ok': True, 'conversations': conversations_data})

def api_messages_view(request, conversation_id):
    if not request.user.is_authenticated:
        return JsonResponse({'ok': False, 'message': 'Non authentifié.'}, status=401)
        
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    
    # Vérifier que l'utilisateur est participant
    if not conversation.participants.filter(pk=request.user.pk).exists():
        return JsonResponse({'ok': False, 'message': 'Accès non autorisé.'}, status=403)
        
    # Marquer les messages comme lus
    Message.objects.filter(
        conversation=conversation,
        lu=False
    ).exclude(
        auteur=request.user
    ).update(lu=True)
    
    messages_list = conversation.messages.select_related('auteur').all()
    
    messages_data = []
    for msg in messages_list:
        messages_data.append({
            'id': msg.pk,
            'auteur': msg.auteur.get_full_name(),
            'auteur_id': msg.auteur.pk,
            'contenu': msg.contenu,
            'date': msg.date_envoi.strftime('%d/%m/%Y %H:%M'),
            'lu': msg.lu,
        })
        
    autre_participant = conversation.autre_participant(request.user)
    
    return JsonResponse({
        'ok': True,
        'messages': messages_data,
        'autre_participant': {
            'id': autre_participant.pk,
            'nom': autre_participant.nom,
            'prenom': autre_participant.prenom,
        },
        'user_id': request.user.pk,
    })

@csrf_exempt
def api_demarrer_conversation_ajax_view(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'ok': False, 'message': 'Non authentifié.'}, status=401)
        
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'message': 'Méthode non autorisée.'}, status=405)
        
    autre = get_object_or_404(UserProfile, pk=user_id)
    if autre == request.user:
        return JsonResponse({'ok': False, 'message': 'Vous ne pouvez pas démarrer une conversation avec vous-même.'}, status=400)
        
    conversations = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=autre
    )
    
    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, autre)
        
    return JsonResponse({'ok': True, 'conversation_id': conversation.pk})
