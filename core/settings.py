import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# La clé signe les tokens JWT : avec la clé par défaut (publique sur GitHub),
# n'importe qui pourrait fabriquer un token administrateur.
if not DEBUG and (SECRET_KEY.startswith('django-insecure') or len(SECRET_KEY) < 40):
    raise RuntimeError('SECRET_KEY absente ou trop faible : définissez une clé longue et secrète dans .env')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Permet à Django de détecter le HTTPS d'origine derrière un proxy/reverse-proxy
# (ex: Nginx) qui transmet l'en-tête X-Forwarded-Proto. Sans cela,
# request.build_absolute_uri() (utilisé pour les image_url) renvoie des URLs en http://.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'channels',

    # Local apps
    'apps.formations',
    'apps.services',
    'apps.realisations',
    'apps.contact',
    'apps.chat',
    'apps.stages',
    'apps.blog',
    'apps.finances',
    'apps.site_config',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.site_config.middleware.MaintenanceMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ← AJOUT : remplace WSGI par ASGI pour Channels/WebSocket
ASGI_APPLICATION = 'core.asgi.application'

# ← AJOUT : Channel layers Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://redis:6379')],
        },
    },
}

# ← AJOUT : Clé Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'visiontech_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cache (compteurs anti brute-force, throttling, mode maintenance).
# Redis est partagé entre les workers ; sinon cache mémoire local (dev).
REDIS_URL = os.getenv('REDIS_URL', '')
if REDIS_URL:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.redis.RedisCache', 'LOCATION': REDIS_URL}}
else:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ] + (['rest_framework.renderers.BrowsableAPIRenderer'] if DEBUG else []),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Limitation de débit : garde-fou global + règles strictes sur les points sensibles
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon':         os.getenv('THROTTLE_ANON', '120/min'),
        'user':         os.getenv('THROTTLE_USER', '300/min'),
        'login':        os.getenv('THROTTLE_LOGIN', '10/min'),
        'register':     os.getenv('THROTTLE_REGISTER', '5/hour'),
        'contact':      os.getenv('THROTTLE_CONTACT', '10/hour'),
        'stage_submit': os.getenv('THROTTLE_STAGE', '10/hour'),
        'chat_start':   os.getenv('THROTTLE_CHAT', '30/hour'),
    },
    # Nombre de proxys devant Django : en production, Nginx de l'hôte (HTTPS) puis
    # Nginx Docker = 2. L'IP réelle est lue dans X-Forwarded-For sans pouvoir être
    # falsifiée par le client. Vérifier dans les logs « security » que les IP sont variées.
    'NUM_PROXIES': int(os.getenv('NUM_PROXIES', '2')),
}

# JWT
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=int(os.getenv('JWT_ACCESS_HOURS', '24'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    'https://api.visiontech.vision',
    'https://visiontech.vision',
    'https://www.visiontech.vision',
]

CORS_ALLOW_CREDENTIALS = True

# CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://api.visiontech.vision',
    'https://visiontech.vision',
    'https://www.visiontech.vision',
]

# Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get', 'post', 'put', 'patch', 'delete'
    ],
}

# Email
EMAIL_BACKEND       = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST          = os.getenv('EMAIL_HOST', 'smtp.zoho.com')
EMAIL_PORT          = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_USE_SSL       = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_TIMEOUT       = int(os.getenv('EMAIL_TIMEOUT', 10))
DEFAULT_FROM_EMAIL  = os.getenv('DEFAULT_FROM_EMAIL', 'VisionTech SARL <contact@visiontechsarl.com>')

# Durcissement HTTP (production)
if not DEBUG:
    SESSION_COOKIE_SECURE   = True
    CSRF_COOKIE_SECURE      = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS     = 31536000
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY  = 'strict-origin-when-cross-origin'
    X_FRAME_OPTIONS         = 'DENY'

# Limites d'upload (Nginx coupe déjà à 20 Mo)
DATA_UPLOAD_MAX_MEMORY_SIZE   = 10 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 500

# Documentation API (Swagger) : désactivée en production sauf ENABLE_API_DOCS=True
ENABLE_API_DOCS = os.getenv('ENABLE_API_DOCS', str(DEBUG)) == 'True'

# Chemin de l'admin Django : à personnaliser en production pour réduire les attaques automatisées
DJANGO_ADMIN_URL = os.getenv('DJANGO_ADMIN_URL', 'admin/').strip('/') + '/'

# Journal de sécurité (échecs de connexion, spam bloqué, maintenance)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'simple': {'format': '[{asctime}] {levelname} {name}: {message}', 'style': '{'}},
    'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'}},
    'loggers': {
        'security':        {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django.security': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
    },
}

# Frontend URL (pour les liens dans les emails)
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://visiontech.vision')