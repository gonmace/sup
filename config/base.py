from decouple import config
from pathlib import Path
import os
import firebase_admin
from firebase_admin import credentials

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY', default='your secret key')

INSTALLED_APPS = [
    # 'django_cotton',
    # 'django.contrib.sites',
    # 'crispy_forms',
    # 'django_comments',
    # 'fluent_comments',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tailwind',
    'import_export',
    'widget_tweaks',
    'adminsortable2',
    'channels',
    # 'user_visit',
    'tracking',
    'fcm_django',

    'streamblocks',
    'streamfield',

    'main.apps.MainConfig',
    'galeria',
    'actividades',
    'clientes',
    # 'componentes',
    'notificaciones.apps.NotificacionesConfig',

]

SITE_ID = 1

# # CRISPY_TEMPLATE_PACK = 'bootstrap3'

# # COMMENTS_APP = 'fluent_comments'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'streamblocks.middleware.RequestMiddleware',
    'notificaciones.middleware.UserMiddleware',
]

# X_FRAME_OPTIONS = "SAMEORIGIN"
# SILENCED_SYSTEM_CHECKS = ["security.W019"]

ROOT_URLCONF = 'config.urls'

TAILWIND_APP_NAME = 'theme'

TAILWIND_CSS_PATH = 'css/tailwind.css'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR / 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

X_FRAME_OPTIONS = 'ALLOW-FROM https://cloud.redlinegs.com'

CSRF_TRUSTED_ORIGINS = [
    'https://sup.tekon-rl.cl',
    'https://cloud.redlinegs.com'
    ]

STREAMFIELD_BLOCK_OPTIONS = {
    "display": {
        "label": "Mostrar",
        "type": "checkbox",
        "default": True
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

FIREBASE_CREDENTIALS_PATH = os.path.join(
    BASE_DIR, 'redlinegs-b0c63-firebase-adminsdk-6z95o-085c505941.json'
    )


# Inicializa la app de Firebase si no se ha inicializado ya
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

FCM_DJANGO_SETTINGS = {
    # an instance of firebase_admin.App to be used
    # as default for all fcm-django requests
    # default: None (the default Firebase app)
    # "DEFAULT_FIREBASE_APP": None,
    # default: _('FCM Django')
    # "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
    # true if you want to have only one active device per
    # registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": True,
}
