"""
Moteur de matching — Algorithme de mise en correspondance.

Calcule un score de compatibilité entre deux utilisateurs
basé sur trois critères pondérés :
  1. Compétences / Lacunes (50%)
  2. Disponibilités horaires (30%)
  3. Proximité filière / niveau (20%)
"""

from django.contrib.auth import get_user_model

UserProfile = get_user_model()


def calculer_score_competences(user_a, user_b):
    """
    Calcule le score de compatibilité compétences/lacunes.
    
    Mesure combien de compétences de user_a correspondent
    aux lacunes de user_b.
    
    Score = len(compétences_A ∩ lacunes_B) / max(len(lacunes_B), 1)
    
    Args:
        user_a: L'utilisateur offrant des compétences (potentiel mentor)
        user_b: L'utilisateur ayant des lacunes (potentiel mentoré)
    
    Returns:
        float: Score entre 0.0 et 1.0
    """
    competences_a = set(user_a.competences.values_list('id', flat=True))
    lacunes_b = set(user_b.lacunes.values_list('id', flat=True))

    if not lacunes_b:
        return 0.0

    intersection = competences_a & lacunes_b
    score = len(intersection) / max(len(lacunes_b), 1)

    return min(score, 1.0)


def calculer_score_disponibilites(user_a, user_b):
    """
    Calcule le score de compatibilité des disponibilités horaires.
    
    Compare les créneaux disponibles jour par jour et retourne
    un score proportionnel aux créneaux communs.
    
    Args:
        user_a: Premier utilisateur
        user_b: Deuxième utilisateur
    
    Returns:
        tuple: (score float entre 0.0 et 1.0, dict des créneaux communs)
    """
    dispo_a = user_a.disponibilites or {}
    dispo_b = user_b.disponibilites or {}

    if not dispo_a or not dispo_b:
        return 0.0, {}

    # Jours de la semaine
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

    total_creneaux = 0
    creneaux_communs = 0
    disponibilites_communes = {}

    for jour in jours:
        creneaux_a = set(dispo_a.get(jour, []))
        creneaux_b = set(dispo_b.get(jour, []))

        # Compter le total de créneaux possibles (union)
        total_creneaux += len(creneaux_a | creneaux_b) if (creneaux_a or creneaux_b) else 0

        # Trouver les créneaux communs
        communs = creneaux_a & creneaux_b
        creneaux_communs += len(communs)

        if communs:
            disponibilites_communes[jour] = sorted(list(communs))

    if total_creneaux == 0:
        return 0.0, {}

    score = creneaux_communs / total_creneaux
    return min(score, 1.0), disponibilites_communes


def calculer_score_filiere_niveau(user_a, user_b):
    """
    Calcule le score de proximité filière/niveau.
    
    - Même filière = 1.0, filières différentes = 0.3
    - Même niveau = +0.5 bonus (pondéré)
    
    Le score final est normalisé entre 0.0 et 1.0.
    
    Args:
        user_a: Premier utilisateur
        user_b: Deuxième utilisateur
    
    Returns:
        float: Score entre 0.0 et 1.0
    """
    score = 0.0

    # Score de filière (poids principal)
    if user_a.filiere and user_b.filiere:
        if user_a.filiere == user_b.filiere:
            score += 1.0
        else:
            score += 0.3
    else:
        score += 0.5  # Filière non renseignée

    # Bonus de niveau
    if user_a.niveau and user_b.niveau:
        if user_a.niveau == user_b.niveau:
            score += 0.5

    # Normaliser entre 0 et 1
    score = score / 1.5  # Score max possible = 1.5

    return min(score, 1.0)


