"""
Minimal Django settings for developing and testing widgy_blog outside of a
full site. Used by manage.py and pytest (see [tool.pytest] in pyproject.toml).
"""
import os
import tempfile

import dj_database_url

BASE_DIR = os.path.dirname(__file__)

DATABASES = {'default': dj_database_url.config(default='sqlite:///test_db.sqlite3')}

SECRET_KEY = "widgy_blog_tests_secret_key"
DEBUG = True
ALLOWED_HOSTS = ['*']

# Speed up tests under SQLite.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Mezzanine configuration. widgy's mezzanine integration (which widgy_blog
# builds on) needs these.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"
GRAPPELLI_INSTALLED = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django.contrib.sitemaps',

    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.pages',
    'mezzanine.forms',
    'filebrowser_safe',
    'grappelli_safe',
    'django_comments',

    'filer',
    'easy_thumbnails',
    'sorl.thumbnail',
    'treebeard',
    'compressor',
    'django_extensions',

    'widgy',
    'widgy.contrib.widgy_mezzanine',
    'widgy.contrib.form_builder',
    'widgy.contrib.page_builder',
    'widgy.contrib.urlconf_include',
    'widgy.contrib.widgy_i18n',
    'widgy.contrib.review_queue',

    'widgy_blog',
]

URLCONF_INCLUDE_CHOICES = tuple()

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SITE_ID = 1

# Mezzanine normally sets this via set_dynamic_settings(); its site utilities
# read it unconditionally.
TESTING = False

# Scratch directory for static/media collected during tests.
TEMP_DIR = tempfile.mkdtemp(prefix='widgy_blog_')

ROOT_URLCONF = 'tests.urls'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(TEMP_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(TEMP_DIR, 'media')

USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = 'en'
LOGIN_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "mezzanine.conf.context_processors.settings",
                "mezzanine.pages.context_processors.page",
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

# Widgy Settings
WIDGY_MEZZANINE_SITE = 'tests.widgy_config.widgy_site'
