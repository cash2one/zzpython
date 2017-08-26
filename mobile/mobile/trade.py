#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,chardet,simplejson,random,socket
from django.core.cache import cache
from datetime import timedelta,date
from django.utils.http import urlquote
from operator import itemgetter, attrgetter
from sphinxapi import *
from zz91page import *
import Image,ImageDraw,ImageFont,ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from settings import spconfig
#from commfunction import subString,filter_tags,replacepic,
from commfunction import filter_tags,formattime,subString
from function import getnowurl
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb
dbc=companydb()
dbsms=smsdb()
dbn=newsdb()
dbads=adsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

zzqianbao=qianbao()
zztrade=ztrade()
ldb_weixin=ldbweixin()
zzc=zcompany()
from qianbao import qianbaopaysave

#----图片上传
def otherimgupload(request):
    #source 
    source=request.GET.get("source")
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    #return HttpResponse(request.FILES)
    hostname = socket.gethostname()
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
                mediatype="video"
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
                picurl="http://"+hostname+"img.zz91.com/other/"+timepath+str(nowtime)+str(tmp)+"."+filetype
            else:
                mediatype="pic"
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
                        wm = Image.open(nowpath+"/media/logo.png")
                        layer = Image.new('RGBA', im.size, (0,0,0,0))
                        layer.paste(wm, (im.size[0] - 120, im.size[1] - 50))
                        im = Image.composite(layer, im, layer)
                    #加字体水印
                    fontPath=nowpath+'/media/SIMHEI.TTF'
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
                #picurl="http://img4.zz91.com/300x15000/other/"+timepath+str(nowtime)+str(tmp)+"."+kzname
                picurl="http://"+hostname+"img.zz91.com/other/"+timepath+str(nowtime)+str(tmp)+"."+kzname
                #picurl="http://images.zz91.com/images.php?width=300&height=15000&picurl=http://img1.zz91.com/other/"+timepath+str(nowtime)+str(tmp)+"."+kzname
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
            list={'path':picurl,'id':picid,'databasepath':databasepath,'mediatype':mediatype}
            listall.append(list)
        return listall
    return None

def tradeindex(request):
    keywords = request.GET.get("keywords")#搜索
    orderflag = request.GET.get("orderflag")#搜索
    if keywords or orderflag:
        return offerlist(request)
    host=getnowurl(request)
    code = request.GET.get("code")
    username=request.session.get("username",None)
    if (code==None):
        code='____'
        categorylist=getindexcategorylist(code,2)
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))
        #return render_to_response('trade/index.html',locals())
        return render_to_response('aui/trade/category.html',locals())
    else:
        categorylist=getindexcategorylist(code,1)
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))
        
        return render_to_response('aui/trade/category.html',locals())
def category(request,code):
    if code:
        nowcategory=getcategory_products(code)
        categorylist=getindexcategorylist(code,1)
        categorylistmain=getindexcategorylist('____',2)
        webtitle=nowcategory['label']
        nowlanmu="<a href='/trade/'>"+nowcategory['label']+"</a>"
    return render_to_response('trade/category.html',locals())
#--供求供应
def offergongyin(request,pinyin="",page=""):
    
    return offerlist(request,pinyin=pinyin,ptype="1",page=page)
#--供求求购
def offerqiugou(request,pinyin="",page=""):
    return offerlist(request,pinyin=pinyin,ptype="2",page=page)
def gettagslist(kname,num):
    #return None
    kname_hex="1"
    if kname:
        kname_hex=getjiami(kname)
    listall=cache.get("mobile_trade_tagslist"+str(kname_hex)+str(num))
    if not listall:
        #-------------最新标签
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"search_count desc" )
        cl.SetLimits (0,num,num)
        res = cl.Query ('','tagslist')
        if (kname):
            res = cl.Query ('@tname '+kname,'tagslist')
        else:
            res = cl.Query ('','tagslist')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                ii=1
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    tags=attrs['tags']
                    tags=tags.replace("/","")
                    list1={'kname':tags}
                    listall.append(list1)
                cache.set("mobile_trade_tagslist"+str(kname_hex)+str(num),listall,60*10)
    return listall
