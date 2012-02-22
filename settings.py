# encoding: utf-8
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
relative_to_project_root = lambda *x: os.path.join(PROJECT_ROOT, *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': relative_to_project_root('istweb_db'),
        'USER': 'istweb_proj',                      # Not used with sqlite3.
        'PASSWORD': '123456',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'
USE_I18N = True
USE_L10N = True

SITE_ID = 1

MEDIA_ROOT = relative_to_project_root('uploads')
MEDIA_URL = ''

STATIC_ROOT = relative_to_project_root('static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    relative_to_project_root('assets'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'YymbZIjMfikrwqPnWARCVaplc`[zeJto\\OKFXgvShLuUx_^HTQ'

TEMPLATE_DIRS = (
    relative_to_project_root('templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.RestrictAccessMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    'contacts.views.contacts_list',
)

INSTALLED_APPS = (
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'home',
    'users',
    'contacts',
    'notification',
    'recommendation',
)

ROOT_URLCONF = 'istweb.urls'

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'
EXCLUDED_URLS = (
    '/admin',
    '/login',
    '/favicon.ico',
    '/static/',
)

RESTRICTED_URLS = ()
