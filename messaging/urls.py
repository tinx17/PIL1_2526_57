"""
Configuration des URLs de l'application messaging.
"""

from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_view, name='conversation'),
    path('start/<int:user_id>/', views.demarrer_conversation_view, name='start'),

    # API JSON Endpoints
    path('api/conversations/', views.api_conversations_view, name='api_conversations'),
    path('api/conversations/<int:conversation_id>/messages/', views.api_messages_view, name='api_messages'),
    path('api/conversations/start/<int:user_id>/', views.api_demarrer_conversation_ajax_view, name='api_start_conversation_ajax'),
]
