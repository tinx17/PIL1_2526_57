from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, UserCreneau
from .matching_bidirectionnel import MatchingBidirectionnel


@receiver(post_save, sender=UserProfile)
def on_user_saved(sender, instance, created, **kwargs):
    """
    Déclenché automatiquement après chaque sauvegarde d'un UserProfile.
    - created=True  : inscription → pas de recalcul (pas encore d'offres/demandes)
    - created=False : mise à jour → recalcul de tous les matchings liés
    """
    if not created:
        algo = MatchingBidirectionnel()
        algo.recalculate_matchings_for_user(instance)


@receiver(post_save, sender=UserCreneau)
def on_user_creneau_saved(sender, instance, **kwargs):
    """
    Déclenché automatiquement après chaque modification
    des créneaux horaires d'un UserProfile.
    Recalcule tous les matchings liés à cet utilisateur.
    """
    algo = MatchingBidirectionnel()
    algo.recalculate_matchings_for_user(instance.user)
