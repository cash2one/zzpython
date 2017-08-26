# -*_ coding:utf-8 -*-            
'''Created on 2014年12月6日
@author:sj
'''
from django.http import HttpResponse,HttpResponseRedirect  
from django.shortcuts import render_to_response,render
from zz91otherweb import Account                             
from django.db import connection                              
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator               
from django.template import RequestContext
import MySQLdb,os,datetime,time,calendar,urllib,sys        
from symbol import if_stmt
from zz91page import *

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/donn.py")
donn = database()
cursor = donn.cursor()

def listl(request):                                      
    searchKey = request.GET.get('searchKey')
    searchKey3 = request.GET.get('searchKey3')                         
    startIndex = request.GET.get('startIndex')          
    if startIndex ==None :                               
        startIndex = 0   
                                   

    page = request.GET.get('page', '')                     
    if not page:
        page=1
        
    funpage = zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)                           
    if searchKey==None :                                  
        sql ="select * from company order by id asc limit %s,%s";  
    else:
        sql= "SELECT * FROM company where "+searchKey3+"="+"'"+searchKey+"'"+" order by id asc limit %s,%s";                                         
#         sql = "SELECT * FROM company where id="+"'"+searchkey3+"'"+"order by id asc limit %s,%s"; 
      
                    
    cursor.execute(sql,[frompageCount,limitNum])                                  
    names = cursor.fetchall()                            
    clist = []                                           
    for obj in names :                                   
        c = Account.Account(obj[0],obj[1],obj[2],obj[4],obj[7])
           
        clist.append(c)                                   
    if searchKey==None :
        sql = 'select count(0) from company'
    else:
        sql = 'select count(0) from company where '+searchKey3+'='+"'"+searchKey+"'"
#         sql = 'select count(0) from company where '+searchKey3+'='+searchKey
#     else:
#         sql = 'select count(0) from company where '+searchKey3+'='+"'"+searchKey+"'"
    cursor.execute(sql)
    alist=cursor.fetchone()

    if alist:
        listcount=alist[0]                                       
    if (int(listcount)>1000000):
        listcount=1000000-1

    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    

    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()                          
    
                                     
                                                          
         
    if searchKey == None:                                 
        searchKey = ''  
        
                                     
    
    return render_to_response('shebei/list.html',locals(), context_instance=RequestContext(request))

def doDelete(request):
    page = request.GET.get('page', '')                                
    id = request.GET.get('id')                      
    sql = 'delete from company where id='+id           
    cursor.execute(sql)
    ''' 打印'''   
    print 'aaaaa'                        
    return HttpResponseRedirect('/list/?page='+page)     




    





    
