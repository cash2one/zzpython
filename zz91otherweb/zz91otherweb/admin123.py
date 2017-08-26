#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91tools import *
from zz91db import *
from zz91db_company import zz91login
from zz91db_ast import companydb
dbc=companydb()
from zz91mail import zz91mail
from zz91settings import SPHINXCONFIG,logpath
from settings import pyuploadpath,pyimgurl
from django.views.decorators.csrf import csrf_exempt
import simplejson,sys
import datetime,time,urllib,re,os,MySQLdb,StringIO,Image,ImageDraw,ImageFont,ImageFilter,random,xlwt,operator,threading
nowpath=os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('UTF-8')
execfile(nowpath+"/func/conn.py")
execfile(nowpath+"/func/function.py")
execfile(nowpath+"/func/funcadmin.py")
conn=database()
cursor = conn.cursor()
zz91n=zz91news()
zzother=zz91other()
zzlogin=zz91login()
zzmail=zz91mail()
zzcomp=zz91company()
aqsiq=aqsiq()
zzadmin=zadmin()


#----AQSIQ
def artical(request):
    page=request.GET.get('page')
    typeid=request.GET.get('typeid')
    ntitle=request.GET.get('ntitle')
    isdelete=request.GET.get('isdelete')
    searchlist={}
    if typeid:
        typename=aqsiq.getaqsiqtypename(typeid)
        searchlist['typeid']=typeid
    searchurl=urllib.urlencode(searchlist)
    alltypelist=zzother.getalltypelist(4)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    qsiqnews=aqsiq.getaqsiqnews(frompageCount,limitNum,ntitle,typeid,isdelete)
    listcount=0
    if (qsiqnews):
        listall=qsiqnews['list']
        listcount=qsiqnews['count']
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
    return render_to_response('newsadmin/artical.html',locals())

def update_aqsiq(request):
    request_url=request.META.get('HTTP_REFERER','/')
    alltypelist=zzother.getalltypelist(4)
    artid=int(request.GET.get('artid'))
    aqsiqdetail=aqsiq.getaqsiqdetail(artid)
    ntitle=aqsiqdetail['ntitle']
    ncontent=aqsiqdetail['ncontent']
    ntypename=aqsiqdetail['typename']
    ntype=aqsiqdetail['ntype']
    ndate=aqsiqdetail['ndate']
    return render_to_response('newsadmin/addartical.html',locals())
def aqsiqdetail(request,id=''):
    aqsiqdetail=aqsiq.getaqsiqdetail(id)
    ntitle=aqsiqdetail['ntitle']
    ncontent=aqsiqdetail['ncontent']
    ntypename=aqsiqdetail['typename']
    ntype=aqsiqdetail['ntype']
    ndate=aqsiqdetail['ndate']
    return render_to_response('newsadmin/aqsiqdetail.html',locals())

def addartical(request):
    request_url=request.META.get('HTTP_REFERER','/')
    ndate=get_str_timeall()
    alltypelist=zzother.getalltypelist(4)
    return render_to_response('newsadmin/addartical.html',locals())
def del_aqsiq(request):
    request_url=request.META.get('HTTP_REFERER','/')
    artid=int(request.GET.get('artid'))
    isdelete=int(request.GET.get('isdelete'))
    aqsiq.del_aqsiq(artid,isdelete)
    return HttpResponseRedirect(request_url)
def redel_aqsiq(request):
    request_url=request.META.get('HTTP_REFERER','/')
    artid=int(request.GET.get('artid'))
    aqsiq.del_aqsiq(artid)
    return HttpResponseRedirect(request_url)
def addarticalok(request):
    request_url=request.POST['request_url']
    alltypelist=zzother.getalltypelist(4)
    ncontent=''
    artid=''
    error=0
    ndate=request.POST['ndate']
    ntype=request.POST['ntype']
    if ntype:
        ntypename=aqsiq.getaqsiqtypename(ntype)
    ntitle=request.POST['ntitle']
    if request.POST.has_key('myEditor'):
        ncontent=request.POST['myEditor']
    if request.POST.has_key('artid'):
        artid=request.POST['artid']
    if not ntitle:
        error=1
    if not ncontent:
        error=1
    if error==1:
        return render_to_response('newsadmin/addartical.html',locals())
    if artid:
        aqsiq.updateaqsiq_news(artid,ntitle,ncontent,ntype)
    else:
        aqsiq.addaqsiq_news(ndate,ntitle,ncontent,ntype)
    return HttpResponseRedirect(request_url)

def mailimg(request):
    return render_to_response('data/mailimg.html',locals())
#----上传文件通用
def mailloadimg(request):
    username=request.session.get("username",None)
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
        return render_to_response('data/loadimg.html',locals())
    return HttpResponse("请选择一个文件.")
    

#----发邮件
def mailto(request):
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        mailto=request.POST['mailto']
        subject=request.POST['subject']
        if request.POST.has_key('myEditor'):
            body=request.POST['myEditor']
        else:
            body=''
        errors='此处不能为空'
        error=0
        if not username:
            error1=errors
            error=1
        if not password:
            error2=errors
            error=1
        if not mailto:
            error3=errors
            error=1
        if not subject:
            error4=errors
            error=1
        if not body:
            error5=errors
            error=1
        if error==1:
            return render_to_response('data/mailto.html',locals())
        if '|' in mailto:
            mailto_list=mailto.split('|')
        else:
            mailto_list=[mailto]
        ismailok=zzmail.mail163(username,username,password,mailto_list,subject,body)
        errorok1=''
        errorok2=''
        if ismailok==1:
            errorok1='账号或密码错误'
        if ismailok==2:
            errorok2='接收方错误'
        if errorok1 or errorok2:
            return render_to_response('data/mailto.html',locals())
        else:
            return HttpResponse('发送成功')
    return render_to_response('data/mailto.html',locals())
