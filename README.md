# IFRI_MentorLink — Groupe 57 (PIL1_2526_57)

Plateforme monolithique de mentorat académique et professionnel développée avec Django pour les étudiants de l'IFRI, Université d'Abomey-Calavi, Bénin.

**Plateforme de mentorat académique et professionnel** développée dans le cadre du Projet Intégrateur de Licence (PIL1 – 2025-2026) à l'IFRI, Université d'Abomey-Calavi, Bénin.

## 🎯 Description

IFRI_MentorLink met en relation des étudiants souhaitant offrir ou recevoir du mentorat académique et professionnel. L'application propose :

- **Gestion de profils** : inscription, connexion, gestion des compétences et lacunes
- **Matching intelligent** : algorithme de mise en correspondance basé sur les compétences, disponibilités et filières
- **Messagerie instantanée** : communication en temps réel via WebSockets

## 📋 Prérequis

- **Python** 3.10 ou supérieur
- **PostgreSQL** 14 ou supérieur
- **Redis** 6 ou supérieur (pour les WebSockets)
- **pip** (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/PIL1_2526_57.git
cd PIL1_2526_57
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Éditez le fichier `.env` avec vos propres valeurs :
- `SECRET_KEY` : clé secrète Django
- `DB_ENGINE` : `postgresql` (par défaut) ou `sqlite` (pour tester localement sans serveur PostgreSQL)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` : identifiants PostgreSQL
- `REDIS_URL` : URL du serveur Redis

*Note: Si vous définissez `DB_ENGINE=sqlite`, l'application utilisera automatiquement une base de données SQLite locale (`db.sqlite3`) et basculera le serveur de messages Django Channels en mode In-Memory (pas besoin de Redis). C'est idéal pour tester le projet rapidement.*

### 5. Créer la base de données PostgreSQL (Si utilisation de PostgreSQL)

```bash
sudo -u postgres psql
CREATE DATABASE mentorlink_db;
CREATE USER votre_user WITH PASSWORD 'votre_password';
ALTER ROLE votre_user SET client_encoding TO 'utf8';
ALTER ROLE votre_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE votre_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mentorlink_db TO votre_user;
\q
```

Ou importez directement le dump SQL :

```bash
sudo -u postgres psql mentorlink_db < bd/structure_bd_finale.sql
```

### 6. Appliquer les migrations

```bash
python manage.py migrate
```

### 7. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 8. Initialiser avec les données de test (Recommandé)

Pour peupler directement la base avec les matières prédéfinies et des comptes de test fictifs de l'IFRI avec historique de chat et offres de mentorat, exécutez la commande personnalisée :

```bash
python manage.py seed_db
```

*Note: Cette commande crée 5 utilisateurs de test (Eckson, Giovanni, Exaucée, Malik, Royal) ayant tous pour mot de passe `password123`.*


### 9. Lancer Redis

```bash
redis-server
```

### 10. Lancer le serveur

**En développement :**

```bash
python manage.py runserver
```

**En production (avec Daphne pour les WebSockets) :**

```bash
daphne mentorlink.asgi:application
```

L'application est accessible sur [http://localhost:8000](http://localhost:8000).

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python + Django 4.2+ |
| Base de données | PostgreSQL |
| Temps réel | Django Channels + Redis |
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Authentification | Django built-in auth + sessions |
| Serveur ASGI | Daphne |

## 📁 Structure du projet

```
PIL1_2526_57/
├── manage.py
├── mentorlink/             # Configuration principale du projet Django
├── accounts/               # Application gestion des comptes, profils et authentification
├── matching/               # Application algorithme de matching et offres/demandes
├── messaging/              # Application messagerie instantanée en temps réel (WebSockets)
├── frontend/               # Fichiers statiques du client (HTML, CSS, JS)
├── static/                 # Fichiers statiques collectés par Django
├── templates/              # Templates HTML globaux
├── bd/                     # Dossier contenant structure_bd_finale.sql
├── run_project.bat         # Script de démarrage rapide pour Windows
└── run_project.sh          # Script de démarrage rapide pour Linux/macOS
```

## 👥 Groupe 57

| Membre | Rôle |
|--------|------|
| Membre 1 | Chef de projet / Backend |
| Membre 2 | Backend / Base de données |
| Membre 3 | Frontend / Design |
| Membre 4 | Frontend / Intégration |
| Membre 5 | Tests / Documentation |

## 📄 Licence

Ce projet est développé dans un cadre académique à l'IFRI, Université d'Abomey-Calavi.
