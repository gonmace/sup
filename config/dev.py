# flake8: noqa
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    # "django_extensions",
    # "debug_toolbar",
    'django_browser_reload',
    'theme'
]

MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

CORS_ALLOW_ALL_ORIGINS = True

CSRF_COOKIE_SECURE = False

CSRF_USE_SESSIONS = False

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'https://dcfb-189-28-76-62.ngrok-free.app']

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

ASGI_APPLICATION = 'config.asgidev.application'

