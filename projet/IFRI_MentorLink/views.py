from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Max


from .models import (
    Offre, Demande,
    OffreCreneau, DemandeCreneau,
    UserCreneau, PointFort, Lacune,Conversation, Message, User
)
from .matching_algorithm import (
    MatchingBidirectionnel
)


# ================================================
# UTILITAIRE : Copier les créneaux profil → offre/demande
# ================================================

def copier_creneaux_profil_vers_offre(user, offre):
    """
    Copie les UserCreneau de l'utilisateur dans OffreCreneau.
    Utilisé quand utiliser_creneaux_profil = true.
    """
    creneaux_profil = UserCreneau.objects.filter(user=user)

    if not creneaux_profil.exists():
        return False, "Votre profil n'a aucun créneau horaire défini."

    for creneau in creneaux_profil:
        OffreCreneau.objects.create(
            offre=offre,
            jour=creneau.jour,
            heure_debut=creneau.heure_debut,
            heure_fin=creneau.heure_fin
        )
    return True, None


def copier_creneaux_profil_vers_demande(user, demande):
    """
    Copie les UserCreneau de l'utilisateur dans DemandeCreneau.
    Utilisé quand utiliser_creneaux_profil = true.
    """
    creneaux_profil = UserCreneau.objects.filter(user=user)

    if not creneaux_profil.exists():
        return False, "Votre profil n'a aucun créneau horaire défini."

    for creneau in creneaux_profil:
        DemandeCreneau.objects.create(
            demande=demande,
            jour=creneau.jour,
            heure_debut=creneau.heure_debut,
            heure_fin=creneau.heure_fin
        )
    return True, None


def valider_creneaux(creneaux):
    """
    Valide la structure des créneaux envoyés manuellement.
    Chaque créneau doit avoir : jour, heure_debut, heure_fin.
    """
    jours_valides = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

    for i, c in enumerate(creneaux):
        if 'jour' not in c or 'heure_debut' not in c or 'heure_fin' not in c:
            return False, f"Créneau {i+1} : les champs 'jour', 'heure_debut' et 'heure_fin' sont obligatoires."
        if c['jour'] not in jours_valides:
            return False, f"Créneau {i+1} : jour '{c['jour']}' invalide."
        if c['heure_debut'] >= c['heure_fin']:
            return False, f"Créneau {i+1} : heure_debut doit être avant heure_fin."
    return True, None


