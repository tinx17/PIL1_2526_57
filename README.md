# Projet_Integrateur_Groupe_57
# IFRI MentorLink 

Plateforme monolithique de mentorat développée avec Django.

## Installation et Lancement du projet

Suivez ces étapes pour lancer l'application sur votre machine locale :

1. **Créer l'environnement virtuel :**
   ```bash
   python -m venv venv
   ```

2. **Activer l'environnement virtuel :**
   * *Sur Git Bash / Linux / macOS :* `source venv/Scripts/activate`
   * *Sur Windows (Invite de commande) :* `venv\Scripts\activate`

3. **Installer les dépendances obligatoires :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialiser la base de données :**
   ```bash
   python manage.py migrate
   ```

5. **Lancer le serveur de test :**
   ```bash
   python manage.py runserver
   ```
   Accédez ensuite au site via l'adresse : http://127.0.0.1:8000

