# =================================================================
# IFRI MentorLink — Algorithme de Matching Bidirectionnel
# =================================================================
# Critères de scoring :
# - Matière identique      : 40 pts
# - Filière + Niveau       : 30 pts (influencé par difficulté matière)
# - Horaire compatible     : 20 pts (chevauchement >= 1h)
# - Format compatible      : 10 pts
# -----------------------------------------------------------------
# Score maximum : 100 pts
# =================================================================

from datetime import datetime, timedelta
from .models import (
    UserProfile, Offre, Demande, Matching,
    PointFort, Lacune, CreneauOffre, CreneauDemande
)

# =================================================================
# DICTIONNAIRE DE DIFFICULTÉ PAR MATIÈRE ET PAR FILIÈRE
# Echelle de 1.0 (facile) à 5.0 (très difficile)
# =================================================================

DIFFICULTE_MATIERES = {
    "anglais": {
        "gl": 2.0, "ia": 2.0, "im": 2.5, "si": 2.5, "seiot": 2.5
    },
    "analyse": {
        "ia": 4.8, "im": 4.5, "gl": 3.8, "si": 3.5, "seiot": 3.5
    },
    "théorie des graphes": {
        "gl": 4.5, "ia": 4.5, "si": 4.0, "seiot": 3.5, "im": 3.0
    },
    "recherche opérationnelle": {
        "gl": 4.8, "ia": 4.5, "si": 4.0, "im": 3.5, "seiot": 3.5
    },
    "architecture cloud et devops": {
        "gl": 4.5, "si": 4.5, "seiot": 4.0, "ia": 3.5, "im": 3.0
    },
    "cryptographie avancée": {
        "si": 5.0, "gl": 4.0, "ia": 3.8, "seiot": 3.5, "im": 2.0
    },
    "big data et data mining": {
        "ia": 4.8, "im": 4.2, "gl": 4.0, "si": 3.5, "seiot": 3.0
    },
    "systèmes embarqués et rtos": {
        "seiot": 5.0, "si": 4.0, "gl": 3.0, "ia": 2.5, "im": 2.0
    },
    "algorithmique": {
        "gl": 5.0, "ia": 4.5, "im": 4.0, "si": 4.0, "seiot": 3.5
    },
    "programmation python": {
        "ia": 5.0, "gl": 4.0, "si": 4.0, "seiot": 3.5, "im": 3.0
    },
    "programmation java": {
        "gl": 5.0, "si": 4.0, "seiot": 3.5, "im": 2.5, "ia": 2.0
    },
    "structures de données": {
        "gl": 5.0, "ia": 4.5, "si": 4.0, "seiot": 3.0, "im": 3.0
    },
    "mathématiques discrètes": {
        "im": 5.0, "ia": 4.5, "gl": 4.0, "si": 4.0, "seiot": 3.5
    },
    "algèbre linéaire": {
        "ia": 5.0, "im": 4.5, "gl": 3.5, "seiot": 3.0, "si": 3.0
    },
    "probabilités et statistiques": {
        "ia": 5.0, "im": 4.5, "gl": 3.5, "si": 3.0, "seiot": 3.0
    },
    "bases de données (sql)": {
        "gl": 4.5, "si": 4.0, "ia": 4.0, "im": 3.5, "seiot": 2.5
    },
    "réseaux informatiques": {
        "si": 5.0, "seiot": 4.5, "gl": 3.5, "ia": 2.5, "im": 2.0
    },
    "systèmes d'exploitation (linux)": {
        "si": 5.0, "seiot": 4.5, "gl": 4.0, "ia": 3.0, "im": 2.5
    },
    "architecture des ordinateurs": {
        "seiot": 5.0, "si": 4.5, "gl": 3.5, "ia": 3.0, "im": 2.0
    },
    "cybersécurité": {
        "si": 5.0, "seiot": 4.0, "gl": 3.5, "ia": 3.0, "im": 2.0
    }
}

# =================================================================
# MAPPING NIVEAU → VALEUR NUMÉRIQUE
# =================================================================

NIVEAU_VALUES = {
    'L1': 1, 'L2': 2, 'L3': 3,
    'M1': 4, 'M2': 5,
}


# =================================================================
# CLASSE PRINCIPALE
# =================================================================

