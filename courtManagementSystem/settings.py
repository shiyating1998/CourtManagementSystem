"""
Django settings for courtManagementSystem project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import logging
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #TODO

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'corsheaders',
    'django_celery_results'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://driven-moderately-gator.ngrok-free.app",
    # Add any other origins that you want to allow here
]

ROOT_URLCONF = 'courtManagementSystem.urls'

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

WSGI_APPLICATION = 'courtManagementSystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'court-management-system',
#         'USER': 'admin',
#         'PASSWORD': '12345678',
#         'HOST': 'db.ck5j8uchwbfr.us-east-1.rds.amazonaws.com',   # Set to '127.0.0.1' if using localhost
#         'PORT': '3306',        # Default port for MySQL
#     }
# }


# localhost
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'court-management-system',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',   # Set to '127.0.0.1' if using localhost
        'PORT': '3306',        # Default port for MySQL
    }
}

# docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'court_management_system',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',  # Name of the MySQL service in docker-compose
        'PORT': '3306',
    }
}


ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.35', 'driven-moderately-gator.ngrok-free.app']


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # Replace with your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jlxxily@gmail.com'
EMAIL_HOST_PASSWORD = 'trpb yqxp dlvk gurv'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'simple',
            # Only capture DEBUG messages
            'filters': ['require_debug_true'],
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'info.log',
            'formatter': 'simple',
            # Capture INFO and above (INFO, WARNING, ERROR, CRITICAL)
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_debug', 'file_info'],
            'level': 'INFO',
            'propagate': False,  # Prevent logs from propagating to root logger
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno == logging.DEBUG,
        },
    },
}




# Stripe config
STRIPE_PUBLIC_KEY = "pk_test_51PfA0tRt3PcgmiF6YXj4ROeapnBMPBd7FqSIGJyGvvMoZrVESulq4n0kTbarADCXxDjQQShUD3GbsaKaustZJut400GUgtILbz"
STRIPE_SECRET_KEY = "sk_test_51PfA0tRt3PcgmiF6E8mEDNQrL0UmX8hDNGesoT1xXQ9MWwOrjIibcL2DhQMCjzrAEfLJrCB8AbbQSdrUdLrqdjQS00GcZ8ptR4"
STRIPE_WEBHOOK_SECRET = 'whsec_69fda7e9e929aa89ada8ba49b4020c1f3932effef277fca147d5e8f877a13f31'


# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# Django Secret key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2i2v5yx+iv_b6f4_8wa=8wbc3anwj3x7mhuc0grvp4z-k%ei50'
