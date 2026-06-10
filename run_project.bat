@echo off
title Démarrage IFRI_MentorLink
echo ===========================================
echo     Démarrage de IFRI_MentorLink
echo ===========================================

:: 1. Activation de l'environnement virtuel
if exist venv (
    echo Activation de l'environnement virtuel venv...
    call venv\Scripts\activate.bat
) else if exist .venv (
    echo Activation de l'environnement virtuel .venv...
    call .venv\Scripts\activate.bat
) else (
    echo Attention: Aucun environnement virtuel detecte. Utilisation de Python global.
)

:: 2. Verification des dependances
echo Verification des dependances Python...
pip install -r requirements.txt

:: 3. Application des migrations et peuplement initial
echo Application des migrations Django...
python manage.py migrate
echo Initialisation de la base de donnees avec les comptes de test (seed_db)...
python manage.py seed_db

:: 4. Demarrage du Backend Django (dans une nouvelle console)
echo Lancement du backend Django sur http://localhost:8000...
start "Backend Django" cmd /k "python manage.py runserver 8000"

:: 5. Demarrage du serveur HTTP Frontend (dans une nouvelle console)
echo Lancement du serveur HTTP pour le frontend sur http://localhost:8080...
start "Frontend Static" cmd /k "python -m http.server 8080 --directory frontend"

echo.
echo ===========================================
echo IFRI_MentorLink est en cours d'execution !
echo Frontend: http://localhost:8080
echo Backend API: http://localhost:8000
echo Fermez les fenetres console ouvertes pour arreter.
echo ===========================================
pause
