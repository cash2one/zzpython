#-*- coding:utf-8 -*-
#coding:utf-8
#!/usr/bin/python
from django.shortcuts import render_to_response
from django.utils.http import urlquote
import simplejson,json
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,random,md5,hashlib,requests
from datetime import timedelta,date
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
import Image,ImageDraw,ImageFont,ImageFilter
from operator import itemgetter, attrgetter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import pymongo

from settings import spconfig,appurl

#from commfunction import subString,filter_tags,replacepic,
from zz91tools import filter_tags,formattime,subString
from zz91db_ast import companydb
from zz91db_ads import adsdb
from zz91conn import database_mongodb
from qianbao import qianbaopaysave
dbc=companydb()
dbs=adsdb()
#连接loginfo集合（表）
dbmongo=database_mongodb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

zzq=zzqianbao()
zzt=zztrade()
zzc=zzcompany()
ldb_weixin=ldbweixin()

#----图片上传
def tradeimgupload(request):
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    #return HttpResponse(request.FILES)
    if request.FILES:
        randid=request.POST.get("randid")
        file = request.FILES['uploadkey']
        #image = Image.open(reqfile)
        suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
        #image.thumbnail((128,128),Image.ANTIALIAS)
        
        
        tempim = StringIO.StringIO()
        mstream = StringIO.StringIO(file.read())
        im = Image.open(mstream)
        
        
        rheight=800
        rwidth=800
        
        pwidth=im.size[0]
        pheight=im.size[1]
        
        rate = int(pwidth/pheight)
        if rate==0:
            rate=1
        nwidth=800
        nheight=800
        if (pwidth>rwidth):
            nwidth=rwidth
            nheight=nwidth /rate
        else:
            nwidth=pwidth
            nheight=pheight
        
        if (pheight>rheight):
            nheight=rheight
            nwidth=rheight*rate
        else:
            nwidth=pwidth
            nheight=pheight
            
        kzname=im.format
        
        if kzname not in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]:
            im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
            #logo水印
            if nwidth/2>130:
                wm = Image.open(nowpath+"/media/images/logo.png")
                layer = Image.new('RGBA', im.size, (0,0,0,0))
                layer.paste(wm, (im.size[0] - 120, im.size[1] - 50))
                im = Image.composite(layer, im, layer)
            #加字体水印
            fontPath=nowpath+'/SIMHEI.TTF'
            fontSize=18
            font = ImageFont.truetype(fontPath,fontSize)
            draw = ImageDraw.Draw(im)
            if nwidth/2>130:
                draw.text((nwidth/2-60,nheight/2-25),u'www.zz91.com',(0,0,0),font=font)
                draw.text((nwidth/2-70,nheight/2),unicode('ZZ91再生网专用','utf-8'),(0,0,0),font=font) 
            del draw
        tmp = random.randint(100, 999)
        newpath="/mnt/data/resources/products/"+timepath
        imgpath=newpath+str(nowtime)+str(tmp)+"."+kzname
        
        databasepath="products/"+timepath+str(nowtime)+str(tmp)+"."+kzname
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        im.save(imgpath,kzname,quality = 60)
        mstream.closed
        tempim.closed
        picurl="http://img3.zz91.com/300x15000/products/"+timepath+str(nowtime)+str(tmp)+"."+kzname
        
        sql="insert into products_pic(product_id,pic_address,gmt_created,randid) values(0,%s,%s,%s)"
        dbc.updatetodb(sql,[databasepath,gmt_created,randid])
        return HttpResponse(picurl)
        """
        sql1="select id from products_pic where pic_address=%s"
        productspicresult=dbc.fetchonedb(sql1,[imgpath])
        if productspicresult:
            productspicid=productspicresult[0]
            return HttpResponse(picurl)
        """
    return render_to_response('trade/uploadimg.html',locals())
    return HttpResponse("请选择一张图片.")
#----图片上传
def otherimgupload(request):
    #source 
    source=request.POST.get("source")
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    #return HttpResponse(request.FILES)
    if request.FILES:
        file = request.FILES.getlist('file')
        if not file:
            return None
        listall=[]
        for f in file:
            
            # 获取文件名后缀
            filetype=f.name.split(".")[-1]
            #视频上传
            if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
                tmp = random.randint(100, 999)
                newpath="/mnt/data/resources/other/"+timepath
                imgpath=newpath+str(nowtime)+str(tmp)+"."+filetype
                databasepath="other/"+timepath+str(nowtime)+str(tmp)+"."+filetype
                if not os.path.isdir(newpath):
                    os.makedirs(newpath)
        
                des_origin_f = open(imgpath,"w")
                for chunk in f.chunks():
                    des_origin_f.write(chunk)  
                des_origin_f.close()
                picurl="http://img1.zz91.com/other/"+timepath+str(nowtime)+str(tmp)+"."+filetype
            else:
                suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG','jpg','mp4']
                tempim = StringIO.StringIO()
                mstream = StringIO.StringIO(f.read())
                im = Image.open(mstream)
                
                
                rheight=800
                rwidth=800
                pwidth=im.size[0]
                pheight=im.size[1]
                rate = int(pwidth/pheight)
                if rate==0:
                    rate=1
                nwidth=800
                nheight=800
                if (pwidth>rwidth):
                    nwidth=rwidth
                    nheight=nwidth /rate
                else:
                    nwidth=pwidth
                    nheight=pheight
                if (pheight>rheight):
                    nheight=rheight
                    nwidth=rheight*rate
                else:
                    nwidth=pwidth
                    nheight=pheight
                kzname=im.format
                
                if kzname not in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]:
                    im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
                    #logo水印
                    
                    if nwidth/2>130:
                        wm = Image.open(nowpath+"/media/images/logo.png")
                        layer = Image.new('RGBA', im.size, (0,0,0,0))
                        layer.paste(wm, (im.size[0] - 120, im.size[1] - 50))
                        im = Image.composite(layer, im, layer)
                    #加字体水印
                    fontPath=nowpath+'/SIMHEI.TTF'
                    fontSize=18
                    font = ImageFont.truetype(fontPath,fontSize)
                    draw = ImageDraw.Draw(im)
                    if nwidth/2>130:
                        draw.text((nwidth/2-60,nheight/2-25),u'www.zz91.com',(0,0,0),font=font)
                        draw.text((nwidth/2-70,nheight/2),unicode('ZZ91再生网专用','utf-8'),(0,0,0),font=font) 
                    del draw
                
                tmp = random.randint(100, 999)
                newpath="/mnt/data/resources/other/"+timepath
                imgpath=newpath+str(nowtime)+str(tmp)+"."+kzname
                databasepath="other/"+timepath+str(nowtime)+str(tmp)+"."+kzname
                if not os.path.isdir(newpath):
                    os.makedirs(newpath)
                im.save(imgpath,kzname,quality = 80)
                mstream.closed
                tempim.closed
                picurl="http://img3.zz91.com/300x15000/other/"+timepath+str(nowtime)+str(tmp)+"."+kzname
            picid=0
            if source=="products":
                sql="insert into products_pic(product_id,pic_address,gmt_created) values(0,%s,%s)"
                result=dbc.updatetodb(sql,[databasepath,gmt_created])
                if result:
                    picid=result[0]
            else:
                sql="insert into other_piclist(path,source,gmt_created) values(%s,%s,%s)"
                result=dbc.updatetodb(sql,[databasepath,source,gmt_created])
                if result:
                    picid=result[0]
            list={'path':picurl,'id':picid,'databasepath':databasepath}
            listall.append(list)
        return listall
    return None
    return render_to_response('trade/otherimg.html',locals())