class MatchingBidirectionnel:
    """
    Algorithme de matching bidirectionnel IFRI MentorLink.

    Score = matiere(40) + filiere_niveau(30) + horaire(20) + format(10)
    Maximum : 100 pts
    """

    # ---------------------------------------------------------------
    # CRITÈRE 1 : MATIÈRE (40 pts)
    # La matière est déjà filtrée en amont → toujours 40 pts ici
    # ---------------------------------------------------------------

    def score_matiere(self):
        return 40

    # ---------------------------------------------------------------
    # CRITÈRE 2 : FILIÈRE + NIVEAU (30 pts)
    # Influencé par la difficulté de la matière dans chaque filière
    # ---------------------------------------------------------------

    def get_difficulte(self, matiere, filiere):
        """
        Retourne la difficulté d'une matière dans une filière.
        Retourne 3.0 (valeur neutre) si matière ou filière inconnue.
        """
        matiere_lower = matiere.lower().strip()
        filiere_lower = filiere.lower().strip()
        return DIFFICULTE_MATIERES.get(matiere_lower, {}).get(filiere_lower, 3.0)

    def score_filiere_niveau(self, offre_user, demande_user, matiere):
        """
        Calcule le score filière + niveau sur 30 pts.

        Logique :
        - Même filière + niveau supérieur offre  : score max
        - Même filière + même niveau             : score moyen
        - Même filière + niveau inférieur offre  : score faible
        - Filière différente                     : score réduit

        La difficulté de la matière dans la filière de l'offre
        augmente le score si elle est élevée (mentor plus spécialisé).
        """

        offre_niveau_val   = NIVEAU_VALUES.get(offre_user.niveau)
        demande_niveau_val = NIVEAU_VALUES.get(demande_user.niveau)

        # Niveau inconnu → 0 pts
        if offre_niveau_val is None or demande_niveau_val is None:
            return 0

        # Difficulté de la matière dans la filière du mentor (offre)
        difficulte_mentor = self.get_difficulte(matiere, offre_user.filiere)

        # Coefficient de difficulté normalisé entre 0.8 et 1.2
        # difficulte entre 1.0 et 5.0 → coeff entre 0.84 et 1.16
        coeff_difficulte = 0.8 + (difficulte_mentor / 5.0) * 0.4

        # Score de base selon filière et niveau
        if offre_user.filiere == demande_user.filiere:
            if offre_niveau_val > demande_niveau_val:
                score_base = 30    # Idéal : même filière, mentor plus avancé
            elif offre_niveau_val == demande_niveau_val:
                score_base = 20    # Même filière, même niveau
            else:
                score_base = 8     # Même filière, mentor moins avancé
        else:
            if offre_niveau_val > demande_niveau_val:
                score_base = 20    # Filière différente, mentor plus avancé
            elif offre_niveau_val == demande_niveau_val:
                score_base = 12    # Filière différente, même niveau
            else:
                score_base = 4     # Filière différente, mentor moins avancé

        # Application du coefficient de difficulté
        score_final = score_base * coeff_difficulte

        # Plafonner à 30 pts maximum
        return min(round(score_final), 30)

    # ---------------------------------------------------------------
    # CRITÈRE 3 : HORAIRE (20 pts)
    # Chevauchement minimum d'1 heure requis
    # ---------------------------------------------------------------

    def get_chevauchement_minutes(self, h1_debut, h1_fin, h2_debut, h2_fin):
        """
        Calcule le nombre de minutes de chevauchement entre deux créneaux.
        Retourne 0 si pas de chevauchement.
        """
        debut_commun = max(h1_debut, h2_debut)
        fin_commune  = min(h1_fin,   h2_fin)

        if debut_commun < fin_commune:
            delta = datetime.combine(
                datetime.today(), fin_commune
            ) - datetime.combine(
                datetime.today(), debut_commun
            )
            return delta.seconds // 60
        return 0

    def score_horaire(self, offre, demande):
        """
        Retourne 20 pts si au moins un couple de créneaux
        (même jour + chevauchement >= 60 minutes), 0 sinon.
        """
        offre_creneaux   = CreneauOffre.objects.filter(offre=offre)
        demande_creneaux = CreneauDemande.objects.filter(demande=demande)

        for oc in offre_creneaux:
            for dc in demande_creneaux:
                if oc.jour == dc.jour:
                    minutes = self.get_chevauchement_minutes(
                        oc.heure_debut, oc.heure_fin,
                        dc.heure_debut, dc.heure_fin
                    )
                    if minutes >= 60:
                        return 20

        return 0

    # ---------------------------------------------------------------
    # CRITÈRE 4 : FORMAT (10 pts)
    # Mixte compatible avec tout
    # ---------------------------------------------------------------

    def score_format(self, format_offre, format_demande):
        """
        Retourne 10 pts si les formats sont compatibles, 0 sinon.

        Règles :
        - mixte    + tout      → 10 pts
        - tout     + mixte     → 10 pts
        - même format          → 10 pts
        - formats différents   → 0 pts
        """
        if format_offre == 'mixte' or format_demande == 'mixte':
            return 10
        if format_offre == format_demande:
            return 10
        return 0

    # ---------------------------------------------------------------
    # SCORE TOTAL
    # ---------------------------------------------------------------

    def calculate_score(self, offre, demande):
        """
        Calcule le score total de compatibilité entre une offre et une demande.
        Score maximum : 100 pts
        """
        score = 0
        score += self.score_matiere()
        score += self.score_filiere_niveau(offre.user, demande.user, offre.matiere)
        score += self.score_horaire(offre, demande)
        score += self.score_format(offre.format, demande.format)
        return score

    # ---------------------------------------------------------------
    # MÉTHODES D'ENRICHISSEMENT DES RÉSULTATS
    # ---------------------------------------------------------------

    def get_matieres_communes(self, offre_user, demande_user):
        """
        Retourne les matières communes entre
        les points forts du mentor et les lacunes du mentoré.
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
        Retourne les créneaux communs avec chevauchement >= 60 minutes.
        """
        offre_creneaux   = CreneauOffre.objects.filter(offre=offre)
        demande_creneaux = CreneauDemande.objects.filter(demande=demande)

        communes = []
        for oc in offre_creneaux:
            for dc in demande_creneaux:
                if oc.jour == dc.jour:
                    minutes = self.get_chevauchement_minutes(
                        oc.heure_debut, oc.heure_fin,
                        dc.heure_debut, dc.heure_fin
                    )
                    if minutes >= 60:
                        debut_commun = max(oc.heure_debut, dc.heure_debut)
                        fin_commune  = min(oc.heure_fin,   dc.heure_fin)
                        communes.append({
                            'jour'       : oc.jour,
                            'heure_debut': str(debut_commun),
                            'heure_fin'  : str(fin_commune),
                            'duree_min'  : minutes
                        })
        return communes

    # ---------------------------------------------------------------
    # CAS 1 : DEMANDE CHERCHE OFFRES
    # ---------------------------------------------------------------

    def execute_matching_for_demande(self, demande, min_score=0):
        """
        Trouve les offres compatibles pour une demande donnée.
        Exclut les offres de l'auteur de la demande.
        """
        offres = Offre.objects.filter(
            matiere=demande.matiere
        ).exclude(
            user=demande.user  # Pas de matching avec soi-même
        )

        results = []
        for offre in offres:
            # Ignorer les offres sans créneaux
            if not CreneauOffre.objects.filter(offre=offre).exists():
                continue

            score = self.calculate_score(offre, demande)

            if score >= min_score:
                results.append({
                    'offre'     : offre,
                    'offre_user': offre.user,
                    'score'     : score
                })

        # Trier par score décroissant
        results.sort(key=lambda x: x['score'], reverse=True)

        # Sauvegarder en base
        for result in results:
            Matching.objects.update_or_create(
                demande=demande,
                offre=result['offre'],
                defaults={'score': result['score']}
            )

        return results

    # ---------------------------------------------------------------
    # CAS 2 : OFFRE CHERCHE DEMANDES
    # ---------------------------------------------------------------

    def execute_matching_for_offre(self, offre, min_score=0):
        """
        Trouve les demandes compatibles pour une offre donnée.
        Exclut les demandes de l'auteur de l'offre.
        """
        demandes = Demande.objects.filter(
            matiere=offre.matiere
        ).exclude(
            user=offre.user  # Pas de matching avec soi-même
        )

        results = []
        for demande in demandes:
            # Ignorer les demandes sans créneaux
            if not CreneauDemande.objects.filter(demande=demande).exists():
                continue

            score = self.calculate_score(offre, demande)

            if score >= min_score:
                results.append({
                    'demande'     : demande,
                    'demande_user': demande.user,
                    'score'       : score
                })

        # Trier par score décroissant
        results.sort(key=lambda x: x['score'], reverse=True)

        # Sauvegarder en base
        for result in results:
            Matching.objects.update_or_create(
                demande=result['demande'],
                offre=offre,
                defaults={'score': result['score']}
            )

        return results

    # ---------------------------------------------------------------
    # RECALCUL APRÈS MODIFICATION DE PROFIL
    # ---------------------------------------------------------------

    def recalculate_matchings_for_user(self, user):
        """
        Recalcule tous les matchings liés à un utilisateur.
        À appeler après modification du profil.
        """
        for demande in Demande.objects.filter(user=user):
            self.execute_matching_for_demande(demande)

        for offre in Offre.objects.filter(user=user):
            self.execute_matching_for_offre(offre)