#----删除数据
def deldata(request):
    request_url=request.META.get('HTTP_REFERER','/')
    pubdate=request.GET.get('pubdate')+' 00:00:00'
    pubdate2=request.GET.get('pubdate2')+' 00:00:00'
    gmt_created=str_to_datetime(pubdate)
    gmt_created2=str_to_datetime(pubdate2)
    zzother.deldata(gmt_created,gmt_created2)
    return HttpResponseRedirect(request_url)
def deldatasis(request):
    request_url=request.META.get('HTTP_REFERER','/')
    dataid=int(request.GET.get('dataid'))
    zzother.deldatasis(dataid)
    return HttpResponseRedirect(request_url)
def delipvisit(request):
    request_url=request.META.get('HTTP_REFERER','/')
    pubdate=request.GET.get('pubdate')+' 00:00:00'
    pubdate2=request.GET.get('pubdate2')+' 00:00:00'
    gmt_created=str_to_datetime(pubdate)
    gmt_created2=str_to_datetime(pubdate2)
    zzother.delipvisit(gmt_created,gmt_created2)
    return HttpResponseRedirect(request_url)

#---百度收录批量查询工具
@csrf_exempt
def baiduincluded(request):
#    baidusl=request.GET.get('baidusl')
#    numb=request.GET.get('numb')
#    if baidusl and numb:
    if request.POST:
        time_begin=time.time()
        baidusl=request.POST['baidusl']
        numb=request.POST['numb']
        listall=[]
        countall=0
        count=0
        countj=''
        baidudate=''
        if baidusl:
            baidusl="".join(baidusl.split())
        if baidusl:
            baiduslist=baidusl.split('http://')[1:]
            lenlist=len(baiduslist)/2
            baiduslist1=[]
            if numb=='1':
                baiduslist1=baiduslist[:lenlist]
            elif numb=='2':
                baiduslist1=baiduslist[lenlist:]
            for baidus in baiduslist1:
                countall+=1
                baidurl='http://'+baidus
                baidu_url='http://www.baidu.com/s?wd='+baidurl+'&ie=utf-8'
                html=getwebhtml(baidu_url)
                if not '抱歉，没有找到与' in html and not '没有找到该URL' in html:
                    count+=1
                    htmls=re.findall('&nbsp;....-..-..&nbsp;',html)
                    if htmls:
                        baidudate=htmls[0].replace('&nbsp;','')
                    else:
                        html=html.replace('<strong>','')
                        html=html.replace('<b>','')
                        htmls=re.findall('..小时以前',html)
                        if htmls:
                            baidudate=htmls[0]
                    list={'baidudate':baidudate,'baidurl':baidurl}
                    listall.append(list)
            if count>0 and countall>0:
#                countj=str((float(count)/countall)*100)+'%'
                time_end=time.time()
                time_all='耗时:'+str(time_end-time_begin)[:5]+'秒'
                countj=str(count)+'/'+str(countall)+','+time_all
#            return simplejson.dumps({'1':1,'2':2},ensure_ascii=False)
            return HttpResponse(countj)
    return render_to_response('newsadmin/baiduincluded2.html',locals())

def baiduincluded2(request):
    baidus=request.GET.get('baidus')
    baidurl='http://'+baidus
    baidurl=baidurl.replace('<br />','')
    baidu_url='http://www.baidu.com/s?wd='+baidurl+'&ie=utf-8'
    html=getwebhtml(baidu_url)
    if not '抱歉，没有找到与' in html and not '没有找到该URL' in html:
        return HttpResponse('1')
    return HttpResponse('0')
