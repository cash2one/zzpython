import os

FILE_CHARSET='UTF-8'
DEFAULT_CHARSET = 'utf-8'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
)
MANAGERS = ADMINS
memcacheconfig="127.0.0.1:11211"
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'templates/media')
ADMIN_HTML_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
SECRET_KEY = '%g0qs$sh=$-9p1#s^y#-up_9*u^-5d1b!m%afyl25764fh*m42'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/?max_entries=2048&timeout=5&cull_percentage=10'
#CACHE_MIDDLEWARE_SECONDS=60*3
#SESSION_COOKIE_AGE = 60*5
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_SAVE_EVERY_REQUEST = True
#STATIC_URL = '/static/'
STATICFILES_FINDERS = (
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'seocompanycrm.urls'
SESSION_FILE_PATH = '/tmp/'
TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates'),
)
SESSION_ENGINE = (
    'django.contrib.sessions.backends.file'
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)
