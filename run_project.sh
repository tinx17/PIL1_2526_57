#!/bin/bash

# Configuration
FRONTEND_PORT=8080
BACKEND_PORT=8000

echo "=== Démarrage d'IFRI_MentorLink ==="

# 1. Activation de l'environnement virtuel Python
if [ -d "venv" ]; then
    echo "Activation de l'environnement virtuel..."
    source venv/Scripts/activate || source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activation de l'environnement virtuel (.venv)..."
    source .venv/Scripts/activate || source .venv/bin/activate
else
    echo "Attention: Aucun environnement virtuel détecté. Utilisation du Python global."
fi

# 2. Installation/Vérification des dépendances
echo "Vérification des dépendances Python..."
pip install -r requirements.txt

# 3. Application des migrations et peuplement initial
echo "Application des migrations Django..."
python manage.py migrate
echo "Initialisation de la base de données avec les comptes de test (seed_db)..."
python manage.py seed_db

# 4. Lancement du Backend Django (port 8000)
echo "Lancement du backend Django sur http://localhost:$BACKEND_PORT..."
python manage.py runserver $BACKEND_PORT &
BACKEND_PID=$!

# 5. Lancement du Frontend statique (port 8080)
echo "Lancement du serveur HTTP pour le frontend sur http://localhost:$FRONTEND_PORT..."
python -m http.server $FRONTEND_PORT --directory frontend &
FRONTEND_PID=$!

# Fonction de nettoyage lors de la fermeture
cleanup() {
    echo -e "\nArrêt des serveurs..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "IFRI_MentorLink arrêté."
    exit 0
}

# Intercepter Ctrl+C
trap cleanup SIGINT SIGTERM

echo "--------------------------------------------------"
echo "IFRI_MentorLink est en cours d'exécution !"
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo "Backend API: http://localhost:$BACKEND_PORT"
echo "Faites Ctrl+C pour arrêter le projet."
echo "--------------------------------------------------"

# Attendre que les processus fils se terminent
wait