'''
class MyThread(object):
    def __init__(self, func_list=None):
    #所有线程函数的返回值汇总，如果最后为0，说明全部成功
        self.ret_flag = 0
        self.func_list = func_list
        self.threads = []
         
    def set_thread_func_list(self, func_list):
        """
        @note: func_list是一个list，每个元素是一个dict，有func和args两个参数
        """
        self.func_list = func_list
 
    def start(self):
        """
        @note: 启动多线程执行，并阻塞到结束
        """
        self.threads = []
        self.ret_flag = 0
        for func_dict in self.func_list:
            if func_dict["args"]:
                t = threading.Thread(target=func_dict["func"], args=func_dict["args"])
            else:
                t = threading.Thread(target=func_dict["func"])
            self.threads.append(t)
 
        for thread_obj in self.threads:
            thread_obj.start()
 
        for thread_obj in self.threads:
            thread_obj.join()
 
    def ret_value(self):
        """
        @note: 所有线程函数的返回值之和，如果为0那么表示所有函数执行成功
        """
        return self.ret_flag

def hetlist2(baiduslist):
    js=0
    count=0
    listall=[]
    baidudate=''
    for baidus in baiduslist:
        js=js+1
        baidurl='http://'+baidus
        baidu_url='http://www.baidu.com/s?wd='+baidurl+'&ie=utf-8'
        html=getwebhtml(baidu_url)
        if not '抱歉，没有找到与' in html and not '没有找到该URL' in html:
            count=count+1
            htmls=re.findall('&nbsp;....-..-..&nbsp;',html)
            if htmls:
                baidudate=htmls[0].replace('&nbsp;','')
            else:
                html=html.replace('<strong>','')
                html=html.replace('<b>','')
                htmls=re.findall('..小时以前',html)
                if htmls:
                    baidudate=htmls[0]
            list={'baidudate':baidudate,'baidurl':baidurl}
            listall.append(list)
    listdir={'count':count,'allcount':js,'list':listall}
    txt=simplejson.dumps(listdir,ensure_ascii=False)
    f=open('dirlist.txt','ab')
    print >>f,txt
    f.close()

def func1(ret_num):
#    time.sleep(5)
    datalist=open('bdlist.txt','r+')
    listd=[]
    for line in datalist:
        line=line.strip()
        listd.append(line)
    datalist.close()
    lend=len(listd)/3
    listd1=listd[:lend]
    hetlist2(listd1)
#    print listd1
    return ret_num
 
def func2(ret_num):
    datalist=open('bdlist.txt','r+')
    listd=[]
    for line in datalist:
        line=line.strip()
        listd.append(line)
    datalist.close()
    lend=len(listd)/3
    listd2=listd[lend:lend*2]
    hetlist2(listd2)
#    print listd2
    return ret_num

def func3(ret_num):
    datalist=open('bdlist.txt','r+')
    listd=[]
    for line in datalist:
        line=line.strip()
        listd.append(line)
    datalist.close()
    lend=len(listd)/3
    listd3=listd[lend*2:]
    hetlist2(listd3)
#    print listd2
    return ret_num

#----百度收录批量查询工具
def baiduincluded(request):
    if request.POST:
        time_begin=int(time.time())
        baidusl=request.POST['baidusl']
        if baidusl:
            baidusl="".join(baidusl.split())
        if baidusl:
            baiduslist=baidusl.split('http://')[1:]
            #lenlist=len(baiduslist)/2
            #baiduslist1=baiduslist[:lenlist]
            #baiduslist2=baiduslist[lenlist:]
            for blist in baiduslist:
                f=open('bdlist.txt','ab')
                print >>f,blist
                f.close()
            mt = MyThread()
            g_func_list = []
            g_func_list.append({"func":func1,"args":(1,)})
            g_func_list.append({"func":func2,"args":(2,)})
            g_func_list.append({"func":func3,"args":(3,)})
            #g_func_list.append({"func":func3,"args":None})
            mt.set_thread_func_list(g_func_list)
            mt.start()
            if mt.ret_flag==0:
                datalist=open('dirlist.txt','r+')
                js=0
                count=0
                allcount=0
                for line in datalist:
                    js+=1
            #        print line
                    linedir=eval(line)
                    count+=linedir['count']
                    allcount+=linedir['allcount']
                if count and allcount:
                    countj='百分比:'+str((float(count)/allcount)*100)+'%'
#                    print countj
                count='收录数:'+str(count)
                allcount='总数:'+str(allcount)
                datalist.close()
                f=open('dirlist.txt','w')
                f1=open('bdlist.txt','w')
                f.close()
                f1.close()
                time_end=int(time.time())
                time_all='查询时间:'+str(time_end-time_begin)+'秒'
    return render_to_response('newsadmin/baiduincluded.html',locals())
'''



#----发邮件
def sendmials(request):
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        mailto=request.POST['mailto']
        subject=request.POST['subject']
        body=request.POST['body']
        errors='此处不能为空'
        error=0
        if not username:
            error1=errors
            error=1
        if not password:
            error2=errors
            error=1
        if not mailto:
            error3=errors
            error=1
        if not subject:
            error4=errors
            error=1
        if not body:
            error5=errors
            error=1
        if error==1:
            return render_to_response('data/sendmials.html',locals())
        if '|' in mailto:
            mailto_list=mailto.split('|')
        else:
            mailto_list=[mailto]
        ismailok=zzmail.mail163(username,username,password,mailto_list,subject,body)
        errorok1=''
        errorok2=''
        if ismailok==1:
            errorok1='账号或密码错误'
        if ismailok==2:
            errorok2='接收方错误'
        if errorok1 or errorok2:
            return render_to_response('data/sendmials.html',locals())
        else:
            return HttpResponseRedirect('datalogin.html?gmt_begin='+gmt_begin+'&gmt_end='+gmt_end)
    
    '''
    fromMail = 'jlj841232468@163.com'
    username = 'jlj841232468@163.com'
    password = '10534jun'
    mailto_list=['1966505278@qq.com','841232468@qq.com']
    subject  = u'[Notice]hello'
    body     = u'hello,this is a mail from ' + fromMail
    '''
#    zzmail.mail163(username,username,password,mailto_list,subject,body)
    return render_to_response('data/sendmials.html',locals())

#----登陆数据详细信息
def logdetail(request):
    arg=request.GET.get('arg')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    gmt_begin2=str_to_int(gmt_begin)
    gmt_end2=str_to_int(gmt_end)
    gmt_begin3=str_to_date(gmt_begin)
    gmt_end3=str_to_date(gmt_end)
    gmt_difference=(gmt_end3-gmt_begin3).days
    loginrecord=zzlogin.getloginrecord(SPHINXCONFIG_news,gmt_begin2,gmt_end2,0,500000,500000,gmt_difference)
    arglist='list'+arg
    listall=loginrecord[arglist]
    page=request.GET.get('page')
    searchlist={}
    searchlist['arg']=arg
    searchlist['gmt_begin']=gmt_begin
    searchlist['gmt_end']=gmt_end
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(30)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    listcount=0
    if listall:
        listall3=[]
        listall2=listall[frompageCount:(frompageCount+limitNum)]
        for list2 in listall2:
            company_id=list2['company_id']
            count=list2['count']
            compdetail=zzcomp.getcompanydetail(company_id)
            list={'account':compdetail['account'],'mail':compdetail['mail'],'count':count}
            listall3.append(list)
        listcount=len(listall)
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
    return render_to_response('data/logdetail.html',locals())
def ipvisitout(request):
    return HttpResponse('正在制作中...请稍候...')
