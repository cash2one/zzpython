#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson
from django.core.cache import cache
from zz91tools import getToday,getYesterday,date_to_str,formattime,getnowurl
from zz91settings import pycmspath,ftpconn,pycmsurl,pyuploadpath,pyimgurl
from zz91db_130 import pycmsdb,otherdb
from zz91page import *
import os,datetime,time,sys,calendar,urllib,random
dbp=pycmsdb()
dbo=otherdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/function.py")
zzp=zzpycms()
pinyin = pinyin()
from frontweb import weblist
#pyftp = pyftp(ftpconn['ip'],ftpconn['uname'],ftpconn['pword'])

def delfromdb(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=str(time.time())
    request_url=request.META.get('HTTP_REFERER','/')
    if '?' in request_url:
        request_url=request_url.replace('?','?freshtime='+freshtime+'&')
    else:
        request_url+='?freshtime='+freshtime
    artid=request.GET.get('artid')
    db=request.GET.get('db')
    sql='delete from '+db+' where id=%s'
    dbp.updatetodb(sql,[artid])
    return HttpResponseRedirect(request_url)

def friendlink(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    friendlinklist=zzp.getfriendlinklist()
    return render_to_response('user/friendlink.html',locals())
def addfrinedlink(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('user/addfrinedlink.html',locals())
#更新友情链接
def updatefriendlink(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    flinkid=request.GET.get('flinkid')
    sql='select sortrank,url,name,logo,remark from py_friendlink where id=%s'
    result=dbp.fetchonedb(sql,[flinkid])
    if result:
        sortrank=result[0]
        url=result[1]
        name=result[2]
        logo=result[3]
        remark=result[4]
    return render_to_response('user/addfrinedlink.html',locals())
#增加友情链接
def addfrinedlinkok(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.GET.get('request_url')
    if request_url:
        freshtime=str(time.time())[-3:]
        request_url=request_url.replace('freshtime=','freshtime='+freshtime)
    
    
    name=request.GET.get('name')
    url=request.GET.get('url')
    sortrank=request.GET.get('sortrank')
    remark=request.GET.get('remark')
    logo=request.GET.get('logo')
    flinkid=request.GET.get('flinkid')
    errors=''
    if not name:
        error1='名称不能为空'
        errors=1
    if not url:
        error2='网址不能为空'
        errors=1
    if errors:
        return render_to_response('user/addfrinedlink.html',locals())
    argument=[sortrank,url,name,logo,remark]
    if flinkid:
        sql='update py_friendlink set sortrank=%s,url=%s,name=%s,logo=%s,remark=%s where id=%s'
        argument.append(flinkid)
    else:
        sql='insert into py_friendlink(sortrank,url,name,logo,remark) values(%s,%s,%s,%s,%s)'
    dbp.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)
#更新密码    
def updatekwd(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.META.get('HTTP_REFERER','/')
    freshtime=time.time()
    upage=request.GET.get('upage')
    if upage:
        oldpwd=request.GET.get('oldpwd')
        newpwd=request.GET.get('newpwd')
        renewpwd=request.GET.get('renewpwd')
        errors=''
        if not oldpwd:
            error1='请输入原密码'
            errors=1
        if not newpwd:
            error2='请输入新密码'
            errors=1
        if not newpwd==renewpwd:
            error3='两次输入的密码不一致'
            errors=1
        if not renewpwd:
            error3='再输入一次新密码'
            errors=1
        if errors:
            return render_to_response('user/updatekwd.html',locals())
        sql='select id from py_user where username=%s and password=%s'
        result=dbp.fetchonedb(sql,[username,oldpwd])
        if result:
            id=result[0]
            sql2='update py_user set password=%s where id=%s'
            dbp.updatetodb(sql2,[newpwd,id])
            return HttpResponseRedirect('http://webcms.zz91.com/user/#1')
        else:
            error1='原密码错误'
    return render_to_response('user/updatekwd.html',locals())
#上传图片
def mailimg(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    return render_to_response('user/mailimg.html',locals())
#----上传文件通用
def mailloadimg(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    tmp=random.randint(100,999)
    if request.FILES:
        file = request.FILES['file']
#        tmp = random.randint(100, 999)
        newpath=pyuploadpath+timepath
        filename=file.name
        
        suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
        officeFormat = ['CSV','DOC','DOCX', 'DOCM', 'DOTX','DOTM','XLS','XLSX','XLSM','XLTX','XLTM','XLSB','XLAM','PDF','TXT','ET']
        
        filetype=filename.split('.')[-1]
        filetype=filetype.upper()
        if filetype in suportFormat:
            imagetype=1
        elif filetype in officeFormat:
            officetype=1
        else:
            return HttpResponse("请选择一个正确的office文件格式.")
        
        imgpath=newpath+str(nowtime)+str(tmp)+filename
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        des_origin_f = open(imgpath,"w")
        for chunk in file.chunks():
            des_origin_f.write(chunk)
        des_origin_f.close()
        
        picurl=imgpath.replace(pyuploadpath,'')
        pic_url=pyimgurl+picurl
        return render_to_response('user/loadimg.html',locals())
    return HttpResponse("请选择一个文件.")

def cleararthtml(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.META.get('HTTP_REFERER','/')
    freshtime=str(time.time())
    if '?' in request_url:
        request_url=request_url.replace('?','?freshtime='+freshtime+'&')
    else:
        request_url=request_url+'?freshtime='+freshtime
    
    getartlist=request.GET.get('getartlist')
    if getartlist:
        sql='select id from py_user_artical where is_del=1 and is_make=1'
        resultlist=dbp.fetchalldb(sql)
        listall=[]
        for list in resultlist:
            listall.append(list)
        listdata={'list':listall}
        return HttpResponse(simplejson.dumps(listdata, ensure_ascii=False))
    
    artid=request.GET.get('artid')
    if artid:
        cleararticalhtml(artid)
        return HttpResponse('1')
    return HttpResponseRedirect(request_url)

def changehand(request):
    freshtime=time.time()
    is_ok=request.GET.get('is_ok')
    auto_id=request.GET.get('auto_id')
    if is_ok=='1':
        is_ok='0'
    else:
        is_ok='1'
    sql='update py_liuyan set is_handle=%s where id=%s'
    dbp.updatetodb(sql,[is_ok,auto_id])
    return HttpResponse('1')

def sendliuyan(request):
    freshtime=time.time()
    liuyanurl='http://webcms.zz91.com/web/weili/lxwm.html'
    request_url=request.META.get('HTTP_REFERER','/')
    name=request.POST['name']
    content=request.POST['msg']
    contact=request.POST['contact']
    leavetype=request.POST['leavetype']
    if name and content and contact and leavetype:
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        phonedetail=dbo.getphonedetail(contact)
        province=phonedetail['province']
        city=phonedetail['city']
        gmt_created=datetime.datetime.now()
        sql='select id from py_liuyan where name=%s and phone=%s and is_handle=0'
        result=dbp.fetchonedb(sql,[name,contact])
        if result:
            errortxt='你已经提交,不能重复提交,我们会尽快与您联系!'
            return render_to_response('user/weilisuliao/leavesuc.html',locals())
        else:
            argument=[name,contact,content,leavetype,ip,province,city,gmt_created,gmt_created]
            sql='insert into py_liuyan(name,phone,content,leavetype,ip,province,city,sendtime,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            dbp.updatetodb(sql,argument)
            return render_to_response('user/weilisuliao/leavesuc.html',locals())
    return HttpResponseRedirect(request_url)

def usermessage(request):
    freshtime=time.time()
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('weddingdress/loginpage.html')
    is_hand=request.GET.get('is_hand')
#    gmt_begin=request.GET.get('gmt_begin')
#    gmt_end=request.GET.get('gmt_end')
    if is_hand:
        if is_hand=='1':
            handname='已处理'
        else:
            handname='未处理'
    searchlist={}
    if is_hand:
        searchlist['is_hand']=is_hand
    searchurl=urllib.urlencode(searchlist)
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    hunshayuyue=zzp.getpyliuyan(frompageCount,limitNum,is_hand)
    listcount=0
    listall=hunshayuyue['list']
    listcount=hunshayuyue['count']
    if int(listcount)>1000000:
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('user/usermessage.html',locals())
#----用户列表
def userlist(request):
    nowurl=getnowurl(request)
    username=request.session.get('username',None)
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    listall=zzp.getuserlist(0,20)['list']
    return render_to_response('user/userlist.html',locals())
def adduser(request):
    nowurl=getnowurl(request)
    username=request.session.get('username',None)
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.META.get('HTTP_REFERER','/')
    freshtime=time.time()
    return render_to_response('user/adduser.html',locals())
def updateuser(request):
    nowurl=getnowurl(request)
    username=request.session.get('username',None)
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    userid=request.GET.get('userid')
    if userid:
        sql='select username,password from py_user where id=%s'
        result=dbp.fetchonedb(sql,[userid])
        if result:
            username1=result[0]
            password=result[1]
    return render_to_response('user/adduser.html',locals())
def adduserok(request):
    nowurl=getnowurl(request)
    username=request.session.get('username',None)
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=str(time.time())[-3:]
    request_url=request.GET.get('request_url')
    if request_url:
        request_url=request_url.replace('freshtime=','freshtime='+freshtime)
    userid=request.GET.get('userid')
    username1=request.GET.get('username1')
    sortrank=request.GET.get('sortrank')
    website=request.GET.get('website')
    if not sortrank:
        sortrank='0'
    error1=''
    error2=''
    error3=''
    if not userid:
        if username1:
            sql1='select id from py_user where username=%s'
            result=dbp.fetchonedb(sql1,[username1])
            if result:
                error1='用户名重复'
        else:
            error1='用户名不能为空'
    password=request.GET.get('password')
    if not password:
        error2='密码不能为空'
        ##
    website=request.GET.get('website')
    if not website:
        error3='域名不能为空'
    if website:
        sql2='select id from py_user where website=%s'
        result=dbp.fetchonedb(sql2,[website])
        if result:
                error3='域名重复'
                
    if error1 or error2 or error3:
        return render_to_response('user/adduser.html',locals())
    argument=[username1,password,sortrank,website]
    if userid:
        sql='update py_user set password=%s,password=%s,sortrank=%s where id=%s'
        argument.append(userid)
    else:
        sql='insert into py_user(username,password,sortrank,website) values(%s,%s,%s,%s)'
    dbp.updatetodb(sql,argument)
    sql=''
    return HttpResponseRedirect(request_url)
def index(request):
    freshtime=time.time()
    domainlist=gethostname(request)
    subname=domainlist['subname']
    domain=domainlist['domain']
    if domain!="zz90.com":
        return weblist(request)
    return HttpResponseRedirect('/user/')
def returnpage(request):
    freshtime=time.time()
    request_url=request.GET.get('request_url')
    return HttpResponseRedirect(request_url)
def default(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html')
    freshtime=time.time()
    #----创建客户主目录
    sortrank=request.session.get('sortrank')
    if sortrank=='0':
        new_path = os.path.join(pycmspath,username)
        if not os.path.isdir(new_path):
            #ftp创建文件夹
#            pyftp.mkdir(ftpconn['ip'],ftpconn['uname'],ftpconn['pword'],ftpconn['ftpath']['pycms'],username)
            #本地创建文件夹
            os.makedirs(new_path)
#    if sortrank=='1':
#        return HttpResponseRedirect('/loginpage.html')
    return render_to_response('user/default.html',locals())
def nexttypelist(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    reid=request.GET.get('reid')
    if reid:
        sql='select reid,typename,pinyin,tempname,sortrank from py_user_arttype1 where id=%s'
        result=dbp.fetchonedb(sql,[reid])
        if result:
            rreid=result[0]
            if rreid:
                rretypename=self.getarttypename(rreid)
            typename=result[1]
            pinyin=result[2]
            tempname=result[3]
            sortrank=result[4]
        reid=int(reid)
        listall=zzp.getnexttypelist(reid)
    return render_to_response('user/nexttypelist.html',locals())
#---获得栏目列表
def arttype(request,typeid=''):
    dbtype='py_user_arttype1' #数据库为py_user_arttype1
    request_url=request.META.get('HTTP_REFERER','/')
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    #当前用户的权重
    sortrank=request.session.get('sortrank')
    if sortrank=='0':
        user_id=request.session.get('user_id')
    else:
        user_id='0'
    freshtime=time.time()
    reid=request.GET.get('reid')
    if not reid:
        reid='0'
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    webtypelist=zzp.getarttypelist(frompageCount,limitNum,user_id,reid=reid)
    listcount=0
    if (webtypelist):
        listall=webtypelist['list']
        listcount=webtypelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('user/arttype.html',locals())
def addarttype(request,typeid=''):
    nowurl=getnowurl(request)
    sortrank=request.session.get('sortrank')
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    user_id=request.session.get('user_id')
    request_url=request.META.get('HTTP_REFERER','/')
    if (sortrank=="0"):
        tempname=zzp.gettempinyinuser(user_id)
    else:
        tempname=""
    
    
    lastpath=nowpath+'/templates/media/'+tempname+'/images/choice'
    nowimgpath='/'+tempname+'/images/choice/'
    if os.path.isdir(lastpath):
        listfile=os.listdir(lastpath)
        listall=[]
        num=0
        for imgfile in listfile:
            num+=1
            imgfile1=imgfile.split('.')[0]
            list={'name':imgfile1,'num':num}
            listall.append(list)
    return render_to_response('user/addarttype.html',locals())
def updatearttype(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    typeid=request.GET.get('typeid')
    sql='select user_id,typename,tempname,sortrank from py_user_arttype1 where id=%s'
    result=dbp.fetchonedb(sql,typeid)
    if result:
        user_id=result[0]
        if user_id:
            username=zzp.getusername(user_id)
        typename=result[1]
        tempnames=result[2]
        sortrank=result[3]
        
        tempname=zzp.gettempinyinuser(user_id)
        lastpath=nowpath+'/templates/media/'+tempname+'/images/choice'
        nowimgpath='/'+tempname+'/images/choice/'
        if os.path.isdir(lastpath):
            listfile=os.listdir(lastpath)
            listall=[]
            num=0
            for imgfile in listfile:
                num+=1
                imgfile1=imgfile.split('.')[0]
                list={'name':imgfile1,'num':num}
                listall.append(list)
    return render_to_response('user/addarttype.html',locals())
#def delarttype(request,typeid=''):
#    nowurl=getnowurl(request)
#    username=request.session.get('username')
#    if not username:
#        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
#    freshtime=time.time()
#    user_id=request.session.get('user_id')
#    request_url=request.META.get('HTTP_REFERER','/')
#    typeid=request.GET.get('typeid')
#    sql='delete from py_user_arttype1 where id=%s and user_id=%s'
#    dbp.updatetodb(sql,[typeid,user_id])
#    return HttpResponseRedirect(request_url)
def delusertemp(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    user_id=request.session.get('user_id')
    request_url=request.META.get('HTTP_REFERER','/')
    temp_id=request.GET.get('temp_id')
    sql='delete from py_user_template where id=%s and user_id=%s'
    dbp.updatetodb(sql,[temp_id,user_id])
    return HttpResponseRedirect(request_url)
def addarttypeok(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    user_id=request.session.get('user_id')
    username=request.GET.get('username')
    if username:
        user_id=zzp.getuser_id(username)
    request_url=request.GET.get('request_url')
    if request_url:
        freshtime=str(time.time())[-3:]
        request_url=request_url.replace('freshtime=','freshtime='+freshtime)
    typename=request.GET.get('typename')
    #模板所属类型
    pageid=request.GET.get('pageid')
    tempnames=request.GET.get('tempnames')
    sortrank=request.GET.get('sortrank')
    typeid=request.GET.get('typeid')
    
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    error1=''
    if not typename:
        error1='不能为空'
    if error1:
        return render_to_response('user/addarttype.html',locals())
    pinyiname = pinyin.get(typename.encode('utf-8'))
    argument=[user_id,typename,pinyiname,tempnames,sortrank,pageid]
    if typeid:
        sql1='select pinyin from py_user_arttype1 where id=%s'
        result1=dbp.fetchonedb(sql1,typeid)
        if result1:
            pinyinold=result1[0]
            if not pinyinold==pinyiname:
                #ftp文件夹重命名
                #try:
                    #pyftp.rename(ftpconn['ip'],ftpconn['uname'],ftpconn['pword'],ftpconn['ftpath']['pycms']+'/'+username,pinyiname,pinyinold)
                #except:
                    #pass
                old_path = os.path.join(pycmspath+username+'/',pinyinold)
                if os.path.isdir(old_path):
                    new_path = os.path.join(pycmspath+username+'/',pinyiname)
                    if not os.path.isdir(new_path):
                        os.rename(old_path, new_path)
        argument.append(typeid)
        sql='update py_user_arttype1 set user_id=%s,typename=%s,pinyin=%s,tempname=%s,sortrank=%s,pageid=%s where id=%s'
        dbp.updatetodb(sql,argument)
    else:
        #ftp创建栏目文件夹
        #try:
            #pyftp.mkdir(ftpconn['ip'],ftpconn['uname'],ftpconn['pword'],ftpconn['ftpath']['pycms']+'/'+username,pinyiname)
        #except:
            #pass
        new_path = os.path.join(pycmspath+username+'/',pinyiname)
        if not os.path.isdir(new_path):
            #----本地创建栏目文件夹
            os.makedirs(new_path)
        sql='insert into py_user_arttype1(user_id,typename,pinyin,tempname,sortrank,pageid) values(%s,%s,%s,%s,%s,%s)'
        dbp.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)

def buildindexhtml(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    user_id=request.session.get('user_id')
    alltypelist=zzp.getarttypelist(0,15,user_id,'0')['list']
    getjindu=request.GET.get('jindu')
    return render_to_response('user/build/buildindexhtml.html',locals())
def buildarttypehtml(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    user_id=request.session.get('user_id')
    alltypelist=zzp.getarttypelist(0,15,user_id,reid='0',all=1)['list']
    getjindu=request.GET.get('jindu')
    return render_to_response('user/build/buildarttypehtml.html',locals())
def buildarticalhtml(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    user_id=request.session.get('user_id')
    alltypelist=zzp.getarttypelist(0,15,user_id,reid='0',all=1)['list']
    getjindu=request.GET.get('jindu')
    return render_to_response('user/build/buildarticalhtml.html',locals())

def buildarticalok(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    user_id=request.session.get('user_id')
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

def template(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    sortrank=request.session.get('sortrank')
    if sortrank=='0':
        user_id=request.session.get('user_id')
    else:
        user_id=''
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    webtypelist=zzp.getuseremplatelist(frompageCount,limitNum,user_id)
    listcount=0
    if (webtypelist):
        listall=webtypelist['list']
        listcount=webtypelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('user/template.html',locals())

def choicetemp(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    user_id=request.session.get('user_id')
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    webtypelist=zzp.getemplatelist(frompageCount,limitNum,user_id)
    listcount=0
    if (webtypelist):
        listall=webtypelist['list']
        listcount=webtypelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('user/choicetemp.html',locals())

def addusertemp(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.GET.get('request_url')
    user_id=request.session.get('user_id')
    temp_id=request.GET.get('temp_id')
    if temp_id:
        sql1='select id from py_user_template where user_id=%s'
        result=dbp.fetchonedb(sql1,user_id)
        if result:
            sql='update py_user_template set temp_id=%s where user_id=%s'
        else:
            sql='insert into py_user_template(temp_id,user_id) values(%s,%s)'
        dbp.updatetodb(sql,[temp_id,user_id])
    return HttpResponseRedirect(request_url)

def artical(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    user_id=request.session.get('user_id')
    sortrank=request.session.get('sortrank')
    if sortrank=='0':
        user_id=request.session.get('user_id')
    else:
        user_id=''
    is_make=request.GET.get('is_make')
    updateismake=request.GET.get('updateismake')
    freshtime=time.time()
    if updateismake:
        sql='update py_user_artical set is_make=0 where is_make=%s'
        dbp.updatetodb(sql,[updateismake])
        return HttpResponseRedirect('artical.html?is_del=0&freshtime='+str(freshtime))
    alltypelist=zzp.getarttypelist(0,15,user_id,reid='0',all=1)['list']
    is_del=request.GET.get('is_del')
    typeid=request.GET.get('typeid')
    searchlist={}
    if typeid:
        typename=zzp.getarttypename(typeid)
        searchlist['typeid']=typeid
    if is_del:
        searchlist['is_del']=is_del
    if is_make:
        searchlist['is_make']=is_make
    searchurl=urllib.urlencode(searchlist)
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    articalist=zzp.getarticalist(frompageCount,limitNum,user_id,typeid=typeid,is_del=is_del,is_make=is_make)
    listcount=0
    listall=articalist['list']
    listcount=articalist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('user/artical.html',locals())
def addartical(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    sortrank=request.session.get('sortrank')
    freshtime=time.time()
    user_id=request.session.get('user_id')
    alltypelist=zzp.getarttypelist(0,20,user_id)['list']
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_created=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return render_to_response('user/addartical.html',locals())
def updateartical(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    sortrank1=request.session.get('sortrank')
    freshtime=time.time()
    user_id=request.session.get('user_id')
    alltypelist=zzp.getarttypelist(0,20,user_id)['list']
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_created=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    artid=request.GET.get('artid')
    sql='select typeid,title,sortrank,litpic,body,keywords,user_id from py_user_artical where id=%s'
    result=dbp.fetchonedb(sql,artid)
    if result:
        typeid=result[0]
        if typeid:
            arttypename=zzp.getarttypename(typeid)
        title=result[1]
        sortrank1=result[2]
        litpic=result[3]
        content=result[4]
        keywords=result[5]
        user_id=result[6]
        if user_id:
            username1=zzp.getusername(user_id)
    return render_to_response('user/addartical.html',locals())
def delartical(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.META.get('HTTP_REFERER','/')
    freshtime=str(time.time())
    if '?' in request_url:
        request_url=request_url.replace('?','?freshtime='+freshtime+'&')
    else:
        request_url=request_url+'?freshtime='+freshtime
    artid=request.GET.get('artid')
    is_del=request.GET.get('is_del')
    sql='update py_user_artical set is_del=%s where id=%s'
    dbp.updatetodb(sql,[is_del,artid])
    return HttpResponseRedirect(request_url)
def addarticalok(request):
    nowurl=getnowurl(request)
    username=request.session.get('username',None)
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    user_id=request.session.get('user_id')
    username1=request.GET.get('username1')
    if username1:
        user_id=zzp.getuser_id(username1)
    freshtime=str(time.time())[-3:]
    request_url=request.POST['request_url']
    if request_url:
        request_url=request_url.replace('freshtime=','freshtime='+freshtime)
    body=''
    artid=''
    keywords=''
    error=0
    litpic=''
    gmt_created=request.POST['gmt_created']
    typeid=request.POST['arttypeid']
    title=request.POST['title']
    if request.POST.has_key('myEditor'):
        litpic=request.POST['litpic']
    if request.POST.has_key('myEditor'):
        body=request.POST['myEditor']
    if request.POST.has_key('artid'):
        artid=request.POST['artid']
    if request.POST.has_key('keywords'):
        keywords=request.POST['keywords']
    sortrank=request.POST['sortrank1']
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    if not title:
        error=1
    if not body:
        error=1
    if error==1:
        if typeid:
            arttypename=zzp.getarttypename(typeid)
        alltypelist=zzp.getarttypelist(0,20,user_id)['list']
        return render_to_response('user/addartical.html',locals())
    if artid:
        sql='update py_user_artical set is_make=0,typeid=%s,title=%s,body=%s,sortrank=%s,gmt_modified=%s,litpic=%s,keywords=%s where id=%s'
        argument=[typeid,title,body,sortrank,gmt_created,litpic,keywords,artid]
    else:
        sql='insert into py_user_artical(user_id,typeid,title,body,sortrank,gmt_date,gmt_created,gmt_modified,litpic,keywords) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        argument=[user_id,typeid,title,body,sortrank,gmt_created[:9],gmt_created,gmt_created,litpic,keywords]
    dbp.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)

def cleararthtmlall(request):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=str(time.time())
    request_url=request.META.get('HTTP_REFERER','/')
    if '?' in request_url:
        request_url=request_url.replace('?','?freshtime='+freshtime+'&')
    else:
        request_url+='?freshtime='+freshtime
    user_id=request.session.get('user_id')
    sql='update py_user_artical set is_make=0 where user_id=%s'
    dbp.updatetodb(sql,[user_id])
    return HttpResponseRedirect(request_url)

def noarticalhtmlnum(request):
    chk_value=request.GET.get('chk_value')
    if chk_value:
        chk_value="("+chk_value+")"
        sql='select count(0) from py_user_artical where is_make=0 and is_del=0 and typeid in '+chk_value
        sql2='select id from py_user_artical where is_make=0 and is_del=0 and typeid in '+chk_value
        count=dbp.fetchnumberdb(sql)
        resultlist=dbp.fetchalldb(sql2)
        listall=[]
        for result in resultlist:
            listall.append(result[0])
        listdata={'list':listall,'count':count}
        return HttpResponse(simplejson.dumps(listdata, ensure_ascii=False))


def buildhtmlok(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    freshtime=time.time()
    request_url=request.META.get('HTTP_REFERER','/')
    freshtime=str(time.time())
    if '?' in request_url:
        request_url=request_url.replace('?','?freshtime='+freshtime+'&')
    else:
        request_url+='?freshtime='+freshtime
    user_id=request.session.get('user_id')
    
    type=request.GET.get('type')
    if type=='1':
        #生成首页html
        htmlall=urllib.urlopen(pycmsurl+'user/htmlurl.html?type='+type+'&user_id='+str(user_id)).read()
        if htmlall:
            file=open(pycmspath+username+'/index.html','w')
            file.write(htmlall)
            file.close()
            #ftp上传
            #pyftp.upload(ftpconn['ftpath']['pycms'],pycmspath+username,'index.html')
            return HttpResponse('1')
    elif type=='2':
        #生成栏目html
        sql='select temp_id from py_user_template where user_id=%s'
        result=dbp.fetchonedb(sql,user_id)
        
        if result:
            temp_id=result[0]
            pinyin=zzp.getempinyin(temp_id)
            
            arttypeid=request.GET.get('buildarttype')
#            buildarttypelist=request.GET.getlist('buildarttype')
#            for arttypeid in buildarttypelist:
            if arttypeid:
                exerypage=16
                sql='select pinyin,tempname,reid from py_user_arttype1 where id=%s'
                result=dbp.fetchonedb(sql,arttypeid)
                if result:
                    pinyinname=result[0]
                    tempname=result[1]
                    reid=result[2]
                    if not reid:
                        reid='0'
                    repinyin=zzp.getarttypepinyin(reid)
                    if repinyin:
                        pinyinname=repinyin+'/'+pinyinname
                    #ftp创建栏目文件夹
                    #try:
                        #pyftp.mkdir(ftpconn['ftpath']['pycms'],pinyinname)
                    #except:
                    #    pass
                    #如果文件夹被全部删除了,就创建这些文件夹
                    new_path = os.path.join(pycmspath+username+'/',pinyinname)
                    if not os.path.isdir(new_path):
                        #----本地创建栏目文件夹
                        os.makedirs(new_path)
                    
                    #列表翻页
                    sql1='select count(0) from py_user_artical where user_id=%s and is_del=0 and typeid=%s'
                    count=dbp.fetchnumberdb(sql1,[user_id,arttypeid])
                    if count>exerypage:
                        page_listcount=count/exerypage
                        if '.0' not in str(page_listcount):
                            page_listcount=int(page_listcount)+1
#                        return HttpResponse(page_listcount)
                        for typelist in range(1,page_listcount+1):
                            pagename='list_'+str(typelist)+'.html'
                            htmlall=urllib.urlopen(pycmsurl+'user/htmlurl.html?type='+type+'&arttypeid='+str(arttypeid)+'&user_id='+str(user_id)+'&page='+str(typelist)).read()
                            if htmlall:
                                file=open(pycmspath+username+'/'+pinyinname+'/'+pagename,'w')
                                file.write(htmlall)
                                file.close()
                                #ftp上传
                                #pyftp.upload(ftpconn['ftpath']['pycms']+'/'+pinyinname,pycmspath+username+'/'+pinyinname,pagename)
#                                return HttpResponse('2')
#                                if typelist==1:
#                                    pyftp.upload(ftpconn['ftpath']['pycms']+'/'+pinyinname,pycmspath+username+'/'+pinyinname,'index.html')
                    htmlall=urllib.urlopen(pycmsurl+'user/htmlurl.html?type='+type+'&arttypeid='+str(arttypeid)+'&user_id='+str(user_id)).read()
                    if htmlall:
                        #return HttpResponse(pycmspath+username+'/'+pinyinname+'/index.html')
                        file=open(pycmspath+username+'/'+pinyinname+'/index.html','w')
                        file.write(htmlall)
                        file.close()
                        #ftp上传
                        #pyftp.upload(ftpconn['ftpath']['pycms']+'/'+pinyinname,pycmspath+username+'/'+pinyinname,'index.html')
                        return HttpResponse('1')
                else:
                    return HttpResponse('err')
    #最终页html
    elif type=='3':
        sql2='update py_user_artical set is_make=1 where id=%s'
        sql3='update py_user_artical set is_make=0 where id=%s'
        #内容管理单独生成1篇文章
        oneartical=request.GET.get('oneartical')
        if oneartical:
            artid=oneartical
            typeid=request.GET.get('typeid')
            if not typeid:
                typeid=dbp.fetchnumberdb('select typeid from py_user_artical where id=%s',[artid])
            rebuild=request.GET.get('rebuild')
            if rebuild:
                dbp.updatetodb(sql3,[artid])
            arttypedetail=zzp.getarttypedetail(typeid)
            if arttypedetail:
                pinyinname=arttypedetail['pinyin']
                repinyin=arttypedetail['repinyin']
                if repinyin:
                    pinyinname=repinyin+'/'+pinyinname
            htmlall=urllib.urlopen(pycmsurl+'user/htmlurl.html?type='+type+'&artid='+artid+'&user_id='+str(user_id)).read()
            if htmlall:
                file=open(pycmspath+username+'/'+pinyinname+'/'+artid+'.html','w')
                file.write(htmlall)
                file.close()
                #ftp上传
                #pyftp.upload(ftpconn['ftpath']['pycms']+'/'+pinyinname,pycmspath+username+'/'+pinyinname,str(artid)+'.html')
                dbp.updatetodb(sql2,[artid])
                return HttpResponse('1')
        #生成页面,生成所有栏目的文章
        else:
            buildarticalist=request.GET.getlist('buildartical')
            if buildarticalist:
                for typeid in buildarticalist:
                    sql='select id from py_user_artical where user_id=%s and typeid=%s and is_make=0'
#                    sql2='update py_user_artical set is_make=1 where id=%s'
                    resultlist1=dbp.fetchalldb(sql,[user_id,typeid])
                    
                    arttypedetail=zzp.getarttypedetail(typeid)
                    if arttypedetail:
                        pinyinname=arttypedetail['pinyin']
                        repinyin=arttypedetail['repinyin']
                        if repinyin:
                            pinyinname=repinyin+'/'+pinyinname
                    
                    for result1 in resultlist1:
                        artid=result1[0]
                        htmlall=urllib.urlopen(pycmsurl+'user/htmlurl.html?type='+type+'&artid='+str(artid)+'&user_id='+str(user_id)).read()
                        if htmlall:
                            file=open(pycmspath+username+'/'+pinyinname+'/'+str(artid)+'.html','w')
                            file.write(htmlall)
                            file.close()
                            #ftp上传
                            #pyftp.upload(ftpconn['ftpath']['pycms']+'/'+pinyinname,pycmspath+username+'/'+pinyinname,str(artid)+'.html')
                            dbp.updatetodb(sql2,[artid])
    return HttpResponseRedirect(request_url+'&jindu=1')

#读取html的url
def htmlurl(request,type="",user_id="",artid="",arttypeid="",page=""):
    if not type:
        type=request.GET.get('type')
    if not user_id:
        user_id=request.GET.get('user_id')
    if not artid:
        artid=request.GET.get('artid')
    friendlinklist=zzp.getfriendlinklist()
    freshtime=time.time()
    if not user_id:
        user_id=request.session.get('user_id')
    if user_id:
        pinyin=zzp.gettempinyinuser(user_id)
        #首页
        if type=='1':
            pinyin=zzp.gettempinyinuser(user_id)
            alltypelist=zzp.getarttypelist(0,20,user_id,'0')['list']
            cqcmlist=zzp.getarticalist(0,5,user_id,typeid=11)['list']
            propiclist=zzp.getarticalist(0,5,user_id,typeid='(2,3)')['list']
            shouindex=1
            return render_to_response('user/'+pinyin+'/index.html',locals())
        #栏目页
        elif type=='2':
            if not arttypeid:
                arttypeid=request.GET.get('arttypeid')
            if user_id and arttypeid:
                arttypedetail=zzp.getarttypedetail(arttypeid)
                if arttypedetail:
                    typename=arttypedetail['typename']
                    urltype=arttypedetail['tempname']
                    pinyinname=arttypedetail['pinyin']
                    reid=arttypedetail['reid']
                    repinyin=arttypedetail['repinyin']
                    if not urltype:
                        urltype='list'
                    alltypelist=zzp.getarttypelist(0,20,user_id,'0')['list']
                    if reid:
                        nowtypelist=zzp.getarticalist(0,20,user_id,typeid=arttypeid)['list']
                        topid=reid
                        jibie='../../'
                    else:
                        topid=int(arttypeid)
                        if arttypeid=='1':
                            articalist=zzp.getarticalist(0,4,user_id,typeid=20)['list']
                            gsjjtxt=zzp.getarticaldetail(24)
                        elif arttypeid=='4':
                            articalist1=zzp.getarticalist(0,4,user_id,typeid=2)['list']
                            articalist2=zzp.getarticalist(0,4,user_id,typeid=3)['list']
                        elif arttypeid=='5':
                            listtypeall=[]
                            sql='select id,typename,pinyin from py_user_arttype1 where reid=5'
                            resultlist=dbp.fetchalldb(sql)
                            for result in resultlist:
                                sontypeid=result[0]
                                sontypename=result[1]
                                sonpinyin=result[2]
                                list1=zzp.getarticalist(0,4,user_id,typeid=sontypeid)['list']
                                list2={'typeid':sontypeid,'typename':sontypename,'pinyin':sonpinyin,'artlist':list1}
                                listtypeall.append(list2)
                        #有翻页的栏目
#                        elif arttypeid in ['2','3']:
                        else:
                            if not page:
                                page=request.GET.get('page')
                            if not page:
                                page=1
                            funpage=zz91page()
                            limitNum=funpage.limitNum(16)
                            nowpage=funpage.nowpage(int(page))
                            frompageCount=funpage.frompageCount()
                            after_range_num = funpage.after_range_num(3)
                            before_range_num = funpage.before_range_num(6)
                            articalist=zzp.getarticalist(frompageCount,limitNum,user_id,typeid=arttypeid)
                            listcount=0
                            listall=articalist['list']
                            listcount=articalist['count']
                            if (int(listcount)>1000000):
                                listcount=1000000-1
                            listcount = funpage.listcount(listcount)
                            page_listcount=funpage.page_listcount()
                            firstpage = funpage.firstpage()
                            lastpage = funpage.lastpage()
                            page_range  = funpage.page_range()
                            if len(page_range)>7:
                                page_range=page_range[:7]
                            nextpage = funpage.nextpage()
                            prvpage = funpage.prvpage()
#                            articalist=zzp.getarticalist(0,20,user_id,typeid=arttypeid)['list']
                        jibie='../'
                    
                    
                    
                    
                    
                    
                    return render_to_response('user/'+pinyin+'/'+urltype+'.html',locals())
        #最终页
        elif type=='3':
            if user_id and artid:
                alltypelist=zzp.getarttypelist(0,20,user_id,'0')['list']
                sql='select typeid,title,litpic,body from py_user_artical where id=%s'
                result=dbp.fetchonedb(sql,artid)
                if result:
                    typeid=result[0]
                    arttypedetail=zzp.getarttypedetail(typeid)
                    if arttypedetail:
#                        typename=arttypedetail['typename']
#                        urltype=arttypedetail['tempname']
                        pinyinname=arttypedetail['pinyin']
                        reid=arttypedetail['reid']
#                        repinyin=arttypedetail['repinyin']
                    title=result[1]
                    litpic=result[2]
                    content=result[3]
                    litpic=litpic.replace('img1.zz91.com/','img3.zz91.com/398x398/')
                    content=content.replace('img1.zz91.com/','img3.zz91.com/900x600/')
                    upartical=zzp.getarticalup(artid,typeid,user_id,pinyinname)#上一篇
                    nextartical=zzp.getarticalnx(artid,typeid,user_id,pinyinname)#下一篇
                    detail='zxdt_detail'
                    if typeid in [2,3]:
                        detail='gyxx_detail'
                    if typeid==7:
                        detail='zxdt_detail'
                    if typeid:
                        topid=int(typeid)
                    if reid:
                        jibie='../../'
                    else:
                        jibie='../'
                return render_to_response('user/'+pinyin+'/'+detail+'.html',locals())
    return HttpResponse()