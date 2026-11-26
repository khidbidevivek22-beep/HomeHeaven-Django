import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'HOMEHEAVEN_DJANGO_SECRET_KEY',
    'django-insecure-local-dev-change-this-before-production'
)

DEBUG = os.environ.get('HOMEHEAVEN_DEBUG', '1') == '1'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'listings',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processor.site_stats',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = os.environ.get(
    'HOMEHEAVEN_EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = os.environ.get('HOMEHEAVEN_SMTP_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('HOMEHEAVEN_SMTP_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('HOMEHEAVEN_SMTP_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('HOMEHEAVEN_SMTP_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or 'no-reply@homeheaven.local'
CONTACT_EMAIL = os.environ.get('HOMEHEAVEN_CONTACT_EMAIL', DEFAULT_FROM_EMAIL)

# Render deployment configuration
if os.environ.get('RENDER'):
    DEBUG = False
    SECRET_KEY = os.environ['HOMEHEAVEN_DJANGO_SECRET_KEY']
    RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_HOSTNAME)
        CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_HOSTNAME}']

    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Render deployment configuration
if os.environ.get('RENDER'):
    DEBUG = False
    SECRET_KEY = os.environ['HOMEHEAVEN_DJANGO_SECRET_KEY']
    RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_HOSTNAME)
        CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_HOSTNAME}']

    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Render error logging
if os.environ.get('RENDER'):
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
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }

SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

WHITENOISE_ROOT = BASE_DIR / 'public_demo_assets'
