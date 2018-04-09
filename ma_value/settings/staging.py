# settings/local.py
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOCAL_SYSTEM = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mavalueapp.herokuapp.com', 'http://mavalueapp.herokuapp.com']

AWS_ACCESS_KEY_ID = 'AKIAIDOKUUZO7UYBUWWQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'pruebarobin'
AWS_S3_REGION_NAME = 'us-west-2'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Database
# ========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd4t4itkc3ejab3',
        'USER': 'xwngugdecipxtm',
        'PASSWORD': 'fcbb6cfc1610dd6e02527b1812e7c07b0fd9102adca0dea04dac91e025bbb7df',
        'HOST': 'ec2-54-243-130-33.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# ----- Config "django-rq"
RQ_QUEUES = {
    'default': {
        'URL': 'redis://h:p1f00455ec8a009a879c60a71a98e36813ed1a65afa2ad98553f6cce1b6320b38@ec2-50-16-50-168.compute-1.amazonaws.com:23549/0',
        'DEFAULT_TIMEOUT': 3600,
    },
    'high': {
        'URL': 'redis://h:p1f00455ec8a009a879c60a71a98e36813ed1a65afa2ad98553f6cce1b6320b38@ec2-50-16-50-168.compute-1.amazonaws.com:23549/0',
        'DEFAULT_TIMEOUT': 3600,
    },
    'low': {
        'URL': 'redis://h:p1f00455ec8a009a879c60a71a98e36813ed1a65afa2ad98553f6cce1b6320b38@ec2-50-16-50-168.compute-1.amazonaws.com:23549/0',
        'DEFAULT_TIMEOUT': 3600,
    }
}

# Module stores
EXPORT_DATA_TO_EXTERNAL_HOST = True
API_PRIMARY = "AWS"

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'content-type',
    'origin',
    'user-agent',
    'x-requested-with',
    'access-control-allow-headers',
    'access-control-allow-methods',
    'access-control-allow-origin',
)

CORS_ORIGIN_WHITELIST = (
    'http://mavalueapp.herokuapp.com',
    'mavalueapp.herokuapp.com',
    'localhost:8000',
    '127.0.0.1:8000'
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
SHOULD_PRINT_DEBUG = False
