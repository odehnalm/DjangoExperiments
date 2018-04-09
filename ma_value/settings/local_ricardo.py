# settings/local.py
from corsheaders.defaults import default_headers

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOCAL_SYSTEM = True

if LOCAL_SYSTEM:
    DJANGO_APPS.insert(-1, 'whitenoise.runserver_nostatic')
    INSTALLED_APPS = DJANGO_APPS + DEVELOPED_APPS + THIRD_PARTY_APPS

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Database
# ========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ma_value_db',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS += ["debug_toolbar"]

# ----- Config "django-rq"
RQ_QUEUES = {
    'default': {
        'URL': 'redis://localhost:6379/0',
        'DEFAULT_TIMEOUT': 3600,
    },
    'high': {
        'URL': 'redis://localhost:6379/0',
        'DEFAULT_TIMEOUT': 3600,
    },
    'low': {
        'URL': 'redis://localhost:6379/0',
        'DEFAULT_TIMEOUT': 3600,
    }
}

# ---- Core Variables

# Module stores
EXPORT_DATA_TO_EXTERNAL_HOST = False
API_PRIMARY = None

CORS_ALLOW_HEADERS = default_headers + (
    'access-control-allow-headers',
    'access-control-allow-methods',
    'access-control-allow-origin',
)

CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    'http://localhost:8000/',
    '127.0.0.1:8000',
    'http://127.0.0.1:8000/'
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'

STATIC_ROOT = join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

WHITENOISE_AUTOREFRESH = LOCAL_SYSTEM
WHITENOISE_USE_FINDERS = LOCAL_SYSTEM

# Module stores
SHOULD_PRINT_DEBUG = True