#---页面IP访问数
def ipvisit(request):
    pubdate=request.GET.get('pubdate')
    pubdate2=request.GET.get('pubdate2')
    if pubdate or pubdate2:
        ipvisit=zzother.getipvisit(pubdate,pubdate2)
    return render_to_response('data/ipvisit.html',locals())
#----登陆数据
def datalogin(request):
    yearlogin=request.GET.get('yearlogin')
    if yearlogin:
        timenow2014=int(time.time())
        count2012=zzother.yearlogin(2012)
        count2013=zzother.yearlogin(2013)
        count2014=zzlogin.getlogincount(SPHINXCONFIG_news,1388505600,timenow2014,0,1,100000)
#    gmt_end=getToday()
#    gmt_begin=gmt_end-datetime.timedelta(days=30)
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if not gmt_end and not gmt_begin:
        return render_to_response('data/datalogin.html',locals())
    if gmt_end and gmt_begin:
        if '00:00:00' not in gmt_end:
            gmt_end=gmt_end+' 00:00:00'
        if '00:00:00' not in gmt_begin:
            gmt_begin=gmt_begin+' 00:00:00'
    else:
        return HttpResponse('请选择两个日期')
#    gmt_begins=date_to_strall(gmt_begin)
#    gmt_ends=date_to_strall(gmt_end)
    gmt_begin2=str_to_int(gmt_begin)
    gmt_end2=str_to_int(gmt_end)
    gmt_begin3=str_to_date(gmt_begin)
    gmt_end3=str_to_date(gmt_end)
    gmt_difference=(gmt_end3-gmt_begin3).days
    if gmt_difference>93:
        return HttpResponse('选择日期不能超过3个月')
        
#    gmt_endt=int_to_str(gmt_end2)
    loginrecord=zzlogin.getloginrecord(SPHINXCONFIG_news,gmt_begin2,gmt_end2,0,500000,500000,gmt_difference)
    count=loginrecord['count']
    list1=loginrecord['list1']
    lenl1=len(list1)
    list2=loginrecord['list2']
    lenl2=len(list2)
    list3=loginrecord['list3']
    lenl3=len(list3)
    list4=loginrecord['list4']
    lenl4=len(list4)
    list5=loginrecord['list5']
    lenl5=len(list5)
    list6=loginrecord['list6']
    lenl6=len(list6)
    list7=loginrecord['list7']
    lenl7=len(list7)
    return render_to_response('data/datalogin.html',locals())

#----数据分析导出
def dataout(request):
	pubdate=request.GET.get('pubdate')
	pubdate2=request.GET.get('pubdate2')
	listall=''
	dpubdate=''
	dpubdate2=''
	if pubdate:
		dpubdate=datetime.datetime.strptime(pubdate+' 00:00:00',"%Y-%m-%d %H:%M:%S")
	if pubdate2:
		dpubdate2=datetime.datetime.strptime(pubdate2+' 00:00:00',"%Y-%m-%d %H:%M:%S")
	if pubdate or pubdate2:
		datalist=zzother.getdatalist('','',dpubdate,dpubdate2)
		listall=datalist['list']
	else:
		return HttpResponse('请选择日期')
	if listall:
#		return render_to_response('data/analyse.html',locals())
		wb =xlwt.Workbook()
		ws = wb.add_sheet(u'Sheetname')
		style_k=xlwt.easyxf('align: wrap off')
		ws.col(0).width = 0x0d00 + 500
		ws.col(1).width = 0x0d00 + 500
		ws.col(2).width = 0x0d00 - 500
		ws.col(3).width = 0x0d00 + 500
		ws.col(4).width = 0x0d00 + 500
		ws.col(5).width = 0x0d00 + 1000
        
		ws.write(0, 0, u'日期')
		ws.write(0, 1, u'总IP数')
		ws.write(0, 2, u'已注册IP数')
		ws.write(0, 3, u'当日注册IP数')
		ws.write(0, 4, u'未注册IP数')
		ws.write(0, 5, u'转化率')
        
		js=0
		for list in listall:
			js=js+1
			ws.write(js, 0, list['gmt_created'])
			ws.write(js, 1, list['all_ipcount'])
			ws.write(js, 2, list['alr_count'])
			ws.write(js, 3, list['reg_count'])
			ws.write(js, 4, list['noreg_count'])
			ws.write(js, 5, list['conversion'])
		if pubdate:
			fname = pubdate+u'-'+u'.xls'
		if pubdate2:
			fname = pubdate+u'-'+pubdate2+u'.xls'
		agent=request.META.get('HTTP_USER_AGENT') 
		if agent and re.search('MSIE',agent):
		    response =HttpResponse(mimetype="application/vnd.ms-excel") #解决ie不能下载的问题
		    response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
		else:
			response =HttpResponse(mimetype="application/ms-excel")#解决ie不能下载的问题
			response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
		wb.save(response)
		return response
	return HttpResponse('无数据')
#----曲线图
def analysischart(request):
    pubdate=request.GET.get('pubdate')
    pubdate2=request.GET.get('pubdate2')
    listall=''
    dpubdate=''
    dpubdate2=''
    argdate=''
    if pubdate:
        dpubdate=datetime.datetime.strptime(pubdate+' 00:00:00',"%Y-%m-%d %H:%M:%S")
        tdate1=pubdate[5:7]+u'月'+pubdate[8:10]+u'日'
    else:
        tdate1=u'过去'
    if pubdate2:
        dpubdate2=datetime.datetime.strptime(pubdate2+' 00:00:00',"%Y-%m-%d %H:%M:%S")
        tdate2=u' 到 '+pubdate2[5:7]+u'月'+pubdate2[8:10]+u'日'
    else:
        tdate2=u'至今'
    tdate=tdate1+tdate2
    if pubdate or pubdate2:
        datalist=zzother.getdatalist('','',dpubdate,dpubdate2)
        listall=datalist['list']
        numb=[]
        if listall:
            datet1=[1,2,3,4,5,6,7]
            for list in listall:
                conversion=float(list['conversion'].replace('%','')[:6])
                numb.append(conversion)
        else:
            return HttpResponse('无数据')
    else:
        return HttpResponse('请选择日期')
    numb.reverse()
    return render_to_response('data/analysischart.html',locals())

