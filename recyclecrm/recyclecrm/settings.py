import os,sys
DEBUG = True

sys.path.append('/mnt/pythoncode/zz91public/')
pyuploadpath="/mnt/data/resources/pyuploadimages/"
pyimgurl="http://img1.zz91.com/pyuploadimages/"
from zz91settings import *
FILE_CHARSET='UTF-8'
DEFAULT_CHARSET = 'utf-8'
spconfig=SPHINXCONFIG
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
ALLOWED_HOSTS = ["*"]

#searchconfig={'servername':'192.168.2.4','serverport':9315}

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
ADMIN_HTML_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
SECRET_KEY = '-#v5*^fq+0^ox-fo7&amp;&amp;o_xw+_2(+_&amp;_mv=xnw3t0stl5h+_pmm'
CACHE_BACKEND = 'memcached://192.168.2.4:11211/?max_entries=2048&timeout=5&cull_percentage=10'
CACHE_MIDDLEWARE_SECONDS=60*3
SESSION_COOKIE_AGE = 60*20
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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
ROOT_URLCONF = 'recyclecrm.urls'
SESSION_FILE_PATH = '/tmp/'
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates/'),
)
WSGI_APPLICATION = 'recyclecrm.wsgi.application'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
)