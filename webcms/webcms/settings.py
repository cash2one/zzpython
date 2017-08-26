import os,sys
sys.path.append('../zz91public/')
from zz91settings import *
ALLOWED_HOSTS = ["webcms.zz91.com"]
FILE_CHARSET='UTF-8'
DEFAULT_CHARSET = 'utf-8'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'templates/media')
ADMIN_HTML_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
SECRET_KEY = '-#v5*^fq+0^ox-fo7&amp;&amp;o_xw+_2(+_&amp;_mv=xnw3t0stl5h+_pmm'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/?max_entries=2048&timeout=5&cull_percentage=10'
#CACHE_MIDDLEWARE_SECONDS=60*3
#SESSION_COOKIE_AGE = 60*5
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_SAVE_EVERY_REQUEST = True
STATICFILES_FINDERS = (
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'webcms.urls'
SESSION_FILE_PATH = '/tmp/'
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)
