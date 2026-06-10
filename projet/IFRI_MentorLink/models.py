from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, nom, prenom, telephone, filiere, niveau, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            filiere=filiere,
            niveau=niveau,
            **extra_fields,
        )
        user.set_password(password)  # hachage automatique PBKDF2-SHA256
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, telephone, filiere, niveau, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nom, prenom, telephone, filiere, niveau, password, **extra_fields)


FILIERE_CHOICES = [
    ("SI", "Sécurité Informatique"),
    ("GL", "Génie Logiciel"),
    ("IA", "Intelligence Artificielle"),
    ("IM", "Internet et Multimédia"),
    ("SeOIT", "Systèmes Embarqués et Internet des Objets"),
]

NIVEAU_CHOICES = [
    ("L1", "Licence 1"),
    ("L2", "Licence 2"),
    ("L3", "Licence 3"),
    ("M1", "Master 1"),
    ("M2", "Master 2"),
]


class User(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    # mot_de_passe → géré par AbstractBaseUser via le champ `password` (hashé automatiquement)
    photo = models.ImageField(max_length=255, null=True, blank=True)
    filiere = models.CharField(max_length=10, choices=FILIERE_CHOICES)
    niveau = models.CharField(max_length=5, choices=NIVEAU_CHOICES)
    bio_courte = models.TextField(null=True, blank=True)
    centres_interet = models.TextField(null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom", "telephone", "filiere", "niveau"]

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"], name="idx_users_email"),
            models.Index(fields=["telephone"], name="idx_users_telephone"),
        ]

    def __str__(self):
        return f"{self.prenom} {self.nom}"


JOURS_CHOICES = [
    ("lundi", "Lundi"),
    ("mardi", "Mardi"),
    ("mercredi", "Mercredi"),
    ("jeudi", "Jeudi"),
    ("vendredi", "Vendredi"),
    ("samedi", "Samedi"),
    ("dimanche", "Dimanche"),
]


class UserCreneau(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="creneaux",
        db_column="user_id",
    )
    jour = models.CharField(max_length=15, choices=JOURS_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        db_table = "users_creneaux"
        indexes = [
            models.Index(fields=["user"], name="idx_uc_user_id"),
            models.Index(fields=["jour"], name="idx_uc_jour"),
        ]

    def __str__(self):
        return f"{self.user} — {self.jour} {self.heure_debut}-{self.heure_fin}"


class PointFort(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="points_forts",
        db_column="user_id",
    )
    matiere = models.CharField(max_length=100)

    class Meta:
        db_table = "points_forts"
        indexes = [
            models.Index(fields=["user"], name="idx_pf_user_id"),
            models.Index(fields=["matiere"], name="idx_pf_matiere"),
            models.Index(fields=["user", "matiere"], name="idx_pf_user_matiere"),
        ]

    def __str__(self):
        return f"{self.user} — {self.matiere}"


class Lacune(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lacunes",
        db_column="user_id",
    )
    matiere = models.CharField(max_length=100)

    class Meta:
        db_table = "lacunes"
        indexes = [
            models.Index(fields=["user"], name="idx_lac_user_id"),
            models.Index(fields=["matiere"], name="idx_lac_matiere"),
            models.Index(fields=["user", "matiere"], name="idx_lac_user_matiere"),
        ]

    def __str__(self):
        return f"{self.user} — {self.matiere}"


FORMAT_CHOICES = [
    ("presentiel", "Présentiel"),
    ("en ligne", "En ligne"),
    ("mixte", "Mixte"),
]


class Offre(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offres",
        db_column="user_id",
    )
    matiere = models.CharField(max_length=100)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    description_offre = models.TextField(null=True, blank=True)
    date_creation_offre = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "offres"
        indexes = [
            models.Index(fields=["user"], name="idx_offres_user_id"),
            models.Index(fields=["matiere"], name="idx_offres_matiere"),
            models.Index(fields=["date_creation_offre"], name="idx_offres_date_creation_offre"),
            models.Index(fields=["user", "matiere"], name="idx_offres_user_matiere"),
        ]

    def __str__(self):
        return f"Offre {self.matiere} par {self.user}"


class OffreCreneau(models.Model):
    offre = models.ForeignKey(
        Offre,
        on_delete=models.CASCADE,
        related_name="creneaux",
        db_column="offre_id",
    )
    jour = models.CharField(max_length=15, choices=JOURS_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        db_table = "offres_creneaux"
        indexes = [
            models.Index(fields=["offre"], name="idx_oc_offre_id"),
            models.Index(fields=["jour"], name="idx_oc_jour"),
            models.Index(fields=["jour", "heure_debut", "heure_fin"], name="idx_oc_horaires"),
        ]

    def __str__(self):
        return f"{self.offre} — {self.jour} {self.heure_debut}-{self.heure_fin}"


class Demande(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="demandes",
        db_column="user_id",
    )
    matiere = models.CharField(max_length=100)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    description_demande = models.TextField(null=True, blank=True)
    date_creation_demande = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demandes"
        indexes = [
            models.Index(fields=["user"], name="idx_demandes_user_id"),
            models.Index(fields=["matiere"], name="idx_demandes_matiere"),
            models.Index(fields=["date_creation_demande"], name="idx_demandes_date_crea"),
            models.Index(fields=["user", "matiere"], name="idx_demandes_user_matiere"),
        ]

    def __str__(self):
        return f"Demande {self.matiere} par {self.user}"


class DemandeCreneau(models.Model):
    demande = models.ForeignKey(
        Demande,
        on_delete=models.CASCADE,
        related_name="creneaux",
        db_column="demande_id",
    )
    jour = models.CharField(max_length=15, choices=JOURS_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        db_table = "demandes_creneaux"
        indexes = [
            models.Index(fields=["demande"], name="idx_dc_demande_id"),
            models.Index(fields=["jour"], name="idx_dc_jour"),
            models.Index(fields=["jour", "heure_debut", "heure_fin"], name="idx_dc_horaires"),
        ]

    def __str__(self):
        return f"{self.demande} — {self.jour} {self.heure_debut}-{self.heure_fin}"


class Matching(models.Model):
    demande = models.ForeignKey(
        Demande,
        on_delete=models.CASCADE,
        related_name="matchings",
        db_column="demande_id",
    )
    offre = models.ForeignKey(
        Offre,
        on_delete=models.CASCADE,
        related_name="matchings",
        db_column="offre_id",
    )
    score = models.IntegerField(null=True, blank=True)
    date_matching = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "matchings"
        constraints = [
            models.UniqueConstraint(
                fields=["demande", "offre"],
                name="uk_matching_demande_offre"
            )
        ]
        indexes = [
            models.Index(fields=["demande"], name="idx_matching_demande_id"),
            models.Index(fields=["offre"], name="idx_matching_offre_id"),
            models.Index(fields=["-score"], name="idx_matching_score"),
        ]

    def __str__(self):
        return f"Matching demande#{self.demande_id} — offre#{self.offre_id} (score: {self.score})"


class Conversation(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations_initiated",
        db_column="user1_id",
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations_received",
        db_column="user2_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversations"
        constraints = [
            models.UniqueConstraint(
                fields=["user1", "user2"],
                name="uk_unique_conversation",
            )
        ]
        indexes = [
            models.Index(fields=["user1"], name="idx_conv_user1_id"),
            models.Index(fields=["user2"], name="idx_conv_user2_id"),
            models.Index(fields=["user1", "user2"], name="idx_conv_double_users"),
            models.Index(fields=["created_at"], name="idx_conv_created_at"),
        ]

    def __str__(self):
        return f"Conversation entre {self.user1} et {self.user2}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        db_column="conversation_id",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages_envoyes",
        db_column="sender_id",
    )
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        indexes = [
            models.Index(fields=["conversation"], name="idx_msg_conversation_id"),
            models.Index(fields=["sender"], name="idx_msg_sender_id"),
            models.Index(fields=["lu"], name="idx_msg_lu"),
            models.Index(fields=["created_at"], name="idx_msg_created_at"),
            # Index partiel (non_lus) — non supporté nativement par Django ORM,
            # à créer manuellement via une migration RunSQL :
            # CREATE INDEX idx_msg_unread ON messages(lu, conversation_id) WHERE lu = FALSE;
        ]

    def __str__(self):
        return f"Message de {self.sender} dans conv#{self.conversation_id}"