#---ip流动
def pagedetail(request):
    upnumb=int(request.GET.get('upnumb'))
    pageid=request.GET.get('pageid')
    page=request.GET.get('page')
    if page:
        page=int(page)
    else:
        page=1
    if pageid:
        list2=zzother.getpagenextdetail(pageid)
    allnumb=0
    page2=page+1
#    allnumb=int(list2[-1]['numb'])
    for lt2 in list2:
        if lt2['typeid']=='100':
            allnumb=lt2['numb']
    other_numb=str(upnumb-int(allnumb))
    
    page_arg=pageid+','+other_numb
    return render_to_response('data/pagedetail.html',locals())

def tongji_chart(request):
    page_arg=request.GET.get('page_arg')
    if page_arg:
        pg=page_arg.split(',')
        pageid=pg[0]
        out_numb=pg[1]
        if pageid:
            list2=zzother.getpagenextdetail(pageid)
        if out_numb:
            out_numb=int(out_numb)
    return render_to_response('chart/tongji_chart.html',locals())

#----数据分析
def analyse(request):
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    datalist=zzother.getdatalist(frompageCount,limitNum)
    listcount=0
    if (datalist):
        listall=datalist['list']
        listcount=datalist['count']
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
    return render_to_response('data/analyse.html',locals())
