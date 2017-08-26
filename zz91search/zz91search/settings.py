# Django settings for myproject project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os.path,sys

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

ALLOWED_HOSTS = ["www.zz91.com","s.zz91.com","ss.zz91.com","sss.zz91.com","trade.zz91.com"]

DEFAULT_CHARSET = 'utf8'
sys.path.append('../zz91public/')
pyuploadpath="/mnt/data/resources/pyuploadimages/"
pyimgurl="http://img1.zz91.com/pyuploadimages/"
from zz91settings import *
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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/upload/')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/upload/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'media')
ADMIN_HTML_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
SECRET_KEY = '93f1q5=1=v#9ew3fczrnq4dm8o+2x-26&x3y#7#6n1rh%&j8jf'
CACHE_MIDDLEWARE_SECONDS=60*15
CACHE_MIDDLEWARE_KEY_PREFIX="search"

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
	#'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
	#'django.middleware.cache.FetchFromCacheMiddleware',#全站缓存
)

ROOT_URLCONF = 'zz91search.urls'

TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
)
