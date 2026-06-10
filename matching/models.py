"""
Modèles de l'application matching.
Définit les offres de mentorat et les résultats de matching.
"""

from django.db import models
from django.conf import settings
from accounts.models import Matiere


class OffreMentorat(models.Model):
    """
    Représente une offre ou une demande de mentorat.
    Un utilisateur peut publier une offre (je peux aider)
    ou une demande (j'ai besoin d'aide).
    """

    TYPE_CHOICES = [
        ('offre', 'Offre de mentorat'),
        ('demande', 'Demande de mentorat'),
    ]

    FORMAT_CHOICES = [
        ('presentiel', 'En présentiel'),
        ('en_ligne', 'En ligne'),
        ('les_deux', 'Présentiel et en ligne'),
    ]

    STATUT_CHOICES = [
        ('active', 'Active'),
        ('fermee', 'Fermée'),
    ]

    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='offres_mentorat',
        verbose_name='Auteur'
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name='Type'
    )
    matieres = models.ManyToManyField(
        Matiere,
        related_name='offres',
        verbose_name='Matières'
    )
    disponibilites = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Disponibilités',
        help_text='Format JSON : {"lundi": ["08h-10h"], ...}'
    )
    format = models.CharField(
        max_length=15,
        choices=FORMAT_CHOICES,
        default='les_deux',
        verbose_name='Format'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Décrivez votre offre ou demande en quelques mots'
    )
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='active',
        verbose_name='Statut'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        verbose_name = 'Offre de mentorat'
        verbose_name_plural = 'Offres de mentorat'
        ordering = ['-date_creation']

    def __str__(self):
        type_label = 'Offre' if self.type == 'offre' else 'Demande'
        return f"{type_label} de {self.auteur.get_full_name()} ({self.get_statut_display()})"


class Matching(models.Model):
    """
    Représente un résultat de matching entre un mentor et un mentoré.
    Stocke le score de compatibilité et les informations communes.
    """

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matchings_mentor',
        verbose_name='Mentor'
    )
    mentore = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matchings_mentore',
        verbose_name='Mentoré'
    )
    score_compatibilite = models.FloatField(
        default=0.0,
        verbose_name='Score de compatibilité',
        help_text='Score entre 0.0 et 1.0'
    )
    matieres_communes = models.ManyToManyField(
        Matiere,
        related_name='matchings',
        blank=True,
        verbose_name='Matières communes'
    )
    disponibilites_communes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Disponibilités communes'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        verbose_name = 'Matching'
        verbose_name_plural = 'Matchings'
        ordering = ['-score_compatibilite']
        # Empêcher les doublons de matching
        unique_together = ['mentor', 'mentore']

    def __str__(self):
        return (
            f"Matching: {self.mentor.get_full_name()} → "
            f"{self.mentore.get_full_name()} "
            f"(Score: {self.score_compatibilite:.0%})"
        )

    @property
    def score_pourcentage(self):
        """Retourne le score en pourcentage (0-100)."""
        return round(self.score_compatibilite * 100)