def offerlistside(request):
    arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    arealistnew=[]
    keywords=request.GET.get("keywords")
    tflag=request.GET.get("tflag")
    for a in arealist:
        ll={'area':a,'area_hex':getjiami(a)}
        arealistnew.append(ll)
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'keywords':keywords,'tflag':tflag,'arealistnew':arealistnew}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('trade/side.html',locals())
def offerlistside_cate(request):
    type=request.GET.get("type")
    code = request.GET.get("code")
    tflag=request.GET.get("tflag")
    keywords=request.GET.get("keywords")
    if (not code):
        code='____'
        categorylist=zzt.getindexcategorylist(code,2)
        first=1
        jsonlist={'keywords':keywords,'tflag':tflag,'categorylist':categorylist}
    else:
        first=None
        #if code:
        backcode=code[:-4]
        categorylist=zzt.getindexcategorylist(code,1)
        if categorylist==[] or categorylist==None:
            categoryname=zzt.getcategoryname(code)
        jsonlist={'keywords':keywords,'tflag':tflag,'backcode':backcode,'categorylist':categorylist}
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('trade/side_category.html',locals())
def xgkeywords(request):
    keywords = request.GET.get("keywords")#搜索
    if keywords:
        if (gethextype(keywords)==False):
            keywords_hex=getjiami(keywords)
        else:
            keywords=getjiemi(keywords)
            keywords_hex=getjiami(keywords)
    xgkeywords=zzt.getcategorylist(kname=keywords,limitcount=30)
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'xgkeywords':xgkeywords}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('trade/xgkeywords.html',locals())
#历史记录
def viewhistory(request):
    collection=dbmongo.loginfo
    #-----输出所有数据并分页
    #分页        
    page=request.GET.get("page")
    company_id=request.GET.get('company_id')
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    clientid=request.GET.get('clientid')
    if (page==None):
        page=1
    if page>1:
        showpage=None
    else:
        showpage=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)  #每页限制条数
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)  
    
    #如果查询框有输入
    arg="http://app.zz91.com/detail/"#这里可以为[] , ? & * .  
    param=".*%s.*"%arg
    partten=re.compile(param)
    if company_id and company_id!="0":
        listcount=collection.find({"company_id":company_id,"url" :partten}).count()  #搜索的记录数
        result=collection.find({"company_id":company_id,"url" :partten}).skip(frompageCount).limit(limitNum)
    elif clientid:
        listcount=collection.find({"clientid":clientid,"url" :partten}).count()  #搜索的记录数
        result=collection.find({"clientid":clientid,"url" :partten}).skip(frompageCount).limit(limitNum)
    else:        
        listcount=collection.count()    #总记录数
        result=collection.find({"url" :partten}).sort("_id",-1).skip(frompageCount).limit(limitNum)  #每页的记录和限制数
    listall=[]
    for list in result:
        url=list['url']
        url=url.replace("http://app.zz91.com/detail/?id=","")
        arrurl=url.split("^and^")
        if arrurl:
            pdtid=arrurl[0]
            list1=getcompinfo(pdtid,"",company_id)
            listall.append(list1)
    
    listcount1 = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()  
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'listall':listall,'showpage':showpage}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('trade/viewhistory.html',locals())
def offerlist(request):
    arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    arealistnew=[]
    productListtop=[]
    for a in arealist:
        ll={'area':a,'area_hex':getjiami(a)}
        arealistnew.append(ll)
    nowlanmu="<a href='/category/'>供求类别</a>"
    page = request.GET.get("page")
    iosapp=request.GET.get("iosapp")
    iosindex=request.GET.get("iosindex")
    sorttype = request.GET.get("sorttype")
    
    if (page == None or page=='' or page=="None" or page==0):
        page = 1
    nowsearcher="offersearch_new"
    keywords = request.GET.get("keywords")#搜索
    keywords_hex=""
    xgcategorylist=None
    if keywords:
        if (gethextype(keywords)==False):
            keywords_hex=getjiami(keywords)
        else:
            try:
                keywords=getjiemi(keywords)
            except:
                keywords=keywords
                keywords_hex=getjiami(keywords)
        
        if str(page)=="1":
            xgcategorylist=getcategorylist(kname=keywords,limitcount=20)
    fromindex=request.GET.get("fromindex")
    adlist=""
    if keywords:
        adlist=getadlistkeywords("736",keywords)
    if keywords:
        webtitle=keywords+"_供求列表"
    if keywords=='None' or keywords=='' or not keywords:
        webtitle="供求列表"
        keywords=''
    company_id=request.GET.get("company_id")
    searchname = urlquote(request.GET.get("searchname"))
    pdt_kind = request.GET.get("ptype")
    province = request.GET.get("province")
    
    #记录搜索记录
    clientid=request.GET.get("clientid")
    updatesearchKeywords(clientid,company_id,keywords,ktype="trade")
    username=getaccount(company_id)
    
    if (gethextype(province)==False):
        province_hex=getjiami(province)
    else:
        province_hex=province
        province=getjiemi(province)
    if province:
        arrprovince=province.split("|")
        pincelist=''
        for s in arrprovince:
            if s:
                pincelist+=s+"|"
        province=pincelist[0:len(pincelist)-1]
    provincecode = request.GET.get("provincecode")
    posttime = request.GET.get("posttime")
    pdtidlist = request.GET.get("pdtidlist")
    priceflag = request.GET.get("priceflag")
    nopiclist = request.GET.get("nopiclist")
    tfromdate = request.GET.get("fromdate")
    ttodate = request.GET.get("todate")
    jmsearchname = request.GET.get("jmsearchname")
    fromsort = request.GET.get("fromsort")
    ttype = request.GET.get("ttype")
    timearg = request.GET.get("timearg")
    forcompany_id = request.GET.get("forcompany_id")
    havepic = request.GET.get("havepic")
    haveprice = request.GET.get("haveprice")
    
    #帮你找
    ordertype=request.GET.get("ordertype")
    if company_id and ordertype:
        sqlo="select businesskeywordslist from app_order where company_id=%s"
        result=dbc.fetchonedb(sqlo,[company_id])
        returnerr=None
        if result:
            if result[0]:
                #return HttpResponse(result[0])
                #sll='{"label":"pet,pp","province":"上海,浙江","otype":"1","otime":"2"}'
                orderlist=json.loads(result[0])
                if orderlist:
                    #{"label":"pet,pp","province":"上海,浙江","otype":"1","otime":"2"}
                    orderlabel=orderlist['label']
                    orderprovice=orderlist['province']
                    orderotype=orderlist['otype']
                    ordertime=orderlist['otime']
                    keywords=orderlabel.replace(",","|")
                    province=orderprovice.replace(",","|")
                    #pdt_kind=orderotype
                    timearg=ordertime
            else:
                returnerr=1
        else:
            returnerr=1
        datatype=request.GET.get("datatype")
        if datatype=="json" and returnerr:
            jsonlist={'productList':'err'}
            return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    #新版app 供求定制
    orderflag=request.GET.get("orderflag")
    if orderflag=="1":
        if not company_id:
            resultlist={"error_code":1,"reason":"您定制的内容暂无信息","productList":''}
            response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
            return response
        sqlo="select type,timelimit,keywordslist,provincelist from app_order_trade where company_id=%s"
        result=dbc.fetchonedb(sqlo,[company_id])
        if result:
            keywords=result[2]
            if keywords:
                keywords=keywords[0:len(keywords)-1]
            province=result[3]
            if province:
                province=province[0:len(province)-1]
            if province=="不限":
                province=""
            #是否自由设置供求
            if not pdt_kind:
                pdt_kind=str(result[0])
            timearg=str(result[1])
            if not keywords:
                resultlist={"error_code":1,"reason":"您定制的内容暂无信息","productList":''}
                response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
                return response
        else:
            resultlist={"error_code":1,"reason":"您定制的内容暂无信息","productList":''}
            response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
            return response
        
    if keywords:
        for ltt0 in ['供应','出售','卖']:
            if ltt0 in keywords:
                keywords=keywords.replace(ltt0,'')
                pdt_kind='1'
        for ltt1 in ['求购','回收','买','收购']:
            if ltt1 in keywords:
                keywords=keywords.replace(ltt1,'')
                pdt_kind='2'
    
    
    nowlanmu2=""
    if keywords:
        nowlanmu2=keywords
    if fromindex:
        nowlanmu2="定制商机"
    isding=1
    if havepic or haveprice:
        isding=''
    pdt_kindname=''
    if pdt_kind=='1':
        pdt_kindname=' 供应'
    if pdt_kind=='2':
        pdt_kindname=' 求购'
    nowlanmu2+=pdt_kindname
    if priceflag:
        nowlanmu2+='－  价格'
    if havepic:
        nowlanmu2+='－  图片'
    if province:
        nowlanmu2+='－ '+province
    #----时间筛选
    if timearg:
        gmt_end=int(time.time())
        if timearg=='1':
            gmt_begin=gmt_end-24*3600
        elif timearg=='2':
            gmt_begin=gmt_end-24*3600*3
        elif timearg=='3':
            gmt_begin=gmt_end-24*3600*7
        elif timearg=='4':
            gmt_begin=gmt_end-24*3600*30
        elif timearg=='5':
            gmt_begin=gmt_end-24*3600*60
        elif timearg=='6':
            gmt_begin=gmt_end-24*3600*90
        elif timearg=='7':
            gmt_begin=gmt_end-24*3600*180
    else:
        timearg=''
    jingjialist=None
    if keywords:
        if (str(page)=='1' or page=='' or str(page)=='None' or str(page)=="0"):
            pdtidlist=keywordsTop(keywords)
            jingjialist=getjingjialist(keywords=keywords,limitcount=10,mycompany_id=company_id)
        else:
            pdtidlist=""
            jingjialist=None
    #‘’‘’‘’‘’‘’‘’‘’‘
    if (nopiclist=='' or nopiclist==None or nopiclist=='None'):
        nopiclist=None
        offerFilterListPicInfo_class="offerFilterListPicInfo"
    else:
        offerFilterListPicInfo_class="offerFilterListPicInfo_long"
    if keywords:
        if (pdtidlist!=None and pdtidlist!=''):
            arrpdtidlist=pdtidlist
            listall=[]
            n=1
            for p in arrpdtidlist:
                if (p!=''):
                    list1=getcompinfo(p[0],keywords,company_id)
                    m=1
                    if (n<=1):
                        m=1
                    elif(n>1 and n<=3):
                        m=2
                    elif (n>3 and n<=7):
                        m=3
                    if (list1!=None):
                        list1['vippaibian']=str(m)
                        n+=1
                        listall.append(list1)
            productListtop=listall
    
    #--------------------------------------------
    if (province=='' or province == None):
        province=''
        
    if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
        pdt_type=''
        pdt_kind='0'
        stab1="offerselect"
        stab2=""
        stab3=""
    if (pdt_kind =='1'):
        pdt_type='0'
        stab1=""
        stab2="offerselect"
        stab3=""
    if (pdt_kind=='2'):
        pdt_type='1'
        stab1=""
        stab2=""
        stab3="offerselect"
    
    
    nowpage=int(page)
    page=20*(int(page)-1)
    keywords2=""
    if keywords:
        #keywords2=keywords.replace('|','')
        keywords2=keywords.replace(' ','')
        
        keywords1=urlquote(keywords2)
       
        #keywords=keywords.replace('|',' ')
        keywords=keywords.replace('\\',' ')
        keywords=keywords.replace('/',' ')
        keywords=keywords.replace('/',' ')
        keywords=keywords.replace('(',' ')
        keywords=keywords.replace(')',' ')
        if (ttype==None):
            ttype=''
    if (posttime==None):
        posttime=''
    if (priceflag==None or str(priceflag)=='None'):
        priceflag=''
    if (nopiclist==None or str(nopiclist)=='None'):
        nopiclist=''
    if (havepic==None or str(havepic)=='None'):
        havepic=''
    #action = '&keywords='+searchname+'&ptype='+pdt_kind+'&province='+urlquote(province)+'&posttime='+str(posttime)+'&ttype='+str(ttype)+'&priceflag='+str(priceflag)+'&nopiclist='+str(nopiclist)+'&jmsearchname='+str(jmsearchname)+'&havepic='+str(havepic)+'&fromsort='+str(fromsort)
    #a(\d*)--b(\d*)--c(\d*)--d(\d*)--e(\d*)--f(\d*)
    action='a'+str(pdt_kind)+'--b'+str(provincecode)+'--c'+str(posttime)+'--d'+str(priceflag)+'--e'+str(nopiclist)+'--f'+str(havepic)+''
    if keywords:
        searchname=str(keywords1)
        searchname=searchname.replace('%28','astokhl')
        searchname=searchname.replace('%29','astokhr')
        searchname=searchname.replace('%5C','asto5c')
        searchname=searchname.replace('/','astoxg')
        searchname=searchname.replace('-','astohg')
    after_range_num = 8
    before_range_num = 9
    port = spconfig['port']

    #----------------------------
    cl = SphinxClient()
    list = SphinxClient()
    
    cl.SetServer ( spconfig['serverid'], port )
    list.SetServer ( spconfig['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    list.SetMatchMode ( SPH_MATCH_BOOLEAN )
    
    #取得总数
    nowdate=date.today()-timedelta(days=2)
    nextday=date.today()+timedelta(days=2)
    formatnowdate=time.mktime(nowdate.timetuple())
    formatnextday=time.mktime(nextday.timetuple())
    searstr=''
    
    if (pdt_kind !='0'):
        searstr+=";filter=pdt_kind,"+pdt_type
        cl.SetFilter('pdt_kind',[int(pdt_type)])
        list.SetFilter('pdt_kind',[int(pdt_type)])
        
    if(havepic=='1'):
        cl.SetFilterRange('havepic',1,100)
        list.SetFilterRange('havepic',1,100)
    #list.SetFilter('viptype',[0],True)
    #cl.SetFilter('offerstaus',[0])
    #list.SetFilter('offerstaus',[0])
    if (ttype == '1'):    
        cl.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
        list.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
        #searstr+=' ;range=refresh_time,'+str(formatnowdate)+','+str(formatnextday)+''
        
    if (posttime =='' or posttime==None or posttime=='None'):
        searstr +=''
    else:
        pfromdate=date.today()-timedelta(days=int(posttime)+1)
        #test=str(time.mktime(pfromdate.timetuple()))
        ptodate=date.today()+timedelta(days=3)
        
        pfromdate_int=int(time.mktime(pfromdate.timetuple()))
        ptodate_int=int(time.mktime(ptodate.timetuple()))
        if (pfromdate!=None):
            cl.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
            list.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
        #searstr += ';refresh_time,'+str(pfromdate_int)+','+str(ptodate_int)+''
    if timearg:
        cl.SetFilterRange('pdt_date',gmt_begin,gmt_end)
        list.SetFilterRange('pdt_date',gmt_begin,gmt_end)
    if haveprice:
        #cl.SetFilterRange('length_price',6,10000)
        #list.SetFilterRange('length_price',6,10000)
        cl.SetFilter('min_price',[0],True)
        list.SetFilter('min_price',[0],True)
    if forcompany_id:
        forcompany_id=int(forcompany_id)
        cl.SetFilter('company_id',[forcompany_id])
        list.SetFilter('company_id',[forcompany_id])
    
    if (province ==None or province ==''):
        provincestr=''
    else:
        if not keywords:
            provincestr=' '+province
        else:
            provincestr='&@(province,city) '+province

    if (priceflag == '1'):
        cl.SetFilter('min_price',[0],True)
        list.SetFilter('min_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price desc,refresh_time desc" )
    elif (priceflag == '2'):
        cl.SetFilter('length_price',[0],True)
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price asc,refresh_time desc" )
    else:
        list.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    if not keywords and not provincestr:
        res = list.Query ('',nowsearcher)
    else:
        if not keywords:
            keywords=""
            res = list.Query ( '@(city,province) '+provincestr+'',nowsearcher)
        else:
            res = list.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)
    if not res:
        listcount=0
    else:
        listcount=res['total_found']
    
    #cl.SetFilterRange('viptype',1,5)
    #cl.SetFilterRange('Prodatediff',0,3)
    
    #获得3天内再生通数据优先排序
    #listallvip=cache.get('list'+action)
    
    cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
    cl.SetLimits (0,100000,100000)
    if not keywords  and not provincestr:
        rescount = cl.Query ('','offersearch_new_vip')
    else:
        if not keywords:
            keywords=""
            rescount = cl.Query ( '@(city,province) '+provincestr+'',"offersearch_new_vip")
        else:
            rescount = cl.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'','offersearch_new_vip')
    pcount=0
    listall=[]
    if rescount:
        if rescount.has_key('matches'):
            tagslist=rescount['matches']
            testcom_id=0
            pcount=1000000
            ppcount=1000
            for match in tagslist:
                id=match['id']
                com_id=match['attrs']['company_id']
                viptype=match['attrs']['viptype']
                phone_rate=int(match['attrs']['phone_rate'])
                phone_num=int(match['attrs']['phone_num'])
                phone_fee=float(match['attrs']['phone_cost'])
                refresh_time=float(match['attrs']['refresh_time'])
                pdt_date=float(match['attrs']['pdt_date'])
                phone_level=float(match['attrs']['phone_level'])
                all_score=float(match['attrs']['all_score'])
                score=float(match['attrs']['score'])
                if viptype>=1:
                    if (testcom_id==com_id):
                        pcount-=1
                    else:
                        pcount=1000000
                else:
                    if (testcom_id==com_id):
                        ppcount-=1
                    else:
                        ppcount=1000
                    pcount=ppcount
                #if phone_num==10000:
                #    phone_sort=10000;
                #else:
                #    phone_sort=phone_rate*0.05+phone_num*0.85+phone_fee*0.1
                phone_sort=100
                if str(viptype)=="6":
                    if int(phone_rate)>=85:
                        phone_sort=100
                    else:
                        phone_sort=2
                    if int(phone_rate)==0:
                        phone_sort=100
                #list1=(id,pcount,viptype,refresh_time,pdt_date,phone_sort,phone_level)
                list1=[id,pcount,viptype,refresh_time,pdt_date,score,phone_sort,all_score]
                #list1=list1+[viptype]
                #list1=list1+[refresh_time]
                listall.append(list1)
                testcom_id=com_id
    
    if sorttype=="member":
        listallvip=sorted(listall, key=itemgetter(1,4,2,6,3),reverse=True)
        ordtext="会员等级"
    elif sorttype=="pro":
        listallvip=sorted(listall, key=itemgetter(1,4,5,2,6,3),reverse=True)
        ordtext="信息质量"
    elif sorttype=="time":
        listallvip=sorted(listall, key=itemgetter(1,4,3,7,2,6),reverse=True)
    else:
        listallvip=sorted(listall, key=itemgetter(1,4,7,2,6,3),reverse=True)
        ordtext="综合"
    #优先排序数
    viplen=len(listallvip)
    
    #供求总数
    listcount+=int(viplen)
    #最后一页的供求数
    lastpNum=int(viplen-ceil(viplen / 20)*20)
    #开始供求数位置
    beginpage=page
    #优先排序页码
    pageNum=0
    if (lastpNum==0):
        pageNum=int(ceil(viplen / 20))
    else:
        pageNum=int(ceil(viplen / 20)+1)
    
    #结束供求数位置
    if (int(nowpage)==int(pageNum) and lastpNum!=0):
        endpage=int(page+lastpNum)
    elif(int(nowpage)==int(pageNum) and lastpNum==0 and int(nowpage)==1):
        endpage=20
    elif(int(nowpage)==int(pageNum) and lastpNum==0):
        endpage=int(page)
    else:
        endpage=page+20
    #列出供求信息列表
    listall=[]
    for match in listallvip[beginpage:endpage]:
        if keywords2==None:
            keywords2=province
        list1=getcompinfo(match[0],keywords2,company_id)
        pdt_name=list1['pdt_name'].upper()
        pdt_name=getlightkeywords(cl,[pdt_name],keywords2.upper(),nowsearcher)
        pdt_detail=list1['pdt_detail']
        pdt_detail=filter_tags(pdt_detail)
        list1['pdt_detail']=pdt_detail
        list1['pdt_name']=pdt_name
        listall.append(list1)
    productList=listall
    
    #普通供求开始数
    offsetNum=0
    limitNum=20
    if (nowpage==pageNum and lastpNum!=0):
        offsetNum=0
        limitNum=20-lastpNum
        notvip=1
    elif (nowpage==pageNum and lastpNum==0 and viplen>0):
        offsetNum=0
        limitNum=20-lastpNum
        notvip=0
    elif (nowpage==pageNum and lastpNum==0 and viplen==0):
        offsetNum=0
        limitNum=20
        notvip=1
    elif (nowpage>pageNum and lastpNum==0):
        offsetNum=(nowpage-pageNum-1)*20
        limitNum=20-lastpNum
        notvip=1
    elif(nowpage>pageNum and lastpNum>0):
        offsetNum=((int(nowpage)-int(pageNum)-1)*20)+(20-int(lastpNum))
        limitNum=20
        notvip=1
    elif (viplen<1):
        offsetNum=(nowpage-1)*20
        limitNum=20
        notvip=1
    else:
        notvip=0
    #优先排序供求结束页的
    #test=str(lastpNum)+'|'+str(pageNum)+'|'+str(offsetNum)+'|'+str(limitNum)
    
    if (nowpage==pageNum and lastpNum!=0):
        listall=productList
    else:
        listall=[]
    if (notvip==1):
        list.SetLimits (offsetNum,limitNum,100000)
        if keywords=='':
            res = list.Query ('',nowsearcher)
        else:
            res = list.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)

        if res:
            if res.has_key('matches'):
                prodlist=res['matches']
                for list in prodlist:
                    id=list['id']
                    list1=getcompinfo(id,keywords2,company_id)
                    pdt_name=list1['pdt_name'].upper()
                    pdt_name=getlightkeywords(cl,[pdt_name],keywords2.upper(),nowsearcher)
                    list1['pdt_name']=pdt_name
                    pdt_detail=list1['pdt_detail']
                    pdt_detail=filter_tags(pdt_detail)
                    list1['pdt_detail']=pdt_detail
                    listall.append(list1)
                productList=listall

    #cache.set('productList', productList, 300)
    #底部页码
    #connt.close()
    try:
        page = int(request.GET.get('page',1))
        if page < 1:
            page = 1
    except ValueError:
            page = 1
    page_listcount=int(ceil(listcount / 20))+1
    page_rangep=[]
    i=1
    while (i<=page_listcount):
        pages={'number':'','nowpage':''}
        pages['number']=i
        if (i==page):
            pages['nowpage']='1'
        else:
            pages['nowpage']=None
            
        page_rangep.append(pages)
        i+=1
    if (page_listcount>1 and page>1):
        firstpage=1
    else:
        firstpage=None
    if (page<page_listcount and page_listcount>1):
        lastpage=1
    else:
        lastpage=None
    if page >= after_range_num:
        page_range = page_rangep[page-after_range_num:page + before_range_num]
    else:
        page_range = page_rangep[0:int(page) + before_range_num]
    nextpage=page+1
    prvpage=page-1
    #大于500页提示

    if(page_listcount>500 and page>=500):
        arrtishi="提示：为了提供最相关的搜索结果，ZZ91再生网只显示500页信息，建议您重新搜索！"
    else:
        arrtishi=None
    if page>1:
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(productList, ensure_ascii=False))
        return render_to_response('trade/listmore.html',locals())
    else:
        datatype=request.GET.get("datatype")
        if datatype=="json":
            jsonlist={'nowlanmu2':nowlanmu2,'adlist':adlist,'productListtop':productListtop,'productList':productList,'pagecount':page_listcount,'xgcategorylist':xgcategorylist,'jingjialist':jingjialist}
            return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
        return render_to_response('trade/list.html',locals())

