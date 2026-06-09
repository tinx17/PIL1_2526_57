"""
URL configuration for app_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ifri_mentorat import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentification
    path('api/inscription/',       views.api_inscription,      name='api_inscription'),
    path('api/login/',             views.api_login,            name='api_login'),
    path('api/update-password/',   views.api_update_password,  name='api_update_password'),

    # Mise à jour du Profil
    path('api/profil/update/',     views.api_update_profil,    name='api_update_profil'),

    # Création d'Offres
    path('api/offres/creer/',      views.api_creer_offre,      name='api_creer_offre'),

    # Créatio de Demandes
    path('api/demandes/creer/',    views.api_creer_demande,    name='api_creer_demande'),

    # Messagerie
    #Création d'une conversation
    path('api/conversations/creer/',                             views.api_creer_conversation,    name='api_creer_conversation'),
    #Affichage de la liste des conversations
    path('api/conversations/liste/',                             views.api_liste_conversations,   name='api_liste_conversations'),
    #Affichage des messages propres à une conversation
    path('api/conversations/<int:conversation_id>/messages/',    views.api_messages_conversation, name='api_messages_conversation'),
    #Envoie d'un message
    path('api/conversations/<int:conversation_id>/envoyer/',     views.api_envoyer_message,       name='api_envoyer_message'),
]