import os
import django.conf.global_settings as DEFAULT_SETTINGS

ADMINS = (
    ('Rachel', 'rachel.twu@gmail.com'),
)

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'herbalcell.views.context_processor',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join('file://', PROJECT_ROOT, 'cache'),
    },
}

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')
ALLOWED_HOSTS = (
    '.herbalcell.com',
)

ROOT_URLCONF = 'herbalcell.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'herbalcell', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'herbalcell',
    'prettylog',
    'django_w3c_validator',
)

LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'}
    },
    'handlers': {
        'catchall': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'prettylog.txt'),
            'maxBytes': 5 * 2 ** 20,  # 5 MiB
            'backupCount': 3,
        },
    },
    'loggers': {
        '': {
            'handlers': ['catchall'],
            'level': 'INFO',
        }
    }
}