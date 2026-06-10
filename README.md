# IFRI_MentorLink — Groupe 57 (PIL1_2526_57)

**Plateforme de mentorat académique et professionnel** développée dans le cadre du Projet Intégrateur de Licence (PIL1 – 2025-2026) à l'Institut de Formation et de Recherche en Informatique (IFRI), Université d'Abomey-Calavi (UAC), Bénin.

---

## Description du Projet

IFRI_MentorLink met en relation des étudiants souhaitant offrir ou recevoir du mentorat académique et professionnel. L'application propose :

* **Backend** : Django monolithique fournissant des endpoints API REST sécurisés et gérant les connexions WebSocket.
* **Frontend** : Client léger statique écrit en HTML5, CSS3 (variables modernes, animations fluides) et JavaScript (Vanilla ES6).

---

## Fonctionnalités Clés (Conformité Specs)

La plateforme implémente l'intégralité des spécifications du cahier des charges :

1. **Gestion des comptes & Authentification** :
   * Inscription sécurisée avec vérification d'unicité de l'email et du téléphone.
   * Connexion flexible via l'adresse email **ou** le numéro de téléphone (via un backend d'authentification personnalisé).
   * Module de réinitialisation sécurisée de mot de passe en cas d'oubli.
2. **Profils Utilisateurs Riches** :
   * Informations académiques (choix restrictif parmi 5 filières et 5 niveaux d'études).
   * Photo de profil personnalisable (upload, prévisualisation en direct et suppression).
   * Saisie des compétences (matières maîtrisées) et des lacunes (matières à améliorer) sous forme de puces interactives.
   * Grille hebdomadaire de disponibilités (calendrier interactif Lun-Dim x 8h-20h) enregistrée au format JSON structuré.
   * Biographie et centres d'intérêt libres.
3. **Mise en Relation & Publication** :
   * Publication d'**Offres** (mentorat proposé) et de **Demandes** (aide recherchée) avec matières, formats (présentiel, en ligne, ou les deux), et disponibilités.
   * Filtrage avancé par matière et format.
4. **Algorithme de Matching Intelligent** :
   * Calcul en temps réel d'un score de compatibilité entre utilisateurs basé sur les pondérations suivantes :
     * **50%** : Recoupement des compétences du mentor avec les lacunes du mentoré.
     * **30%** : Recoupement des disponibilités horaires communes.
     * **20%** : Proximité académique (filières et niveaux d'études identiques ou proches).
   * Présentation claire des correspondances avec badge de score (%), compétences communes, et créneaux horaires partagés.
5. **Messagerie Instantanée en Temps Réel** :
   * Échanges instantanés bidirectionnels via WebSockets (Django Channels + ASGI Daphne).
   * Persistance historique complète en base de données.
   * Notifications visuelles immédiates et badges de messages non lus intégrés dans la barre de navigation.

---

## Stack Technique

| Composant | Technologie |
|-----------|-------------|
| **Système** | Python 3.10+ |
| **Backend Framework** | Django 6.0.6 |
| **Temps réel (WebSocket)** | Django Channels + Daphne ASGI |
| **Base de Données** | PostgreSQL (Production & Local) |
| **Cache & Canal Messages** | Redis (ou InMemory en fallback) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Gestion d'icônes** | Lucide Icons |

---

## Structure du Projet

```
PIL1_2526_57/
├── manage.py               # Script de gestion Django
├── mentorlink/             # Configuration globale du projet Django
│   ├── settings.py         # Fichier de configuration
│   ├── middleware.py       # Middleware CORS personnalisé
│   └── urls.py             # Routage racine des applications
├── accounts/               # Module de gestion des comptes, profils et API Auth
├── matching/               # Module de calcul de compatibilité et offres/demandes
├── messaging/              # Module de messagerie WebSocket temps réel
├── frontend/               # Fichiers statiques du client (Interface Utilisateur)
│   ├── CSS/                # Feuilles de styles
│   ├── JS/                 # Fichiers logiques (script.js, profil.js, etc.)
│   └── pages/              # Pages HTML de l'application
├── static/                 # Fichiers statiques collectés
├── templates/              # Templates HTML globaux
├── bd/                     # Dump SQL de la structure finale
├── run_project.bat         # Script de démarrage rapide pour Windows
└── run_project.sh          # Script de démarrage rapide pour Linux/macOS
```

---

## Procédure de Lancement et Configuration

### Étape 1 : Cloner le projet
```bash
git clone https://github.com/tinx17/PIL1_2526_57.git
cd PIL1_2526_57
```

### Étape 2 : Créer et activer l'environnement virtuel
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### Étape 3 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 4 : Configurer le fichier d'environnement `.env`
Dupliquez le fichier `.env.example` et renommez-le en `.env` :
```bash
cp .env.example .env
```
Renseignez vos identifiants PostgreSQL et la configuration de l'application dans `.env` :
```ini
SECRET_KEY=votre_cle_secrete_django
DB_ENGINE=postgresql
DB_NAME=mentorlink_db
DB_USER=votre_utilisateur_postgres
DB_PASSWORD=votre_mot_de_passe_postgres
DB_HOST=127.0.0.1
DB_PORT=5432
CHANNEL_BACKEND=memory  # Utilisez 'redis' en production ou si Redis est installé localement
```

### Étape 5 : Préparer la Base de Données PostgreSQL
1. Assurez-vous que votre service PostgreSQL est démarré.
2. Créez la base de données vide nommée `mentorlink_db` via PgAdmin ou la console SQL :
   ```sql
   CREATE DATABASE mentorlink_db;
   ```

### Étape 6 : Appliquer les migrations & Initialiser les données (seed_db)
Exécutez les commandes Django pour configurer la base de données et créer les matières de base ainsi que les comptes étudiants de test :
```bash
python manage.py migrate
python manage.py seed_db
```
*Note : La commande `seed_db` réinitialise proprement la base et crée 5 comptes étudiants de test à l'IFRI avec des profils complets, des historiques de messagerie et des offres. Le mot de passe de tous ces comptes de test est `password123`.*

---

## Exécution de l'Application

### Option A : Démarrage Rapide (Recommandé)
Les scripts de démarrage lancent automatiquement le serveur backend Django sur le port **8000** et le serveur HTTP statique frontend sur le port **8080**.

* **Sur Windows** : Double-cliquez sur le fichier `run_project.bat` (ou lancez `.\run_project.bat` dans la console Windows).
* **Sur Linux/macOS** : Rendez le script exécutable et lancez-le :
  ```bash
  chmod +x run_project.sh
  ./run_project.sh
  ```

### Option B : Démarrage Manuel (Deux terminaux distincts)
1. **Démarrer le Backend** :
   ```bash
   python manage.py runserver 8000
   ```
2. **Démarrer le Frontend** :
   ```bash
   # Depuis la racine du projet
   python -m http.server 8080 --directory frontend
   ```

Une fois démarré, accédez au site web via l'adresse : **`http://localhost:8080`**

---

## 🔍 Guide de Résolution des Problèmes (Dépannage)

Si vous rencontrez un message **"Erreur avec le serveur backend"** ou **"Erreur de connexion au serveur backend"** lors de l'inscription ou de la connexion, veuillez suivre ces points de vérification :

1. **Le serveur backend n'est pas démarré** :
   Assurez-vous que la console exécutant `python manage.py runserver 8000` est bien active et ne contient aucune erreur de lancement.
2. **Base de données PostgreSQL inaccessible (Erreur HTTP 500)** :
   Si le service PostgreSQL n'est pas démarré sur votre machine, ou si les identifiants dans le fichier `.env` sont incorrects, Django ne pourra pas se connecter à la base de données. Toute tentative d'écriture (ex : Inscription) ou de lecture renverra une erreur HTTP 500 (Internal Server Error). Vérifiez les logs de votre console Django pour confirmer si une exception de connexion SQL y est affichée.
3. **Protocole `file://` interdit par les navigateurs** :
   N'ouvrez pas les fichiers HTML du frontend en double-cliquant directement dessus depuis votre explorateur de fichiers (ce qui donne une URL du type `file:///C:/...`). Les politiques de sécurité CORS des navigateurs modernes bloquent le protocole `file://` pour les requêtes dynamiques (`fetch`). Vous devez obligatoirement passer par le serveur local frontend à l'adresse `http://localhost:8080`.
4. **Ports déjà utilisés** :
   Si le port 8000 ou 8080 est déjà utilisé par une autre application, les serveurs ne pourront pas démarrer. Vous pouvez libérer les ports ou les modifier dans vos commandes de lancement (ex: `python manage.py runserver 8001` et modifier l'adresse dans `frontend/JS/script.js`).

---

## Groupe 57 — Répartition des Rôles

Le développement a été structuré selon une répartition équilibrée des tâches pour assurer la cohérence et le respect des contraintes académiques :

| Membre de l'Équipe | Rôle Principal |
|--------------------|----------------|
| **Royal AHOUMENOU** | Chef de projet & Architecte Backend |
| **Giovanni GBASSE** | Développeur Backend & SQL |
| **Eckson AHOUANSOU** | Designer Graphique, Dev Front-End & Intégrateur |
| **Exaucée BOGNON** | Développeuse Front-End |
| **Malik FAGNON** | Développeur Front-End & Ingénieur QA |

---

## Licence

Ce projet est réalisé dans un cadre académique au sein de l'IFRI, Université d'Abomey-Calavi (UAC), dans le cadre du Projet Intégrateur de Licence 1.