#----供求列表(排序最复杂)
def offerlist(request,pinyin="",ptype="",page=""):
    mnew = request.GET.get("mnew")
    sorttype = request.GET.get("sorttype")
    if pinyin:
        keywords=zztrade.getcategorylabel(pinyin)
        if not keywords:
            return page404(request)
        nopinyin=None
    else:
        keywords = request.GET.get("keywords")#搜索
        nopinyin=1
    #shoprolist=getshoprolist()
    #showpost=1
    arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    host=getnowurl(request)
    #alijsload="1"
    nowlanmu="<a href='/trade/'>供求类别</a>"
    if not page or page=="":
        page = request.GET.get("page")
    if (page == None or page=='' or page=="None"):
        page = "1"
    pagenum=page
    nowsearcher="offersearch_new"
    
    if (keywords):
        keywords=keywords.replace("+","")
        keywords=keywords.replace("\\","")
        keywords=keywords.replace("#","")
        keywords=keywords.replace(")","")
        keywords=keywords.replace("(","")
    #热门搜索
    hotsearchlist=gettagslist(keywords,10)
    keywords_real = keywords#搜索
    keywords111=str(host)
    arrkey=keywords111.split("keywords=")
    if len(arrkey)>1:
        keywords111=arrkey[1]
        arrkey=keywords111.split("^and^")
        keywords111=arrkey[0]
    
        #keywords111="ppr%D4%D9%C9%FA%BF%C5%C1%A3"
        charttype=chardet.detect(urllib.unquote(str(keywords111)))['encoding']
        #keywords111=charttype
        #if charttype:
        #    if ("utf" not in charttype):
        #       keywords=urllib.unquote(str(keywords111)).decode('gb2312','ignore').encode('utf-8')
    if not keywords:
        keywords=keywords_real
    if keywords:
        adlist=getadlistkeywords("736",keywords)
    if keywords:
        webtitle=keywords+"_供求列表"
    if keywords=='None' or keywords=='':
        webtitle="供求列表"
        keywords=''
    
    company_id=request.session.get("company_id",None)
    if keywords:
        #保存搜索记录
        updatesearchKeywords(request,company_id,keywords,ktype="trade")
    if company_id:
        
        #----判断是否为来电宝用户,获取来电宝余额
        isldb=None
        viptype=getviptype(company_id)
        if viptype=='10051003':
            isldb=1
            #ldbblance=getldblaveall(company_id,"")
            #qianbaoblance=ldbblance
        #else:
            #qianbaoblance=getqianbaoblance2(company_id,"")
    username=request.session.get("username",None)
    searchname = urlquote(request.GET.get("searchname"))
    if ptype:
        pdt_kind=ptype
    else:
        pdt_kind = request.GET.get("ptype")
    province = request.GET.get("province")
    provincecode = request.GET.get("provincecode")
    posttime = request.GET.get("posttime")
    pdtidlist = request.GET.get("pdtidlist")
    priceflag = str(request.GET.get("priceflag"))
    nopiclist = request.GET.get("nopiclist")
    tfromdate = request.GET.get("fromdate")
    ttodate = request.GET.get("todate")
    jmsearchname = request.GET.get("jmsearchname")
    fromsort = request.GET.get("fromsort")
    #新版app 供求定制
    orderflag=request.GET.get("orderflag")
    if orderflag:
        username=request.session.get("username",None)
        company_id=request.session.get("company_id",None)
        if username and (company_id==None or str(company_id)=="0"):
            company_id=getcompanyid(username)
            request.session['company_id']=company_id
        if (username==None or (company_id==None or str(company_id)=="0")):
            return HttpResponseRedirect("/login/?done="+host)
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
            pdt_kind=str(result[0])
            timearg=str(result[1])
            showkeywords="定制信息"
            if not keywords:
                return HttpResponseRedirect("/order/business.html")
        else:
            return HttpResponseRedirect("/order/business.html")
    else:
        showkeywords=keywords
        if showkeywords:
            if "|" in showkeywords:
                showkeywords="定制信息"
    for ltt0 in ['供应','出售','卖']:
        if keywords:
            if ltt0 in keywords:
                keywords=keywords.replace(ltt0,'')
                pdt_kind='1'
    for ltt1 in ['求购','回收','买','收购']:
        if keywords:
            if ltt1 in keywords:
                keywords=keywords.replace(ltt1,'')
                pdt_kind='2'
    
    forcompany_id = request.GET.get("company_id")
    havepic = request.GET.get("havepic")
    haveprice = request.GET.get("haveprice")
    isding=1
    if havepic or haveprice:
        isding=''
    pdt_kindname=''
    if pdt_kind=='1':
        pdt_kindname='供应'
    if pdt_kind=='2':
        pdt_kindname='求购'
    nowlanmu2=pdt_kindname
    if haveprice:
        nowlanmu2+='－ 价格'
    if havepic:
        nowlanmu2+='－ 图片'
    #----时间筛选
    timearg = request.GET.get("timearg")
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
    else:
        timearg=''

    if (str(page)=='1' or page=='' or str(page)=='None'):
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
    #获得相关类别
    #categorylist=getcategorylist(kname=keywords,limitcount=20)
    if (pdtidlist!=None and pdtidlist!=''):
        #arrpdtidlist=pdtidlist.split(',')
        arrpdtidlist=pdtidlist
        listall=[]
        n=1
        for p in arrpdtidlist:
            if (p!=''):
                list1=getcompinfo(p[0],"",keywords,company_id)
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
        gqtype="p1"
    if (pdt_kind =='1'):
        pdt_type='0'
        stab1=""
        stab2="offerselect"
        stab3=""
        gqtype="gy"
    if (pdt_kind=='2'):
        pdt_type='1'
        stab1=""
        stab2=""
        stab3="offerselect"
        gqtype="qg"
    
    if not page:
        page=1
    nowpage=int(page)
    page=20*(int(page)-1)
    #keywords2=keywords.replace('|',' ')
    if keywords:
        keywords2=keywords.replace(' ','')
        
        keywords1=urlquote(keywords2)
        ttype = request.GET.get("ttype")
        #keywords=keywords.replace('|',' ')
        keywords=keywords.replace('\\',' ')
        keywords=keywords.replace('/',' ')
        keywords=keywords.replace('/',' ')
        keywords=keywords.replace('(',' ')
        keywords=keywords.replace(')',' ')
        seo_keywords=keywords
    
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
    searchname=str(keywords1)
    searchname=searchname.replace('%28','astokhl')
    searchname=searchname.replace('%29','astokhr')
    searchname=searchname.replace('%5C','asto5c')
    searchname=searchname.replace('/','astoxg')
    searchname=searchname.replace('-','astohg')
    after_range_num = 8
    before_range_num = 9
    port = spconfig['port']
    gqtext="供求"
    if pdt_kind=="1":
        gyurl="gy"
        gqtext="供应"
    if pdt_kind=="2":
        gyurl="qg"
        gqtext="求购"
    #----------------------------
    cl = SphinxClient()
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
        cl.SetFilterRange('length_price',4,10000)
        list.SetFilterRange('length_price',4,10000)
        cl.SetFilter('haveprice',[1],True)
        list.SetFilter('haveprice',[1],True)
    if forcompany_id:
        forcompany_id=int(forcompany_id)
        cl.SetFilter('company_id',[forcompany_id])
        list.SetFilter('company_id',[forcompany_id])
        forcompany_name=getppccompanyinfo(forcompany_id)
        if forcompany_name:
            forcompany_name=forcompany_name['companyname']
        seo_keywords=forcompany_name
    
    if (province ==None or province ==''):
        provincestr=''
    else:
        provincestr='&@(province,city) '+province

    if (priceflag == '1'):
        cl.SetFilter('length_price',[0],True)
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price desc,refresh_time desc" )
    elif (priceflag == '2'):
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price asc,refresh_time desc" )
    else:
        list.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    if keywords=='':
        res = list.Query ('',nowsearcher)
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
    if not keywords:
        rescount = cl.Query ('','offersearch_new_vip')
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
                """
                if phone_num==10000:
                    phone_sort=10000;
                else:
                    phone_sort=phone_rate*0.05+phone_num*0.85+phone_fee*0.1
                """
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
                listall.append(list1)
                testcom_id=com_id
    #listallvip=sorted(listall, key=itemgetter(1,4,5,2,6,3),reverse=True)
    if sorttype=="member":
        listallvip=sorted(listall, key=itemgetter(1,4,2,5,3),reverse=True)
        ordtext="会员等级"
    elif sorttype=="pro":
        listallvip=sorted(listall, key=itemgetter(1,4,5,2,3),reverse=True)
        ordtext="信息质量"
    else:
        listallvip=sorted(listall, key=itemgetter(1,4,7,2,3),reverse=True)
        ordtext="排序"
    if havepic:
        ordtext="有图片"
    if haveprice:
        ordtext="有价格"
    if not sorttype:
        sorttype=''
    #优先排序数
    viplen=len(listallvip)
    #供求总数
    listcount+=int(viplen)
    #最后一页的供求数
    lastpNum=int(viplen-ceil(viplen / 20)*20)
    #3天内供求页码
    vippage=ceil(viplen / 20)
    #开始供求数位置
    beginpage=page
    #优先排序页码
    """
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
    """
    #一页内
    if viplen<=20 and int(nowpage)==1:
        endpage=viplen
        limitNum=20-viplen
        notvip=0
        if limitNum>0:
            offsetNum=0
            notvip=1
    elif int(nowpage)<vippage:
        endpage=page+20
        limitNum=20
        notvip=0
    elif int(nowpage)==vippage:
        if lastpNum==0:
            endpage=page+20
            limitNum=20
            notvip=0
        else:
            endpage=page+lastpNum
            offsetNum=0
            limitNum=20-lastpNum
            notvip=1
    elif int(nowpage)>vippage:
        limitNum=20
        endpage=page+20
        offsetNum=int(nowpage)*20-viplen-20
        notvip=1
    
    #列出供求信息列表
    listall=[]
    productList=[]
    if listallvip:
        for match in listallvip[beginpage:endpage]:
            list1=getcompinfo(match[0],"",keywords2,company_id)
            listall.append(list1)
        productList=listall
        
    
    #普通供求开始数
    """
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
    """
    listall=productList
    
    if (notvip==1):
        list.SetLimits (offsetNum,limitNum,100000)
        if not keywords:
            res = list.Query ('',nowsearcher)
        else:
            res = list.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)

        if res:
            if res.has_key('matches'):
                prodlist=res['matches']
                for list in prodlist:
                    id=list['id']
                    list1=getcompinfo(id,"",keywords2,company_id)
                    listall.append(list1)
                productList=listall
    try:
        page = int(pagenum)
        if int(page) < 1:
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
    nextpage=int(page)+1
    prvpage=int(page)-1
    return render_to_response('aui/trade/list.html',locals())
    #return render_to_response('2016new/trade/list.html',locals())
