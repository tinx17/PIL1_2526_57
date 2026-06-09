from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserCreneau
from .matching_algorithm import MatchingBidirectionnel


@receiver(post_save, sender=User)
def on_user_saved(sender, instance, **kwargs):
    """
    Déclenché automatiquement après chaque modification d'un User.
    Recalcule tous les matchings liés à cet utilisateur.
    """
    algo = MatchingBidirectionnel()
    algo.recalculate_matchings_for_user(instance)


@receiver(post_save, sender=UserCreneau)
def on_user_creneau_saved(sender, instance, **kwargs):
    """
    Déclenché automatiquement après chaque modification
    des créneaux d'un User.
    Recalcule tous les matchings liés à cet utilisateur.
    """
    algo = MatchingBidirectionnel()
    algo.recalculate_matchings_for_user(instance.user)