# ================================================
# CRÉER UNE OFFRE
# ================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creer_offre(request):
    """
    Crée une offre de mentorat.

    Endpoint : POST /api/offres/creer/

    Body JSON :
    {
        "matiere": "Python",
        "format": "presentiel",
        "description_offre": "...",           (optionnel)
        "utiliser_creneaux_profil": true,     (true ou false)
        "creneaux": [                          (obligatoire si utiliser_creneaux_profil = false)
            { "jour": "lundi", "heure_debut": "18:00", "heure_fin": "20:00" },
            { "jour": "mercredi", "heure_debut": "17:00", "heure_fin": "19:00" }
        ]
    }
    """

    user = request.user
    data = request.data

    # ── 1. Champs obligatoires ──────────────────────────────
    matiere = data.get('matiere')
    format_ = data.get('format')
    utiliser_profil = data.get('utiliser_creneaux_profil', False)

    if not matiere:
        return Response({'error': "Le champ 'matiere' est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    if not format_:
        return Response({'error': "Le champ 'format' est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    if format_ not in ['presentiel', 'en ligne', 'mixte']:
        return Response({'error': "Format invalide. Valeurs acceptées : 'presentiel', 'en ligne', 'mixte'."}, status=status.HTTP_400_BAD_REQUEST)

    # ── 2. Vérifier que la matière est dans les points_forts ─
    if not PointFort.objects.filter(user=user, matiere=matiere).exists():
        return Response(
            {'error': f"Vous ne pouvez pas proposer '{matiere}' : cette matière n'est pas dans vos points forts."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ── 3. Créer l'offre ────────────────────────────────────
    offre = Offre.objects.create(
        user=user,
        matiere=matiere,
        format=format_,
        description_offre=data.get('description_offre', '')
    )

    # ── 4. Gérer les créneaux ───────────────────────────────
    if utiliser_profil:
        # Option 1 : importer depuis le profil
        succes, erreur = copier_creneaux_profil_vers_offre(user, offre)
        if not succes:
            offre.delete()
            return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Option 2 : créneaux manuels
        creneaux = data.get('creneaux', [])
        if not creneaux:
            offre.delete()
            return Response(
                {'error': "Vous devez fournir au moins un créneau ou activer 'utiliser_creneaux_profil'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        valide, erreur = valider_creneaux(creneaux)
        if not valide:
            offre.delete()
            return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)

        for c in creneaux:
            OffreCreneau.objects.create(
                offre=offre,
                jour=c['jour'],
                heure_debut=c['heure_debut'],
                heure_fin=c['heure_fin']
            )

    # ── 5. Lancer le matching automatiquement ───────────────
    algo = MatchingBidirectionnel()
    algo.execute_matching_for_offre(offre)

    return Response({
        'success': True,
        'message': 'Offre créée avec succès.',
        'offre_id': offre.id,
        'creneaux_source': 'profil' if utiliser_profil else 'manuel'
    }, status=status.HTTP_201_CREATED)


# ================================================
# CRÉER UNE DEMANDE
# ================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creer_demande(request):
    """
    Crée une demande de mentorat.

    Endpoint : POST /api/demandes/creer/

    Body JSON :
    {
        "matiere": "Python",
        "format": "en ligne",
        "description_demande": "...",          (optionnel)
        "utiliser_creneaux_profil": true,      (true ou false)
        "creneaux": [                           (obligatoire si utiliser_creneaux_profil = false)
            { "jour": "mardi", "heure_debut": "19:00", "heure_fin": "21:00" }
        ]
    }
    """

    user = request.user
    data = request.data

    # ── 1. Champs obligatoires ──────────────────────────────
    matiere = data.get('matiere')
    format_ = data.get('format')
    utiliser_profil = data.get('utiliser_creneaux_profil', False)

    if not matiere:
        return Response({'error': "Le champ 'matiere' est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    if not format_:
        return Response({'error': "Le champ 'format' est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    if format_ not in ['presentiel', 'en ligne', 'mixte']:
        return Response({'error': "Format invalide. Valeurs acceptées : 'presentiel', 'en ligne', 'mixte'."}, status=status.HTTP_400_BAD_REQUEST)

    # ── 2. Vérifier que la matière est dans les lacunes ─────
    if not Lacune.objects.filter(user=user, matiere=matiere).exists():
        return Response(
            {'error': f"Vous ne pouvez pas demander '{matiere}' : cette matière n'est pas dans vos lacunes."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ── 3. Créer la demande ─────────────────────────────────
    demande = Demande.objects.create(
        user=user,
        matiere=matiere,
        format=format_,
        description_demande=data.get('description_demande', '')
    )

    # ── 4. Gérer les créneaux ───────────────────────────────
    if utiliser_profil:
        # Option 1 : importer depuis le profil
        succes, erreur = copier_creneaux_profil_vers_demande(user, demande)
        if not succes:
            demande.delete()
            return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Option 2 : créneaux manuels
        creneaux = data.get('creneaux', [])
        if not creneaux:
            demande.delete()
            return Response(
                {'error': "Vous devez fournir au moins un créneau ou activer 'utiliser_creneaux_profil'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        valide, erreur = valider_creneaux(creneaux)
        if not valide:
            demande.delete()
            return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)

        for c in creneaux:
            DemandeCreneau.objects.create(
                demande=demande,
                jour=c['jour'],
                heure_debut=c['heure_debut'],
                heure_fin=c['heure_fin']
            )

    # ── 5. Lancer le matching automatiquement ───────────────
    algo = MatchingBidirectionnel()
    algo.execute_matching_for_demande(demande)

    return Response({
        'success': True,
        'message': 'Demande créée avec succès.',
        'demande_id': demande.id,
        'creneaux_source': 'profil' if utiliser_profil else 'manuel'
    }, status=status.HTTP_201_CREATED)


# ================================================
# PROFIL UTILISATEUR
# ================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profil(request):
    """
    Retourne le profil complet de l'utilisateur connecté.

    Endpoint : GET /api/profil/
    """
    user = request.user

    creneaux = [
        {
            'jour': c.jour,
            'heure_debut': str(c.heure_debut),
            'heure_fin': str(c.heure_fin)
        }
        for c in UserCreneau.objects.filter(user=user)
    ]

    points_forts = list(
        PointFort.objects.filter(user=user).values_list('matiere', flat=True)
    )

    lacunes = list(
        Lacune.objects.filter(user=user).values_list('matiere', flat=True)
    )

    return Response({
        'id': user.id,
        'nom': user.nom,
        'prenom': user.prenom,
        'email': user.email,
        'telephone': user.telephone,
        'photo': user.photo,
        'filiere': user.filiere,
        'niveau': user.niveau,
        'bio_courte': user.bio_courte,
        'centres_interet': user.centres_interet,
        'creneaux': creneaux,
        'points_forts': points_forts,
        'lacunes': lacunes,
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_profil(request):
    """
    Modifie les informations du profil de l'utilisateur connecté.
    Seuls les champs envoyés sont mis à jour.

    Endpoint : PUT /api/profil/modifier/

    Body JSON (tous optionnels) :
    {
        "nom": "...",
        "prenom": "...",
        "telephone": "...",
        "photo": "...",
        "filiere": "GL",
        "niveau": "M1",
        "bio_courte": "...",
        "centres_interet": "...",
        "creneaux": [
            { "jour": "lundi", "heure_debut": "18:00", "heure_fin": "20:00" }
        ]
    }
    """
    user = request.user
    data = request.data

    FILIERE_VALIDES = ['SI', 'GL', 'IA', 'IM', 'SeOIT']
    NIVEAU_VALIDES = ['L1', 'L2', 'L3', 'M1', 'M2']

    # ── Champs simples ──────────────────────────────────────
    champs_modifiables = ['nom', 'prenom', 'telephone', 'photo', 'bio_courte', 'centres_interet']
    for champ in champs_modifiables:
        if champ in data:
            setattr(user, champ, data[champ])

    if 'filiere' in data:
        if data['filiere'] not in FILIERE_VALIDES:
            return Response(
                {'error': f"Filière invalide. Valeurs acceptées : {FILIERE_VALIDES}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.filiere = data['filiere']

    if 'niveau' in data:
        if data['niveau'] not in NIVEAU_VALIDES:
            return Response(
                {'error': f"Niveau invalide. Valeurs acceptées : {NIVEAU_VALIDES}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.niveau = data['niveau']

    user.save()  # → déclenche le signal post_save → recalcul matchings automatique

    # ── Créneaux (remplacement complet si envoyés) ──────────
    if 'creneaux' in data:
        creneaux = data['creneaux']
        valide, erreur = valider_creneaux(creneaux)
        if not valide:
            return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)

        UserCreneau.objects.filter(user=user).delete()
        for c in creneaux:
            UserCreneau.objects.create(
                user=user,
                jour=c['jour'],
                heure_debut=c['heure_debut'],
                heure_fin=c['heure_fin']
            )

    return Response({
        'success': True,
        'message': 'Profil mis à jour avec succès.'
    }, status=status.HTTP_200_OK)


# ================================================
# OFFRES
# ================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_offres(request):
    """
    Retourne toutes les offres de l'utilisateur connecté.

    Endpoint : GET /api/offres/
    """
    user = request.user
    offres = Offre.objects.filter(user=user).order_by('-date_creation_offre')

    results = []
    for offre in offres:
        creneaux = [
            {
                'jour': c.jour,
                'heure_debut': str(c.heure_debut),
                'heure_fin': str(c.heure_fin)
            }
            for c in OffreCreneau.objects.filter(offre=offre)
        ]
        results.append({
            'id': offre.id,
            'matiere': offre.matiere,
            'format': offre.format,
            'description_offre': offre.description_offre,
            'date_creation_offre': offre.date_creation_offre,
            'creneaux': creneaux
        })

    return Response({'offres': results}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detail_offre(request, offre_id):
    """
    Retourne le détail d'une offre.

    Endpoint : GET /api/offres/{offre_id}/
    """
    try:
        offre = Offre.objects.get(id=offre_id, user=request.user)
    except Offre.DoesNotExist:
        return Response({'error': 'Offre non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    creneaux = [
        {
            'jour': c.jour,
            'heure_debut': str(c.heure_debut),
            'heure_fin': str(c.heure_fin)
        }
        for c in OffreCreneau.objects.filter(offre=offre)
    ]

    return Response({
        'id': offre.id,
        'matiere': offre.matiere,
        'format': offre.format,
        'description_offre': offre.description_offre,
        'date_creation_offre': offre.date_creation_offre,
        'creneaux': creneaux
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_offre(request, offre_id):
    """
    Modifie une offre existante.
    Seuls les champs envoyés sont mis à jour.

    Endpoint : PUT /api/offres/{offre_id}/modifier/

    Body JSON (tous optionnels) :
    {
        "format": "mixte",
        "description_offre": "...",
        "utiliser_creneaux_profil": true,
        "creneaux": [
            { "jour": "lundi", "heure_debut": "18:00", "heure_fin": "20:00" }
        ]
    }
    """
    try:
        offre = Offre.objects.get(id=offre_id, user=request.user)
    except Offre.DoesNotExist:
        return Response({'error': 'Offre non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if 'format' in data:
        if data['format'] not in ['presentiel', 'en ligne', 'mixte']:
            return Response(
                {'error': "Format invalide. Valeurs acceptées : 'presentiel', 'en ligne', 'mixte'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        offre.format = data['format']

    if 'description_offre' in data:
        offre.description_offre = data['description_offre']

    offre.save()

    # ── Mise à jour des créneaux ────────────────────────────
    if 'utiliser_creneaux_profil' in data or 'creneaux' in data:
        OffreCreneau.objects.filter(offre=offre).delete()

        utiliser_profil = data.get('utiliser_creneaux_profil', False)
        if utiliser_profil:
            succes, erreur = copier_creneaux_profil_vers_offre(request.user, offre)
            if not succes:
                return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)
        elif 'creneaux' in data:
            valide, erreur = valider_creneaux(data['creneaux'])
            if not valide:
                return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)
            for c in data['creneaux']:
                OffreCreneau.objects.create(
                    offre=offre,
                    jour=c['jour'],
                    heure_debut=c['heure_debut'],
                    heure_fin=c['heure_fin']
                )

    # ── Recalcul du matching ────────────────────────────────
    algo = MatchingBidirectionnel()
    algo.execute_matching_for_offre(offre)

    return Response({
        'success': True,
        'message': 'Offre mise à jour avec succès.'
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_offre(request, offre_id):
    """
    Supprime une offre (et ses créneaux + matchings par CASCADE).

    Endpoint : DELETE /api/offres/{offre_id}/supprimer/
    """
    try:
        offre = Offre.objects.get(id=offre_id, user=request.user)
    except Offre.DoesNotExist:
        return Response({'error': 'Offre non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    offre.delete()  # CASCADE → supprime OffreCreneau + Matching liés automatiquement

    return Response({
        'success': True,
        'message': 'Offre supprimée avec succès.'
    }, status=status.HTTP_200_OK)


# ================================================
# DEMANDES
# ================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_demandes(request):
    """
    Retourne toutes les demandes de l'utilisateur connecté.

    Endpoint : GET /api/demandes/
    """
    user = request.user
    demandes = Demande.objects.filter(user=user).order_by('-date_creation_demande')

    results = []
    for demande in demandes:
        creneaux = [
            {
                'jour': c.jour,
                'heure_debut': str(c.heure_debut),
                'heure_fin': str(c.heure_fin)
            }
            for c in DemandeCreneau.objects.filter(demande=demande)
        ]
        results.append({
            'id': demande.id,
            'matiere': demande.matiere,
            'format': demande.format,
            'description_demande': demande.description_demande,
            'date_creation_demande': demande.date_creation_demande,
            'creneaux': creneaux
        })

    return Response({'demandes': results}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detail_demande(request, demande_id):
    """
    Retourne le détail d'une demande.

    Endpoint : GET /api/demandes/{demande_id}/
    """
    try:
        demande = Demande.objects.get(id=demande_id, user=request.user)
    except Demande.DoesNotExist:
        return Response({'error': 'Demande non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    creneaux = [
        {
            'jour': c.jour,
            'heure_debut': str(c.heure_debut),
            'heure_fin': str(c.heure_fin)
        }
        for c in DemandeCreneau.objects.filter(demande=demande)
    ]

    return Response({
        'id': demande.id,
        'matiere': demande.matiere,
        'format': demande.format,
        'description_demande': demande.description_demande,
        'date_creation_demande': demande.date_creation_demande,
        'creneaux': creneaux
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_demande(request, demande_id):
    """
    Modifie une demande existante.
    Seuls les champs envoyés sont mis à jour.

    Endpoint : PUT /api/demandes/{demande_id}/modifier/

    Body JSON (tous optionnels) :
    {
        "format": "en ligne",
        "description_demande": "...",
        "utiliser_creneaux_profil": true,
        "creneaux": [
            { "jour": "mardi", "heure_debut": "19:00", "heure_fin": "21:00" }
        ]
    }
    """
    try:
        demande = Demande.objects.get(id=demande_id, user=request.user)
    except Demande.DoesNotExist:
        return Response({'error': 'Demande non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if 'format' in data:
        if data['format'] not in ['presentiel', 'en ligne', 'mixte']:
            return Response(
                {'error': "Format invalide. Valeurs acceptées : 'presentiel', 'en ligne', 'mixte'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        demande.format = data['format']

    if 'description_demande' in data:
        demande.description_demande = data['description_demande']

    demande.save()

    # ── Mise à jour des créneaux ────────────────────────────
    if 'utiliser_creneaux_profil' in data or 'creneaux' in data:
        DemandeCreneau.objects.filter(demande=demande).delete()

        utiliser_profil = data.get('utiliser_creneaux_profil', False)
        if utiliser_profil:
            succes, erreur = copier_creneaux_profil_vers_demande(request.user, demande)
            if not succes:
                return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)
        elif 'creneaux' in data:
            valide, erreur = valider_creneaux(data['creneaux'])
            if not valide:
                return Response({'error': erreur}, status=status.HTTP_400_BAD_REQUEST)
            for c in data['creneaux']:
                DemandeCreneau.objects.create(
                    demande=demande,
                    jour=c['jour'],
                    heure_debut=c['heure_debut'],
                    heure_fin=c['heure_fin']
                )

    # ── Recalcul du matching ────────────────────────────────
    algo = MatchingBidirectionnel()
    algo.execute_matching_for_demande(demande)

    return Response({
        'success': True,
        'message': 'Demande mise à jour avec succès.'
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_demande(request, demande_id):
    """
    Supprime une demande (et ses créneaux + matchings par CASCADE).

    Endpoint : DELETE /api/demandes/{demande_id}/supprimer/
    """
    try:
        demande = Demande.objects.get(id=demande_id, user=request.user)
    except Demande.DoesNotExist:
        return Response({'error': 'Demande non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    demande.delete()  # CASCADE → supprime DemandeCreneau + Matching liés automatiquement

    return Response({
        'success': True,
        'message': 'Demande supprimée avec succès.'
    }, status=status.HTTP_200_OK)
# ================================================
# VUES MATCHING
# ================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def matching_demande(request, demande_id):
    """
    Exécute le matching pour une DEMANDE.
    La demande cherche les OFFRES compatibles (mentors potentiels).

    Endpoint : POST /api/matching/demande/{demande_id}/
    """
    try:
        demande = Demande.objects.get(id=demande_id, user=request.user)

        if not DemandeCreneau.objects.filter(demande_id=demande.id).exists():
            return Response(
                {'error': "Cette demande n'a pas de créneaux horaires définis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        algo = MatchingBidirectionnel()
        results = algo.execute_matching_for_demande(demande, min_score=0)

        formatted_results = []
        for result in results:
            offre      = result['offre']
            offre_user = result['offre_user']

            matieres_communes      = algo.get_matieres_communes(offre_user, demande.user)
            disponibilites_communes = algo.get_disponibilites_communes(offre, demande)

            creneaux_offre = [
                {'jour': oc.jour, 'heure_debut': str(oc.heure_debut), 'heure_fin': str(oc.heure_fin)}
                for oc in OffreCreneau.objects.filter(offre_id=offre.id)
            ]

            formatted_results.append({
                'offre_id': offre.id,
                'score': result['score'],
                'mentor': {
                    'id':      offre_user.id,
                    'nom':     offre_user.nom,
                    'prenom':  offre_user.prenom,
                    'photo':   offre_user.photo,
                    'filiere': offre_user.filiere,
                    'niveau':  offre_user.niveau,
                },
                'matieres_communes':       matieres_communes,
                'disponibilites_communes': disponibilites_communes,
                'offre': {
                    'matiere':     offre.matiere,
                    'format':      offre.format,
                    'description': offre.description_offre,
                    'creneaux':    creneaux_offre,
                }
            })

        return Response({
            'success':       True,
            'demande_id':    demande_id,
            'total_results': len(formatted_results),
            'results':       formatted_results
        }, status=status.HTTP_200_OK)

    except Demande.DoesNotExist:
        return Response({'error': 'Demande non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def matching_offre(request, offre_id):
    """
    Exécute le matching pour une OFFRE.
    L'offre cherche les DEMANDES compatibles (mentoés potentiels).

    Endpoint : POST /api/matching/offre/{offre_id}/
    """
    try:
        offre = Offre.objects.get(id=offre_id, user=request.user)

        if not OffreCreneau.objects.filter(offre_id=offre.id).exists():
            return Response(
                {'error': "Cette offre n'a pas de créneaux horaires définis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        algo = MatchingBidirectionnel()
        results = algo.execute_matching_for_offre(offre, min_score=0)

        formatted_results = []
        for result in results:
            demande      = result['demande']
            demande_user = result['demande_user']

            matieres_communes       = algo.get_matieres_communes(offre.user, demande_user)
            disponibilites_communes = algo.get_disponibilites_communes(offre, demande)

            creneaux_demande = [
                {'jour': dc.jour, 'heure_debut': str(dc.heure_debut), 'heure_fin': str(dc.heure_fin)}
                for dc in DemandeCreneau.objects.filter(demande_id=demande.id)
            ]

            formatted_results.append({
                'demande_id': demande.id,
                'score':      result['score'],
                'mentoré': {
                    'id':      demande_user.id,
                    'nom':     demande_user.nom,
                    'prenom':  demande_user.prenom,
                    'photo':   demande_user.photo,
                    'filiere': demande_user.filiere,
                    'niveau':  demande_user.niveau,
                },
                'matieres_communes':       matieres_communes,
                'disponibilites_communes': disponibilites_communes,
                'demande': {
                    'matiere':     demande.matiere,
                    'format':      demande.format,
                    'description': demande.description_demande,
                    'creneaux':    creneaux_demande,
                }
            })

        return Response({
            'success':       True,
            'offre_id':      offre_id,
            'total_results': len(formatted_results),
            'results':       formatted_results
        }, status=status.HTTP_200_OK)

    except Offre.DoesNotExist:
        return Response({'error': 'Offre non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def interface_mentorat(request):
    return render(request, 'IFRI_MentorLink/index.html')

# ================================================
# CONVERSATIONS - CRÉER OU RÉCUPÉRER
# ================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creer_ou_obtenir_conversation(request):
    """
    Crée une nouvelle conversation ou retourne une existante.
    Si une conversation existe déjà entre les deux utilisateurs, elle est retournée.

    Endpoint : POST /api/conversations/creer/

    Body JSON :
    {
        "interlocuteur_id": 2
    }
    """
    user = request.user
    data = request.data
    interlocuteur_id = data.get('interlocuteur_id')

    if not interlocuteur_id:
        return Response(
            {'error': "Le champ 'interlocuteur_id' est obligatoire."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if int(interlocuteur_id) == user.id:
        return Response(
            {'error': "Vous ne pouvez pas démarrer une conversation avec vous-même."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        interlocuteur = User.objects.get(id=interlocuteur_id)
    except User.DoesNotExist:
        return Response(
            {'error': "Utilisateur introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Chercher si une conversation existe déjà
    conversation = Conversation.objects.filter(
        Q(user1=user, user2=interlocuteur) |
        Q(user1=interlocuteur, user2=user)
    ).first()

    if conversation:
        return Response({
            'success': True,
            'message': 'Conversation déjà existante.',
            'conversation_id': conversation.id,
            'created': False
        }, status=status.HTTP_200_OK)

    # Créer une nouvelle conversation
    conversation = Conversation.objects.create(
        user1=user,
        user2=interlocuteur
    )

    return Response({
        'success': True,
        'message': 'Conversation créée avec succès.',
        'conversation_id': conversation.id,
        'created': True
    }, status=status.HTTP_201_CREATED)


# ================================================
# CONVERSATIONS - LISTER
# ================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_conversations(request):
    """
    Retourne toutes les conversations de l'utilisateur connecté,
    triées par date du dernier message.

    Endpoint : GET /api/conversations/
    """
    user = request.user

    conversations = Conversation.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).annotate(
        dernier_message_date=Max('messages__created_at')
    ).order_by('-dernier_message_date')

    liste = []
    total_non_lus = 0

    for conv in conversations:
        # Déterminer l'interlocuteur
        interlocuteur = conv.user2 if conv.user1.id == user.id else conv.user1

        # Récupérer le dernier message
        dernier_msg = conv.messages.order_by('-created_at').first()

        # Compter les messages non lus (reçus par l'utilisateur)
        non_lus = conv.messages.filter(lu=False).exclude(sender=user).count()
        total_non_lus += non_lus

        liste.append({
            'conversation_id': conv.id,
            'interlocuteur': {
                'id': interlocuteur.id,
                'nom': interlocuteur.nom,
                'prenom': interlocuteur.prenom,
                'photo': str(interlocuteur.photo) if interlocuteur.photo else None,
                'filiere': interlocuteur.filiere,
                'niveau': interlocuteur.niveau,
            },
            'dernier_message': dernier_msg.contenu if dernier_msg else None,
            'dernier_message_date': dernier_msg.created_at if dernier_msg else None,
            'messages_non_lus': non_lus,
            'created_at': conv.created_at
        })

    return Response({
        'success': True,
        'total_conversations': len(liste),
        'total_messages_non_lus': total_non_lus,
        'conversations': liste
    }, status=status.HTTP_200_OK)


# ================================================
# CONVERSATIONS - DÉTAIL
# ================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detail_conversation(request, conversation_id):
    """
    Retourne les détails d'une conversation avec l'historique des messages.

    Endpoint : GET /api/conversations/{conversation_id}/

    Query params (optionnel) :
    - page: numéro de page (par défaut: 1)
    - per_page: messages par page (par défaut: 50)
    """
    user = request.user

    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {'error': 'Conversation introuvable.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier que l'utilisateur participe à la conversation
    if conversation.user1.id != user.id and conversation.user2.id != user.id:
        return Response(
            {'error': "Vous n'avez pas accès à cette conversation."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Déterminer l'interlocuteur
    interlocuteur = conversation.user2 if conversation.user1.id == user.id else conversation.user1

    # Marquer les messages de l'interlocuteur comme lus
    Message.objects.filter(
        conversation=conversation,
        lu=False
    ).exclude(sender=user).update(lu=True)

    # Récupérer les messages
    messages = conversation.messages.order_by('-created_at')

    # Pagination simple (optionnel)
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 50))
    start = (page - 1) * per_page
    messages_paginates = messages[start:start + per_page]

    liste_messages = []
    for msg in messages_paginates.reverse():  # Inverser pour l'ordre chronologique
        liste_messages.append({
            'message_id': msg.id,
            'sender': {
                'id': msg.sender.id,
                'nom': msg.sender.nom,
                'prenom': msg.sender.prenom,
                'photo': str(msg.sender.photo) if msg.sender.photo else None,
            },
            'contenu': msg.contenu,
            'lu': msg.lu,
            'created_at': msg.created_at,
            'est_expediteur': msg.sender.id == user.id
        })

    return Response({
        'success': True,
        'conversation_id': conversation.id,
        'interlocuteur': {
            'id': interlocuteur.id,
            'nom': interlocuteur.nom,
            'prenom': interlocuteur.prenom,
            'photo': str(interlocuteur.photo) if interlocuteur.photo else None,
            'filiere': interlocuteur.filiere,
            'niveau': interlocuteur.niveau,
            'bio_courte': interlocuteur.bio_courte,
        },
        'messages': liste_messages,
        'total_messages': conversation.messages.count(),
        'page': page,
        'per_page': per_page
    }, status=status.HTTP_200_OK)


# ================================================
# MESSAGES - ENVOYER
# ================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def envoyer_message(request, conversation_id):
    """
    Envoie un message dans une conversation.

    Endpoint : POST /api/conversations/{conversation_id}/messages/envoyer/

    Body JSON :
    {
        "contenu": "Bonjour, comment ça va ?"
    }
    """
    user = request.user
    data = request.data
    contenu = data.get('contenu', '').strip()

    if not contenu:
        return Response(
            {'error': "Le message ne peut pas être vide."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {'error': 'Conversation introuvable.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier que l'utilisateur participe à la conversation
    if conversation.user1.id != user.id and conversation.user2.id != user.id:
        return Response(
            {'error': "Vous n'êtes pas autorisé à envoyer un message dans cette conversation."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Créer le message
    message = Message.objects.create(
        conversation=conversation,
        sender=user,
        contenu=contenu
    )

    return Response({
        'success': True,
        'message': 'Message envoyé avec succès.',
        'message_id': message.id,
        'created_at': message.created_at
    }, status=status.HTTP_201_CREATED)


# ================================================
# MESSAGES - MARQUER COMME LU
# ================================================

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def marquer_message_comme_lu(request, message_id):
    """
    Marque un message comme lu.

    Endpoint : PUT /api/messages/{message_id}/marquer-lu/
    """
    user = request.user

    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response(
            {'error': 'Message introuvable.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier que l'utilisateur est le destinataire
    if message.sender.id == user.id:
        return Response(
            {'error': "Vous ne pouvez pas marquer votre propre message comme lu."},
            status=status.HTTP_403_FORBIDDEN
        )

    message.lu = True
    message.save()

    return Response({
        'success': True,
        'message': 'Message marqué comme lu.'
    }, status=status.HTTP_200_OK)


# ================================================
# MESSAGES - SUPPRIMER
# ================================================

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_message(request, message_id):
    """
    Supprime un message (uniquement par l'expéditeur).

    Endpoint : DELETE /api/messages/{message_id}/supprimer/
    """
    user = request.user

    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response(
            {'error': 'Message introuvable.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier que l'utilisateur est l'expéditeur
    if message.sender.id != user.id:
        return Response(
            {'error': "Vous ne pouvez supprimer que vos propres messages."},
            status=status.HTTP_403_FORBIDDEN
        )

    message.delete()

    return Response({
        'success': True,
        'message': 'Message supprimé avec succès.'
    }, status=status.HTTP_204_NO_CONTENT)


# ================================================
# CONVERSATIONS - SUPPRIMER
# ================================================

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_conversation(request, conversation_id):
    """
    Supprime une conversation et tous ses messages.

    Endpoint : DELETE /api/conversations/{conversation_id}/supprimer/
    """
    user = request.user

    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {'error': 'Conversation introuvable.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier que l'utilisateur participe à la conversation
    if conversation.user1.id != user.id and conversation.user2.id != user.id:
        return Response(
            {'error': "Vous n'avez pas accès à cette conversation."},
            status=status.HTTP_403_FORBIDDEN
        )

    conversation.delete()  # CASCADE → supprime tous les messages liés

    return Response({
        'success': True,
        'message': 'Conversation supprimée avec succès.'
    }, status=status.HTTP_204_NO_CONTENT)
