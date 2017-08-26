#-*- coding:utf-8 -*-
import MySQLdb   
import settings
from settings import pyuploadpath,pyimgurl,spconfig
import codecs
from django.utils.http import urlquote
import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import sys
import datetime,md5,hashlib
from datetime import timedelta, date 
import os
import urllib

from django.core.cache import cache
import random
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle
from math import ceil
#验证码
import memcache,qrcode,six
import Image,ImageDraw,ImageFont,ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from xml.etree import ElementTree as ET

from sphinxapi import *
from zz91page import *
from alipay import Alipay
import requests

from zz91db_ast import companydb
from zz91db_2_news import newsdb

dbc=companydb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/yzm.py")
execfile(nowpath+"/views_app.py")

def index(request):
    
    return render_to_response('webapp/index.html',locals())