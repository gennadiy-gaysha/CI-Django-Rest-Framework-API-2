from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv()

CLOUDINARY_STORAGE = {'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')}
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Adjust the REST_FRAMEWORK setting based on the DEV environment variable
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Sessions in Development
        'rest_framework.authentication.SessionAuthentication'
        if os.environ.get('DEV') == '1'
        # Tokens in Production
        else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,
    'DATETIME_FORMAT': '%d %b %Y',
}

# Check if DEV environment variable is set to '1' (development mode)
if os.environ.get('DEV') != '1':
    # Apply production-specific settings
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]

REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
# To be able to have the front end app and the API deployed to different platforms, set
# the JWT_AUTH_SAMESITE attribute to 'None'. Without this the cookies would be blocked.
JWT_AUTH_SAMESITE = 'None'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'drf_api.serializers.CurrentUserSerializer'
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEV') == '1'



# ALLOWED_HOSTS = ["127.0.0.1", 'drf-api-app-gaysha-repeat-150999686cdd.herokuapp.com']
# CI:
# ALLOWED_HOSTS = [
#    os.environ.get('ALLOWED_HOST'),
#    'localhost',
# ]
# ChatGPT:
# Dynamically set the ALLOWED_HOSTS from environment variable
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')
# Dynamically set the ALLOWED_HOSTS with a default fallback
ALLOWED_HOSTS = [
   os.environ.get('ALLOWED_HOST', '127.0.0.1'),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',

    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',

    'profiles',
    'posts',
    'comments',
    'likes',
    'followers',
]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===============================================================================
# All ChatGPT explanations see at the very bottom.
# Initialize an empty list for CORS origins
cors_origins = []

# Get the CLIENT_ORIGIN from the environment and append it if it exists
client_origin = os.environ.get('CLIENT_ORIGIN')
if client_origin:
    cors_origins.append(client_origin)

# Get the CLIENT_ORIGIN_DEV from the environment and append it if it exists
client_origin_dev = os.environ.get('CLIENT_ORIGIN_DEV')
if client_origin_dev:
    cors_origins.append(client_origin_dev)

# Now, ensure CORS_ALLOWED_ORIGINS is always a list, even if empty or filled based on conditions
CORS_ALLOWED_ORIGINS = cors_origins

# If there are no specific CLIENT_ORIGIN or CLIENT_ORIGIN_DEV, you might want to specify a default or fallback
if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://.*\.gitpod\.io$",
    ]
# ===============================================================================

# Enable sending cookies in cross-origin requests so
# that users can get authentication functionality
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'drf_api.urls'

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

WSGI_APPLICATION = 'drf_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Check if DEV environment variable is set to '1' for development mode
if os.environ.get('DEV') == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Production mode settings
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
    # print('Connected!')

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ===============================================================================
# The provided code is a configuration snippet for a Django project that uses the
# django-cors-headers library to manage Cross-Origin Resource Sharing (CORS) settings.
# CORS is a security feature that browsers implement to restrict web pages from making
# requests to a different domain than the one that served the web page, unless the
# server at the other domain explicitly allows it. This code dynamically configures
# which client origins are allowed to make cross-origin requests to your Django backend.
# Here's a breakdown of how the code works:

# Initializing an Empty List for CORS Origins:

# cors_origins = []

# This line initializes an empty list named cors_origins. This list will be used to
# store the URLs of the client applications (such as your React frontend) that are allowed
# to make requests to your Django backend.

# Getting CLIENT_ORIGIN from the Environment:

# client_origin = os.environ.get('CLIENT_ORIGIN')
# if client_origin:
#     cors_origins.append(client_origin)

# This section attempts to retrieve a value for CLIENT_ORIGIN from the environment
# variables, which should be the URL of your deployed client application (for example,
# your React app hosted on a service like Netlify or Vercel). If CLIENT_ORIGIN is
# found and is not None, it's added to the cors_origins list. This setup allows you
# to configure the allowed origin(s) without hardcoding them into your source code,
# making your application more secure and easier to manage, especially when moving
# between different environments (development, staging, production, etc.).

# Getting CLIENT_ORIGIN_DEV from the Environment:

# client_origin_dev = os.environ.get('CLIENT_ORIGIN_DEV')
# if client_origin_dev:
#     cors_origins.append(client_origin_dev)

# Similarly, this section retrieves the CLIENT_ORIGIN_DEV environment variable,
# intended to represent the URL of your local development environment for the client
# application (commonly http://localhost:3000 for React development servers). If it
# exists, it's also added to the cors_origins list. This allows you to work on your
# application locally, making API requests to your Django backend without facing CORS
# errors.

# Ensuring CORS_ALLOWED_ORIGINS Is Always a List:

# CORS_ALLOWED_ORIGINS = cors_origins

# This line assigns the cors_origins list to the CORS_ALLOWED_ORIGINS setting used by
# django-cors-headers. This setting defines which origins are permitted to make
# cross-origin requests to your backend. It must be a list of strings representing the
# allowed origins.

# Specifying a Fallback with CORS_ALLOWED_ORIGIN_REGEXES:

# if not CORS_ALLOWED_ORIGINS:
#     CORS_ALLOWED_ORIGIN_REGEXES = [
#         r"^https://.*\.gitpod\.io$",
#     ]

# If no specific client origins are configured (i.e., if CORS_ALLOWED_ORIGINS is empty),
# this code sets up a fallback using CORS_ALLOWED_ORIGIN_REGEXES. This setting allows
# you to specify a list of regular expressions that match against the Origin header of
# incoming requests. In this case, it's configured to allow requests from any subdomain
# of gitpod.io, which is useful if you're using Gitpod as a cloud development environment.

# Summary:
# This code dynamically configures your Django application to accept cross-origin requests
# from specified client applications. It enhances security by allowing you to specify
# allowed origins through environment variables, supports both production and development
# environments by enabling different origins for each, and provides flexibility through
# the use of regular expressions for matching origins.


