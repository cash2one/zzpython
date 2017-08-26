#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar,json,xlwt
import StringIO,qrcode
from conn import bestjoydb
from zz91page import *

from zzwx.client import Client
from zz91settings import weixinconfig
wxc = Client(weixinconfig['bestjoyserver']['appid'], weixinconfig['bestjoyserver']['secret'])

db = bestjoydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/crmtools.py")
execfile(nowpath+"/func/order_function.py")

orddb=orderfun()


#欢迎页
def index(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    #订单总数
    sql="select count(0) as count from orderlist"
    result=db.fetchonedb(sql)
    ordercount=result['count']
    #未分配订单数
    sql="select count(0) as count from orderlist where status=0"
    result=db.fetchonedb(sql)
    ordercount_noassgin=result['count']
    #已分配订单数据
    sql="select count(0) as count from orderlist where status=1"
    result=db.fetchonedb(sql)
    ordercount_assgin=result['count']
    
    #代理商数据
    sql="select count(0) as count from agentlist where isdel=0"
    result=db.fetchonedb(sql)
    agentcount=result['count']
    
    return render_to_response('index.html',locals())

#添加订单
def addorder(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    return render_to_response('addorder.html',locals())

def province(request):
    return render_to_response('province.html',locals())
#订单添加
def addorder_save(request):
    
    proname=request.GET.get("proname")
    if not proname:
        proname=''
    protype=request.GET.get("protype")
    if not protype:
        protype=''
    prosize=request.GET.get("prosize")
    proprice=request.GET.get("proprice")
    pronumber=request.GET.get("pronumber")
    prodesc=request.GET.get("prodesc")
    if not prodesc:
        prodesc=''
    area=request.GET.get("area")
    address=request.GET.get("address")
    postcode=request.GET.get("postcode")
    contactname=request.GET.get("contactname")
    phone1=request.GET.get("phone1")
    phone2=request.GET.get("phone2")
    phone3=request.GET.get("phone3")
    phone=phone1+"-"+phone2+"-"+phone3
    mobile=request.GET.get("mobile")
    yuyue_time=request.GET.get("mobile")
    status=0
    agentlist_id=0
    gmt_created=gmt_modified=datetime.datetime.now()
    no=random.randrange(10000,99999)
    orderno=str(dateall_to_int(gmt_created))+str(no)
    aid=request.GET.get("aid")
    if aid:
        values=[orderno,proname,protype,prosize,proprice,pronumber,prodesc,area,address,postcode,contactname,phone,mobile,yuyue_time,gmt_modified,aid]
        sql="update orderlist set orderno=%s,proname=%s,protype=%s,prosize=%s,proprice=%s,pronumber=%s,prodesc=%s,area=%s,address=%s,postcode=%s,contactname=%s,phone=%s,mobile=%s,yuyue_time=%s,gmt_modified=%s where id=%s"
        result=db.updatetodb(sql,values)
    else:
        values=[orderno,proname,protype,prosize,proprice,pronumber,prodesc,area,address,postcode,contactname,phone,mobile,status,agentlist_id,yuyue_time,gmt_created,gmt_modified]
        sql="insert into orderlist(orderno,proname,protype,prosize,proprice,pronumber,prodesc,area,address,postcode,contactname,phone,mobile,status,agentlist_id,yuyue_time,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=db.updatetodb(sql,values)
    if result:
        res={'err':'false','errkey':''}
    else:
        res={'err':'true','errkey':'错误'}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
def order_del(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    id=request.GET.get("id")
    sql="update orderlist set status=3 where id=%s"
    db.updatetodb(sql,[id])
    return HttpResponseRedirect(request_url)
def modorder(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    aid=request.GET.get("id")
    sql="select * from orderlist where id=%s"
    result=db.fetchonedb(sql,[aid])
    area=result['area']
    if len(area)>=12:
        arealabel2=orddb.getarea(area_code=area[0:12])
    if len(area)>=16:
        arealabel3=orddb.getarea(area_code=area[0:16])
    if len(area)>=20:
        arealabel4=orddb.getarea(area_code=area[0:20])
    result['arealabel']=arealabel2+"->"+arealabel3+"->"+arealabel4
    result['yuyue_time']=formattime(result['yuyue_time'],1)
    phone=result['phone']
    arrphone=phone.split("-")
    if len(arrphone)>=2:
        phone1=arrphone[0]
        phone2=arrphone[1]
        phone3=arrphone[2]
        result['phone1']=phone1
        result['phone2']=phone2
        result['phone3']=phone3
    return render_to_response('modorder.html',locals())
#订单列表
def orderlist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    page=request.GET.get('page')
    status=request.GET.get('status')
    if not page:
        page=1
    if not status:
        status='0'
    orderno=request.GET.get("orderno")
    proname=request.GET.get("proname")
    if not proname:
        proname=''
    protype=request.GET.get("protype")
    if not protype:
        protype=''
    prosize1=request.GET.get("prosize1")
    prosize2=request.GET.get("prosize2")
    proprice2=request.GET.get("proprice2")
    proprice1=request.GET.get("proprice1")
    pronumber1=request.GET.get("pronumber1")
    pronumber2=request.GET.get("pronumber2")
    prodesc=request.GET.get("prodesc")
    if not prodesc:
        prodesc=''
    area=request.GET.get("area")
    if not area:
        area=''
    address=request.GET.get("address")
    if not address:
        address=''
    postcode=request.GET.get("postcode")
    if not postcode:
        postcode=''
    contactname=request.GET.get("contactname")
    if not contactname:
        contactname=''
    phone=request.GET.get("phone")
    mobile=request.GET.get("mobile")
    agentlist_id = request.GET.get("agentlist_id")
    if not agentlist_id:
        agentlist_id=''
    searchlist={}
   
    if orderno:
        searchlist['orderno']=orderno
    if proname:
        searchlist['proname']=proname
    if protype:
        searchlist['protype']=protype
    if prosize1:
        searchlist['prosize1']=prosize1
    if prosize2:
        searchlist['prosize2']=prosize2
    if proprice1:
        searchlist['proprice1']=proprice1
    if proprice2:
        searchlist['proprice2']=proprice2
    if pronumber1:
        searchlist['pronumber1']=pronumber1
    if pronumber2:
        searchlist['pronumber2']=pronumber2
    if prodesc:
        searchlist['prodesc']=prodesc
    if area:
        searchlist['area']=area
    if address:
        searchlist['address']=address
    if postcode:
        searchlist['postcode']=postcode
    if contactname:
        searchlist['contactname']=contactname
    if mobile:
        searchlist['mobile']=mobile
    if phone:
        searchlist['phone']=phone
    if agentlist_id:
        searchlist['agentlist_id']=agentlist_id
    searchurl=urllib.urlencode(searchlist)
    #过滤@号
    if searchlist:
        for ss in searchlist:
            values=searchlist[ss]
            values=values.replace("@"," ")
            searchlist[ss]=values
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    #获得客户
    allcustomer=orddb.orderlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist,status=status)
    if allcustomer:
        listcount=allcustomer['count']
        listall=allcustomer['list']
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        if len(page_range)>7:
            page_range=page_range[:7]
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
    
    return render_to_response('orderlist.html',locals())
#订单导出
def orderout(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    status=request.GET.get('status')
    page=1
    orderno=request.GET.get("orderno")
    proname=request.GET.get("proname")
    if not proname:
        proname=''
    protype=request.GET.get("protype")
    if not protype:
        protype=''
    prosize1=request.GET.get("prosize1")
    prosize2=request.GET.get("prosize2")
    proprice2=request.GET.get("proprice2")
    proprice1=request.GET.get("proprice1")
    pronumber1=request.GET.get("pronumber1")
    pronumber2=request.GET.get("pronumber2")
    prodesc=request.GET.get("prodesc")
    if not prodesc:
        prodesc=''
    area=request.GET.get("area")
    if not area:
        area=''
    address=request.GET.get("address")
    if not address:
        address=''
    postcode=request.GET.get("postcode")
    if not postcode:
        postcode=''
    contactname=request.GET.get("contactname")
    if not contactname:
        contactname=''
    phone=request.GET.get("phone")
    mobile=request.GET.get("mobile")
    agentlist_id = request.GET.get("agentlist_id")
    if not agentlist_id:
        agentlist_id=''
    searchlist={}
   
    if orderno:
        searchlist['orderno']=orderno
    if proname:
        searchlist['proname']=proname
    if protype:
        searchlist['protype']=protype
    if prosize1:
        searchlist['prosize1']=prosize1
    if prosize2:
        searchlist['prosize2']=prosize2
    if proprice1:
        searchlist['proprice1']=proprice1
    if proprice2:
        searchlist['proprice2']=proprice2
    if pronumber1:
        searchlist['pronumber1']=pronumber1
    if pronumber2:
        searchlist['pronumber2']=pronumber2
    if prodesc:
        searchlist['prodesc']=prodesc
    if area:
        searchlist['area']=area
    if address:
        searchlist['address']=address
    if postcode:
        searchlist['postcode']=postcode
    if contactname:
        searchlist['contactname']=contactname
    if mobile:
        searchlist['mobile']=mobile
    if phone:
        searchlist['phone']=phone
    if agentlist_id:
        searchlist['agentlist_id']=agentlist_id
    searchurl=urllib.urlencode(searchlist)
    #过滤@号
    if searchlist:
        for ss in searchlist:
            values=searchlist[ss]
            values=values.replace("@"," ")
            searchlist[ss]=values
    #获得客户
    listall=orddb.orderlist(frompageCount=0,limitNum=10000,searchlist=searchlist,status=status)

    if listall:
        wb =xlwt.Workbook()
        ws = wb.add_sheet(u'订单信息')
        style_k=xlwt.easyxf('align: wrap off')
        
        ws.col(0).width = 0x0d00 + 1000
        ws.col(1).width = 0x0d00 + 8000
        ws.col(2).width = 0x0d00 - 500
        ws.col(3).width = 0x0d00 - 500
        ws.col(4).width = 0x0d00 + 1000
        ws.col(5).width = 0x0d00 + 1000
        ws.col(6).width = 0x0d00 + 1000
        ws.col(7).width = 0x0d00 + 1000
        ws.col(8).width = 0x0d00 + 1000
        ws.col(9).width = 0x0d00 + 1000
        ws.col(10).width = 0x0d00 + 1000
        ws.col(11).width = 0x0d00 + 1000
        ws.col(12).width = 0x0d00 + 1000
        
        ws.write(0, 0, u'订单编号')
        ws.write(0, 1, u'产品名称')
        ws.write(0, 2, u'款式/型号')
        ws.write(0, 3, u'尺码')
        ws.write(0, 4, u'单价')
        ws.write(0, 5, u'数量')
        ws.write(0, 6, u'备注')
        ws.write(0, 7, u'地区')
        ws.write(0, 8, u'地址')
        ws.write(0, 9, u'邮编')
        ws.write(0, 10, u'收货人')
        ws.write(0, 11, u'电话')
        ws.write(0, 12, u'手机号码')
        
        js=0
        newsurl=''
        for all in listall['list']:
            orderno=all['orderno']
            proname=all['proname']
            protype=all['protype']
            prosize=all['prosize']
            proprice=all['proprice']
            pronumber=all['pronumber']
            prodesc=all['prodesc']
            arealabel=all['arealabel']
            address=all['address']
            postcode=all['postcode']
            contactname=all['contactname']
            phone=all['phone']
            mobile=all['mobile']
            js=js+1
            ws.write(js, 0, orderno)
            ws.write(js, 1, proname.decode('utf-8','ignore'))
            ws.write(js, 2, protype.decode('utf-8','ignore'))
            ws.write(js, 3, prosize)
            ws.write(js, 4, proprice)
            ws.write(js, 5, pronumber)
            ws.write(js, 6, prodesc.decode('utf-8','ignore'))
            ws.write(js, 7, arealabel.decode('utf-8','ignore'))
            ws.write(js, 8, address.decode('utf-8','ignore'))
            ws.write(js, 9, postcode.decode('utf-8','ignore'))
            ws.write(js, 10, contactname.decode('utf-8','ignore'))
            ws.write(js, 11, phone.decode('utf-8','ignore'))
            ws.write(js, 12, mobile)
        fname = '订单信息.xls'
        agent=request.META.get('HTTP_USER_AGENT') 
        if agent and re.search('MSIE',agent):
            response =HttpResponse(content_type="application/vnd.ms-excel") #解决ie不能下载的问题
            response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
        else:
            response =HttpResponse(content_type="application/vnd.ms-excel")#解决ie不能下载的问题
            response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
        wb.save(response)
        return response
    return HttpResponse('无数据')
#代理商管理
def agentlist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    page=request.GET.get('page')
    if not page:
        page=1
    aname=request.GET.get("aname")
    if not aname:
        aname=''
    dtype=request.GET.get("dtype")
    if not dtype:
        dtype=''
    area=request.GET.get("area")
    if not area:
        area=''
    address=request.GET.get("address")
    if not address:
        address=''
    postcode=request.GET.get("postcode")
    if not postcode:
        postcode=''
    contactname=request.GET.get("contactname")
    if not contactname:
        contactname=''
    phone=request.GET.get("phone")
    if not phone:
        phone=''
    searchlist={}
   
    if aname:
        searchlist['aname']=aname
    if dtype:
        searchlist['dtype']=dtype
    if area:
        searchlist['area']=area
    if address:
        searchlist['address']=address
    if postcode:
        searchlist['postcode']=postcode
    if contactname:
        searchlist['contactname']=contactname
    if phone:
        searchlist['phone']=phone
    searchurl=urllib.urlencode(searchlist)
    #过滤@号
    if searchlist:
        for ss in searchlist:
            values=searchlist[ss]
            values=values.replace("@"," ")
            searchlist[ss]=values
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    #获得客户
    allcustomer=orddb.agentlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    if allcustomer:
        listcount=allcustomer['count']
        listall=allcustomer['list']
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
    return render_to_response('agentlist.html',locals())
#分配匹配
def assign(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    page=request.GET.get('page')
    if not page:
        page=1
    aname=request.GET.get("aname")
    if not aname:
        aname=''
    dtype=request.GET.get("dtype")
    if not dtype:
        dtype=''
    area=request.GET.get("area")
    if not area:
        assignarea=''
    else:
        assignarea=area[0:16]
    address=request.GET.get("address")
    if not address:
        address=''
    postcode=request.GET.get("postcode")
    if not postcode:
        postcode=''
    contactname=request.GET.get("contactname")
    if not contactname:
        contactname=''
    phone=request.GET.get("phone")
    if not phone:
        phone=''
    searchlist={}
   
    if aname:
        searchlist['aname']=aname
    if dtype:
        searchlist['dtype']=dtype
    if area:
        searchlist['area']=area
    if assignarea:
        searchlist['assignarea']=assignarea
    if address:
        searchlist['address']=address
    if postcode:
        searchlist['postcode']=postcode
    if contactname:
        searchlist['contactname']=contactname
    if phone:
        searchlist['phone']=phone
    orderid=request.GET.get("orderid")
    if orderid:
        searchlist['orderid']=orderid
    searchurl=urllib.urlencode(searchlist)
    if orderid:
        sql="select agentlist_id from orderlist where id=%s"
        result=db.fetchonedb(sql,[orderid])
        if result:
            agentlist_id=result['agentlist_id']
            if str(agentlist_id)!="0":
                return HttpResponse("该订单已经分配，不要重复分配！")
    #过滤@号
    if searchlist:
        for ss in searchlist:
            values=searchlist[ss]
            values=values.replace("@"," ")
            searchlist[ss]=values
    if area:
        if len(area)>=12:
            arealabel2=orddb.getarea(area_code=area[0:12])
        if len(area)>=16:
            arealabel3=orddb.getarea(area_code=area[0:16])
        if len(area)>=20:
            arealabel4=orddb.getarea(area_code=area[0:20])
        arealabel=arealabel2+"-"+arealabel3
    
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    #获得客户
    allcustomer=orddb.agentlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    if allcustomer:
        listcount=allcustomer['count']
        listall=allcustomer['list']
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        if len(page_range)>7:
            page_range=page_range[:7]
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
    return render_to_response('assign.html',locals())
#分配
def assign_save(request):
    
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    agentid=request.GET.get("agentid")
    orderid=request.GET.get("orderid")
    if orderid:
        order=orddb.orderdetail(orderid)
    sql="select weixinid from agent_contact where agent_id=%s and checked=1"
    result=db.fetchalldb(sql,[agentid])
    if result:
        for list in result:
            weixinid=list['weixinid']
            datava={
                "touser":weixinid,
                "template_id":"dobF8p5gug2Te4rgjNQeli5qJuAo776Q2HsA5u8twZ4",
                "url":"http://bestjoy.asto.com.cn/agent/agent_ordershow.html?order_id="+str(orderid)+"&weixinid="+str(weixinid),
                "topcolor":"#FF0000",
                "data":{
                    "first": {
                    "value":"有新的发货订单，敬请查收！",
                    "color":"#173177"
                    },
                    "keyword1":{
                    "value":str(order['orderno']),
                    "color":"#173177"
                    },
                    "keyword2":{
                    "value":order['proname'],
                    "color":"#173177"
                    },
                    "keyword3":{
                    "value":str(order['protype'])+"/"+str(order['prosize']),
                    "color":"#173177"
                    },
                    "keyword4":{
                    "value":str(order['proprice'])+"/"+str(order['pronumber']),
                    "color":"#173177"
                    },
                    "keyword5":{
                    "value":str(order['arealabel'])+str(order['address']),
                    "color":"#173177"
                    },
                    "remark":{
                    "value":"请尽快联系客户，预约时间，有问题请致电步多健全国电商服务热线：400-115-2022",
                    "color":"#173177"
                    },
                }
            }
            datava=json.dumps(datava,ensure_ascii=False,indent=2)
            token=wxc.send_template_message(datava)
    
    sql="update orderlist set agentlist_id=%s,status=1 where id=%s"
    result=db.updatetodb(sql,[agentid,orderid])
    
    return render_to_response('assign_save.html',locals())
#放入未分配
def reassign(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    orderid=request.GET.get("orderid")
    sql="update orderlist set status=0,agentlist_id=0 where id=%s"
    result=db.updatetodb(sql,[orderid])
    return HttpResponseRedirect(request_url)
#添加代理商
def addagent(request):
    return render_to_response('addagent.html',locals())
#代理商添加
def addagent_save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    aname=request.GET.get("aname")
    if not aname:
        aname=''
    dtype=request.GET.get("dtype")
    if not dtype:
        dtype=''
    area=request.GET.get("area")
    address=request.GET.get("address")
    postcode=request.GET.get("postcode")
    contactname=request.GET.get("contactname")
    if not contactname:
        contactname=''
    phone=request.GET.get("phone")
    isdel=0
    gmt_modified=datetime.datetime.now()
    gmt_created=request.GET.get("gmt_created")
    if not  gmt_created:
        gmt_created=gmt_modified
   
    aid=request.GET.get("aid")
    
    values=[aname,dtype,area,address,postcode,contactname,phone,gmt_created,gmt_modified]
    valuesup=[aname,dtype,area,address,postcode,contactname,phone,gmt_created,aid]
    if aid:
        sql="update agentlist set aname=%s,dtype=%s,area=%s,address=%s,postcode=%s,contactname=%s,phone=%s,gmt_created=%s where id=%s"
        result=db.updatetodb(sql,valuesup)
    else:
        sql="insert into agentlist(aname,dtype,area,address,postcode,contactname,phone,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=db.updatetodb(sql,values)
    if result:
        res={'err':'false','errkey':''}
    else:
        res={'err':'true','errkey':'错误'}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
#获得城市
def arealist(request):
    label=request.GET.get("label")
    if label:
        res=orddb.getarealist(label=label)
        res=simplejson.dumps(res,ensure_ascii=False)
        return HttpResponse(res)
#删除代理商
def agent_del(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    id=request.GET.get("id")
    sql="update agentlist set isdel=1 where id=%s"
    db.updatetodb(sql,[id])
    sql="delete from agent_contact where agent_id=%s"
    db.updatetodb(sql,[id])
    return HttpResponseRedirect(request_url)
#修改代理商
def modagent(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    aid=request.GET.get("id")
    sql="select * from agentlist where id=%s"
    result=db.fetchonedb(sql,[aid])
    area=result['area']
    result['gmt_created']=formattime(result['gmt_created'],1)
    if area:
        arealabel4=''
        arealabel3=''
        if len(area)>=12:
            arealabel2=orddb.getarea(area_code=area[0:12])
        if len(area)>=16:
            arealabel3=orddb.getarea(area_code=area[0:16])
        if len(area)>=20:
            arealabel4=orddb.getarea(area_code=area[0:20])
        result['arealabel']=arealabel2+"->"+arealabel3+"->"+arealabel4
    return render_to_response('modagent.html',locals())
#新增绑定二维码
def getbind(request):
    aid=request.GET.get('aid')
    sql="select aname,contactname from agentlist where id=%s"
    result=db.fetchonedb(sql,[aid])
    return render_to_response('ewm.html',locals())
#解绑二维码
def agent_unweixin(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    aid=request.GET.get('id')
    request_url=request.META.get('HTTP_REFERER','/')
    sql="delete from agent_contact where agent_id=%s"
    db.updatetodb(sql,[aid])
    return HttpResponseRedirect(request_url)
#生成二维码图片
def getewm(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("login.html")
    request_url=request.META.get('HTTP_REFERER','/')
    aid=request.GET.get('aid')
    gmt_created=gmt_modified=datetime.datetime.now()
    no=random.randrange(100000,999999)
    randomstr=getjiami(str(dateall_to_int(gmt_created))+str(no)+str(aid))
    if aid:
        sql="insert into agent_contact(agent_id,randomstr,gmt_created) values(%s,%s,%s)"
        db.updatetodb(sql,[aid,randomstr,gmt_created])
    arg="http://bestjoy.asto.com.cn/agent/binding.html?randomstr="+randomstr
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=2,
    )
    qr.add_data(arg)
    qr.make(fit=True)
    img = qr.make_image()
    mstream = StringIO.StringIO()
    img.save(mstream, "GIF")
    mstream.closed
    return HttpResponse(mstream.getvalue(),'image/gif')


