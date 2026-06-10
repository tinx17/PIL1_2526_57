# Algorithme de Matching BIDIRECTIONNEL
# ================================================
# - Demande cherche Offres (mentors potentiels)
# - Offre cherche Demandes (mentoés potentiels)
# ================================================

from django.db.models import Q
from .models import (
    User, Offre, Demande, Matching,
    PointFort, Lacune, Conversation, Message,
    OffreCreneau, DemandeCreneau
)
from datetime import time


class MatchingBidirectionnel:
    """
    Classe responsable du calcul du matching BIDIRECTIONNEL.

    VERSION BIDIRECTIONNELLE :
    - Une DEMANDE peut chercher les OFFRES compatibles
    - Une OFFRE peut chercher les DEMANDES compatibles

    Points attribués :
    - Matière identique : 40 pts
    - Filière + Niveau : 40 pts (même formule dans les deux sens)
    - Horaire compatible (au moins 1 chevauchement) : 20 pts
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Score maximum : 100 pts
    """

    # Mapping niveau → valeur numérique
    NIVEAU_VALUES = {
        'L1': 1,
        'L2': 2,
        'L3': 3,
        'M1': 4,
        'M2': 5,
    }

    # Points pour chaque critère
    POINTS = {
        'matiere': 40,
        'filiere_niveau': 40,
        'horaire': 20,
    }

    def __init__(self):
        pass

    # ========================================
    # ÉTAPE 1 : Filtrer par matière
    # ========================================

    def get_offres_by_matiere(self, matiere):
        """Récupère toutes les offres pour une matière donnée"""
        return Offre.objects.filter(matiere=matiere)

    def get_demandes_by_matiere(self, matiere):
        """Récupère toutes les demandes pour une matière donnée"""
        return Demande.objects.filter(matiere=matiere)

    # ========================================
    # ÉTAPE 2 : Calculer points filière + niveau
    # ========================================

    def calculate_filiere_niveau_score(self, offre_user, demande_user):
        """
        Calcule les points pour compatibilité filière + niveau.

        IMPORTANT : Cette fonction est SYMÉTRIQUE
        - offre_user = celui qui enseigne
        - demande_user = celui qui apprend

        La logique reste IDENTIQUE peu importe qui cherche qui.

        Cas 1 : MÊME FILIÈRE
        - Même niveau : +30 pts
        - Niveau inférieur (offre < demande) : +10 pts
        - Niveau supérieur (offre > demande) : +40 pts

        Cas 2 : FILIÈRE DIFFÉRENTE
        - Même niveau : +15 pts
        - Niveau inférieur : +5 pts
        - Niveau supérieur : +25 pts

        Args:
            offre_user (User): Auteur de l'offre (celui qui enseigne)
            demande_user (User): Auteur de la demande (celui qui apprend)

        Returns:
            int: Points attribués (0-40)
        """

        offre_niveau_val = self.NIVEAU_VALUES.get(offre_user.niveau, 0)
        demande_niveau_val = self.NIVEAU_VALUES.get(demande_user.niveau, 0)

        # CAS 1 : MÊME FILIÈRE
        if offre_user.filiere == demande_user.filiere:

            if offre_niveau_val == demande_niveau_val:
                return 30  # Même filière, même niveau

            elif offre_niveau_val < demande_niveau_val:
                return 10  # Même filière, niveau inférieur (mentor moins avancé)

            else:
                return 40  # Même filière, niveau SUPÉRIEUR (idéal)

        # CAS 2 : FILIÈRE DIFFÉRENTE
        else:

            if offre_niveau_val == demande_niveau_val:
                return 15  # Filière différente, même niveau

            elif offre_niveau_val < demande_niveau_val:
                return 5   # Filière différente, niveau inférieur

            else:
                return 25  # Filière différente, niveau SUPÉRIEUR

    # ========================================
    # ÉTAPE 3 : Vérifier chevauchement horaires
    # ========================================

    def have_time_overlap(self, h1_debut, h1_fin, h2_debut, h2_fin):
        """
        Vérifie si deux créneaux horaires se chevauchent.

        Cas 1 : h1 chevauche le début de h2 (h1 finit pendant h2)
                h1_debut <= h2_debut < h1_fin

        Cas 2 : h1 chevauche la fin de h2 (h1 commence pendant h2)
                h1_debut < h2_fin <= h1_fin

        Cas 3 : h1 englobe complètement h2 (h1 commence avant et finit après h2)
                h1_debut <= h2_debut and h2_fin <= h1_fin

        Cas 4 : h1 est imbriqué dans h2 (h1 est plus court et au milieu de h2)
                h2_debut <= h1_debut and h1_fin <= h2_fin

        Si l'un de ces 4 cas est vrai, il y a chevauchement
        """
        cas_debut = (h1_debut <= h2_debut) and (h2_debut < h1_fin)
        cas_fin = (h1_debut < h2_fin) and (h2_fin <= h1_fin)
        cas_englobe = (h1_debut <= h2_debut) and (h2_fin <= h1_fin)
        cas_imbrique = (h2_debut <= h1_debut) and (h1_fin <= h2_fin)
        return cas_debut or cas_fin or cas_englobe or cas_imbrique

    def has_any_horaire_overlap(self, offre, demande):
        """
        Vérifie s'il existe AU MOINS UN chevauchement horaire
        entre TOUS les créneaux de l'offre et TOUS les créneaux de la demande.

        Retourne True si au moins 1 couple (créneau_offre, créneau_demande)
        a un jour identique et un chevauchement horaire.
        """

        # OffreCreneau et DemandeCreneau : noms corrects depuis models.py
        offre_creneaux = OffreCreneau.objects.filter(offre_id=offre.id)
        demande_creneaux = DemandeCreneau.objects.filter(demande_id=demande.id)

        for oc in offre_creneaux:
            for dc in demande_creneaux:

                if oc.jour == dc.jour:
                    if self.have_time_overlap(
                        oc.heure_debut, oc.heure_fin,
                        dc.heure_debut, dc.heure_fin
                    ):
                        return True

        return False

    def calculate_horaire_score(self, offre, demande):
        """
        Calcule les points pour compatibilité horaire.

        Returns: 20 si au moins 1 chevauchement, 0 sinon
        """

        if self.has_any_horaire_overlap(offre, demande):
            return 20
        else:
            return 0

    # ========================================
    # CALCUL FINAL DU SCORE (SYMÉTRIQUE)
    # ========================================

    def calculate_score(self, offre, demande):
        """
        Calcule le score de compatibilité entre une offre et une demande.

        IMPORTANT : Cette fonction est SYMÉTRIQUE
        - Peu importe qui cherche qui (demande→offre ou offre→demande)
        - La formule reste IDENTIQUE
        - offre_user = mentor (celui qui enseigne)
        - demande_user = mentoré (celui qui apprend)

        Score = 40 (matière) + filière_niveau_score + horaire_score
        Max = 100 points
        """

        score = 0

        # Étape 1 : Matière identique
        score += self.POINTS['matiere']  # +40

        # Étape 2 : Filière + Niveau
        offre_user = offre.user
        demande_user = demande.user

        filiere_niveau_score = self.calculate_filiere_niveau_score(
            offre_user, demande_user
        )
        score += filiere_niveau_score  # +0 à +40

        # Étape 3 : Horaire
        horaire_score = self.calculate_horaire_score(offre, demande)
        score += horaire_score  # +0 ou +20

        return score

    # ========================================
    # MÉTHODES D'ENRICHISSEMENT DES RÉSULTATS
    # ========================================

    def get_matieres_communes(self, offre_user, demande_user):
        """
        Retourne la liste des matières en commun entre :
        - les points_forts du mentor (offre_user)
        - les lacunes du mentoré (demande_user)
        """
        points_forts = set(
            PointFort.objects.filter(user=offre_user).values_list('matiere', flat=True)
        )
        lacunes = set(
            Lacune.objects.filter(user=demande_user).values_list('matiere', flat=True)
        )
        return list(points_forts & lacunes)

    def get_disponibilites_communes(self, offre, demande):
        """
        Retourne la liste des créneaux communs (jour + plage horaire qui se chevauche)
        entre une offre et une demande.
        """
        offre_creneaux = OffreCreneau.objects.filter(offre_id=offre.id)
        demande_creneaux = DemandeCreneau.objects.filter(demande_id=demande.id)

        communes = []
        for oc in offre_creneaux:
            for dc in demande_creneaux:
                if oc.jour == dc.jour:
                    if self.have_time_overlap(
                        oc.heure_debut, oc.heure_fin,
                        dc.heure_debut, dc.heure_fin
                    ):
                        # Intersection exacte des deux plages
                        debut_commun = max(oc.heure_debut, dc.heure_debut)
                        fin_commune = min(oc.heure_fin, dc.heure_fin)
                        communes.append({
                            'jour': oc.jour,
                            'heure_debut': str(debut_commun),
                            'heure_fin': str(fin_commune),
                        })
        return communes

    # ========================================
    # CAS 1 : DEMANDE CHERCHE OFFRES (mentors)
    # ========================================

    def execute_matching_for_demande(self, demande, min_score=0):
        """
        Exécute le matching pour une DEMANDE.

        Une demande cherche les OFFRES compatibles (mentors potentiels).

        Direction : Demande → Offres

        Args:
            demande (Demande): La demande
            min_score (int): Score minimum (défaut: 0)

        Returns:
            list: Liste des matchings triés par score
        """

        # ÉTAPE 1 : Récupérer les offres pour cette matière
        offres = self.get_offres_by_matiere(demande.matiere)

        # ÉTAPE 2 : Calculer les scores
        matching_results = []

        for offre in offres:
            # Vérifier que l'offre a au moins 1 créneau
            if not OffreCreneau.objects.filter(offre_id=offre.id).exists():
                continue

            score = self.calculate_score(offre, demande)

            if score >= min_score:
                matching_results.append({
                    'offre': offre,
                    'score': score,
                    'offre_user': offre.user
                })

        # ÉTAPE 3 : Trier par score décroissant
        matching_results.sort(key=lambda x: x['score'], reverse=True)

        # ÉTAPE 4 : Sauvegarder dans la table matchings
        for result in matching_results:
            Matching.objects.update_or_create(
                demande=demande,
                offre=result['offre'],
                defaults={'score': result['score']}
            )

        return matching_results

    # ========================================
    # CAS 2 : OFFRE CHERCHE DEMANDES (mentoés)
    # ========================================

    def execute_matching_for_offre(self, offre, min_score=0):
        """
        Exécute le matching pour une OFFRE.

        Une offre cherche les DEMANDES compatibles (mentoés potentiels).

        Direction : Offre → Demandes

        Args:
            offre (Offre): L'offre
            min_score (int): Score minimum (défaut: 0)

        Returns:
            list: Liste des matchings triés par score
        """

        # ÉTAPE 1 : Récupérer les demandes pour cette matière
        demandes = self.get_demandes_by_matiere(offre.matiere)

        # ÉTAPE 2 : Calculer les scores
        matching_results = []

        for demande in demandes:
            # Vérifier que la demande a au moins 1 créneau
            if not DemandeCreneau.objects.filter(demande_id=demande.id).exists():
                continue

            score = self.calculate_score(offre, demande)

            if score >= min_score:
                matching_results.append({
                    'demande': demande,
                    'score': score,
                    'demande_user': demande.user
                })

        # ÉTAPE 3 : Trier par score décroissant
        matching_results.sort(key=lambda x: x['score'], reverse=True)

        # ÉTAPE 4 : Sauvegarder dans la table matchings
        for result in matching_results:
            Matching.objects.update_or_create(
                demande=result['demande'],
                offre=offre,
                defaults={'score': result['score']}
            )

        return matching_results

    # ========================================
    # RECALCULER SI CHANGEMENT DE PROFIL
    # ========================================

    def recalculate_matchings_for_user(self, user):
        """
        Recalcule TOUS les matchings concernant cet utilisateur.

        Inclut :
        - Les demandes créées par cet user (cherchent des offres)
        - Les offres créées par cet user (cherchent des demandes)
        """

        demandes = Demande.objects.filter(user=user)
        for demande in demandes:
            self.execute_matching_for_demande(demande)

        offres = Offre.objects.filter(user=user)
        for offre in offres:
            self.execute_matching_for_offre(offre)
