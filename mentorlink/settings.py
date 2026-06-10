"""
Configuration Django pour le projet IFRI_MentorLink.
Groupe 57 — PIL1_2526_57

Toutes les variables sensibles sont lues depuis le fichier .env
via python-decouple.
"""

import os
from pathlib import Path
from decouple import config

# ──────────────────────────────────────────────
# Chemins de base
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────
# Sécurité
# ──────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-changez-moi-en-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']

# ──────────────────────────────────────────────
# Applications installées
# ──────────────────────────────────────────────
INSTALLED_APPS = [
    'daphne',                          # Serveur ASGI pour Channels
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Applications tierces
    'channels',
    # Applications du projet
    'accounts',
    'matching',
    'messaging',
]

# ──────────────────────────────────────────────
# Middleware
# ──────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ──────────────────────────────────────────────
# URLs et ASGI
# ──────────────────────────────────────────────
ROOT_URLCONF = 'mentorlink.urls'
ASGI_APPLICATION = 'mentorlink.asgi.application'

# ──────────────────────────────────────────────
# Templates
# ──────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'messaging.context_processors.unread_messages_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'mentorlink.wsgi.application'

# ──────────────────────────────────────────────
# Base de données — PostgreSQL par défaut, SQLite possible en dev
# ──────────────────────────────────────────────
DB_ENGINE = config('DB_ENGINE', default='postgresql')

if DB_ENGINE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='mentorlink_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# ──────────────────────────────────────────────
# Django Channels — Couche de canaux (Redis par défaut, In-Memory en dev)
# ──────────────────────────────────────────────
CHANNEL_BACKEND = config('CHANNEL_BACKEND', default='redis')

if CHANNEL_BACKEND == 'memory' or DB_ENGINE == 'sqlite':
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [config('REDIS_URL', default='redis://localhost:6379')],
            },
        },
    }

# ──────────────────────────────────────────────
# Modèle utilisateur personnalisé
# ──────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.UserProfile'

# ──────────────────────────────────────────────
# Backends d'authentification (email ou téléphone)
# ──────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrPhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ──────────────────────────────────────────────
# Validation des mots de passe
# ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ──────────────────────────────────────────────
# Internationalisation
# ──────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────
# Fichiers statiques (CSS, JavaScript, Images)
# ──────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ──────────────────────────────────────────────
# Fichiers médias (photos de profil, etc.)
# ──────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ──────────────────────────────────────────────
# URLs de redirection pour l'authentification
# ──────────────────────────────────────────────
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/matching/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ──────────────────────────────────────────────
# Clé primaire par défaut
# ──────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
