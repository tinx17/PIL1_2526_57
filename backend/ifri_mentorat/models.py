from django.db import models

class UserProfile(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255) 
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)  # e.g., 'mentor' or 'mentee'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"
# Create your models here.
