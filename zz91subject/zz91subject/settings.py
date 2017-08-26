# Django settings for zz91 project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os.path
import sys
sys.path.append('../zz91public/')
from zz91settings import *
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


ALLOWED_HOSTS = ["*"]


DEFAULT_CHARSET = 'utf8'
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'templates/media')
MAIN_STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'media')
ADMIN_HTML_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
WEB_NAME = 'ZZ91再生网-专题'
WEB_DOMAIN = 'http://subject.zz91.com/'#
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jntzft8v18yxis3#1tlahw7u3l7!y)po21whz00-*zej@wdko6'
#CACHE_BACKEND = 'file:///var/tmp/django_cache' 
#CACHE_BACKEND = 'memcached://192.168.110.119:11211/?max_entries=2048&timeout=5&cull_percentage=10'
#CACHE_MIDDLEWARE_SECONDS=60*3
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',#全站缓存
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',#全站缓存
    #'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'zz91subject.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	#'/usr/python/Django-1.2.3/django/bin/myproject/templates',
	os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
