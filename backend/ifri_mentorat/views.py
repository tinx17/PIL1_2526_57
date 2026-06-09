import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import (UserProfile, PointFort, Lacune, Offre, Demande,
                     CreneauDemande, CreneauOffre, Conversation, Message,
                     UserCreneau, FormatType, Matching)
from django.db.models import Q, Max
from datetime import datetime

# =================================================================
# CONSTANTES GLOBALES
# =================================================================

JOURS_VALIDES    = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
FILIERES_VALIDES = ['ia', 'si', 'gl', 'im', 'seiot']
NIVEAUX_VALIDES  = ['L1', 'L2', 'L3', 'M1', 'M2']
FORMATS_VALIDES  = [f.value for f in FormatType]

# =================================================================
# FONCTIONS UTILITAIRES
# =================================================================

def valider_heure(heure_str):
    try:
        datetime.strptime(heure_str, '%H:%M')
        return True
    except ValueError:
        return False

# =================================================================
# API INSCRIPTION
# POST /api/inscription/
# =================================================================

@csrf_exempt
def api_inscription(request):
    if request.method == "POST":
        try:
            data            = json.loads(request.body)
            email_saisi     = data.get('email',     '').strip().lower()
            telephone_saisi = data.get('telephone', '').strip()

            # Vérification des champs obligatoires
            nom    = data.get('nom',    '').strip()
            prenom = data.get('prenom', '').strip()
            if not nom or not prenom:
                return JsonResponse({
                    "status": "error",
                    "message": "Le nom et le prénom sont obligatoires."
                }, status=400)

            mot_de_passe = data.get('mot_de_passe', '').strip()
            if not mot_de_passe:
                return JsonResponse({
                    "status": "error",
                    "message": "Le mot de passe est obligatoire."
                }, status=400)

            # Validation filière
            filiere = data.get('filiere', '').strip().lower()
            if filiere not in FILIERES_VALIDES:
                return JsonResponse({
                    "status": "error",
                    "message": f"Filière invalide. Valeurs acceptées : {', '.join(FILIERES_VALIDES).upper()}"
                }, status=400)

            # Validation niveau
            niveau = data.get('niveau', '').strip()
            if niveau not in NIVEAUX_VALIDES:
                return JsonResponse({
                    "status": "error",
                    "message": f"Niveau invalide. Valeurs acceptées : {', '.join(NIVEAUX_VALIDES)}"
                }, status=400)

            # Vérification unicité email
            if UserProfile.objects.filter(email=email_saisi).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Cette adresse e-mail est déjà associée à un compte MentorLink."
                }, status=400)

            # Vérification unicité téléphone
            if UserProfile.objects.filter(telephone=telephone_saisi).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Ce numéro de téléphone est déjà enregistré sur la plateforme."
                }, status=400)

            # Création de l'utilisateur
            nouvel_etudiant = UserProfile.objects.create(
                nom             = nom,
                prenom          = prenom,
                telephone       = telephone_saisi,
                email           = email_saisi,
                mot_de_passe    = make_password(mot_de_passe),
                filiere         = filiere,
                niveau          = niveau,
                bio_courte      = data.get('bio_courte',      '').strip(),
                centre_interet = data.get('centre_interet', '').strip()
            )

            # Création des points forts
            points_forts = data.get('points_forts', [])
            if isinstance(points_forts, list):
                for matiere in points_forts:
                    if matiere.strip():
                        PointFort.objects.create(
                            user=nouvel_etudiant,
                            matiere=matiere.strip()
                        )

            # Création des lacunes
            lacunes = data.get('lacunes', [])
            if isinstance(lacunes, list):
                for matiere in lacunes:
                    if matiere.strip():
                        Lacune.objects.create(
                            user=nouvel_etudiant,
                            matiere=matiere.strip()
                        )

            # Création des créneaux horaires
            creneaux = data.get('creneaux', [])
            if isinstance(creneaux, list):
                for creneau in creneaux:
                    jour        = creneau.get('jour',        '').strip().lower()
                    heure_debut = creneau.get('heure_debut', '').strip()
                    heure_fin   = creneau.get('heure_fin',   '').strip()
                    if jour in JOURS_VALIDES and valider_heure(heure_debut) and valider_heure(heure_fin):
                        UserCreneau.objects.create(
                            user=nouvel_etudiant,
                            jour=jour,
                            heure_debut=heure_debut,
                            heure_fin=heure_fin
                        )

            return JsonResponse({
                "status" : "success",
                "message": "Votre compte IFRI MentorLink a été créé avec succès !",
                "user_id": nouvel_etudiant.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Méthode non autorisée."}, status=405)


# =================================================================
# API LOGIN
# POST /api/login/
# =================================================================

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        try:
            data               = json.loads(request.body)
            email_saisi        = data.get('email',        '').strip().lower()
            mot_de_passe_saisi = data.get('mot_de_passe', '')

            try:
                utilisateur = UserProfile.objects.get(email=email_saisi)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Aucun compte trouvé avec cette adresse e-mail."
                }, status=404)

            if not check_password(mot_de_passe_saisi, utilisateur.mot_de_passe):
                return JsonResponse({
                    "status": "error",
                    "message": "Mot de passe incorrect. Veuillez réessayer."
                }, status=401)

            return JsonResponse({
                "status" : "success",
                "message": f"Bienvenue {utilisateur.prenom} ! Vous êtes connecté à MentorLink.",
                "user_id": utilisateur.id,
                "prenom" : utilisateur.prenom
            }, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Méthode non autorisée."}, status=405)


# =================================================================
# API UPDATE PASSWORD
# POST /api/update-password/
# =================================================================

@csrf_exempt
def api_update_password(request):
    if request.method == "POST":
        try:
            data         = json.loads(request.body)
            email_saisi  = data.get('email',    '').strip().lower()
            new_password = data.get('password', '').strip()

            if not new_password:
                return JsonResponse({
                    "status": "error",
                    "message": "Le mot de passe ne peut pas être vide."
                }, status=400)

            try:
                user = UserProfile.objects.get(email=email_saisi)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Aucun compte trouvé avec cette adresse e-mail."
                }, status=404)

            user.mot_de_passe = make_password(new_password)
            user.save()

            return JsonResponse({
                "status" : "success",
                "message": "Mot de passe mis à jour avec succès !"
            }, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez POST."
    }, status=405)


