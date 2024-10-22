import os
from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env.str("ENV_PATH", default=BASE_DIR / ".env.dev"))

DEBUG = env.bool("DEBUG")

SECRET_KEY = env.str("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "corsheaders",
    "siteapi",
    "haunted_auth",
    "haunted_sessions",
    "ghost_sharing",
    "django_email_verification",
    "environ",
    "django_ckeditor_5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hauntedserver.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "hauntedserver.jinja2.environment",
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "hauntedserver.wsgi.application"


DATABASES = {
    "default": env.db(),
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / "hsutils" / "openapi"]
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    "default": env.cache(),
}


def verified_callback(user):
    user.is_active = True


EMAIL_MAIL_CALLBACK = verified_callback

EMAIL_MAIL_HTML = "email_confirmation_body.html.j2"
EMAIL_MAIL_PLAIN = "email_confirmation_body.txt.j2"
EMAIL_MAIL_SUBJECT = "Confirm your email"
EMAIL_MAIL_PAGE_TEMPLATE = "confirm_template.html"
EMAIL_MAIL_TOKEN_LIFE = int(timedelta(days=1).total_seconds())

CORS_ALLOW_CREDENTIALS = env(
    "CORS_ALLOW_CREDENTIALS",
    default=False,
)
CORS_ALLOWED_ORIGINS = tuple(
    env(
        "CORS_ALLOWED_ORIGINS",
        default="",
    ).split(","),
)
CSRF_TRUSTED_ORIGINS = tuple(
    env(
        "CSRF_TRUSTED_ORIGINS",
        default="",
    ).split(","),
)
ALLOWED_HOSTS = tuple(
    env(
        "ALLOWED_HOSTS",
        default="",
    ).split(","),
)
EMAIL_FROM_ADDRESS = env("EMAIL_FROM_ADDRESS")
EMAIL_PAGE_DOMAIN = env("EMAIL_PAGE_DOMAIN")
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

SITE_ID = env.int("SITE_ID")

COOP_API_KEY = env("COOP_API_KEY")
COOP_SERVER_URL = env("COOP_SERVER_URL")

TEST_RUN = DEBUG or "PYTEST_CURRENT_TEST" in os.environ

CKEDITOR_5_BASEPATH = f"/{STATIC_URL}ckeditor/ckeditor/"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "codeBlock",
            "sourceEditing",
            "insertImage",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells", "tableProperties", "tableCellProperties"],
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1", "class": "ck-heading_heading1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
            ],
        },
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        },
    },
}

MINIO_URL = env("MINIO_URL")
MINIO_SECURE = env.bool("MINIO_SECURE")
MINIO_ACCESS_KEY = env("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = env("MINIO_SECRET_KEY")
MINIO_GHOST_BUCKET = env("MINIO_GHOST_BUCKET")
MINIO_GHOST_BUCKET_STAGING = env("MINIO_GHOST_BUCKET_STAGING")

MAX_GHOST_SIZE = 5 * 2**20  # 5 MiB
GHOST_QUOTA = 100 * 2**20  # 100 MiB

SESSION_RETENTION_WEEKS = env.int("SESSION_RETENTION_WEEKS")