def detail301(request):
    id=request.GET.get("id")
    return HttpResponsePermanentRedirect("/trade/detail"+str(id)+".html")
#竞价点击计费
def hiturl(request):
    rd=request.GET.get("rd")
    area=request.GET.get("area")
    userid=clientid=request.GET.get("clientid")
    company_id=request.session.get("company_id",None)
    
    t=random.randrange(0,1000000)
    gmt_created=datetime.datetime.now()
    userid=request.session.get("userid",None)
    if not userid:
        userid=getjiami(str(t)+str(gmt_created)+clientid)
        request.session['userid']=userid
    else:
        request.session['userid']=userid
    if company_id:
        request.session['userid']=userid
        userid=company_id
        
    if not rd:
        return HttpResponse("err")
    sql="select key_id,pdt_id,id,keywords from app_jingjia_search where hiturl=%s"
    result=dbc.fetchonedb(sql,[rd])
    if result:
        key_id=result[0]
        pdt_id=result[1]
        search_id=result[2]
        keywords=result[3]
        if pdt_id:
            sql="select check_status from products where id=%s"
            result=dbc.fetchonedb(sql,[pdt_id])
            check_status=''
            if result:
                check_status=str(result[0])
            if check_status!="2":
                sql="select company_id,price from app_jingjia_keywords where id=%s"
                result=dbc.fetchonedb(sql,[key_id])
                if result:
                    forcompany_id=result[0]
                    price=result[1]
                    sourcetype=1
                    user_company_id=company_id
                    if str(company_id)!=str(forcompany_id):
                        gmt_created=datetime.datetime.now()
                        sqlc="select id from app_jingjia_click where key_id=%s and userid=%s"
                        res=dbc.fetchonedb(sqlc,[key_id,userid])
                        if not res:
                            clickcount=1
                            sqld="insert into app_jingjia_click(key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,company_id,area,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            dbc.updatetodb(sqld,[key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,forcompany_id,area,gmt_created])
                            #扣款
                            zzqianbao.getpayfee(company_id=forcompany_id,forcompany_id=company_id,product_id=search_id,ftype=55,fee=-int(price))
                        else:
                            sqld="update app_jingjia_click set clickcount=clickcount+1 where id=%s"
                            dbc.updatetodb(sqld,[res[0]])
        
        return HttpResponseRedirect("/trade/detail"+str(pdt_id)+".html")
    else:
        return HttpResponse("err")
    #resjson={'err':'false','errkey':''}
    #return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