# =================================================================
# API UPDATE PROFIL
# POST /api/profil/update/
# =================================================================

@csrf_exempt
def api_update_profil(request):
    if request.method == "POST":
        try:
            data    = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({
                    "status": "error",
                    "message": "user_id est obligatoire."
                }, status=400)

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }, status=404)

            # -----------------------------------------------
            # 1. CHAMPS SIMPLES
            # -----------------------------------------------
            user.nom    = data.get('nom',    user.nom).strip()
            user.prenom = data.get('prenom', user.prenom).strip()

            # Champs nullable → or ''
            user.bio_courte      = data.get('bio_courte',      user.bio_courte      or '').strip()
            user.centre_interet = data.get('centre_interet', user.centre_interet or '').strip()

            # Filière
            if 'filiere' in data:
                filiere = data.get('filiere').strip().lower()
                if filiere not in FILIERES_VALIDES:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Filière invalide. Valeurs acceptées : {', '.join(FILIERES_VALIDES).upper()}"
                    }, status=400)
                user.filiere = filiere

            # Niveau
            if 'niveau' in data:
                niveau = data.get('niveau').strip()
                if niveau not in NIVEAUX_VALIDES:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Niveau invalide. Valeurs acceptées : {', '.join(NIVEAUX_VALIDES)}"
                    }, status=400)
                user.niveau = niveau

            # Téléphone — vérification unicité uniquement si modifié
            if 'telephone' in data:
                nouveau_tel = data.get('telephone').strip()
                if nouveau_tel != user.telephone:
                    if UserProfile.objects.filter(telephone=nouveau_tel).exclude(id=user_id).exists():
                        return JsonResponse({
                            "status": "error",
                            "message": "Ce numéro de téléphone est déjà utilisé par un autre compte."
                        }, status=400)
                user.telephone = nouveau_tel

            # Email — vérification unicité uniquement si modifié
            if 'email' in data:
                nouvel_email = data.get('email').strip().lower()
                if nouvel_email != user.email:
                    if UserProfile.objects.filter(email=nouvel_email).exclude(id=user_id).exists():
                        return JsonResponse({
                            "status": "error",
                            "message": "Cette adresse e-mail est déjà utilisée par un autre compte."
                        }, status=400)
                user.email = nouvel_email

            user.save()

            # -----------------------------------------------
            # 2. POINTS FORTS
            # -----------------------------------------------
            if 'points_forts' in data:
                points_forts = data.get('points_forts', [])
                if not isinstance(points_forts, list):
                    return JsonResponse({
                        "status": "error",
                        "message": "points_forts doit être une liste."
                    }, status=400)
                PointFort.objects.filter(user=user).delete()
                for matiere in points_forts:
                    if matiere.strip():
                        PointFort.objects.create(user=user, matiere=matiere.strip())

            # -----------------------------------------------
            # 3. LACUNES
            # -----------------------------------------------
            if 'lacunes' in data:
                lacunes = data.get('lacunes', [])
                if not isinstance(lacunes, list):
                    return JsonResponse({
                        "status": "error",
                        "message": "lacunes doit être une liste."
                    }, status=400)
                Lacune.objects.filter(user=user).delete()
                for matiere in lacunes:
                    if matiere.strip():
                        Lacune.objects.create(user=user, matiere=matiere.strip())

            # -----------------------------------------------
            # 4. CRÉNEAUX HORAIRES
            # -----------------------------------------------
            if 'creneaux' in data:
                creneaux = data.get('creneaux', [])
                if not isinstance(creneaux, list):
                    return JsonResponse({
                        "status": "error",
                        "message": "creneaux doit être une liste."
                    }, status=400)
                UserCreneau.objects.filter(user=user).delete()
                for creneau in creneaux:
                    jour        = creneau.get('jour',        '').strip().lower()
                    heure_debut = creneau.get('heure_debut', '').strip()
                    heure_fin   = creneau.get('heure_fin',   '').strip()

                    if jour not in JOURS_VALIDES:
                        return JsonResponse({
                            "status": "error",
                            "message": f"Jour invalide : '{jour}'. Valeurs acceptées : {', '.join(JOURS_VALIDES)}"
                        }, status=400)
                    if not valider_heure(heure_debut) or not valider_heure(heure_fin):
                        return JsonResponse({
                            "status": "error",
                            "message": "Format d'heure invalide. Utilisez HH:MM (ex: 14:00)"
                        }, status=400)
                    if heure_debut >= heure_fin:
                        return JsonResponse({
                            "status": "error",
                            "message": f"L'heure de début ({heure_debut}) doit être avant l'heure de fin ({heure_fin})."
                        }, status=400)

                    UserCreneau.objects.create(
                        user=user,
                        jour=jour,
                        heure_debut=heure_debut,
                        heure_fin=heure_fin
                    )

            return JsonResponse({
                "status" : "success",
                "message": "Votre profil a été mis à jour avec succès !"
            }, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez POST."
    }, status=405)


