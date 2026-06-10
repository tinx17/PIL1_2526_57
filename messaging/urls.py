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
]
