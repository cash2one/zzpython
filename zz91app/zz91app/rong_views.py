#! /usr/bin/env python
# coding=utf-8

import os
import json
import unittest
import logging
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect

app_key = "n19jmcy59ued9"
app_secret = "wbunqDULV8T"

os.environ.setdefault('rongcloud_app_key', app_key)
os.environ.setdefault('rongcloud_app_secret', app_secret)

from rong import ApiClient
client = ApiClient()

def gettoken(request):
    userid=request.GET.get("userid")
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    
    result = client.user_get_token(
            str(userid),
            'test-name1',
            'http://img0.zz91.com/zz91/images/indexLogo.png')
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False))
    