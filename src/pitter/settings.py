import os
from typing import List


def get_key(filename):
    with open(filename, 'r') as file_with_key:
        return file_with_key.read()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'cru)q9q-!=#ip!)(i=rawgbjdfxiyrm+znk05iz=5p*w7r9(yh')
SECRET_PASSWORD_PEPPER = os.environ.get('SECRET_PASSWORD_PEPPER', 'a-z2e3M-83*3cQ*mlZZXU')

PUBLIC_KEY_PATH = os.environ.get('PUBLIC_KEY_PATH', '../additional/rsa.public')
PRIVATE_KEY_PATH = os.environ.get('PRIVATE_KEY_PATH', '../additional/rsa.private')
JWT_PUBLIC_KEY = get_key(PUBLIC_KEY_PATH)
JWT_PRIVATE_KEY = get_key(PRIVATE_KEY_PATH)
JWT_EXPIRATION_SECONDS = os.environ.get('JWT_EXPIRATION_SECONDS', 60 * 60 * 24 * 3)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB_NUMBER = os.environ.get('REDIS_DB_NUMBER', 0)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')

SPEECH_TRANSCRIPTION_MAX_LENGTH = os.environ.get('SPEECH_TRANSCRIPTION_MAX_LENGTH', 140)
SPEECH_TO_TEXT_SUPPORTED_LANGUAGES = ['ru', 'en']

SMTP_HOST_IP = os.environ.get('SMTP_HOST_IP', 'smtp.mail.ru')
SMTP_HOST_PORT = int(os.environ.get('SMTP_HOST_PORT', 465))
SMTP_SENDER_ADDRESS = os.environ['SMTP_SENDER_ADDRESS']
SMTP_SENDER_PASSWORD = os.environ['SMTP_SENDER_PASSWORD']

DEBUG: bool = bool(int(os.getenv('DEBUG', 1)))  # pylint: disable=invalid-envvar-default

ALLOWED_HOSTS: List[str] = ['*']  # On develop only

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'pitter',
    'api_client',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pitter.middleware.AuthenticationMiddleware',
    'pitter.middleware.ErrorHandlerMiddleware',
]

ROOT_URLCONF = 'pitter.urls'

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
            ]
        },
    }
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE', 'postgres'),
        'USER': os.getenv('PGUSER', 'postgres'),
        'PASSWORD': os.getenv('PGPASSWORD', 'postgres'),
        'HOST': os.getenv('PGHOST', 'localhost'),
        'PORT': os.getenv('PGPORT', '5432')
    }
}

WSGI_APPLICATION = 'pitter.wsgi.application'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_URL = '/static/'

STATIC_ROOT = '/static'

# DRF

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'EXCEPTION_HANDLER': 'pitter.middleware.custom_exception_handler',
    'PAGE_SIZE': os.environ.get('PAGE_SIZE', 1),
}

# Swagger

SWAGGER_SETTINGS = {
    'DEEP_LINKING': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
        'X-Device-Info': {'type': 'apiKey', 'name': 'X-Device-Info', 'in': 'header'},
    },
}

# Integrations
SPEECH_TO_TEXT_INTEGRATION_URI = os.environ.get("SPEECH_TO_TEXT_INTEGRATION_URI",
                                                "http://localhost:8118/api/pitter/v1/speech-recognition")
