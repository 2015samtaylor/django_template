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
from .config import EMAIL_HOST_USER, imap_password_sam, django_db_password
import google.auth
from google.auth import credentials
from storages.backends.gcloud import GoogleCloudStorage
from google.cloud import storage

# Custom Google Cloud Storage class
class CustomGoogleCloudStorage(GoogleCloudStorage):
    def path(self, name):
        # Construct the path to the file in Google Cloud Storage
        return f"https://storage.googleapis.com/{self.bucket_name}/{name}"



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(f'Here is the base dir {BASE_DIR}')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)do_a(klkmb0yol0!m3a7s^@+_1pjnxd41)byup57kvd!_z5ye"

# SECURITY WARNING: don't run with debug turned on in production!
# You must set settings.ALLOWED_HOSTS if DEBUG is False.
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "emailscraper_app.apps.EmailscraperAppConfig",
    "ckeditor",
    "ckeditor_uploader",
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
    # "emailscraper_app" #if default conventions
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django_hosting",
        "USER": "samuel_taylor",
        "PASSWORD": django_db_password,
        "HOST": "192.168.1.219",
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = imap_password_sam

GS_CREDENTIALS, project_id = google.auth.load_credentials_from_file(
    r'C:\Users\becky\Desktop\Git_Directory\Django_Email_Hub\django-hosting-427421-72dd7e5957fe.json'
)
GD_PROJECT_ID = project_id
GS_BUCKET_NAME = 'django_hosting'


DEFAULT_FILE_STORAGE = 'emailscraper_proj.settings.CustomGoogleCloudStorage'
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
MEDIA_ROOT = None  # Ensure MEDIA_ROOT is set to None

# Ensure the default image exists in the Google Cloud Storage bucket
def check_default_image_in_gcs(bucket_name, file_name, credentials, project_id):
    client = storage.Client(credentials=credentials, project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    print(f"Checking for file {file_name} in bucket {bucket_name}")
    if not blob.exists():
        raise FileNotFoundError(f"Default image not found in Google Cloud Storage at {file_name}")
    else:
        print(f"File {file_name} found in bucket {bucket_name}")

DEFAULT_IMAGE_NAME = 'profile_pics/default.jpg'
check_default_image_in_gcs(GS_BUCKET_NAME, DEFAULT_IMAGE_NAME, GS_CREDENTIALS, GD_PROJECT_ID)


STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'emailscraper_app', 'static'), #path to css and js
]



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


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_ALLOW_NONIMAGE_FILES = False

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Image'],  # Add the Image button to the toolbar
        ],
        'extraPlugins': 'uploadimage',  # Add the necessary plugins
        'filebrowserUploadUrl': f'{MEDIA_URL}ckeditor/upload/',
        'filebrowserBrowseUrl': f'{MEDIA_URL}ckeditor/browse/',
    }
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.getcwd(), 'Logs', 'Email_Sender.log'),
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
