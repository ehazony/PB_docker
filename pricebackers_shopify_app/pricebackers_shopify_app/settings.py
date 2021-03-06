"""
Django settings for pricebackers_shopify_app project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from shopify_app import *
from decouple import config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
from dotenv import load_dotenv
load_dotenv()
# Make this unique and store it as an environment variable. 
# Do not share it with anyone or commit it to version control.
SECRET_KEY = os.getenv('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
SESSION_COOKIE_SAMESITE = 'lax'
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'PUT']
# Application definition

INSTALLED_APPS = [
    "pricebackers_shopify_app",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shopify_app.apps.ShopifyAppConfig',
    'home.apps.HomeConfig',
    'allauth',
    'dj_rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'dashboard',
    'corsheaders',

]
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticated',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		# 'rest_framework.authentication.BasicAuthentication',  # default - may need to remove
		# 'rest_framework.authentication.SessionAuthentication',  # default - may need to remove
		'rest_framework.authentication.TokenAuthentication',  # token authentication to the api
		# 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
	),
}
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shopify_app.middleware.LoginProtection',
]

ROOT_URLCONF = 'pricebackers_shopify_app.urls'

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
                'shopify_app.context_processors.current_shop',
            ],
        },
    },
]

WSGI_APPLICATION = 'pricebackers_shopify_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		"NAME": config("DB_NAME"),
		"USER": config("DB_USER"),
		"PASSWORD": config("DB_PASSWORD"),
		'HOST': config("HOST"),
		'PORT': '5432',
	}
}


STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'
MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/



EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
EMAIL_HOST_USER = 'AKIASWWOKNMNANDMIQ6T'
EMAIL_HOST_PASSWORD = 'BJrJ1vbrk+JzfLNRvdyFczrP0U9hhPS/Op3SQJ0vLGt1'
DEFAULT_FROM_EMAIL = 'jonathan@pricebackers.com'
MAILER_LIST = ['efraimhazony@gmail.com']
ADMINS = [('Efraim', 'efraim@pricebackers.com'), ('Jonathan', 'jonathan@pricebackers.com'), ]
MANAGERS = ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_PORT = 587

KMS_FIELD_REGION = 'us-east-2'
KMS_FIELD_CACHE_SIZE = 500

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True