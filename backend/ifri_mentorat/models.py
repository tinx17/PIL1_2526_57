from django.db import models

# ENUMÉRATION POUR LE FORMAT DES OFFRES ET DEMANDES

class FormatType(models.TextChoices):
    PRESENTIEL = 'presentiel', 'Présentiel'
    EN_LIGNE = 'en ligne', 'En ligne'
    MIXTE = 'mixte', 'Mixte'


# =================================================================
# TABLE 1 : USERS (UserProfile)
# =================================================================
class UserProfile(models.Model):
    # L'identifiant (id SERIAL PRIMARY KEY) est géré automatiquement par Django
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=255) # Stocké hashé via make_password
    photo = models.CharField(max_length=255, blank=True, null=True)
    filiere = models.CharField(max_length=100, blank=True, null=True)
    niveau = models.CharField(max_length=50, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom.upper()} {self.prenom} ({self.filiere})"



# TABLE 2 : COMPETENCES

class Competence(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='competences')
    matiere = models.CharField(max_length=100)
    disponibilite = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Compétence {self.matiere} de {self.user.nom}"



# TABLE 3 : LACUNES

class Lacune(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='lacunes')
    matiere = models.CharField(max_length=100)
    disponibilite = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Lacune {self.matiere} de {self.user.nom}"



# TABLE 4 : OFFRES

class Offre(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='offres')
    matiere = models.CharField(max_length=100)
    disponibilite = models.CharField(max_length=255)
    format = models.CharField(
        max_length=20,
        choices=FormatType.choices,
        default=FormatType.MIXTE
    )
    description_offres = models.TextField(blank=True, null=True)
    date_offre = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offre en {self.matiere} par {self.user.nom}"



# TABLE 5 : DEMANDES

class Demande(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='demandes')
    matiere = models.CharField(max_length=100)
    disponibilite = models.CharField(max_length=255)
    format = models.CharField(
        max_length=20,
        choices=FormatType.choices,
        default=FormatType.MIXTE
    )
    description_demande = models.TextField(blank=True, null=True)
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande en {self.matiere} par {self.user.nom}"



# TABLE 6 : CONVERSATIONS

class Conversation(models.Model):
    # Les related_name permettent de différencier les deux clés étrangères pointant vers la même table
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_initiees')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_recues')
    date_conversation = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Recrée la contrainte d'unicité UNIQUE (user1_id, user2_id) du fichier .sql
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Discussion entre {self.user1.nom} et {self.user2.nom}"



# TABLE 7 : MESSAGES

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.sender.nom} à {self.date_envoi}"



# Create your models here.
