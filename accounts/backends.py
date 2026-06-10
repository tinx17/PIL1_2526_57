"""
Backend d'authentification personnalisé.
Permet la connexion par email OU numéro de téléphone.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserProfile = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    """
    Backend d'authentification qui accepte l'email ou le téléphone
    comme identifiant, en plus du nom d'utilisateur standard.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Tente d'authentifier l'utilisateur avec son email, téléphone
        ou nom d'utilisateur.

        Args:
            request: La requête HTTP
            username: L'identifiant (email, téléphone ou username)
            password: Le mot de passe

        Returns:
            L'utilisateur authentifié ou None
        """
        if username is None or password is None:
            return None

        try:
            # Chercher l'utilisateur par email, téléphone ou username
            user = UserProfile.objects.get(
                Q(email=username) |
                Q(telephone=username) |
                Q(username=username)
            )
        except UserProfile.DoesNotExist:
            # Exécuter le hash du mot de passe pour éviter les attaques timing
            UserProfile().set_password(password)
            return None
        except UserProfile.MultipleObjectsReturned:
            # En cas de doublons, prendre le premier résultat par email
            user = UserProfile.objects.filter(
                Q(email=username) |
                Q(telephone=username) |
                Q(username=username)
            ).first()

        # Vérifier le mot de passe et que l'utilisateur est actif
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