# =================================================================
# API CRÉER OFFRE
# POST /api/offres/creer/
# =================================================================

@csrf_exempt
def api_creer_offre(request):
    if request.method == "POST":
        try:
            data    = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({
                    "status": "error",
                    "message": "user_id est obligatoire."
                }, status=400)

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }, status=404)

            matiere     = data.get('matiere',     '').strip()
            format_     = data.get('format',      '').strip()
            description = data.get('description', '').strip()
            creneaux    = data.get('creneaux',    [])

            if not matiere:
                return JsonResponse({
                    "status": "error",
                    "message": "La matière est obligatoire."
                }, status=400)

            if not PointFort.objects.filter(user=user, matiere=matiere).exists():
                return JsonResponse({
                    "status": "error",
                    "message": f"Vous ne pouvez pas proposer une offre en '{matiere}' car cette matière n'est pas dans vos points forts."
                }, status=400)

            if format_ not in FORMATS_VALIDES:
                return JsonResponse({
                    "status": "error",
                    "message": f"Format invalide. Valeurs acceptées : {', '.join(FORMATS_VALIDES)}"
                }, status=400)

            if not isinstance(creneaux, list) or len(creneaux) == 0:
                return JsonResponse({
                    "status": "error",
                    "message": "Au moins un créneau horaire est obligatoire."
                }, status=400)

            # Validation des créneaux avant création
            for creneau in creneaux:
                jour        = creneau.get('jour',        '').strip().lower()
                heure_debut = creneau.get('heure_debut', '').strip()
                heure_fin   = creneau.get('heure_fin',   '').strip()

                if jour not in JOURS_VALIDES:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Jour invalide : '{jour}'."
                    }, status=400)
                if not valider_heure(heure_debut) or not valider_heure(heure_fin):
                    return JsonResponse({
                        "status": "error",
                        "message": "Format d'heure invalide. Utilisez HH:MM (ex: 14:00)"
                    }, status=400)
                if heure_debut >= heure_fin:
                    return JsonResponse({
                        "status": "error",
                        "message": f"L'heure de début ({heure_debut}) doit être avant l'heure de fin ({heure_fin})."
                    }, status=400)

            # Création de l'offre
            offre = Offre.objects.create(
                user              = user,
                matiere           = matiere,
                format            = format_,
                description_offre = description,
            )

            # Création des créneaux
            for creneau in creneaux:
                CreneauOffre.objects.create(
                    offre       = offre,
                    jour        = creneau.get('jour').strip().lower(),
                    heure_debut = creneau.get('heure_debut').strip(),
                    heure_fin   = creneau.get('heure_fin').strip(),
                )

            return JsonResponse({
                "status"  : "success",
                "message" : "Offre créée avec succès !",
                "offre_id": offre.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez POST."
    }, status=405)


