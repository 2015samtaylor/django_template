"""
Django settings for emailscraper_proj project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from .access_secrets import access_secret_version

PROJECT_ID = "django-hosting-427421"

# Access secrets from Google Cloud Secret Manager
EMAIL_HOST_USER = access_secret_version(PROJECT_ID, "EMAIL_HOST_USER")
imap_password_sam = access_secret_version(PROJECT_ID, "imap_password_sam")
django_db_password = access_secret_version(PROJECT_ID, "django_db_password")
django_secret_key = access_secret_version(PROJECT_ID, "django_secret_key")
GS_JSON_PATH = access_secret_version(PROJECT_ID, "GS_JSON_PATH")
GS_BUCKET_NAME = access_secret_version(PROJECT_ID, "GS_BUCKET_NAME")
django_db_user = access_secret_version(PROJECT_ID, "django_db_user")
django_hosting_json_file = access_secret_version(PROJECT_ID, "django_hosting_json_file")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(f'Here is the base dir {BASE_DIR}')

# Ensure the Logs directory exists
LOGS_DIR = os.path.join(BASE_DIR, 'Logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = django_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
# You must set settings.ALLOWED_HOSTS if DEBUG is False.
DEBUG =True

ALLOWED_HOSTS = [
    os.getenv('CLOUD_RUN_URL', 'localhost'),  # Fetch from environment variable or fallback to localhost
    '127.0.0.1', 
    'localhost', 
    '.run.app',  # Allow Cloud Run domains
]

#For cloud run deployment
CSRF_COOKIE_HTTPONLY = False    # Make sure this is False for JavaScript access
CSRF_COOKIE_SECURE = True       # Set to True if using HTTPS (which you are)
CSRF_TRUSTED_ORIGINS = [
    'https://django-hosting-764972118687.us-central1.run.app',
]


# Application definition

INSTALLED_APPS = [
    "emailscraper_app.apps.EmailscraperAppConfig",
    # "ckeditor",
    # "ckeditor_uploader",
    "storages",
    "users.apps.UsersConfig",
    "crispy_forms",
    "crispy_bootstrap4",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
     'users.custom_middleware.EnsureUserActivationMiddleware',
]

ROOT_URLCONF = "emailscraper_proj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "emailscraper_proj.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Detect whether the app is running locally or on Cloud Run
import os

# Define IP addresses
LOCAL_IP = "10.168.0.5"
EXTERNAL_IP = "35.236.35.240"

# Check if the app is running in the cloud or locally
RUNNING_IN_CLOUD = os.getenv("RUNNING_IN_CLOUD") == "true"  # Check if in cloud environment (GCP, Cloud Run, etc.)
RUNNING_LOCALLY = not RUNNING_IN_CLOUD  # Inverse of RUNNING_IN_CLOUD

# Common settings for both environments
BASE_STATIC_DIR = os.path.join(BASE_DIR, "emailscraper_app", "static")

# Adjust static files settings based on the environment
if RUNNING_IN_CLOUD:
    print("Running in Cloud")
    # GCP (Cloud) Settings
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # Use WhiteNoise for production
    STATICFILES_DIRS = []  # Empty in production (GCP)
    INSTALLED_APPS += ["whitenoise.runserver_nostatic"]  # Add WhiteNoise in production
    STATIC_URL = "/static/"  # Assuming the static URL remains the same for both environments
    # Set DB host for cloud (external IP)
    DB_HOST = EXTERNAL_IP
    DEBUG = False
else:
    print("Running Locally")
    # Local Development Settings
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"  # Default storage for local development
    STATICFILES_DIRS = [BASE_STATIC_DIR]  # Path to Local CSS & JS
    STATIC_URL = "/static/"  # Local static URL
    # Set DB host for local environment (local IP)
    DB_HOST = LOCAL_IP
    DEBUG = True

# Optional: For Google App Engine (GAE) or Cloud Run, you might have specific settings for static files
if os.getenv("GAE_ENV", "").startswith("standard") or os.getenv("CLOUD_RUN"):
    STATICFILES_DIRS = []  # Ensure this is empty in production for GAE/Cloud Run

# Set Debugging based on Cloud/Local environment
DEBUG = not RUNNING_IN_CLOUD  # Debugging is true locally, false in production



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django_db",
        "USER": django_db_user,
        "PASSWORD": django_db_password,
        "HOST": EXTERNAL_IP,
        "PORT": "3306"
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#Not default, added in explicitly
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS='bootstrap4'

#First time users re-routed to this
LOGIN_REDIRECT_URL = 'landing_page'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
LOGOUT_URL = 'login'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = imap_password_sam

# At a project level in case it needs to be duplicated. 
GS_JSON_PATH = GS_JSON_PATH #from import
GS_BUCKET_NAME = GS_BUCKET_NAME #gcs_storage.py custom storage reads this in
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'users.gcs_storage_utils.gcs_storage.CustomGoogleCloudStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
STATIC_URL = "/static/"

if DEBUG:

    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
    )
    CACHE_MIDDLEWARE_SECONDS = 0
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
        ]),
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserUploadMethod': 'form',
    },
}

# Ensure the Logs directory exists
LOGS_DIR = os.path.join(BASE_DIR, 'Logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django_hosting.log'),
            'level': 'INFO',  # Adjust to the level you need
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'emailscraper_app': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
