from django.shortcuts import render

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import UserProfile

@csrf_exempt  # Indispensable pour communiquer avec votre frontend indépendant
def api_inscription(request):
    if request.method == "POST":
        try:
            # 1. Récupérer et décoder les données envoyées en JSON par Vue.js
            data = json.loads(request.body)
            
            # Nettoyage et normalisation pour éviter les contournements (doublons)
            email_saisi = data.get('email', '').strip().lower()
            telephone_saisi = data.get('telephone', '').strip()

            # 2. Validation de sécurité : Vérification de l'unicité (Exigence Page 5)
            if UserProfile.objects.filter(email=email_saisi).exists():
                return JsonResponse({
                    "status": "error", 
                    "message": "Cette adresse e-mail est déjà associée à un compte MentorLink."
                }, status=400)
                
            if UserProfile.objects.filter(telephone=telephone_saisi).exists():
                return JsonResponse({
                    "status": "error", 
                    "message": "Ce numéro de téléphone est déjà enregistré sur la plateforme."
                }, status=400)

            # 3. Insertion propre dans PostgreSQL via l'ORM (Exigence Page 7)
            nouvel_etudiant = UserProfile.objects.create(
                nom=data.get('nom', '').strip(),
                prenom=data.get('prenom', '').strip(),
                email=email_saisi,
                telephone=telephone_saisi,
                # Chiffrement irréversible du mot de passe avant la sauvegarde en base
                mot_de_passe=make_password(data.get('mot_de_passe')), 
                filiere=data.get('filiere', '').strip(),
                niveau=data.get('niveau', '').strip(),
                bio_courte=data.get('bio_courte', '').strip(),
                centres_interet=data.get('centres_interet', '').strip(),
                photo=data.get('photo', '') # Peut être vide au départ
            )

            # 4. Réponse au format JSON standard pour le Frontend indépendant
            return JsonResponse({
                "status": "success",
                "message": "Votre compte IFRI MentorLink a été créé avec succès !",
                "user_id": nouvel_etudiant.id
            }, status=201)

        except Exception as e:
            # En cas de problème de clé manquante ou de format JSON invalide
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Méthode non autorisée. Utilisez POST."}, status=405)