#----页面分析导出
def analyse_pageout(request):
    pubdate=request.GET.get('pubdate')
    pubdate2=request.GET.get('pubdate2')
    listall=''
    dpubdate=''
    dpubdate2=''
    if pubdate:
        dpubdate=datetime.datetime.strptime(pubdate+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    if pubdate2:
        dpubdate2=datetime.datetime.strptime(pubdate2+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    if pubdate or pubdate2:
        datalist=zzother.getstatistics_page('',dpubdate,dpubdate2)
    else:
        return HttpResponse('请选择日期')
    if datalist:
#        return render_to_response('data/analyse.html',locals())
        wb =xlwt.Workbook()
        ws = wb.add_sheet(u'Sheetname')
        style_k=xlwt.easyxf('align: wrap off')
        
        ws.col(0).width = 0x0d00 + 500
        ws.col(1).width = 0x0d00 + 500
        
        ws.write(0, 0, u'日期')
        ws.write(0, 1, u'页面类型')
        ws.write(0, 2, u'入口页')
        ws.write(0, 3, u'登录页')
        ws.write(0, 4, u'注册页')
        ws.write(0, 5, u'离开页')
        
        js=0
        for list in datalist:
            js=js+1
            ws.write(js, 0, list['gmt_created'])
            ws.write(js, 1, list['typename'])
            ws.write(js, 2, list['in_page'])
            ws.write(js, 3, list['log_page'])
            ws.write(js, 4, list['reg_page'])
            ws.write(js, 5, list['out_page'])
        if pubdate:
            fname = pubdate+u'-'+u'.xls'
        if pubdate2:
            fname = pubdate+u'-'+pubdate2+u'.xls'
        agent=request.META.get('HTTP_USER_AGENT') 
        if agent and re.search('MSIE',agent):
            response =HttpResponse(mimetype="application/vnd.ms-excel") #解决ie不能下载的问题
            response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
        else:
            response =HttpResponse(mimetype="application/ms-excel")#解决ie不能下载的问题
            response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
        wb.save(response)
        return response
    return HttpResponse('无数据')
#----页面分析
def analyse_page(request):
    pubdate=request.GET.get('pubdate')
    pubdate2=request.GET.get('pubdate2')
    if not pubdate and not pubdate2:
        return render_to_response('data/analyse_page.html',locals())
    listall=''
    dpubdate=''
    dpubdate2=''
    if pubdate:
        dpubdate=datetime.datetime.strptime(pubdate+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    if pubdate2:
        dpubdate2=datetime.datetime.strptime(pubdate2+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    if pubdate or pubdate2:
        statistics_page=zzother.getstatistics_page('',dpubdate,dpubdate2)
    else:
        return HttpResponse('请选择日期')
    '''
    page=request.GET.get('page')
    datetoday=request.GET.get('datetoday')
    if datetoday:
        if u'00:00:00' not in datetoday:
            datetoday=datetoday+u' 00:00:00'
        datetoday=datetime.datetime.strptime(datetoday,"%Y-%m-%d %H:%M:%S")
    pagecount=zzother.get_pagecount()
    oneday=datetime.timedelta(days=1)
    if page:
        page=int(page)
    else:
        page=1
    if not datetoday and page==1:
        datetoday=getYesterday()
    if page==pagecount:
        nextpage=pagecount
    else:
        nextpage=page+1
        nextdate=(datetoday-oneday).strftime('%Y-%m-%d %H:%M:%S')
    if page==1:
        prvpage=1
    else:
        prvpage=page-1
        prvtdate=(datetoday+oneday).strftime('%Y-%m-%d %H:%M:%S')
    statistics_page=zzother.getstatistics_page(datetoday)
    datetoday=datetoday.strftime('%Y-%m-%d %H:%M:%S')
    '''
    return render_to_response('data/analyse_page.html',locals())

def del_type(request):
    request_url=request.META.get('HTTP_REFERER','/')
    typeid=request.GET.get('typeid')
    sql='delete from pagetype where id=%s'
    updatetodb(sql,conn,cursor,[typeid])
    return HttpResponseRedirect(request_url)

def add_type(request):
    request_url=request.META.get('HTTP_REFERER','/')
    typeid=request.GET.get('typeid')
    typename=zzother.gettypename(typeid)
    return render_to_response('data/add_type.html',locals())
def add_typeok(request):
    request_url=request.GET.get('request_url')
    typename=request.GET.get('typename')
    sortrank=request.GET.get('sortrank')
    url=request.GET.get('url')
    typeid=request.GET.get('typeid')
    error1=''
    error2=''
    if not typename:
        error1='不能为空'
    if not url:
        error2='不能为空'
    if error1 or error2:
        return render_to_response('addwebtype.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    if typeid:
        sql='update pagetype set name=%s,url=%s,id=%s where id=%s'
        updatetodb(sql,conn,cursor,[typename,url,sortrank,typeid])
    else:
        sql='insert into pagetype(name,url,id) values(%s,%s,%s)'
        updatetodb(sql,conn,cursor,[typename,url,sortrank])
    return HttpResponseRedirect(request_url)
#----页面类型
def analyse_type(request):
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    typelist=zzother.gettypelist(frompageCount,limitNum)
    listcount=0
    if (typelist):
        listall=typelist['list']
        listcount=typelist['count']
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
    return render_to_response('data/analyse_type.html',locals())
#----跳出率
def jumpout(request):
    return render_to_response('data/jumpout.html',locals())
    
def imgload(request):
    type=request.GET.get("type")
    return render_to_response('imgload.html',locals())
#----图片上传
def upload(request):
    type=request.GET.get("type")
    username=request.session.get("username",None)
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        
        file = request.FILES['file']
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
        im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
        tmp = random.randint(100, 999)
        newpath=pyuploadpath+timepath
        imgpath=newpath+str(nowtime)+str(tmp)+"."+im.format
        if not os.path.isdir(newpath):
        	os.makedirs(newpath)

#        im.save(imgpath,im.format,quality = 100)

        des_origin_f = open(imgpath,"w")
        for chunk in file.chunks():  
            des_origin_f.write(chunk)  
        des_origin_f.close()

        mstream.closed
        tempim.closed
        picurl=imgpath.replace(pyuploadpath,'')
        pic_url=pyimgurl+picurl
        return render_to_response('loadimg.html',locals())
    return HttpResponse("请选择一张图片.<a onclick='window.history.back(-1)'>返回</a>")

def returnpage(request):
    request_url=request.GET.get('request_url')
    wtype=request.GET.get('wtype')
    if wtype:
        request_url=request_url+'&wtype='+wtype
    return HttpResponseRedirect(request_url)

#----首页
def default(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('loginpage.html')
    admintypelist=getadmintypelist()
    return render_to_response('index.html',locals())

def webtype(request):
	wtype=request.GET.get('wtype')
	reid=request.GET.get('reid')
	topid=request.GET.get('topid')
	page=request.GET.get('page')
	if reid:
		re_name=gettypename(reid)
	if topid:
		typename2=gettypename(topid)
	if not page:
	    page=1
	funpage=zz91page()
	limitNum=funpage.limitNum(15)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(3)
	before_range_num = funpage.before_range_num(6)
	webtypelist=getwebtypelist(frompageCount,limitNum,reid,wtype)
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
	return render_to_response('webtype.html',locals())
#----添加栏目
def addwebtype(request):
	request_url=request.META.get('HTTP_REFERER','/')
	wtype=request.GET.get('wtype')
	typeid=request.GET.get('typeid')
	topid=request.GET.get('topid')
	return render_to_response('addwebtype.html',locals())

def addwebtypeok(request):
    wtype=request.GET.get('wtype')
    typename=request.GET.get('typename')
    sortrank=request.GET.get('sortrank')
    request_url=request.GET.get('request_url')
    typeid=request.GET.get('typeid')
    uptypeid=request.GET.get('uptypeid')
    topid=request.GET.get('topid')
    error1=''
    if not typename:
        error1='不能为空'
    if error1:
        return render_to_response('addwebtype.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    if uptypeid:
        retypeid=''
        retypename=request.GET.get('retypename')
        if retypename:
            retypeid=gettypeid(retypename)
        toptypename=request.GET.get('toptypename')
        toptypeid=''
        if toptypename:
            toptypeid=gettypeid(toptypename)
        sql='update webtype set typename=%s,sortrank=%s,reid=%s,topid=%s where id=%s'
        updatetodb(sql,conn,cursor,[typename,sortrank,retypeid,toptypeid,uptypeid])
    elif topid:
        typeid=int(typeid)
        topid=int(topid)
        sql='insert into webtype(reid,topid,typename,sortrank) values(%s,%s,%s,%s)'
        updatetodb(sql,conn,cursor,[typeid,topid,typename,sortrank])
    elif typeid:
        typeid=int(typeid)
        sql='insert into webtype(reid,topid,typename,sortrank) values(%s,%s,%s,%s)'
        updatetodb(sql,conn,cursor,[typeid,typeid,typename,sortrank])
    else:
        sql='insert into webtype(typename,sortrank,wtype) values(%s,%s,%s)'
        updatetodb(sql,conn,cursor,[typename,sortrank,wtype])
    return HttpResponseRedirect(request_url)

def updatetype(request):
	request_url=request.META.get('HTTP_REFERER','/')
	reid=request.GET.get('reid')
	uptypeid=int(request.GET.get('typeid'))
	typedetail=gettypedetail(uptypeid)
	typename=typedetail['typename']
	sortrank=typedetail['sortrank']
	retypename=typedetail['retypename']
	toptypename=typedetail['toptypename']
	return render_to_response('addwebtype.html',locals())

def deletetype(request):
	typeid=int(request.GET.get('typeid'))
	sql='delete from webtype where id=%s'
	updatetodb(sql,conn,cursor,[typeid])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def website(request):
	wtype=request.GET.get('wtype')
	page=request.GET.get('page')
	title=request.GET.get('title')
#	if title:
#		title=title.encode('utf8')
	recycle=request.GET.get('recycle')
	recommend=request.GET.get('recommend')
	if recommend:
		if recommend=='1':
			recommend_name='头条'
		if recommend=='2':
			recommend_name='首页'
	typeid=request.GET.get('typeid')
	if typeid:
		typename=gettypename(typeid)
	topid=request.GET.get('topid')
	
	#翻页参数
	searchlist={}
	if wtype:
		searchlist['wtype']=wtype
	if recycle:
		searchlist['recycle']=recycle
	if typeid:
		searchlist['typeid']=typeid
	if recommend:
		searchlist['recommend']=recommend
	searchurl=urllib.urlencode(searchlist)
	
	alltypelist=zzother.getalltypelist(wtype)
	if not page:
	    page=1
	funpage=zz91page()
	limitNum=funpage.limitNum(15)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(3)
	before_range_num = funpage.before_range_num(6)
	webtypelist=getwebsitelist(frompageCount,limitNum,recycle,typeid,recommend,'',topid,wtype,title)
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
	return render_to_response('website.html',locals())
def page404(request):
    page=request.GET.get('page')
    url=request.GET.get('url')
    wtype=request.GET.get('wtype')
    #翻页参数
    searchlist={}
    if url:
        searchlist['url']=url
    searchurl=urllib.urlencode(searchlist)
    
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    webtypelist=getpage404list(frompageCount,limitNum,wtype)
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
    return render_to_response('page404.html',locals())
def deletepage404(request):
    request_url=request.META.get('HTTP_REFERER','/')
    id=int(request.GET.get('id'))
    sql='delete from page404 where id=%s'
    updatetodb(sql,conn,cursor,[id])
    return HttpResponseRedirect(request_url)
def deleteweb(request):
	request_url=request.META.get('HTTP_REFERER','/')
	webid=int(request.GET.get('webid'))
	sql='update website set isdelete=1 where id=%s'
	updatetodb(sql,conn,cursor,[webid])
	return HttpResponseRedirect(request_url)
def reduction(request):
	request_url=request.META.get('HTTP_REFERER','/')
	webid=int(request.GET.get('webid'))
	sql='update website set isdelete=0 where id=%s'
	updatetodb(sql,conn,cursor,[webid])
	return HttpResponseRedirect(request_url)
#----推荐
def recommend(request):
	request_url=request.META.get('HTTP_REFERER','/')
	updatetime=datetime.datetime.now()
	webid=int(request.GET.get('webid'))
	recommend=int(request.GET.get('recommend'))
	sql='update website set recommend=%s,updatetime=%s where id=%s'
	updatetodb(sql,conn,cursor,[recommend,updatetime,webid])
	return HttpResponseRedirect(request_url)
#----取消推荐
def cancelrecommend(request):
	request_url=request.META.get('HTTP_REFERER','/')
	updatetime=datetime.datetime.now()
	webid=int(request.GET.get('webid'))
	sql='update website set recommend=0,updatetime=%s where id=%s'
	updatetodb(sql,conn,cursor,[updatetime,webid])
	return HttpResponseRedirect(request_url)
#----修改网站
def updateweb(request):
	request_url=request.META.get('HTTP_REFERER','/')
	webid=int(request.GET.get('webid'))
	webdetail=getwebdetail(webid)
	wtype=webdetail['wtype']
	alltypelist=zzother.getalltypelist(wtype)
	webname=webdetail['name']
	typeid=webdetail['typeid']
	typename=webdetail['typename']
	pic=webdetail['pic']
	weburl=webdetail['url']
	sortrank=webdetail['sortrank']
	gmt_created=webdetail['gmt_created']
	return render_to_response('addwebsite.html',locals())
#----添加网站
def addwebsite(request):
	request_url=request.META.get('HTTP_REFERER','/')
	wtype=request.GET.get('wtype')
	gmt_created=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	alltypelist=zzother.getalltypelist(wtype)
	return render_to_response('addwebsite.html',locals())
def addwebsiteok(request):
	request_url=request.GET.get('request_url')
	wtype=request.GET.get('wtype')
	webid=request.GET.get('webid')
	webname=request.GET.get('webname')
	pic=request.GET.get('pic')
	weburl=request.GET.get('weburl')
	typeid=request.GET.get('typeid')
	typename=gettypename(typeid)
	sortrank=request.GET.get('sortrank')
	gmt_created=request.GET.get('gmt_created')
	updatetime=datetime.datetime.now()
	if sortrank:
		sortrank=int(sortrank)
	else:
		sortrank=50
	if not gmt_created:
		gmt_created=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	alltypelist=zzother.getalltypelist(wtype)
	error1=''
	error2=''
	error3=''
	if not webname:
		error1='不能为空'
	if not weburl:
		error2='不能为空'
	gmt_created=gmt_created.replace('.','-')
	if gmt_created[-1:]=='-' or gmt_created.replace('-','').isdigit()==False:
		error3='日期格式不对'
	if error1 or error2 or error3:
		return render_to_response('addwebsite.html',locals())
	if webid:
		sql='update website set name=%s,pic=%s,url=%s,typeid=%s,gmt_created=%s,updatetime=%s,sortrank=%s where id=%s'
		updatetodb(sql,conn,cursor,[webname,pic,weburl,typeid,gmt_created,updatetime,sortrank,webid])
	else:
		sql='insert into website(name,pic,url,typeid,gmt_created,updatetime,sortrank,wtype) values(%s,%s,%s,%s,%s,%s,%s,%s)'
		updatetodb(sql,conn,cursor,[webname,pic,weburl,typeid,gmt_created,updatetime,sortrank,wtype])
	return HttpResponseRedirect(request_url)

def webartical(request):
    wtype=request.GET.get('wtype')
    page=request.GET.get('page')
    typeid=request.GET.get('typeid')
    if typeid:
        typename=gettypename(typeid)
    
    #翻页参数
    searchlist={}
    if typeid:
        searchlist['typeid']=typeid
    searchurl=urllib.urlencode(searchlist)
    
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    webtypelist=getwebsitelist(frompageCount,limitNum,'','','','','',wtype,'')
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
    
    
    return render_to_response('webartical.html',locals())

def addwebartical(request):
    request_url=request.META.get('HTTP_REFERER','/')
    wtype=request.GET.get('wtype')
    alltypelist=zzother.getalltypelist(wtype)
    gmt_created=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return render_to_response('addwebartical.html',locals())
def update_artical(request):
    request_url=request.META.get('HTTP_REFERER','/')
    wtype=request.GET.get('wtype')
    alltypelist=zzother.getalltypelist(wtype)
    artid=request.GET.get('artid')
    webdetail=getwebdetail(artid)
    wtype=webdetail['wtype']
    alltypelist=zzother.getalltypelist(wtype)
    title=webdetail['name']
    typeid=webdetail['typeid']
    typename=webdetail['typename']
    litpic=webdetail['pic']
    weburl=webdetail['url']
    sortrank=webdetail['sortrank']
    gmt_created=webdetail['gmt_created']
    content=webdetail['content']
    gmt_created=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return render_to_response('addwebartical.html',locals())
def addwebarticalok(request):
    request_url=request.POST['request_url']
    ncontent=''
    artid=''
    error=0
    wtype=request.POST['wtype']
    sortrank=request.POST['sortrank']
    gmt_created=request.POST['gmt_created']
    litpic=request.POST['litpic']
    typeid=request.POST['typeid']
    weburl=request.POST['weburl']
    if typeid:
        ntypename=zzother.gettypename(typeid)
    title=request.POST['title']
    if request.POST.has_key('myEditor'):
        content=request.POST['myEditor']
    if request.POST.has_key('artid'):
        artid=request.POST['artid']
    if not title:
        error=1
    if not content:
        error=1
    if error==1:
        return render_to_response('addwebartical.html',locals())
    updatetime=datetime.datetime.now()
    if artid:
        zzother.updateartical(title,litpic,weburl,typeid,content,updatetime,sortrank,wtype,artid)
    else:
        zzother.addwebartical(title,litpic,weburl,typeid,content,gmt_created,updatetime,sortrank,wtype)
    return HttpResponseRedirect(request_url)
    
def visiturl(request):
    page=request.GET.get('page')
    account=request.GET.get('account')
    searchlist={}
    if account:
        searchlist['account']=account
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    visiturllist=zzother.getvisiturl(frompageCount,limitNum,account)
    if not visiturllist['list']:
        visiturllist=zzother.getvisiturl(frompageCount,limitNum,account,1)
    listcount=0
    if (visiturllist):
        listall=visiturllist['list']
        listcount=visiturllist['count']
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
    return render_to_response('data/visiturl.html',locals())

#文件上传功能
def uploadfileadmin(request):
    listall=zzadmin.getseofilelist()
    return render_to_response('uploadfileadmin.html',locals())
def uploadfileok(request):
    if request.method == 'POST':
        request_url=request.META.get('HTTP_REFERER','/')
        #默认路径
        path='/home/xbin/upload/'
        
        file = request.FILES['file']
        timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
        newpath=pyuploadpath+timepath
        path=newpath
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
            
        filename=file.name
        
        handle_uploaded_file(path,request.FILES['file'], str(request.FILES['file']))
        filename=str(request.FILES['file'])
        
        
        url="http://www.zz91.com/404/"+timepath+filename
        gmt_created=datetime.datetime.now()
        gmt_modify=datetime.datetime.now()
        sql="insert into seo_xmlfile (filename,path,url,gmt_created,gmt_modify) values(%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,[filename,path,url,gmt_created,gmt_modify])
        return render_to_response("uploadfileok.html",locals())
    return HttpResponse("Failed")
#上传函数
def handle_uploaded_file(path,file, filename):
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
#删除已上传的文件
def del_this_file(request):
    request_url=request.META.get('HTTP_REFERER','/')
    id=request.GET.get('id')
    result=zzadmin.getthisfilename(id=id)
    if result:
        filename=result['filename']
        path=result['path']
        filename_and_path=path+filename
        if os.path.exists(filename_and_path):
            os.remove(filename_and_path)
        #删除记录
        sql="delete from seo_xmlfile where id=%s"
        dbc.updatetodb(sql,[id])
    return HttpResponseRedirect(request_url)

#敏感词
def mingang(request):
    request_url=request.META.get('HTTP_REFERER','/')
    page=request.GET.get('page')
    account=request.GET.get('account')
    searchlist={}
    if account:
        searchlist['account']=account
        searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    listmingan=zzadmin.getminganglist(frompageCount=frompageCount,limitNum=limitNum)
    listcount=0
    if (listmingan):
        listall=listmingan['list']
        listcount=listmingan['count']
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
    return render_to_response("admin/mingang.html",locals())


