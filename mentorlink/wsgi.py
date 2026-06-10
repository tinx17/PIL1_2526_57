"""
Configuration WSGI pour le projet IFRI_MentorLink.
Utilisé pour le déploiement traditionnel (sans WebSockets).
Pour le support WebSocket, utilisez asgi.py avec Daphne.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorlink.settings')

application = get_wsgi_application()
