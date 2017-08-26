#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
#from zz91db_company import zz91login
#from zz91db_offer import zz91offer
#from zz91db_huanbao import zz91huanbao
#from zz91settings import SPHINXCONFIG,SPHINXCONFIG_news,logpath
#from zz91tools import getToday,getYesterday,date_to_str
#from settings import pyuploadpath,pyimgurl
import datetime,time,urllib,csv,os,xlrd,re,sys
from zz91tools import getToday,date_to_str,get_url_content,get_content,get_inner_a,get_a_url,remove_content_a,remove_content_div,filter_tags,getnextdate,getsortlist
from zz91db_ast import companydb
from bs4 import BeautifulSoup
zzcomp=companydb()
#zzlogin=zz91login()
#zzoffer=zz91offer()
#zzhuanbao=zz91huanbao()
#from auto_net_price import getnetbaijia
#from auto_huanbao_check import huanbaocheck
#from auto_suliao_zaocan import getsuliaozaocan
#from auto_jinshu_zaocan import getjinshuzaocan
#from auto_suliao_getwanping import getwanping
#from auto_suliao_wanbao import getsuliaowanbao
#from func.auto_duanxin135 import getduanxin135,getduanxin430
#from func.auto_weekprice import getweekprice,getchart
#from auto_luanma_chart import chart_luanma,chartall
#from auto_jinshu_zixun import getjinshufei
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/auto_duanxin135.py")
execfile(nowpath+"/func/auto_weekprice.py")


def index(request):
    return render_to_response('automation/index.html',locals())

def feisuliao(request):
    return render_to_response('automation/feisuliao.html',locals())

def suliao_price(request):
    return render_to_response('automation/suliao_price.html',locals())

def suliao_net_price(request):
    return render_to_response('automation/suliao_net_price.html',locals())

def area_price(request):
    return render_to_response('automation/area_price.html',locals())

def chartdata(request):
    return render_to_response('automation/chartdata.html',locals())

def week_price(request):
#    arg=request.GET.get('arg')
#    if arg=='1':
#        hangqing_huigu=1
    listchartdir=[
                  {'id':'44','name':'WTI'},
                  {'id':'646','name':'连塑PVC'},
                  {'id':'647','name':'连塑LL'},
                  {'id':'41','name':'中塑价格指数'},
                  {'id':'42','name':'中塑现货指数'},
                  ]
    listsltdir2=['PP','LDPE','HDPE','ABS','EPS','PC','PA','PMMA']
    listpagedir=['1','2','3','4','5','6']
    sltype=request.GET.get('sltype')
    type2=request.GET.get('type2')
    page=request.GET.get('page')
    gmt_created=request.GET.get('gmt_created')
    if page:
        listpagedir=getsortlist(page,listpagedir)
    if sltype:
        listsltdir2=getsortlist(sltype,listsltdir2)
        if gmt_created:
            gmt_created2=gmt_created[5:]
            weekprice=getweekprice(sltype,gmt_created2,page)
    if type2:
        listchartdir=getsortlist(type2,listchartdir,'1')
        chart=getchart(type2,page)
        
    gmt_created2=request.GET.get('gmt_created2')
    jinshutype=request.GET.get('jinshutype')
    if jinshutype:
        jinshuweekprice=getjinshuweekprice(jinshutype,gmt_created2)
    
    return render_to_response('automation/week_price.html',locals())

def duanxin_price(request):
    arg=request.GET.get('arg')
    type=request.GET.get('type')
    if arg=='1':
        duanxin135=getduanxin135()
    if arg=='2':
        duanxin430_10=1
    if type:
        duanxin430=getduanxin430(type)
    return render_to_response('automation/duanxin_price.html',locals())

def zaocanwanbao(request):
    return render_to_response('automation/zaocanwanbao.html',locals())

def net_price(request):
    return HttpResponseRedirect(request_url)

def huanbao(request):
    return render_to_response('automation/huanbao.html',locals())

def huanbao_check(request):
    return HttpResponseRedirect(request_url)