# =================================================================
# API CRÉER DEMANDE
# POST /api/demandes/creer/
# =================================================================

@csrf_exempt
def api_creer_demande(request):
    if request.method == "POST":
        try:
            data    = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({
                    "status": "error",
                    "message": "user_id est obligatoire."
                }, status=400)

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }, status=404)

            matiere     = data.get('matiere',     '').strip()
            format_     = data.get('format',      '').strip()
            description = data.get('description', '').strip()
            creneaux    = data.get('creneaux',    [])

            if not matiere:
                return JsonResponse({
                    "status": "error",
                    "message": "La matière est obligatoire."
                }, status=400)

            if not Lacune.objects.filter(user=user, matiere=matiere).exists():
                return JsonResponse({
                    "status": "error",
                    "message": f"Vous ne pouvez pas créer une demande en '{matiere}' car cette matière n'est pas dans vos lacunes."
                }, status=400)

            if format_ not in FORMATS_VALIDES:
                return JsonResponse({
                    "status": "error",
                    "message": f"Format invalide. Valeurs acceptées : {', '.join(FORMATS_VALIDES)}"
                }, status=400)

            if not isinstance(creneaux, list) or len(creneaux) == 0:
                return JsonResponse({
                    "status": "error",
                    "message": "Au moins un créneau horaire est obligatoire."
                }, status=400)

            # Validation des créneaux avant création
            for creneau in creneaux:
                jour        = creneau.get('jour',        '').strip().lower()
                heure_debut = creneau.get('heure_debut', '').strip()
                heure_fin   = creneau.get('heure_fin',   '').strip()

                if jour not in JOURS_VALIDES:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Jour invalide : '{jour}'."
                    }, status=400)
                if not valider_heure(heure_debut) or not valider_heure(heure_fin):
                    return JsonResponse({
                        "status": "error",
                        "message": "Format d'heure invalide. Utilisez HH:MM (ex: 14:00)"
                    }, status=400)
                if heure_debut >= heure_fin:
                    return JsonResponse({
                        "status": "error",
                        "message": f"L'heure de début ({heure_debut}) doit être avant l'heure de fin ({heure_fin})."
                    }, status=400)

            # Création de la demande
            demande = Demande.objects.create(
                user                = user,
                matiere             = matiere,
                format              = format_,
                description_demande = description,
            )

            # Création des créneaux
            for creneau in creneaux:
                CreneauDemande.objects.create(
                    demande     = demande,
                    jour        = creneau.get('jour').strip().lower(),
                    heure_debut = creneau.get('heure_debut').strip(),
                    heure_fin   = creneau.get('heure_fin').strip(),
                )

            return JsonResponse({
                "status"    : "success",
                "message"   : "Demande créée avec succès !",
                "demande_id": demande.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez POST."
    }, status=405)


# =================================================================
# API 1 — Créer ou récupérer une conversation
# POST /api/conversations/creer/
# =================================================================

@csrf_exempt
def api_creer_conversation(request):
    if request.method == "POST":
        try:
            data             = json.loads(request.body)
            user_id          = data.get('user_id')
            interlocuteur_id = data.get('interlocuteur_id')

            if not user_id or not interlocuteur_id:
                return JsonResponse({
                    "status": "error",
                    "message": "user_id et interlocuteur_id sont obligatoires."
                }, status=400)

            if user_id == interlocuteur_id:
                return JsonResponse({
                    "status": "error",
                    "message": "Vous ne pouvez pas démarrer une conversation avec vous-même."
                }, status=400)

            try:
                user          = UserProfile.objects.get(id=user_id)
                interlocuteur = UserProfile.objects.get(id=interlocuteur_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Un des utilisateurs est introuvable."
                }, status=404)

            conversation = Conversation.objects.filter(
                Q(user1=user, user2=interlocuteur) |
                Q(user1=interlocuteur, user2=user)
            ).first()

            if conversation:
                return JsonResponse({
                    "status"         : "exists",
                    "message"        : "Conversation déjà existante.",
                    "conversation_id": conversation.id
                }, status=200)

            conversation = Conversation.objects.create(
                user1=user,
                user2=interlocuteur
            )

            return JsonResponse({
                "status"         : "success",
                "message"        : "Conversation créée avec succès.",
                "conversation_id": conversation.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez POST."
    }, status=405)


