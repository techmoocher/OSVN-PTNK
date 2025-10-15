"""Django settings for the Operation Smile PTNK project."""

from __future__ import annotations

import os
from importlib import import_module
from pathlib import Path


# --- Core paths -----------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Security -------------------------------------------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me')
DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() in {'1', 'true', 'yes'}

ALLOWED_HOSTS = [host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if host.strip()]
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]


# --- Third-party availability ---------------------------------------------------
try:
    import_module('whitenoise')
except ModuleNotFoundError:
    WHITENOISE_AVAILABLE = False
else:
    WHITENOISE_AVAILABLE = True


# --- Application definition -----------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages.apps.PagesConfig',
    'activities.apps.ActivitiesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if WHITENOISE_AVAILABLE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'operation_smile_ptnk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'operation_smile_ptnk.wsgi.application'
ASGI_APPLICATION = 'operation_smile_ptnk.asgi.application'


# --- Database -------------------------------------------------------------------
default_db_engine = os.environ.get('DJANGO_DB_ENGINE', 'django.db.backends.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': default_db_engine,
        'NAME': os.environ.get('DJANGO_DB_NAME', str(BASE_DIR / 'db.sqlite3')),
    }
}

if default_db_engine != 'django.db.backends.sqlite3':
    DATABASES['default'].update(
        {
            'USER': os.environ.get('DJANGO_DB_USER', ''),
            'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
            'HOST': os.environ.get('DJANGO_DB_HOST', ''),
            'PORT': os.environ.get('DJANGO_DB_PORT', ''),
        }
    )


# --- Password validation --------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# --- Internationalization -------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'Asia/Ho_Chi_Minh')
USE_I18N = True
USE_TZ = True


# --- Static & Media -------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

if WHITENOISE_AVAILABLE and not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- Custom project settings ----------------------------------------------------
JOIN_US_GOOGLE_FORM_URL = os.environ.get(
    'JOIN_US_GOOGLE_FORM_URL',
    'https://docs.google.com/forms/d/your-form-id/viewform',
)


# --- Default field type ---------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'