#----供求最终页
def detail(request,pid=""):
    host=getnowurl(request)
    #showpost=1
    backurl=request.META.get('HTTP_REFERER','/')
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    nowlanmu='<a href="/category/">交易中心 </a>'
    nowlanmu2='<a href="/category/">交易中心 </a> > '
    keywords1=''
    keywords=request.GET.get("keywords")
    gmt_created=datetime.datetime.now()
    if not keywords:
        if '&' in backurl:
            keywords1=re.findall('keywords=(.*?)&',backurl)
        else:
            keywords1=re.findall('keywords=(.*)',backurl)
    if keywords and keywords!="None":
        nowlanmu2+='<a href="/trade/?keywords='+str(keywords)+'">'+str(keywords)+'</a>&nbsp;>'
    if not pid:
        id=request.GET.get("id")
    else:
        id=pid
    done = request.path
    favoriteflag=0
    if company_id:
        favoriteflag=isfavorite(id,'10091006',company_id)
    list=zztrade.getproductdetail(id)
    forcompany_id=0
    if list:
        forcompany_id=list['company_id']
    if forcompany_id==0:
        return render_to_response('404.html',locals())
    #记录pv
    getproductspv(id,forcompany_id)
    paymoney=10
    """
    #----判断举报状态
    reportcheck=zztrade.getreportcheck(company_id,forcompany_id,pid)
    if reportcheck==0:
        idcheck=1
        idchecktxt='举报处理中'
    if reportcheck==1:
        idcheck=1
        idchecktxt='举报已处理'
    if reportcheck==2:
        idcheck=1
        idchecktxt='举报退回'
    now = int(time.time())
    paymoney=10
    
    #该公司是否被举报成功过
    isjubao=zztrade.getreportischeck(forcompany_id,pid)
    #----判断是否为来电宝用户,获取来电宝余额
    isldb=None
    viptype=zzqianbao.getviptype(company_id)
    if viptype=='10051003':
        isldb=1
        paymoney=ldb_weixin.getldbonephonemoney(company_id)
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        qianbaoblance=zzqianbao.getqianbaoblance2(company_id)
    """
    #是否查看过
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    """
    if not isseecompany:
        paytype=request.GET.get("paytype")
        if paytype:
            if qianbaoblance>=paymoney:
                if isldb:
                    seepay=ldb_weixin.getpayfee(company_id,forcompany_id,paymoney)
                else:
                    seepay=zzqianbao.getpayfee(company_id,forcompany_id,id,paytype)
                if seepay==1:
                    isseecompany=1
            else:
                isseecompany==None
    """
    #z置顶客户显示联系方式
    keywordstopcompanyflag=zztrade.keywordstopcompany(id)
    if keywordstopcompanyflag:
        isseecompany=1
        forvipflag=None
    #流量宝客户联系方式公开
    forqianbaoblance=zzqianbao.getqianbaoblance2(forcompany_id)
    #钱包余额必须打5元
    if forqianbaoblance>8:
        jingjiaflag=zzqianbao.jingjia_keywords_online(forcompany_id)
        if jingjiaflag:
            isseecompany=1
            forvipflag=None
    if list:
        #来电宝客户显示400
        if list['viptype']:
            if list['viptype']['ldb']:
                list['mobile1']=None
                if list['viptype']['ldb']['ldbphone']:
                    list['mobile1']=list['viptype']['ldb']['ldbphone']
                    isseecompany=1
            list['mobilelist']=[]
        webtitle=list['title']
    return render_to_response('aui/trade/detail.html',locals())