def productsimglist(request):
    id=request.GET.get("id")
    list=zzt.getproductdetail(id)
    #返回json数据
    datatype=request.GET.get("datatype")
    #if datatype=="json":
    #    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    return render_to_response('trade/piclist.html',locals())
#----供求最终页
def detail(request):
    jsonlist1={'idcheck':'','idchecktxt':''}
    host=getnowurl(request)
    backurl=request.META.get('HTTP_REFERER','/')
    company_id=request.GET.get("company_id")
    if not company_id:
        company_id=0
    #username=getaccount(company_id)
    appsystem=request.GET.get("appsystem")
    isios=None
    if (appsystem=="iOS"):
        isios=1

    alijsload="1"
    nowlanmu='<a href="/category/">交易中心 </a>'
    nowlanmu2='<a href="/category/">交易中心 </a> > '
    keywords1=''
    keywords=request.GET.get("keywords")
    if not keywords:
        if '&' in backurl:
            keywords1=re.findall('keywords=(.*?)&',backurl)
        else:
            keywords1=re.findall('keywords=(.*)',backurl)
        if keywords1:
            keywords=urllib.unquote(keywords1[0])
    if keywords:
        nowlanmu2+='<a href="/offerlist/?keywords='+keywords+'">'+keywords+'</a>&nbsp;>'
    id=request.GET.get("id")
    if not id:
        id=0
    done = request.path
    iszstflag=zzt.getiszstcompany(company_id)
    list=zzt.getproductdetail(id,isseeflag=1)
    favoriteflag=0
    if company_id:
        favoriteflag=isfavorite(id,'10091001',company_id)
    if list:
        forcompany_id=list['company_id']
        list['favoriteflag']=favoriteflag
    else:
        forcompany_id=0
    
    foriszstflag=zzt.getiszstcompany(forcompany_id)
    #----判断举报状态
    reportcheck=zzt.getreportcheck(company_id,forcompany_id,id)
    if reportcheck==0:
        idcheck=1
        idchecktxt='举报处理中'
        jsonlist1.setdefault('idcheck',idcheck)
        jsonlist1.setdefault('idchecktxt',idchecktxt)
    if reportcheck==1:
        idcheck=1
        idchecktxt='举报已处理'
        jsonlist1.setdefault('idcheck',idcheck)
        jsonlist1.setdefault('idchecktxt',idchecktxt)
    if reportcheck==2:
        idcheck=1
        idchecktxt='举报退回'
        jsonlist1.setdefault('idcheck',idcheck)
        jsonlist1.setdefault('idchecktxt',idchecktxt)
    #该公司是否被举报成功过
    isjubao=zzt.getreportischeck(forcompany_id,id)
    #----判断是否为来电宝用户,获取来电宝余额
    isldb=None
    viptype=zzt.getviptype(company_id)
    paymoney=10
    #来电宝客户    
    if viptype=='10051003':
        isldb=1
        paymoney=ldb_weixin.getldbonephonemoney(company_id)
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        qianbaoblance=zzq.getqianbaoblance2(company_id)
    
    #诚信档案
    zxinfo=zzc.getcxinfocheck(forcompany_id)
    isseecompany=zzq.getisseecompany(company_id,forcompany_id)
    forviptype=zzt.getviptype(forcompany_id)
    #是否显示举报
    forvipflag=1
    #高会联系方式公开
    if forviptype:
        if forviptype=="100510021001" or forviptype=="100510021002" or forviptype=="100510021000" or forviptype=="10051001":
            isseecompany=1
            forvipflag=None
    #z置顶客户显示联系方式
    keywordstopcompanyflag=keywordstopcompany(id)
    if keywordstopcompanyflag:
        isseecompany=1
        forvipflag=None
    #流量宝客户联系方式公开
    forqianbaoblance=zzq.getqianbaoblance2(forcompany_id)
    if forqianbaoblance>=8:
        jingjiaflag=zzq.jingjia_keywords_online(forcompany_id)
        if jingjiaflag:
            isseecompany=1
            forvipflag=None
    #记录pv
    getproductspv(id,forcompany_id)
    #高会查看联系方式
    if list:
        compzstflag=list['viptype']['vipcheck']
        if iszstflag==1 or compzstflag==1:
            viewflag=1
        else:
            viewflag=None
        webtitle=list['title']
        
        if not isseecompany:
            list['tel_country_code']=""
            list['tel_area_code']=""
            list['tel']=""
            list['mobile']=""
            list['mobile1']="无"
            list['mobilelist']=""
            isseecompany=None
        
        nowlanmu2+='&nbsp;'+webtitle
        products_type_code=list['products_type_code']
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'list':list,'isseecompany':isseecompany,'company_id':company_id,'qianbaoblance':qianbaoblance,'paymoney':paymoney,'foriszstflag':foriszstflag,'isjubao':isjubao,'forvipflag':forvipflag,'id':id,'forcompany_id':forcompany_id,'isldb':isldb,'host':host,'idcheck':jsonlist1['idcheck'],'idchecktxt':jsonlist1['idchecktxt'],'zxinfo':zxinfo}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('trade/detail.html',locals())
#判断联系方式是否直接可以查看
def showcontact(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    forcompany_id=request.POST.get("forcompany_id")
    
    companyinfo=zzc.show_contact(company_id=company_id,forcompany_id=forcompany_id)
    if not companyinfo:
        companyinfo={}
    return HttpResponse(simplejson.dumps(companyinfo, ensure_ascii=False))
#查看联系方式
def viewcontact(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    forcompany_id=request.POST.get("forcompany_id")
    paytype=request.POST.get("paytype")
    id=request.POST.get("id")
    if not company_id:
        company_id=request.GET.get("company_id")
        forcompany_id=request.GET.get("forcompany_id")
        paytype=request.GET.get("paytype")
        id=request.GET.get("id")
    if not company_id or str(company_id)=="0":
        messagedata={'err':'true','errkey':'系统错误','type':''}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    viptype=zzt.getviptype(company_id)
    paymoney=10
    #来电宝客户    
    if viptype=='10051003':
        isldb=1
        paymoney=ldb_weixin.getldbonephonemoney(company_id)
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        isldb=None
        qianbaoblance=zzq.getqianbaoblance2(company_id)
    if paytype:
        if qianbaoblance>=paymoney:
            if isldb:
                if qianbaoblance>=paymoney:
                    ldb_weixin.getpayfee(company_id,forcompany_id,paymoney)
                    #加入通信录
                    zzc.joinaddressbook(company_id,forcompany_id)
                else:
                    messagedata={'err':'true','errkey':'余额不足','type':'viewcontact'}
                    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            else:
                #判断是否首次安装APP查看扣费
                #account=getaccount(company_id)
                #installDaynum=zzq.getfistinstallapp(account)
                #if installDaynum:
                    #paytype=13
                zzq.getpayfee(company_id,forcompany_id,id,paytype)
                #加入通信录
                zzc.joinaddressbook(company_id,forcompany_id)
            list=zzc.getcompanydetail(forcompany_id)
            messagedata={'err':'false','errkey':'','type':'viewcontact','list':list}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            messagedata={'err':'true','errkey':'余额不足','type':'viewcontact'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    messagedata={'err':'true','errkey':'系统错误','type':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    
def pro_report(request):
    company_id=request.POST.get("company_id")
    """
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    if not company_id:
        company_id=request.GET.get("company_id")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    forcompany_id=request.POST.get("forcompany_id")
    if not forcompany_id:
        forcompany_id=request.GET.get("forcompany_id")
    product_id=request.POST.get("product_id")
    if not product_id:
        product_id=request.GET.get("product_id")
    if not product_id:
        product_id=0
    content=request.POST.get("chk_value")
    if not content:
        content=request.GET.get("chk_value")
    if content:
        #----一家公司只能被一个客户投诉一次
        sql='select id from pay_report where company_id=%s and forcompany_id=%s and product_id=%s'
        result=dbc.fetchonedb(sql,[company_id,forcompany_id,product_id])
        if not result:
            zzt.getpro_report(company_id,forcompany_id,product_id,content)
    messagedata={'err':'false','errkey':'','type':'pro_report'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#报价列表
def pricelist(request):
    keywords=request.GET.get("keywords")
    type=request.GET.get("type")
    page=request.GET.get("page")
    arealist=['浙江','广州','江苏','福建','安徽','河南','河北','湖北','湖南','山东','海南','哈尔滨','北京','上海','广西','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    
    nowlanmu='<a href="/category/">交易中心 </a>'
    if keywords:
        if type=="0":
            webtitle=keywords+"行情报价"
        else:
            webtitle=keywords+"商家报价"
    else:
        webtitle="行情报价"
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(8)
    before_range_num = funpage.before_range_num(9)
    if type=='0':
        pricelist=zzt.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=keywords)
    else:
        pricelist=zzt.getpricelist_company(kname=keywords,frompageCount=frompageCount,limitNum=limitNum)
    listall=pricelist['list']
    listcount=pricelist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'arealist':arealist,'listall':listall,'keywords':keywords,'type':type}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    if int(page)>1:
        return render_to_response('trade/pricelistmore.html',locals())
    return render_to_response('trade/pricelist.html',locals())
#类别
def category(request):
    host=getnowurl(request)
    type=request.GET.get("type")
    webtitle="供求类别"
    nowlanmu="<a href='/category/'>供求分类</a>"
    code = request.GET.get("code")
    username=request.session.get("username",None)
    if (code==None):
        code='____'
        categorylist=zzt.getindexcategorylist(code,2)
        if type=="1":
            #返回json数据
            datatype=request.GET.get("datatype")
            if datatype=="json":
                return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))
            return render_to_response('trade/rightcatory.html',locals())
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))
        return render_to_response('trade/index.html',locals())
    else:
        categorylist=zzt.getindexcategorylist(code,1)
        if categorylist==[] or categorylist==None:
            categoryname=zzt.getcategoryname(code)
            return HttpResponseRedirect("/offerlist/?keywords="+categoryname)
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))
        return render_to_response('trade/categorymore.html',locals())
def fj(request):
    myaddress=request.GET.get("myaddress")
    keywords=request.GET.get("keywords")
    arealist=['浙江','广州','江苏','福建','安徽','河南','河北','湖北','湖南','山东','海南','哈尔滨','北京','上海','广西','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'arealist':arealist,'myaddress':myaddress,'keywords':keywords}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('trade/fj.html',locals())
#----发布供求
def post(request):
    sep=request.GET.get("sep")
    ptype=request.GET.get("ptype")
    saveform="products_save"
    company_id=request.GET.get("company_id")
    code=request.GET.get("code")
    randid = random.randint(10000000, 99999999)
    
    if ptype=="10331000":
        pname="供应信息"
    else:
        pname="求购信息"
    if sep=="1":
        return render_to_response('trade/post1.html',locals())
    if sep=="2":
        code='____'
        categorylist=zzt.getindexcategorylist(code,2)
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            jsonlist={'categorylist':categorylist,'ptype':ptype}
            return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
        return render_to_response('trade/post2.html',locals())
    if sep=="3":
        label=zzt.getcategoryname(code)
        return render_to_response('trade/post3.html',locals())
#----发布保存供求
def products_save(request):
    saveform="products_save"
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    proid=request.POST.get("proid")
    account=getaccount(company_id)
    randid=request.POST.get("randid")
    gmt_modified=gmt_created=datetime.datetime.now()
    error='false'
    products=request.POST.get('products')
    category=request.POST.get('category')
    title=request.POST.get('title')
    if not title:
        error='供求标题不能为空'
    quantity=request.POST.get('quantity')
    if not quantity:
        error='请输入数量'
    if quantity:
        if (quantity.isdigit()!=True):
            error="数量必须是数字"
    quantity_unit=request.POST.get('quantity_unit')
    price=request.POST.get('price')
    if price:
        if(price=="电议或面议"):
            price=0
        else:
            if (price.isdigit()!=True):
                error="价格必须数字"
    price_unit=request.POST.get('price_unit')
    if products=='10331001':
        price=''
        price_unit=''
    details=request.POST.get('details')
    if not details:
        error='产品简介不能为空'
        
    validity=request.POST.get('validity')
    vali="-1"
    if validity=="长期（一年内）":
        vali="-1"
    if validity=="三个月":
        vali="90"
    if validity=="二个月":
        vali="60"
    if validity=="十天":
        vali="10"
    if vali:
        if vali=='-1':
            validitytime='9999-12-31 23:59:59'
        else:
            validitytime=gmt_created + datetime.timedelta(days = int(vali))
    shape=request.POST.get('shape')
    level=request.POST.get('level')
    color=request.POST.get('color')
    if not color:
        color=''
    appearance=request.POST.get('appearance')
    if not appearance:
        appearance=''
    source=request.POST.get('source1')
    if not source:
        source=''
    origin=request.POST.get('origin')
    if not origin:
        origin=''
    useful=request.POST.get('useful')
    if not useful:
        useful=''
    specification=request.POST.get('specification')
    if not specification:
        specification=''
    impurity=request.POST.get('impurity')
    if not impurity:
        impurity=''
    manufacture=request.POST.get('manufacture')
    if not manufacture:
        manufacture=''
    tradesm=request.POST.get('tradesm')
    if not tradesm:
        tradesm=''
    
    if error!='false':
        messagedata={'err':'true','errkey':error}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        if proid:
            sql="update products set title=%s,quantity=%s,source_type_code=%s,quantity_unit=%s,price=%s,price_unit=%s,details=%s,expire_time=%s,gmt_modified=%s,manufacture=%s,check_status=0 where id=%s"
            dbc.updatetodb(sql,[title,quantity,'app_myrc',quantity_unit,price,price_unit,details,validitytime,gmt_modified,manufacture,proid])
            sql2="update products_pic set product_id=%s where randid=%s"
            dbc.updatetodb(sql2,[proid,randid])
            messagedata={'err':'false','errkey':'','type':'tradesave'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            
            sql="insert into products(category_products_main_code,company_id,account,products_type_code,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_modified,real_time,refresh_time,expire_time,source_type_code,location,provide_status,total_quantity,is_show_in_price,source,specification,origin,min_price,max_price,goods_type_code,tags,tags_admin,impurity,color,useful,appearance,manufacture)"
            sql+=" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'app_myrc','','N','',0,%s,%s,%s,0,0,'','','',%s,%s,%s,%s,%s)"
            result=dbc.updatetodb(sql,[category,company_id,account,trade_type,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_created,gmt_created,gmt_created,validitytime,source,specification,origin,impurity,color,useful,appearance,manufacture])
            qpic=""
            if result:
                product_id=result[0]
                if shape:
                    sql="select id from product_addproperties where pid=%s and property='形态'"
                    resultc=dbc.fetchonedb(sql,[product_id])
                    if not resultc:
                        sql="insert into product_addproperties(pid,property,content,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                        dbc.updatetodb(sql,[product_id,'形态',shape,gmt_created,gmt_modified])
                    else:
                        sql="update product_addproperties set content=%s where pid=%s and property='形态'"
                        dbc.updatetodb(sql,[shape,product_id])
                if level:
                    sql="select id from product_addproperties where pid=%s and property='级别'"
                    resultc=dbc.fetchonedb(sql,[product_id])
                    if not resultc:
                        sql="insert into product_addproperties(pid,property,content,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                        dbc.updatetodb(sql,[product_id,'级别',level,gmt_created,gmt_modified])
                    else:
                        sql="update product_addproperties set content=%s where pid=%s and property='级别'"
                        dbc.updatetodb(sql,[level,product_id])
                #交易说明
                if tradesm:
                    sql="select id from product_addproperties where pid=%s and property='交易说明'"
                    resultc=dbc.fetchonedb(sql,[product_id])
                    if not resultc:
                        sql="insert into product_addproperties(pid,property,content,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                        dbc.updatetodb(sql,[product_id,'交易说明',tradesm,gmt_created,gmt_modified])
                    else:
                        sql="update product_addproperties set content=%s where pid=%s and property='交易说明'"
                        dbc.updatetodb(sql,[tradesm,product_id])
                sql2="update products_pic set product_id=%s where randid=%s"
                dbc.updatetodb(sql2,[product_id,randid])
                messagedata={'err':'false','errkey':'','type':'tradesave'}
            else:
                messagedata={'err':'true','errkey':'系统错误，请重试'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def leavewordsuploadimg(request):
    piclist=otherimgupload(request)
    return HttpResponse(simplejson.dumps(piclist, ensure_ascii=False))
#----发布保存供求（新版app）
def post_save(request):
    saveform="products_save"
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #上传图片
    piclist=otherimgupload(request)
    
    proid = request.POST.get('proid')
    account=getaccount(company_id)
    gmt_modified=gmt_created=datetime.datetime.now()
    error='false'
    trade_type=request.POST.get('trade_type')
    category=request.POST.get('trade_code')
    title=request.POST.get('title')
    if not title:
        error='供求标题不能为空'
    quantity=request.POST.get('quantity')
    if not quantity:
        error='请输入数量'
    if quantity:
        if (quantity.isdigit()!=True):
            error="数量必须是数字"
    quantity_unit=request.POST.get('quantity_unit')
    price=request.POST.get('price')
    if price:
        if(price=="电议或面议"):
            price=0
        else:
            if (price.isdigit()!=True):
                error="价格必须数字"
    price_unit=request.POST.get('price_unit')
    if trade_type=='10331001':
        price=''
        price_unit=''
        trade_typetext="求购"
    else:
        trade_typetext="供应"
    details=request.POST.get('details')
    if not details:
        error='产品简介不能为空'
        
    validity=request.POST.get('validity')
    if validity=='-1':
        validitytime='9999-12-31 23:59:59'
    else:
        validitytime=gmt_created + datetime.timedelta(days = int(validity))

    
    if error!='false':
        messagedata={'err':'true','errkey':error}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        if proid:
            sql="update products set title=%s,quantity=%s,source_type_code=%s,quantity_unit=%s,price=%s,price_unit=%s,details=%s,expire_time=%s,gmt_modified=%s,check_status=0 where id=%s and company_id=%s"
            dbc.updatetodb(sql,[title,quantity,'app_myrc',quantity_unit,price,price_unit,details,validitytime,gmt_modified,proid,company_id])
            if piclist:
                for p in piclist:
                    if p:
                        sql2="update products_pic set product_id=%s where id=%s"
                        dbc.updatetodb(sql2,[proid,p['id']])
            messagedata={'err':'false','errkey':'','type':'tradesave'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            #购买显示联系方式
            contactflag=request.POST.get('contactflag')
            if (contactflag=="1"):
                showcontactnum=request.POST.get('showcontactnum')
                if showcontactnum:
                    qianbaopaysave(company_id=company_id,paytype="11",money=showcontactnum)
            
            
            sql="insert into products(category_products_main_code,company_id,account,products_type_code,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_modified,real_time,refresh_time,expire_time,source_type_code,location,provide_status,total_quantity,is_show_in_price,source,specification,origin,min_price,max_price,goods_type_code,tags,tags_admin,impurity,color,useful,appearance,remark,old_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'app_myrc','','N','',0,'','','',0,0,'','','','','','','','',0)"
            result=dbc.updatetodb(sql,[category,company_id,account,trade_type,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_created,gmt_created,gmt_created,validitytime])
            qpic="http://img0.zz91.com/zz91/images/indexLogo.png"
            if result:
                product_id=result[0]
                #购买供求置顶
                protopchecked=request.POST.get('protopchecked')
                if protopchecked:
                    payreturn=qianbaopaysave(company_id=company_id,proid=product_id,paytype="9")
                #购买流量宝
                llbchecked=request.POST.get('llbchecked')
                if str(llbchecked)=="1":
                    gmt_created=datetime.datetime.now()
                    keywords=request.POST.get('keywords')
                    if keywords:
                        sqld="insert into app_jingjia_keywords(company_id,keywords,price,product_id,gmt_created) values(%s,%s,%s,%s,%s)"
                        dbc.updatetodb(sqld,[company_id,keywords,5,product_id,gmt_created])
                    
                if piclist:
                    i=0
                    for p in piclist:
                        if (i==0):
                            qpic=p['path']
                        if p:
                            sql2="update products_pic set product_id=%s where id=%s"
                            dbc.updatetodb(sql2,[product_id,p['id']])
                            i+=1
                #写入朋友圈
                qtitle="我发布了一条供求"
                qcontent=trade_typetext+title
                qcompany_id=company_id
                #qpic=""
                qtype="post_products"
                qurl="http://m.zz91.com/detail/?id="+str(product_id)+""
                insert_appquan(qcompany_id,qtitle,qcontent,qpic,qurl,qtype,gmt_created)
                sharelist={'title':qcontent,'pic':qpic,'url':qurl}
                messagedata={'err':'false','errkey':'','type':'tradesave','sharelist':sharelist}
            else:
                messagedata={'err':'true','errkey':'系统错误，请重试3'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#留言保存
def leavewords_save(request):
    webtitle="客户留言"
    nowlanmu="<a href='/category/'>交易中心</a>"
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    be_inquired_type=request.POST.get("be_inquired_type")
    send_username=getaccount(company_id)
    send_company_id=request.POST.get("company_id")

    re_company_id = request.POST.get('forcompany_id')

    title='我对贵公司的产品感兴趣！'
    content = request.POST.get('content')
    errflag=None
    if (content=="" or content==None):
        messagedata={'err':'true','errkey':'来写点什么吧...'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
    if (errflag==None):
        if not be_inquired_type:    
            be_inquired_type=0
        be_inquired_id=request.POST.get('pid')
        inquired_type=0
        sender_account=send_username
        receiver_account=getaccount(re_company_id)
        send_time=datetime.datetime.now()
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        
        if company_id>re_company_id:
            conversation_group=str(company_id)+"-"+str(re_company_id)
        else:
            conversation_group=str(re_company_id)+"-"+str(company_id)
        #加入通信录
        if re_company_id:
            zzc.joinaddressbook(company_id,re_company_id)
        value=[title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified,conversation_group]
        sql="insert into inquiry(title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified,conversation_group) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        #更新app聊天
        chat_group=conversation_group.replace("-",",")
        sql="select id,chat_count from app_chat where chat_group=%s"
        result=dbc.fetchonedb(sql,[chat_group])
        if result:
            chat_count=result[1]
            if chat_count:
                chat_countlist=eval(chat_count)
                for ll in chat_countlist:
                    chat_countnum=chat_countlist[ll]
                    if str(ll)==str(company_id):
                        chat_countnum=chat_countnum+1
                    chat_countlist[ll]=chat_countnum
                chat_countarr=str(chat_countlist)
                #chat_countarr=type(eval(chat_count))
                #mycount=chat_countarr[str(company_id)]
                #tocount=chat_countarr[str(re_company_id)]
                #chat_countarr[str(re_company_id)]=int(tocount)+1
                #chat_countarr=chat_countarr[0]
            else:
                chat_countarr='{"'+str(company_id)+'":1,"'+str(re_company_id)+'":0}'
                
            sql="update app_chat set gmt_modified=%s,chat_content=%s,chat_count=%s where id=%s"
            dbc.updatetodb(sql,[gmt_modified,content[0:1000],chat_countarr,result[0]]);
        else:
            chat_countarr='{"'+str(company_id)+'":1,"'+str(re_company_id)+'":0}'
            sql="insert into app_chat (chat_group,chat_content,chat_count,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,[chat_group,content[0:1000],chat_countarr,gmt_modified,gmt_modified]);
        #----更新弹窗
        #updateopenfloat(re_company_id,0)
        sucflag="1"
        messagedata={'err':'false','errkey':'','type':'leavewords'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#收藏
def favorite(request):
    webtitle="我的收藏"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    account=getaccount(company_id)
    
    cid=request.POST.get("forcompany_id")
    pdtid=request.POST.get("pdtid")
    products_type_code=request.POST.get("products_type_code")
    
    favorite_type_code=request.POST.get("favorite_type_code")
    favoriteflag=request.POST.get("favoriteflag")
    
    if favorite_type_code==None or favorite_type_code=="":
        if (pdtid==None or pdtid=='None'):
            favorite_type_code="10091002"
            content_id=cid
            
        else:
            if (products_type_code=="10331000"):
                favorite_type_code="10091006"
            if (products_type_code=="10331001"):
                favorite_type_code="10091006"
            content_id=pdtid
        #加入通信录
        if cid:
            zzc.joinaddressbook(company_id,cid)
    else: 
        content_id=request.POST.get("content_id")
    if not content_id:
        content_id=0
        
    content_title=request.POST.get("title")
    if not content_title:
        content_title="err"
    if str(favoriteflag)=="1":
        sql="delete from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
        dbc.updatetodb(sql,[favorite_type_code,content_id,company_id]);
        messagedata={'err':'false','errkey':'取消成功','type':'favorite'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()

    value=[favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account]
    sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
    clist=dbc.fetchonedb(sql,[favorite_type_code,content_id,company_id])
    if (clist):
        sucflag=None
    else:
        sql="insert into myfavorite(favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account) values(%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        sucflag=1
    messagedata={'err':'false','errkey':'收藏成功','type':'favorite'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

#活动用户统计数据
def user_tongjidata(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    tongjidata=zzt.getcompanypv(company_id)
    list={'err':'false','errkey':'','tongjidata':tongjidata}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
