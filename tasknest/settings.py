"""
Django settings for TaskNest.

This file contains the primary configuration settings for the Django project.
Includes security, database, middleware, installed apps, authentication, CORS, and static file settings.
"""

from pathlib import Path
import os
import dj_database_url
from datetime import timedelta
import cloudinary
import cloudinary.api
import cloudinary.uploader

# Import environment variables if present
if os.path.isfile('env.py'):
    import env

# BASE_DIR: Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: Load the secret key from environment variables
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG: Enable/disable debugging mode
DEBUG = True  # Change to False in production!

# ALLOWED_HOSTS: List of hosts allowed to access the application
ALLOWED_HOSTS = [
    '.herokuapp.com',
    'ep-shy-hall-a2g98y0a.eu-central-1.aws.neon.tech',
    '127.0.0.1',
    'localhost',
    'https://tasknest-frontend-b8d8d5129c14.herokuapp.com/',
    'https://tasknest-backend-c911b6c54076.herokuapp.com/',
]

# Application definitions
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'cloudinary',
    'django_filters',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    # Local apps
    'tasks',
]

# Middleware: Order matters here for CORS and security
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

# CORS settings
# Determine if we are running in production or development environment
IS_PRODUCTION = os.getenv('DJANGO_ENV') == 'production'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Local development URL
]

if IS_PRODUCTION:
    CORS_ALLOWED_ORIGINS.append('https://tasknest-backend-c911b6c54076.herokuapp.com')  # Add production URL
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
CORS_ALLOW_HEADERS = ["Content-Type", "authorization", "X-Requested-With", 
    "Accept", 
    "Origin", 
    "User-Agent",]

# URL Configuration
ROOT_URLCONF = 'tasknest.urls'

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'staticfiles', 'build')],  # For React integration
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

# WSGI Configuration
WSGI_APPLICATION = 'tasknest.wsgi.application'

# Database configuration: Switch between SQLite (development) and PostgreSQL (production)
if 'DEV' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Authentication and JWT settings
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %Y',
}

# Settings for django-allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATED_REDIRECT_URL = '/'  # Redirect after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # Redirect after logout

# settings.py

DJRESTAUTH_USER_DETAILS_SERIALIZER = 'tasks.serializers.UserSerializer'


# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
JWT_AUTH_SECURE = True

# Rest Auth Serializers
# REST_AUTH_SERIALIZERS = {
#     'USER_DETAILS_SERIALIZER': 'tasks.serializers.CustomUserSerializer',
# }

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Static Files Configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_ROOT = BASE_DIR / 'staticfiles' / 'build'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media File Configuration
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Site ID for Django Allauth
SITE_ID = 1

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
