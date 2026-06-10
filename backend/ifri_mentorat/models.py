from django.db import models


# ÉNUMÉRATIONS


class FormatType(models.TextChoices):
    PRESENTIEL = 'presentiel', 'Présentiel'
    EN_LIGNE = 'en ligne', 'En ligne'
    MIXTE = 'mixte', 'Mixte'

class JourSemaine(models.TextChoices):
    LUNDI = 'lundi', 'Lundi'
    MARDI = 'mardi', 'Mardi'
    MERCREDI = 'mercredi', 'Mercredi'
    JEUDI = 'jeudi', 'Jeudi'
    VENDREDI = 'vendredi', 'Vendredi'
    SAMEDI = 'samedi', 'Samedi'
    DIMANCHE = 'dimanche', 'Dimanche'

class Filiere(models.TextChoices):
    IA = 'ia', 'Intelligence Artificielle (IA)'
    SI = 'si', 'Sécurité Informatique (SI)'
    GL = 'gl', 'Génie Logiciel (GL)'
    IM = 'im', 'Informatique Mathématique (IM)'
    SEIOT = 'seiot', 'Systèmes Embarqués et Intelligence des Objets (SeIOT)'

class Niveau(models.TextChoices):
    L1 = 'L1', 'Licence 1'
    L2 = 'L2', 'Licence 2'
    L3 = 'L3', 'Licence 3' 
    M1 = 'M1', 'Master 1'
    M2 = 'M2', 'Master 2'


# TABLE 1 : USERS

class UserProfile(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=255)
    filiere = models.CharField(max_length=100, choices = Filiere.choices)
    niveau = models.CharField(max_length=50, blank=True, null=True, choices = Niveau.choices)
    bio_courte = models.TextField(blank=True, null=True)
    centre_interet = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.nom.upper()} {self.prenom} ({self.filiere})"



# TABLE 1B : USERS_CRENEAUX

class UserCreneau(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='creneaux')
    jour = models.CharField(max_length=15, choices=JourSemaine.choices)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        db_table = 'users_creneaux'

    def __str__(self):
        return f"{self.user.nom} — {self.jour} {self.heure_debut}-{self.heure_fin}"



# TABLE 2 : POINTS_FORTS

class PointFort(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='points_forts')
    matiere = models.CharField(max_length=100)

    class Meta:
        db_table = 'points_forts'

    def __str__(self):
        return f"Point fort '{self.matiere}' de {self.user.nom}"



# TABLE 3 : LACUNES

class Lacune(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='lacunes')
    matiere = models.CharField(max_length=100)

    class Meta:
        db_table = 'lacunes'

    def __str__(self):
        return f"Lacune '{self.matiere}' de {self.user.nom}"



# TABLE 4 : OFFRES

class Offre(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='offres')
    matiere = models.CharField(max_length=100)
    format = models.CharField(max_length=50, choices=FormatType.choices)
    description_offre = models.TextField(blank=True, null=True)
    date_creation_offre = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'offres'

    def __str__(self):
        return f"Offre '{self.matiere}' par {self.user.nom}"



# TABLE 4B : OFFRES_CRENEAUX

class CreneauOffre(models.Model):
    offre       = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='creneaux')
    jour        = models.CharField(max_length=15, choices=JourSemaine.choices)
    heure_debut = models.TimeField()
    heure_fin   = models.TimeField()

    class Meta:
        db_table = 'offres_creneaux'

    def __str__(self):
        return f"{self.jour} {self.heure_debut}-{self.heure_fin} (Offre #{self.offre.id})"



# TABLE 5 : DEMANDES

class Demande(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='demandes')
    matiere = models.CharField(max_length=100)
    format = models.CharField(max_length=50, choices=FormatType.choices)
    description_demande = models.TextField(blank=True, null=True)
    date_creation_demande = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demandes'

    def __str__(self):
        return f"Demande '{self.matiere}' par {self.user.nom}"



# TABLE 5B : DEMANDES_CRENEAUX

class CreneauDemande(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='creneaux')
    jour = models.CharField(max_length=15, choices=JourSemaine.choices)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        db_table = 'demandes_creneaux'

    def __str__(self):
        return f"{self.jour} {self.heure_debut}-{self.heure_fin} (Demande #{self.demande.id})"



# TABLE 6 : MATCHINGS

class Matching(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='matchings')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='matchings')
    score = models.IntegerField(blank=True, null=True)
    date_matching = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'matchings'

    def __str__(self):
        return f"Matching Offre#{self.offre.id} / Demande#{self.demande.id} — Score: {self.score}"



# TABLE 7 : CONVERSATIONS

class Conversation(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_initiees')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_recues')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Conversation entre {self.user1.nom} et {self.user2.nom}"


# TABLE 8 : MESSAGES

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"Message de {self.sender.nom} à {self.created_at}"