#判断联系方式是否直接可以查看
def showcontact(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    if not company_id:
        errlist={'err':'true','errkey':'未登录','type':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    forcompany_id=request.POST.get("forcompany_id")
    companyinfo=zzc.show_contact(company_id=company_id,forcompany_id=forcompany_id)
    if not companyinfo:
        companyinfo={}
    return HttpResponse(simplejson.dumps(companyinfo, ensure_ascii=False))
#查看联系方式
def viewcontact(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    if not company_id:
        errlist={'err':'true','errkey':'未登录','type':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    forcompany_id=request.POST.get("forcompany_id")
    paytype=request.POST.get("paytype")
    id=request.POST.get("id")
    if not forcompany_id:
        forcompany_id=request.GET.get("forcompany_id")
        paytype=request.GET.get("paytype")
        id=request.GET.get("id")
    
    #是否查看过
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    if isseecompany:
        list=zzc.getcompanydetail(forcompany_id)
        if list['viptype']:
            if list['viptype']['ldb']:
                list['mobile1']=None
                if list['viptype']['ldb']['ldbphone']:
                    list['mobile1']=list['viptype']['ldb']['ldbphone']
                    list['mobilelist']=[list['viptype']['ldb']['ldbphone']]
        companyinfo={}
        companyinfo['mobilelist']=list['mobilelist']
        companyinfo['mobile1']=list['mobile1']
        companyinfo['contact']=list['contact']
        messagedata={'err':'false','errkey':'','type':'viewcontact','list':companyinfo}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        viptype=zzqianbao.getviptype(company_id)
        paymoney=10
        #来电宝客户    
        if viptype=='10051003':
            isldb=1
            paymoney=ldb_weixin.getldbonephonemoney(company_id)
            ldbblance=ldb_weixin.getldblaveall(company_id)
            qianbaoblance=ldbblance
        else:
            isldb=None
            qianbaoblance=zzqianbao.getqianbaoblance2(company_id)
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
                    zzqianbao.getpayfee(company_id,forcompany_id,id,paytype)
                    #加入通信录
                    zzc.joinaddressbook(company_id,forcompany_id)
                list=zzc.getcompanydetail(forcompany_id)
                companyinfo={}
                companyinfo['mobilelist']=list['mobilelist']
                companyinfo['mobile1']=list['mobile1']
                companyinfo['contact']=list['contact']
                messagedata={'err':'false','errkey':'','type':'viewcontact','list':companyinfo}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            else:
                messagedata={'err':'true','errkey':'余额不足','type':'viewcontact'}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    messagedata={'err':'true','errkey':'系统错误','type':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#举报
def pro_report(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    if not company_id:
        errlist={'err':'true','errkey':'未登录','type':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    forcompany_id=request.GET.get("forcompany_id")
    product_id=request.GET.get("product_id")
    content=request.GET.get("chk_value")
    if content:
        #----一家公司只能被一个客户投诉一次
        sql='select id from pay_report where company_id=%s and forcompany_id=%s and product_id=%s'
        result=dbc.fetchonedb(sql,[company_id,forcompany_id,product_id])
        if not result:
            zztrade.getpro_report(company_id,forcompany_id,product_id,content)
            messagedata={'err':'false','errkey':'','type':''}
        else:
            messagedata={'err':'true','errkey':'你已经举报过','type':'jubao'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    return HttpResponse('1')

#拨打电话记录
def telclicklog(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    backurl = request.META.get('HTTP_REFERER','/')
    if not company_id:
        company_id=request.GET.get("company_id",None)
    gmt_created=datetime.datetime.now()
    tel=request.GET.get("tel")
    pagefrom=request.GET.get("pagefrom")
    forcompany_id=request.GET.get("forcompany_id")
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    if (company_id==None or str(company_id)=="0"):
        company_id=0
    if tel:
        sqlp="insert into phone_telclick_log(company_id,tel,pagefrom,gmt_created,url,forcompany_id) values(%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sqlp,[company_id,tel,pagefrom,gmt_created,backurl,forcompany_id])
    """
    sql="select id from phone_telclick_log where tel=%s and company_id=%s and DATEDIFF(CURDATE(),gmt_created)<=0"
    result=dbc.fetchonedb(sql,[tel,company_id])
    if not result:
        sqlp="insert into phone_telclick_log(company_id,tel,pagefrom,gmt_created,url,forcompany_id) values(%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sqlp,[company_id,tel,pagefrom,gmt_created,backurl,forcompany_id])
    else:
        sqlp="update phone_telclick_log set num=num+1,forcompany_id=%s where id=%s"
        dbc.updatetodb(sqlp,[forcompany_id,result[0]])
    """
    return HttpResponse(simplejson.dumps({'err':'false'}, ensure_ascii=False))

def pricelist(request):
    keywords=request.GET.get("keywords")
    type=request.GET.get("type")
    page=request.GET.get("page")
    nowlanmu='<a href="/trade/">交易中心 </a>'
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
        pricelist=zztrade.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=keywords)
    else:
        pricelist=zztrade.getpricelist_company(kname=keywords,frompageCount=frompageCount,limitNum=limitNum)
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
    return render_to_response('trade/pricelist.html',locals())

#----发布保存供求（新版app）
def post_save(request):
    saveform="products_save"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    proid = request.POST.get('proid')
    account=username
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
    
    
    shape=request.POST.get('shape')
    level=request.POST.get('level')
    color=request.POST.get('color')
    if not color:
        color=''
    appearance=request.POST.get('appearance')
    if not appearance:
        appearance=''
    source=request.POST.get('source')
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
    
    piclist=request.POST.get('piclist')
    piclist=piclist.split(",")
    if error!='false':
        messagedata={'err':'true','errkey':error}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        #购买显示联系方式
        contactflag=request.POST.get('contactflag')
        if (contactflag=="1"):
            showcontactnum=request.POST.get('showcontactnum')
            if showcontactnum:
                qianbaopaysave(company_id=company_id,paytype="11",money=showcontactnum)
        if proid:
            sql="update products set category_products_main_code=%s,products_type_code=%s,title=%s,quantity=%s,source_type_code=%s,quantity_unit=%s,price=%s,price_unit=%s,details=%s,expire_time=%s,gmt_modified=%s,source=%s,specification=%s,origin=%s,impurity=%s,color=%s,useful=%s,appearance=%s,manufacture=%s,check_status=0 where id=%s and company_id=%s"
            dbc.updatetodb(sql,[category,trade_type,title,quantity,'app_myrc',quantity_unit,price,price_unit,details,validitytime,gmt_modified,source,specification,origin,impurity,color,useful,appearance,manufacture,proid,company_id])
            product_id=proid
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
            #图片
            if piclist:
                for p in piclist:
                    if p:
                        sql2="update products_pic set product_id=%s where id=%s"
                        dbc.updatetodb(sql2,[proid,p])
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
                        
                #购买供求置顶
                protopchecked=request.POST.get('protopchecked')
                if protopchecked:
                    payreturn=qianbaopaysave(company_id=company_id,proid=product_id,paytype="9")
                #购买流量宝
                llbchecked=request.POST.get('llbchecked')
                if llbchecked:
                    gmt_created=datetime.datetime.now()
                    keywords=request.POST.get('keywords')
                    if keywords:
                        sqld="insert into app_jingjia_keywords(company_id,keywords,price,product_id,gmt_created) values(%s,%s,%s,%s,%s)"
                        dbc.updatetodb(sqld,[company_id,keywords,5,product_id,gmt_created])
                if piclist:
                    i=0
                    for p in piclist:
                        if p:
                            if (i==0):
                                sql="select pic_address from products_pic where id=%s"
                                result=dbc.fetchonedb(sql,[p])
                                if result:
                                    picurl=result[0]
                                    qpic="http://img3.zz91.com/300x15000/"+picurl
                            sql2="update products_pic set product_id=%s where id=%s"
                            dbc.updatetodb(sql2,[product_id,p])
                            i+=1
                #写入朋友圈
                qtitle="我发布了一条供求"
                qcontent=trade_typetext+title
                qcompany_id=company_id
                #qpic=""
                qtype="post_products"
                qurl="http://m.zz91.com/detail/?id="+str(product_id)+""
                insert_appquan(qcompany_id,qtitle,qcontent,qpic,qurl,qtype,gmt_created)
                
                messagedata={'err':'false','errkey':'','type':'tradesave'}
            else:
                messagedata={'err':'true','errkey':'系统错误，请重试3'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#供求发布成功，匹配供求
def post_success(request):
    keywords=request.GET.get("keywords")
    trade_type=request.GET.get("trade_type")
    llbchecked=request.GET.get("llbchecked")
    ptype=0
    if (trade_type=="10331000"):
        ptype=1
    if (trade_type=="10331001"):
        ptype=2
    listall=zztrade.getcompanyproductslistnew(kname=keywords,frompageCount=0,limitNum=30,pdt_type=ptype)
    return render_to_response('aui/trade/post_success.html',locals())

#留言成功
def question_success(request):
    forcompany_id=request.GET.get("forcompany_id")
    quanfachecked=request.GET.get("quanfachecked")
    return render_to_response('aui/trade/question_success.html',locals())