# =================================================================
# API 2 — Lister toutes les conversations d'un utilisateur
# GET /api/conversations/liste/?user_id=1
# =================================================================

def api_liste_conversations(request):
    if request.method == "GET":
        try:
            user_id = request.GET.get('user_id')

            if not user_id:
                return JsonResponse({
                    "status": "error",
                    "message": "user_id est obligatoire."
                }, status=400)

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }, status=404)

            conversations = Conversation.objects.filter(
                Q(user1=user) | Q(user2=user)
            ).annotate(
                dernier_message_date=Max('messages__created_at')
            ).order_by('-dernier_message_date')

            liste         = []
            total_non_lus = 0

            for conv in conversations:
                interlocuteur = conv.user2 if conv.user1.id == int(user_id) else conv.user1
                dernier_msg   = conv.messages.order_by('-created_at').first()
                non_lus       = conv.messages.filter(lu=False).exclude(sender_id=user_id).count()
                total_non_lus += non_lus

                liste.append({
                    "conversation_id"     : conv.id,
                    "interlocuteur_id"    : interlocuteur.id,
                    "interlocuteur_nom"   : f"{interlocuteur.prenom} {interlocuteur.nom}",
                    "dernier_message"     : dernier_msg.contenu if dernier_msg else None,
                    "dernier_message_date": str(dernier_msg.created_at) if dernier_msg else None,
                    "non_lus"             : non_lus,
                    "created_at"          : str(conv.created_at)
                })

            return JsonResponse({
                "status"       : "success",
                "total_non_lus": total_non_lus,
                "conversations": liste
            }, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez GET."
    }, status=405)


# =================================================================
# API 3 — Récupérer les messages d'une conversation
# GET /api/conversations/<id>/messages/?user_id=1
# =================================================================

def api_messages_conversation(request, conversation_id):
    if request.method == "GET":
        try:
            user_id = request.GET.get('user_id')

            if not user_id:
                return JsonResponse({
                    "status": "error",
                    "message": "user_id est obligatoire."
                }, status=400)

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }, status=404)

            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Conversation introuvable."
                }, status=404)

            if conversation.user1.id != int(user_id) and conversation.user2.id != int(user_id):
                return JsonResponse({
                    "status": "error",
                    "message": "Vous n'avez pas accès à cette conversation."
                }, status=403)

            # Marquer les messages comme lus
            Message.objects.filter(
                conversation=conversation,
                lu=False
            ).exclude(sender_id=user_id).update(lu=True)

            messages       = conversation.messages.order_by('created_at')
            liste_messages = []

            for msg in messages:
                liste_messages.append({
                    "message_id"    : msg.id,
                    "sender_id"     : msg.sender.id,
                    "sender_nom"    : f"{msg.sender.prenom} {msg.sender.nom}",
                    "contenu"       : msg.contenu,
                    "lu"            : msg.lu,
                    "created_at"    : str(msg.created_at),
                    "est_expediteur": msg.sender.id == int(user_id)
                })

            return JsonResponse({
                "status"  : "success",
                "messages": liste_messages
            }, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez GET."
    }, status=405)


# =================================================================
# API 4 — Envoyer un message
# POST /api/conversations/<id>/envoyer/
# =================================================================

@csrf_exempt
def api_envoyer_message(request, conversation_id):
    if request.method == "POST":
        try:
            data    = json.loads(request.body)
            user_id = data.get('user_id')
            contenu = data.get('contenu', '').strip()

            if not user_id:
                return JsonResponse({
                    "status": "error",
                    "message": "user_id est obligatoire."
                }, status=400)

            if not contenu:
                return JsonResponse({
                    "status": "error",
                    "message": "Le message ne peut pas être vide."
                }, status=400)

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }, status=404)

            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Conversation introuvable."
                }, status=404)

            if conversation.user1.id != int(user_id) and conversation.user2.id != int(user_id):
                return JsonResponse({
                    "status": "error",
                    "message": "Vous n'êtes pas autorisé à envoyer un message dans cette conversation."
                }, status=403)

            message = Message.objects.create(
                conversation=conversation,
                sender=user,
                contenu=contenu
            )

            return JsonResponse({
                "status"    : "success",
                "message"   : "Message envoyé avec succès.",
                "message_id": message.id,
                "created_at": str(message.created_at)
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée. Utilisez POST."
    }, status=405)
