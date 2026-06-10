import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from accounts.models import Matiere
from matching.models import OffreMentorat, Matching
from messaging.models import Conversation, Message

UserProfile = get_user_model()

class Command(BaseCommand):
    help = "Peuple la base de données avec des données de test professionnelles et propres pour l'IFRI"

    def handle(self, *args, **options):
        self.stdout.write("Nettoyage de la base de données...")
        
        # Supprimer les données existantes pour éviter les conflits et doublons
        Message.objects.all().delete()
        Conversation.objects.all().delete()
        Matching.objects.all().delete()
        OffreMentorat.objects.all().delete()
        UserProfile.objects.all().delete()
        Matiere.objects.all().delete()

        self.stdout.write("Création des matières prédéfinies...")
        matieres_noms = [
            "React", "Node.js", "Python", "Java", "C++", "TypeScript", "SQL",
            "Machine Learning", "DevOps", "Cybersécurité", "Algorithmique", "UML",
            "Cloud AWS", "Linux", "GraphQL", "Statistiques"
        ]
        
        matieres_obj = {}
        for nom in matieres_noms:
            mat, _ = Matiere.objects.get_or_create(nom=nom)
            matieres_obj[nom] = mat

        self.stdout.write("Création des profils utilisateurs de test...")
        
        users_data = [
            {
                "email": "eckson.ahouansou@uac.bj",
                "nom": "AHOUANSOU",
                "prenom": "Eckson",
                "telephone": "+22990909090",
                "filiere": "GL",
                "niveau": "L3",
                "bio": "Étudiant en L3 Génie Logiciel passionné par le Web et les bases de données.",
                "disponibilites": {"lundi": ["8h-10h", "14h-16h"], "mercredi": ["16h-18h"]},
                "competences": ["React", "Python", "Algorithmique"],
                "lacunes": ["SQL", "DevOps"]
            },
            {
                "email": "giovanni.gbasse@uac.bj",
                "nom": "GBASSE",
                "prenom": "Giovanni",
                "telephone": "+22991919191",
                "filiere": "IA",
                "niveau": "L2",
                "bio": "Intéressé par le Machine Learning et la programmation Python.",
                "disponibilites": {"mardi": ["10h-12h"], "jeudi": ["14h-16h"]},
                "competences": ["Python", "Machine Learning", "Statistiques"],
                "lacunes": ["React", "TypeScript"]
            },
            {
                "email": "exaucee.bognon@uac.bj",
                "nom": "BOGNON",
                "prenom": "Exaucée",
                "telephone": "+22992929292",
                "filiere": "SI",
                "niveau": "L3",
                "bio": "Future experte en sécurité informatique et administration système Linux.",
                "disponibilites": {"vendredi": ["8h-10h", "18h-20h"]},
                "competences": ["Cybersécurité", "Linux", "SQL"],
                "lacunes": ["GraphQL", "React"]
            },
            {
                "email": "malik.fagnon@uac.bj",
                "nom": "FAGNON",
                "prenom": "Malik",
                "telephone": "+22993939393",
                "filiere": "IM",
                "niveau": "L1",
                "bio": "Débutant motivé à l'IFRI en Licence 1 Internet & Multimédia.",
                "disponibilites": {"lundi": ["14h-16h"], "mardi": ["10h-12h"]},
                "competences": ["TypeScript", "UML"],
                "lacunes": ["Algorithmique", "Python"]
            },
            {
                "email": "royal.ahoumenou@uac.bj",
                "nom": "AHOUMENOU",
                "prenom": "Royal",
                "telephone": "+22994949494",
                "filiere": "SE_IoT",
                "niveau": "L2",
                "bio": "Passionné par l'IoT, Arduino et les microcontrôleurs.",
                "disponibilites": {"mercredi": ["16h-18h"], "jeudi": ["14h-16h"]},
                "competences": ["C++", "Linux", "DevOps"],
                "lacunes": ["Python", "Machine Learning"]
            }
        ]

        users_obj = {}
        for ud in users_data:
            user = UserProfile.objects.create_user(
                username=ud["email"],
                email=ud["email"],
                nom=ud["nom"],
                prenom=ud["prenom"],
                telephone=ud["telephone"],
                password="password123", # Mot de passe commun pour les tests
                filiere=ud["filiere"],
                niveau=ud["niveau"],
                bio=ud["bio"],
                disponibilites=ud["disponibilites"]
            )
            
            for c in ud["competences"]:
                user.competences.add(matieres_obj[c])
            for l in ud["lacunes"]:
                user.lacunes.add(matieres_obj[l])
                
            user.save()
            users_obj[ud["email"]] = user
            self.stdout.write(f"Utilisateur créé : {user.get_full_name()} ({ud['email']})")

        self.stdout.write("Création des offres et demandes de mentorat...")
        
        # Offre de Eckson
        o1 = OffreMentorat.objects.create(
            auteur=users_obj["eckson.ahouansou@uac.bj"],
            type="offre",
            format="les_deux",
            description="Je propose mon aide pour le développement frontend avec React ou pour préparer les TPs d'algorithmique.",
            disponibilites={"lundi": ["8h-10h"], "mercredi": ["16h-18h"]},
            statut="active"
        )
        o1.matieres.add(matieres_obj["React"], matieres_obj["Algorithmique"])

        # Offre de Giovanni
        o2 = OffreMentorat.objects.create(
            auteur=users_obj["giovanni.gbasse@uac.bj"],
            type="offre",
            format="en_ligne",
            description="Tutorat en Python et initiation au Machine Learning.",
            disponibilites={"mardi": ["10h-12h"]},
            statut="active"
        )
        o2.matieres.add(matieres_obj["Python"], matieres_obj["Machine Learning"])

        # Demande de Malik
        o3 = OffreMentorat.objects.create(
            auteur=users_obj["malik.fagnon@uac.bj"],
            type="demande",
            format="presentiel",
            description="Recherche de l'aide en algorithmique pour mieux comprendre la complexité des algorithmes et les structures de données.",
            disponibilites={"lundi": ["14h-16h"]},
            statut="active"
        )
        o3.matieres.add(matieres_obj["Algorithmique"])

        self.stdout.write("Création des conversations et messages de test...")
        
        # Conversation entre Malik (mentorable) et Eckson (mentor)
        c1 = Conversation.objects.create()
        c1.participants.add(users_obj["malik.fagnon@uac.bj"], users_obj["eckson.ahouansou@uac.bj"])
        c1.save()

        # Messages
        m1 = Message.objects.create(
            conversation=c1,
            auteur=users_obj["malik.fagnon@uac.bj"],
            contenu="Bonjour Eckson, j'ai vu que tu proposes du mentorat en Algorithmique. J'aurais besoin d'aide pour le prochain TP.",
            lu=True
        )
        m1.date_envoi = timezone.now() - timedelta(hours=1)
        m1.save()

        m2 = Message.objects.create(
            conversation=c1,
            auteur=users_obj["eckson.ahouansou@uac.bj"],
            contenu="Salut Malik ! Avec plaisir. On peut s'organiser un créneau en présentiel à la bibliothèque de l'IFRI.",
            lu=True
        )
        m2.date_envoi = timezone.now() - timedelta(minutes=45)
        m2.save()

        m3 = Message.objects.create(
            conversation=c1,
            auteur=users_obj["malik.fagnon@uac.bj"],
            contenu="Super ! Le lundi à 14h te convient-il ?",
            lu=False
        )
        m3.date_envoi = timezone.now() - timedelta(minutes=30)
        m3.save()

        self.stdout.write(self.style.SUCCESS("Base de données peuplée avec succès !"))
        self.stdout.write("Comptes créés :")
        for email in users_obj.keys():
            self.stdout.write(f"  - {email} / Mot de passe : password123")
