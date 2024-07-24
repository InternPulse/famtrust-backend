import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("FAMTRUST_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("ENV") == "DEV"

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "accounts",
    "family_memberships",
    "transactions",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    "django_filters",
    "rest_framework",
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
    "famtrust.middleware.ValidateUserMiddleware",
]

ROOT_URLCONF = "famtrust.urls"

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

WSGI_APPLICATION = "famtrust.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if os.environ.get("ENV") == "DEV":
    DB_NAME = os.environ.get("DB_NAME") + "_dev"
else:
    DB_NAME = os.environ.get("DB_NAME")

if os.environ.get("DB_ENGINE") == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / DB_NAME,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": f"django.db.backends.{os.environ.get('DB_ENGINE')}",
            "NAME": DB_NAME,
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

try:
    MAX_PAGE_SIZE = min(int(os.environ.get("MAX_PAGE_SIZE")), 100)
except TypeError:
    MAX_PAGE_SIZE = 100

try:
    PAGE_SIZE = min(int(os.environ.get("PAGE_SIZE")), 25)
except TypeError:
    PAGE_SIZE = 25

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("famtrust.renderers.CustomJSONRenderer",),
    "EXCEPTION_HANDLER": "famtrust.utils.custom_exception_handler",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "famtrust.utils.Pagination",
    # the number of items to return per request by default
    "PAGE_SIZE": PAGE_SIZE,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "ORDERING_PARAM": "order_by",
    "SEARCH_PARAM": "q",
}

API_VERSION = os.environ.get("API_VERSION", "v1")

DESCRIPTION = """This microservice hosts the API endpoints related to
account-related operations, family-related operations, and transactions.
"""

SPECTACULAR_SETTINGS = {
    "TITLE": (
        "FamTrust - Family Management, Accounts & Transactions Microservice"
    ),
    "DESCRIPTION": DESCRIPTION,
    "VERSION": API_VERSION,
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SERVERS": [
        {
            "url": (
                "http://localhost:8000"
                if DEBUG
                else os.environ.get("PRODUCTION_URL")
            )
        }
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
}

EXTERNAL_AUTH_URL = os.environ.get("EXTERNAL_AUTH_URL")
