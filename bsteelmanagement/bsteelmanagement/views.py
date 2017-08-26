#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from sphinxapi import SphinxClient,SPH_MATCH_BOOLEAN,SPH_SORT_EXTENDED
from zz91page import *
import datetime,time,urllib,re,sys,os,MySQLdb,settings,StringIO,Image,ImageDraw,ImageFont,ImageFilter,random
import simplejson
import md5,hashlib
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/function.py")
reload(sys)
sys.setdefaultencoding('UTF-8')

conn=database()
cursor = conn.cursor()
#获得token
def tokeninfo(request):
    token=request.POST.get("usertoken")
    #过期时间为2小时  MINUTE,HOUR
    sql="select token from token where token=%s and TIMESTAMPDIFF(HOUR,gmt_created,NOW())<=2"
    listd=fetchonedb(sql,[token])
    if not listd:
        messagedata={'err':'true','errkey':'未获得TOKEN'}
    else:
        messagedata={'err':'false','errkey':'','result':token}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#获取新token
def get_token(request):
    token=request.GET.get("usertoken")
    md5pwd=request.GET.get("md5pwd")
    if md5pwd:
        md5pwd=md5pwd.lower()
    username=request.GET.get("username")
    if not md5pwd:
        messagedata={'err':'true','result':'没有密码'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    if not username:
        messagedata={'err':'true','result':'没有用户名'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    """
    sql="select token from token where TIMESTAMPDIFF(HOUR,gmt_created,NOW())<=1 order by id desc"
    listd=fetchonedb(sql)
    if listd:
        messagedata={'err':'false','result':listd[0]}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    """
    
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    token = hashlib.md5(str(md5pwd)+str(username)+str(gmt_modified))
    token = token.hexdigest()
    sucflag=0
    ousername="bsteel"
    opasswd="bs89076"
    omd5pwd = hashlib.md5(opasswd)
    omd5pwd = omd5pwd.hexdigest()[8:-8]
    messagedata={'err':'true','result':'未获得TOKEN'}
    if username==ousername and omd5pwd==md5pwd:
        sqlb="select id from token where token=%s"
        listb=fetchonedb(sqlb,[token])
        if not listb:
            sqlm="insert into token(token,gmt_created) values(%s,%s)"
            updateintodb(sqlm,[token,gmt_created])
        else:
            sqlm="update app_token set gmt_created=%s where token=%s"
            updateintodb(sqlm,[gmt_created,token])
        messagedata={'err':'false','result':token}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#----图片上传
def upload(request):
    token=request.POST.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        file = request.FILES['file']
        #image = Image.open(reqfile)
        suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
        #image.thumbnail((128,128),Image.ANTIALIAS)
        tempim = StringIO.StringIO()
        mstream = StringIO.StringIO(file.read())
        im = Image.open(mstream)
        rheight=500
        rwidth=500
        
        pwidth=im.size[0]
        pheight=im.size[1]
        
        rate = int(pwidth/pheight)
        if rate==0:
            rate=1
        nwidth=200
        nheight=200
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
        
        #im.thumbnail((10,10),Image.ANTIALIAS)
        im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
        tmp = random.randint(100, 999)
        
#        newpath="/usr/data/resources/products/"+timepath
        newpath=nowpath+'/templates/media/img/'+timepath
        
        imgpath=newpath+str(nowtime)+str(tmp)+"."+im.format
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        im.save(imgpath,im.format,quality = 60)
        mstream.closed
        tempim.closed
#        picurl="http://img1.zz91.com/products/"+timepath+str(nowtime)+str(tmp)+"."+im.format
        picurl=newpath.replace(nowpath+'/templates/media','')+str(nowtime)+str(tmp)+"."+im.format
        
        '''sql="insert into products_pic(product_id,pic_address,gmt_created) values(0,%s,%s)"
        cursor.execute(sql,[imgpath,gmt_created])
        sql1="select id from products_pic where pic_address=%s"
        cursor.execute(sql1,[imgpath])
        productspicresult = cursor.fetchone()
        if productspicresult:
            productspicid=productspicresult[0]
            #del request.session["productspicid"]
            #request.session['productspicid']=productspicid
            return HttpResponse("<script>parent.changepic('"+picurl+"','"+str(productspicid)+"')</script>")
            '''
        return render_to_response('loadimg.html',locals())
    return HttpResponse("请选择一张图片.")
#----图片上传页
def uploadimg(request):
    return render_to_response('uploadimg.html',locals())
def adminindex(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    return render_to_response('index.html',locals())
#--返回
def returnpage(request):
    return HttpResponseRedirect(request.session['request_url'])
#----首页
def default(request):
    return articallist(request)
#----类型管理
def arttype(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    typelist=gettypelist()
    return render_to_response('arttype.html',locals())
def addarttype(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    request.session['request_url']=request.META.get('HTTP_REFERER', '/')
    return render_to_response('addarttype.html',locals())
def addarttypeok(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    arttype=request.GET.get('arttype')
    sortrank=request.GET.get('sortrank')
    error1=''
    if not arttype:
        error1='不能为空'
    if error1:
        return render_to_response('addarttype.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    sql='insert into bsteel_arttype(name,sortrank) values(%s,%s)'
    updateintodb(sql,[arttype,sortrank])
    return HttpResponseRedirect(request.session['request_url'])
def updatetype(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    request.session['request_url']=request.META.get('HTTP_REFERER', '/')
    type_id=int(request.GET.get('type_id'))
    typedetail=gettypedetail(type_id)
    type_name=typedetail['name']
    type_sortrank=typedetail['sortrank']
    typelist=gettypelist()
    return render_to_response('arttype.html',locals())
def updatetypeok(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    arttype=request.GET.get('type_name')
    sortrank=request.GET.get('type_sortrank')
    type_id=int(request.GET.get('type_id'))
    error1=''
    if not arttype:
        error1='不能为空'
    if error1:
        return render_to_response('updatetype.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    sql='update bsteel_arttype set name=%s,sortrank=%s where id=%s'
    updateintodb(sql,[arttype,sortrank,type_id])
    return HttpResponseRedirect("arttype.html")
def deletetype(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    type_id=int(request.GET.get('type_id'))
    sql='delete from bsteel_arttype where id=%s'
    updateintodb(sql,[type_id])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    
#----文章管理
def artical(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    typelist=gettypelist()
    typeid=request.GET.get('typeid')
    stitle=request.GET.get('stitle')
    isdelete=request.GET.get('isdelete')
    if not isdelete:
        isdelete=0
    sort=request.GET.get('sort')
    if typeid:
        typename=gettypedetail(typeid)['name']
    page=request.GET.get('page')
    page_listcount=request.GET.get('page_listcount')
    if (page==None or page=='' or page=='0'):
        page=1
    elif page.isdigit()==False:
        page=1
    if page_listcount and int(page)>int(page_listcount):
        page=page_listcount
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    articallist=getarticallist(frompageCount,limitNum,isdelete,typeid,stitle,sort)
    listcount=0
    if (articallist):
        listall=articallist['list']
        listcount=articallist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('artical.html',locals())
def updateartical(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    artid=request.GET.get('id')
    artdetail=getarticaldetail(artid)
    pubdate=artdetail['gmt_created']
    typelist=gettypelist()
    request.session['request_url']=request.META.get('HTTP_REFERER', '/')
    return render_to_response('addartical.html',locals())
def addartical(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    request.session['request_url']=request.META.get('HTTP_REFERER', '/')
    typelist=gettypelist()
    pubdate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return render_to_response('addartical.html',locals())
def addarticalok(request):
    token=request.POST.get("token")
    datatype=request.POST.get("datatype")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    artid=''
    plist=''
    artid=request.POST.get('artid')
    content=request.POST.get('myEditor')
    if not content:
        content=request.POST.get('content')
    
    if not content:
        messagedata={'err':'true','result':'必须填写内容'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

    title=request.POST.get('title')
    if not title:
        messagedata={'err':'true','result':'必须填写标题'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    typeid=request.POST.get('typeid')
    if not typeid:
        messagedata={'err':'true','result':'必须文章类型'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    click=request.POST.get('click')
    if click:
        click=int(click)
    if not click:
        click=0
    editor=request.POST.get('editor')
    if not editor:
        editor=''
    gmt_created=request.POST.get('pubdate')
    if not gmt_created:
        gmt_created=datetime.datetime.now()
    sortrank=datetime.datetime.now()
    if title and content:
        if artid:
            sql='update bsteel_artical set title=%s,typeid=%s,content=%s,click=%s,editor=%s,sortrank=%s where id=%s'
            updateintodb(sql,[title,typeid,content,click,editor,sortrank,artid])
        else:
            sql='insert into bsteel_artical(title,typeid,content,gmt_created,sortrank,click,editor) values(%s,%s,%s,%s,%s,%s,%s)'
            updateintodb(sql,[title,typeid,content,gmt_created,sortrank,click,editor])
    if datatype=="json":
        messagedata={'err':'false','result':'suc'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    return HttpResponseRedirect("artical.html")

#----文章列表页
def articallist(request,page='',begintime='',endtime=''):
    if not begintime and begintime!='':
        begintime=time.strftime('%Y-%m-%d',time.localtime(time.time()-3600*24*30))
    if not endtime and endtime!='':
        endtime=time.strftime('%Y-%m-%d',time.localtime(time.time()+3600*24))
    stitle=request.GET.get('stitle')
    page_listcount=request.GET.get('page_listcount')
    if (page==None or page=='' or page=='0'):
        page=1
    elif page.isdigit()==False:
        page=1
    if page_listcount and int(page)>int(page_listcount):
        page=page_listcount
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    articallist=getarticallist(frompageCount,limitNum,isdelete='0',stitle=stitle,begintime=begintime,endtime=endtime)
    listcount=0
    if (articallist):
        listall=articallist['list']
        listcount=articallist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    companypricelist=getcompanypricelist(kname="废钢",limitcount=10,titlelen="")
    return render_to_response('index2.html',locals())

#----文章详细页
def articaldetail(request,id=''):
    art=getarticaldetail(id)
    articalup=getarticalup(id)
    articalnx=getarticalnx(id)
    companypricelist=getcompanypricelist(kname="废钢",limitcount=10,titlelen="")
    return render_to_response('detail.html',locals())
def delartical(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    request_url=request.META.get('HTTP_REFERER', '/')
    klist=request.GET.getlist('checkAll')
    if klist:
        for kl in klist:
            sql='update bsteel_artical set isdelete=1 where id=%s'
            updateintodb(sql,[kl])
    return HttpResponseRedirect(request_url)
#----文章还原
def reduction(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    request_url=request.META.get('HTTP_REFERER', '/')
    klist=request.GET.getlist('checkAll')
    if klist:
        for kl in klist:
            sql='update bsteel_artical set isdelete=0 where id=%s'
            updateintodb(sql,[kl])
    return render_to_response('recycle.html',locals())
#----永久删除
def redelartical(request):
    token=request.GET.get("token")
    if token:
        if not getloginstatus(token):
            return HttpResponse(err)
    else:
        username=request.session.get('username')
        if not username:
            return HttpResponseRedirect('login.html')
    request_url=request.META.get('HTTP_REFERER', '/')
    sql='delete from bsteel_artical where isdelete=%s'
    updateintodb(sql,[1])
    return render_to_response('recycle.html',locals())
