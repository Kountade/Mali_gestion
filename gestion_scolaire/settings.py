from pathlib import Path
import os
from django.contrib.messages import constants as messages


MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-69+-ja64ym4$)uagc)dxrvl48f3f5^+i+p!jd+r=wtm91yq!@s"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ["web-production-5958.up.railway.app", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-5958.up.railway.app',
    'https://votre-autre-domaine.com'
]



# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "application",  # Remplacez par le nom de votre application
    "crispy_forms",
    "crispy_bootstrap5",
    "django_bootstrap5",
    'formtools',
    
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
     "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Middleware de localisation
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gestion_scolaire.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gestion_scolaire.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
from django.utils.translation import gettext_lazy as _
# Internationalization
LANGUAGE_CODE = 'fr'  # Langue par défaut (français)
TIME_ZONE = 'UTC'
USE_I18N = True  # Activation de la prise en charge des langues
USE_L10N = True  # Activation de la localisation des formats de dates et nombres
USE_TZ = True

LANGUAGES = [
    ('fr', _('Français')),  # Français
    ('en', _('Anglais')),   # Anglais
    ('ar', _('العربية')),   # Arabe
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR / 'locale'),  # Dossier pour les fichiers de traduction
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Dossier static à la racine de votre projet
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Dossier où les fichiers seront collectés lors du déploiement
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Fichiers médias
MEDIA_URL = '/media/'  # URL pour accéder aux fichiers médias téléchargés
MEDIA_ROOT = BASE_DIR / 'media'  # Dossier où les fichiers téléchargés seront stockés

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Redirection après connexion
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'