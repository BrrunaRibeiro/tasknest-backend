from pathlib import Path
import os
import dj_database_url
import cloudinary
import cloudinary.api
import cloudinary.uploader
from datetime import timedelta  
if os.path.isfile('env.py'):
    import env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Retrieving environment variables
SECRET_KEY = os.environ.get('SECRET_KEY')

CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)


# Set default file storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'  
MEDIA_URL = '/media/'  

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '.herokuapp.com',
    'ep-shy-hall-a2g98y0a.eu-central-1.aws.neon.tech',
    '127.0.0.1',
    'https://tasknest-frontend-b8d8d5129c14.herokuapp.com/',
    'https://tasknest-backend-c911b6c54076.herokuapp.com/',
    'http://127.0.0.1:8000',
    'http://localhost',
    'localhost:8000',
    'localhost',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'cloudinary',
    'tasks',
]

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
]

# Cors settings
CORS_ALLOWED_ORIGINS = [  
    'http://localhost:3000',  
    'https://tasknest-backend-c911b6c54076.herokuapp.com',
    'http://127.0.0.1:8000',
    'http://localhost',
    'http://192.168.1.252:3000',
    'https://tasknest-frontend-b8d8d5129c14.herokuapp.com',
    'https://localhost:8000',
]  
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "OPTIONS",
]
CORS_ALLOW_HEADERS = [
    "Content-Type",
    "authorization",
]

ROOT_URLCONF = 'tasknest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'staticfiles', 'build')],
        #tell Django and WhiteNoise where to look for Reacts index.html file in deployment
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

WSGI_APPLICATION = 'tasknest.wsgi.application'


# Database(PostgreSQL)
if 'DEV' in os.environ:  
    # Development database (SQLite)  
    DATABASES = {  
        'default': {  
            'ENGINE': 'django.db.backends.sqlite3',  
            'NAME': BASE_DIR / 'db.sqlite3',  
        }  
    }  
else:  
    # Production database (PostgreSQL or other)  
    DATABASES = {  
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))  
    } 

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# JWT settings
SIMPLE_JWT = {  
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),  
    'ROTATE_REFRESH_TOKENS': True,  
    'BLACKLIST_AFTER_ROTATION': True,  
    'AUTH_HEADER_TYPES': ('Bearer',),  
} 

REST_FRAMEWORK = {  
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (  
        'rest_framework_simplejwt.authentication.JWTAuthentication',  
    ), 
}  

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_ROOT = BASE_DIR / 'staticfiles' / 'build'

#Using Whitenoise for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