def calculate_score(user_a, user_b):
    """
    Calcule le score global de compatibilité entre deux utilisateurs.
    
    Pondération :
      - Compétences / Lacunes : 50%
      - Disponibilités horaires : 30%
      - Proximité filière / niveau : 20%
    
    Args:
        user_a: Premier utilisateur
        user_b: Deuxième utilisateur
    
    Returns:
        dict: {
            'score': float (0.0 à 1.0),
            'score_competences': float,
            'score_disponibilites': float,
            'score_filiere': float,
            'disponibilites_communes': dict,
            'matieres_communes_ids': list
        }
    """
    # 1. Score compétences/lacunes (bidirectionnel — on prend le meilleur)
    score_comp_ab = calculer_score_competences(user_a, user_b)
    score_comp_ba = calculer_score_competences(user_b, user_a)
    score_competences = max(score_comp_ab, score_comp_ba)

    # 2. Score disponibilités
    score_dispo, dispo_communes = calculer_score_disponibilites(user_a, user_b)

    # 3. Score filière/niveau
    score_filiere = calculer_score_filiere_niveau(user_a, user_b)

    # Score global pondéré
    score_global = (
        score_competences * 0.50 +
        score_dispo * 0.30 +
        score_filiere * 0.20
    )

    # Déterminer les matières communes (compétences de A ∩ lacunes de B et vice-versa)
    comp_a = set(user_a.competences.values_list('id', flat=True))
    lac_b = set(user_b.lacunes.values_list('id', flat=True))
    comp_b = set(user_b.competences.values_list('id', flat=True))
    lac_a = set(user_a.lacunes.values_list('id', flat=True))

    matieres_communes_ids = list((comp_a & lac_b) | (comp_b & lac_a))

    return {
        'score': round(score_global, 3),
        'score_competences': round(score_competences, 3),
        'score_disponibilites': round(score_dispo, 3),
        'score_filiere': round(score_filiere, 3),
        'disponibilites_communes': dispo_communes,
        'matieres_communes_ids': matieres_communes_ids,
    }


def get_suggestions(user, limit=10):
    """
    Récupère les meilleures suggestions de matching pour un utilisateur.
    
    Calcule le score de compatibilité avec tous les autres utilisateurs
    actifs et retourne les N meilleures suggestions triées par score
    décroissant.
    
    Args:
        user: L'utilisateur pour lequel chercher des suggestions
        limit: Nombre maximum de suggestions à retourner (défaut: 10)
    
    Returns:
        list: Liste de dicts triés par score décroissant, chaque dict contenant :
            - 'utilisateur': l'objet UserProfile
            - 'score': score global
            - 'score_competences': détail du score compétences
            - 'score_disponibilites': détail du score disponibilités
            - 'score_filiere': détail du score filière/niveau
            - 'disponibilites_communes': créneaux communs
            - 'matieres_communes': QuerySet des matières communes
    """
    from accounts.models import Matiere

    # Récupérer tous les utilisateurs actifs sauf l'utilisateur courant
    autres_utilisateurs = UserProfile.objects.filter(
        is_active=True
    ).exclude(
        pk=user.pk
    ).prefetch_related('competences', 'lacunes')

    suggestions = []

    for autre in autres_utilisateurs:
        # Calculer le score de compatibilité
        resultat = calculate_score(user, autre)

        # Ne garder que les suggestions avec un score minimum
        if resultat['score'] > 0.0:
            # Récupérer les objets Matière pour les matières communes
            matieres_communes = Matiere.objects.filter(
                id__in=resultat['matieres_communes_ids']
            )

            suggestions.append({
                'utilisateur': autre,
                'score': resultat['score'],
                'score_percentage': int(resultat['score'] * 100),
                'score_competences': resultat['score_competences'],
                'score_disponibilites': resultat['score_disponibilites'],
                'score_filiere': resultat['score_filiere'],
                'disponibilites_communes': resultat['disponibilites_communes'],
                'matieres_communes': matieres_communes,
            })

    # Trier par score décroissant et limiter
    suggestions.sort(key=lambda x: x['score'], reverse=True)

    return suggestions[:limit]
