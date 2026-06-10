"""
Modèles de l'application accounts.
Définit le profil utilisateur étendu et le modèle Matière.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Matiere(models.Model):
    """
    Représente une matière académique (ex: Algorithmique, Python, Réseaux...).
    Utilisée pour les compétences, lacunes et offres de mentorat.
    """
    nom = models.CharField(max_length=100, unique=True, verbose_name='Nom de la matière')

    class Meta:
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class UserProfile(AbstractUser):
    """
    Profil utilisateur étendu pour IFRI_MentorLink.
    Étend AbstractUser de Django avec des champs spécifiques
    au contexte académique de l'IFRI.
    """

    # ── Choix pour les champs à sélection ──
    FILIERE_CHOICES = [
        ('IA', 'Intelligence Artificielle'),
        ('IM', 'Internet et Multimédia'),
        ('GL', 'Génie Logiciel'),
        ('SE_IoT', 'Systèmes Embarqués et IoT'),
        ('SI', 'Sécurité Informatique'),
    ]

    NIVEAU_CHOICES = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
    ]

    # ── Informations personnelles ──
    nom = models.CharField(max_length=100, verbose_name='Nom de famille')
    prenom = models.CharField(max_length=100, verbose_name='Prénom')
    email = models.EmailField(unique=True, verbose_name='Adresse email')
    telephone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Numéro de téléphone',
        help_text='Format : +229XXXXXXXX'
    )
    photo_profil = models.ImageField(
        upload_to='photos_profil/',
        blank=True,
        null=True,
        verbose_name='Photo de profil'
    )

    # ── Informations académiques ──
    filiere = models.CharField(
        max_length=10,
        choices=FILIERE_CHOICES,
        verbose_name='Filière',
        blank=True
    )
    niveau = models.CharField(
        max_length=5,
        choices=NIVEAU_CHOICES,
        verbose_name='Niveau d\'études',
        blank=True
    )

    # ── Compétences et lacunes ──
    competences = models.ManyToManyField(
        Matiere,
        related_name='utilisateurs_competents',
        blank=True,
        verbose_name='Compétences'
    )
    lacunes = models.ManyToManyField(
        Matiere,
        related_name='utilisateurs_en_difficulte',
        blank=True,
        verbose_name='Lacunes'
    )

    # ── Disponibilités ──
    disponibilites = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Disponibilités',
        help_text='Format JSON : {"lundi": ["08h-10h", "14h-16h"], ...}'
    )

    # ── Autres ──
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Biographie courte'
    )
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date d\'inscription'
    )

    # Utiliser l'email comme identifiant de connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom', 'telephone']

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.get_filiere_display() or 'N/A'})"

    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur."""
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        """Retourne le prénom de l'utilisateur."""
        return self.prenom
