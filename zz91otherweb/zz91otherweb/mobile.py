#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
#from zz91db_huzhu import zz91huzhu
from zz91db_mobile import payorder
from zz91db_ast import companydb
#from zz91db_130 import otherdb
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime,getoptionlist,date_to_strall,date_to_str,filter_tags
import time,urllib,sys,os,datetime
#dbo=otherdb()
dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/mobile_function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/huzhu_function.py")
reyzmatxt='psl123'

zzm=mobile()
zzms=mshop()
zzweixin=zweixin()
zzhuzhu=zz91huzhu()

def delqbyzm(request):
    yzmatxt=request.GET.get('yzmatxt')
    if yzmatxt==reyzmatxt:
        return HttpResponse('1')
    return HttpResponse('0')
def redelqb(request):
    yzmatxt=request.GET.get('yzmatxt')
    deldataid=request.GET.get('deldataid')
    deldbname=request.GET.get('deldbname')
    request_url=request.META.get('HTTP_REFERER','/')
    if yzmatxt==reyzmatxt:
        if deldbname:
            sql='delete from '+deldbname+' where id=%s'
            dbc.updatetodb(sql,[deldataid])
    return HttpResponseRedirect(request_url)
#----便捷删除ast数据
def delastdbsimp(request):
    id=request.GET.get('id')
    db=request.GET.get('db')
    sql='delete from '+db+' where id=%s'
    dbc.updatetodb(sql,[id])
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#----钱包充值广告
def qianbao_gg(request):
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    qianbao_gglist=zzm.getqianbao_gglist(frompageCount,limitNum)
    listcount=0
    listall=qianbao_gglist['list']
    listcount=qianbao_gglist['count']
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
    return render_to_response('mobile/qianbao_gg.html',locals())
def updateqbgg(request):
    request_url=request.META.get('HTTP_REFERER','/')
    qbgg_id=request.GET.get('qbgg_id')
    sql='select begin_time,end_time,infee,sendfee,txt from qianbao_gg where id=%s'
    result=dbc.fetchonedb(sql,qbgg_id)
    if result:
        begin_time=formattime(result[0],1)
        end_time=formattime(result[1],1)
        infee=result[2]
        sendfee=result[3]
        txt=result[4]
    return render_to_response('mobile/updateqbgg.html',locals())
def updateqbggok(request):
    request_url=request.GET.get('request_url')
    qbgg_id=request.GET.get('qbgg_id')
    begin_time=request.GET.get('begin_time')
    end_time=request.GET.get('end_time')
    infee=request.GET.get('infee')
    sendfee=request.GET.get('sendfee')
    txt=request.GET.get('txt')
    sql='update qianbao_gg set begin_time=%s,end_time=%s,infee=%s,sendfee=%s,txt=%s where id=%s'
    dbc.updatetodb(sql,[begin_time,end_time,infee,sendfee,txt,qbgg_id])
    return HttpResponseRedirect(request_url)
#----微信
def weixinscore(request):
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
    weixinscore=zzweixin.getweixinscore(frompageCount,limitNum,account)
    listcount=0
    if (weixinscore):
        listall=weixinscore['list']
        listcount=weixinscore['count']
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
    return render_to_response('weixin/weixinscore.html',locals())
def accountscore(request):
    page=request.GET.get('page')
    account=request.GET.get('account')
    nickname=request.GET.get('nickname')
    contact=request.GET.get('contact')
    mobile=request.GET.get('mobile')
    searchlist={}
    if account:
        searchlist['account']=account
    if nickname:
        nickname=nickname.encode('utf8')
        searchlist['nickname']=nickname
    if contact:
        contact=contact.encode('utf8')
        searchlist['contact']=contact
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    accountscore=zzweixin.getaccountscore(frompageCount,limitNum,account,nickname,contact,mobile)
    listcount=0
    if (accountscore):
        listall=accountscore['list']
        listcount=accountscore['count']
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
    return render_to_response('weixin/accountscore.html',locals())
def scoreexchange(request):
    prizelog_id=request.GET.get('prizelog_id')
    if prizelog_id:
        request_url=request.META.get('HTTP_REFERER','/')
        zzweixin.updateprizelog(int(prizelog_id))
        HttpResponseRedirect(request_url)
    page=request.GET.get('page')
    account=request.GET.get('account')
    prizeid=request.GET.get('prizeid')
    ischeck=request.GET.get('ischeck')
    type=request.GET.get('type')
    if ischeck=='0':
        check_name='未兑换'
    elif ischeck=='1':
        check_name='已兑换'
    elif ischeck=='2':
        check_name='全部'
    if not ischeck:
        ischeck='0'
    if prizeid:
        prizetitle=zzweixin.getprize(int(prizeid))
    prizetypelist=zzweixin.getprizetype()
    searchlist={}
    if account:
        searchlist['account']=account
    if prizeid:
        searchlist['prizeid']=prizeid
    if ischeck:
        searchlist['ischeck']=ischeck
    if prizelog_id:
        searchlist['prizelog_id']=prizelog_id
    if type:
        searchlist['type']=type
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    scoreexchange=zzweixin.getscoreexchange(frompageCount,limitNum,account=account,prizeid=prizeid,ischeck=ischeck,type=type)
    listcount=0
    if (scoreexchange):
        listall=scoreexchange['list']
        listcount=scoreexchange['count']
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
    return render_to_response('weixin/scoreexchange.html',locals())
def addweixinscore(request):
    request_url=request.META.get('HTTP_REFERER','/')
    account=request.GET.get('account')
    return render_to_response('weixin/addweixinscore.html',locals())
def addweixinscoreok(request):
    request_url=request.GET.get('request_url')
    account=request.GET.get('account')
    score=request.GET.get('score')
    error1=''
    error2=''
    if not account:
        error1='请输入帐号'
    if not score:
        error2='请输入积分'
    if error1 or error2:
        return render_to_response('weixin/addweixinscore.html',locals())
    has_account=zzweixin.hasaccount(account)
    if has_account:
        zzweixin.addwexinscore(account,score)
        return HttpResponseRedirect(request_url)
    error1="无此账号"
    return render_to_response('weixin/addweixinscore.html',locals())
#流量宝
def shop_llb_keywords(request):
    searchlist={}
    page=request.GET.get('page')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    checked=request.GET.get('checked')
    if account:
        searchlist['account']=account
    if mobile:
        searchlist['mobile']=mobile
    if checked:
        searchlist['checked']=checked
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    llblist=zzms.getllb_keywords(frompageCount,limitNum,searchlist=searchlist)
    listcount=0
    if llblist:
        listall=llblist['list']
        listcount=llblist['count']
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
    return render_to_response('mobile/shop/shop_llb_keywords.html',locals())

def delshop_llb_keywords(request):
    request_url=request.META.get('HTTP_REFERER','/')
    id=request.GET.get('id')
    sql='delete from app_jingjia_keywords where id=%s'
    dbc.updatetodb(sql,[id])
    return HttpResponseRedirect(request_url)

def pay_order(request):
    searchlist={}
    page=request.GET.get('page')
    out_trade_no=request.GET.get('out_trade_no')
    mobile=request.GET.get('mobile')
    is_success=request.GET.get('is_success')
    if out_trade_no:
        searchlist['out_trade_no']=out_trade_no
    if mobile:
        searchlist['mobile']=mobile
    if is_success:
        searchlist['is_success']=is_success
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    pay_orderlist=zzm.getpay_orderlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=0
    listall=pay_orderlist['list']
    listcount=pay_orderlist['count']
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
    return render_to_response('mobile/pay_order.html',locals())

def huzhu(request):
    categorylist=zzhuzhu.getcategorylist()
    page=request.GET.get('page')
    account=request.GET.get('account')
    typeid=request.GET.get('typeid')
    if typeid:
        typename=zzhuzhu.getbbs_post_category(typeid)
    is_del=request.GET.get('is_del')
    check_status=request.GET.get('check_status')
    if check_status=='0':
        check_name='未审核'
    elif check_status=='1':
        check_name='已审核'
    elif check_status=='2':
        check_name='已读'
    elif check_status=='3':
        check_name='退回'
    ispush=request.GET.get('ispush')
    if ispush=='0':
        push_name='未推送'
    elif ispush=='1':
        push_name='已推送'

    guanzhu_id=request.GET.get('guanzhu_id')
    
    if guanzhu_id=='1':
        guanzhu_name='废金属'
    elif guanzhu_id=='2':
        guanzhu_name='废塑料'
    elif guanzhu_id=='3':
        guanzhu_name='综合废料'
    
    searchlist={}
    if account:
        searchlist['account']=account
    if typeid:
        searchlist['typeid']=typeid
    if is_del:
        searchlist['is_del']=is_del
    if check_status:
        searchlist['check_status']=check_status
    if ispush:
        searchlist['ispush']=ispush
    if guanzhu_id:
        searchlist['guanzhu_id']=guanzhu_id
    searchurl=urllib.urlencode(searchlist)

    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if ispush=='1':
        bbspostlist=zzhuzhu.getpushlist(frompageCount,limitNum,guanzhu_id)
    else:
        bbspostlist=zzhuzhu.getbbspostlist(frompageCount,limitNum,typeid,check_status,ispush,is_del,account)
    listcount=0
    if (bbspostlist):
        listall=bbspostlist['list']
        listcount=bbspostlist['count']
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
    return render_to_response('mobile/huzhu.html',locals())

#展会直播
def zhibo(request):
    searchlist={}
    ztype=request.GET.get("ztype")
    if ztype:
        searchlist['ztype']=ztype
    searchurl=urllib.urlencode(searchlist)
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    zhibolist=zzhuzhu.getzhibolist(frompageCount,limitNum,searchlist=searchlist)
    listcount=0
    if (zhibolist):
        listall=zhibolist['list']
        listcount=zhibolist['count']
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
    return render_to_response('zhibo/zhibo.html',locals())
def zhibo_add(request):
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_created=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return render_to_response('zhibo/zhibo_add.html',locals())
def zhibo_save(request):
    request_url=request.POST.get('request_url')
    content=request.POST.get('myEditor')
    gmt_created=request.POST.get('gmt_created')
    zid=request.POST.get('zid')
    title=request.POST.get('title')
    ztype=request.POST.get('ztype')
    if zid:
        sql="update subject_zhibo set content=%s,title=%s,gmt_created=%s,ztype=%s where id=%s"
        dbc.updatetodb(sql,[content,title,gmt_created,ztype,zid])
    else:
        sql="insert into subject_zhibo(title,content,gmt_created,ztype) values(%s,%s,%s,%s)"
        dbc.updatetodb(sql,[title,content,gmt_created,ztype])
    return HttpResponseRedirect(request_url)
def zhibo_mod(request):
    request_url=request.META.get('HTTP_REFERER','/')
    sql="select content,gmt_created,ztype,title from subject_zhibo where id=%s"
    zid=request.GET.get('zid')
    result=dbc.fetchonedb(sql,[zid])
    if result:
        content=result[0]
        gmt_created=result[1]
        ztype=result[2]
        title=result[3]
        gmt_created=formattime(gmt_created)
    return render_to_response('zhibo/zhibo_add.html',locals())
def zhibo_del(request):
    request_url=request.META.get('HTTP_REFERER','/')
    zid=request.GET.get('zid')
    sql="delete from subject_zhibo where id=%s"
    dbc.updatetodb(sql,[zid])
    return HttpResponseRedirect(request_url)

def pushtype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    checktitle=request.GET.getlist('checktitle')
    checktype=request.GET.getlist('checktype')
    zzhuzhu.addbbs_post_invite(checktitle,checktype)
    return HttpResponseRedirect(request_url)

def add_bbs_post(request):
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_created=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    categorylist=zzhuzhu.getcategorylist()
    return render_to_response('mobile/add_bbs_post.html',locals())

def del_bbs_post(request):
    request_url=request.META.get('HTTP_REFERER','/')
    postid=request.GET.get('postid')
    is_del=request.GET.get('is_del')
    zzhuzhu.updatedb(is_del,postid)
    return HttpResponseRedirect(request_url)

def add_bbs_postok(request):
    request_url=request.POST['request_url']
    title=request.POST['title']
    content=request.POST['myEditor']
    litpic=request.POST['litpic']
    gmt_created=request.POST['gmt_created']
    bbs_post_category_id=request.POST['bbs_post_category_id']
    postid=''
    if request.POST.has_key('postid'):
        postid=request.POST['postid']
    account='admin'
    company_id=0
    check_status=1
    postsource=0
    error=''
    if not content:
        error=1
    if error:
        return render_to_response('mobile/add_bbs_post.html',locals())
    if postid:
        zzhuzhu.update_bbs_post(bbs_post_category_id,title,content,check_status,gmt_created,postsource,litpic,postid)
    else:
        zzhuzhu.add_bbs_post(company_id,account,bbs_post_category_id,title,content,check_status,gmt_created,postsource,litpic)
    return HttpResponseRedirect(request_url)

def update_bbs_post(request):
    request_url=request.META.get('HTTP_REFERER','/')
    categorylist=zzhuzhu.getcategorylist()
    postid=request.GET.get('postid')
    bbs_post_detail=zzhuzhu.getbbs_post_detail(postid)
    title=bbs_post_detail['title']
    content=bbs_post_detail['content']
    litpic=bbs_post_detail['litpic']
    gmt_created=bbs_post_detail['gmt_created']
    bbs_post_category=bbs_post_detail['bbs_post_category']
    bbs_post_category_id=bbs_post_detail['bbs_post_category_id']
    return render_to_response('mobile/add_bbs_post.html',locals())

def replylist(request):
    page=request.GET.get('page')
    postid=request.GET.get('postid')
    account=request.GET.get('account')
    
    searchlist={}
    if account:
        searchlist['account']=account
    if postid:
        searchlist['postid']=postid
    searchurl=urllib.urlencode(searchlist)
    
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    replylist=zzhuzhu.getreplylist(frompageCount,limitNum,postid,account)
    listcount=0
    if (replylist):
        listall=replylist['list']
        listcount=replylist['count']
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
    return render_to_response('mobile/replylist.html',locals())

def exchangetype(request):
    page=request.GET.get('page')
    type=request.GET.get('type')
    closeflag=request.GET.get('closeflag')
    
    searchlist={}
    if closeflag:
        searchlist['closeflag']=closeflag
    if type:
        searchlist['type']=type
    searchurl=urllib.urlencode(searchlist)
    
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    replylist=zzweixin.getexchangetypelist(frompageCount,limitNum,type,closeflag)
    listcount=0
    if (replylist):
        listall=replylist['list']
        listcount=replylist['count']
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
    return render_to_response('mobile/exchangetype.html',locals())

def addexchangetype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('mobile/addexchangetype.html',locals())

def updatexchangetype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    changetypeid=request.GET.get('changetypeid')
    sql='select title,pic,webpic,score,num,numall,content,ord,closeflag,gmt_created,type from weixin_prize where id=%s'
    result=dbc.fetchonedb(sql,[changetypeid])
    if result:
        title=result[0]
        pic=result[1]
        webpic=result[2]
        score=result[3]
        num=result[4]
        if not num:
            num='0'
        numall=result[5]
        content=result[6]
        ord=result[7]
        closeflag=result[8]
        gmt_created=result[9]
        imgtpye=result[10]
    return render_to_response('mobile/addexchangetype.html',locals())

def upchangetype_close(request):
    is_ok=request.GET.get('is_ok')
    auto_id=request.GET.get('auto_id')
    if is_ok=='1':
        is_ok='0'
    else:
        is_ok='1'
    sql='update weixin_prize set closeflag=%s where id=%s'
    dbc.updatetodb(sql,[is_ok,auto_id])
    return HttpResponse('1')

def delexchangetype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    changetypeid=request.GET.get('changetypeid')
    sql='delete from weixin_prize where id=%s'
    dbc.updatetodb(sql,[changetypeid])
    return HttpResponseRedirect(request_url)

def addexchangetypeok(request):
    request_url=request.GET.get('request_url')
    title=request.GET.get('title')
    pic=request.GET.get('pic')
    webpic=request.GET.get('webpic')
    score=request.GET.get('score')
    num=request.GET.get('num')
    numall=request.GET.get('numall')
    content=request.GET.get('content')
    ord=request.GET.get('ord')
    imgtype=request.GET.get('imgtype')
    closeflag=request.GET.get('closeflag')
    changetypeid=request.GET.get('changetypeid')
    error=''
    errors='此处不能为空'
    if not title:
        error1=errors
        error=1
    if not score:
        error2=errors
        error=1
    if not num:
        error3=errors
        error=1
    if not numall:
        error4=errors
        error=1
    if not content:
        error5=errors
        error=1
    if error:
        return render_to_response('mobile/addexchangetype.html',locals())
    if ord:
        ord=int(ord)
    else:
        ord=50
    argument=[title,pic,webpic,score,num,numall,content,ord,closeflag,imgtype]
    if changetypeid:
        argument.append(changetypeid)
        sql='update weixin_prize set title=%s,pic=%s,webpic=%s,score=%s,num=%s,numall=%s,content=%s,ord=%s,closeflag=%s,type=%s where id=%s'
    else:
        gmt_created=datetime.datetime.now()
        sql='insert into weixin_prize(title,pic,webpic,score,num,numall,content,ord,closeflag,type,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        argument.append(gmt_created)
    dbc.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)
def paytype(request):
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    replylist=zzm.getpaytypelist(frompageCount,limitNum)
    listcount=0
    listall=replylist['list']
    listcount=replylist['count']
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
    return render_to_response('mobile/paytype.html',locals())

def addpaytype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    sublist=zzm.getpaytypelist(0,100,subid=0)
    return render_to_response('mobile/addpaytype.html',locals())
def updatepaytype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    paytypeid=request.GET.get('paytypeid')
    sublist=zzm.getpaytypelist(0,100,subid=0)
    sql='select name,fee,sortrank,subid from pay_wallettype where id=%s'
    result=zzm.dbc.fetchonedb(sql,[paytypeid])
    if result:
        name=result[0]
        fee=result[1]
        sortrank=result[2]
        subid=result[3]
        if subid!=0:
            subname=zzm.getftypename(subid)
    return render_to_response('mobile/addpaytype.html',locals())
def addpaytypeok(request):
    request_url=request.GET.get('request_url')
    name=request.GET.get('name')
    subid=request.GET.get('subid')
    fee=request.GET.get('fee')
    sortrank=request.GET.get('sortrank')
    paytypeid=request.GET.get('paytypeid')
    error=''
    errors='此处不能为空'
    if not name:
        error1=errors
        error=1
    if error:
        return render_to_response('mobile/addpaytype.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    argument=[name,fee,sortrank,subid]
    if paytypeid:
        argument.append(paytypeid)
        sql='update pay_wallettype set name=%s,fee=%s,sortrank=%s,subid=%s where id=%s'
    else:
        sql='insert into pay_wallettype(name,fee,sortrank,subid) values(%s,%s,%s,%s)'
    zzm.dbc.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)

def delpaytype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    paytypeid=request.GET.get('paytypeid')
    sql='delete from pay_wallettype where id=%s'
    zzm.dbc.updatetodb(sql,[paytypeid])
    return HttpResponseRedirect(request_url)

def report(request):
    gmtdate=request.GET.get('gmtdate')
    ischeck=request.GET.get('ischeck')
    account=request.GET.get('account')
    foraccount=request.GET.get('foraccount')
    if not ischeck:
        ischeck="0"
        ischeckname='未审核'
    if ischeck=='1':
        ischeckname='已审核'
    elif ischeck=='2':
        ischeckname='退回'
    searchlist={}
    if ischeck:
        searchlist['ischeck']=ischeck
    if account:
        searchlist['account']=account
    if foraccount:
        searchlist['foraccount']=foraccount
    searchurl=urllib.urlencode(searchlist)
    check_status=request.GET.get('check_status')
    report_id=request.GET.get('report_id')
    if check_status:
        sql='update pay_report set check_status=%s where id=%s'
        dbc.updatetodb(sql,[check_status,report_id])
    backfee=request.GET.get('backfee')
    if backfee:
        zzm.getbackfee(report_id,backfee=backfee)
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    reportlist=zzm.getreportlist(frompageCount,limitNum,ischeck,gmtdate,account=account,foraccount=foraccount)
    listcount=0
    listall=reportlist['list']
    listcount=reportlist['count']
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
    return render_to_response('mobile/report.html',locals())

def outfee(request):
    paytype=request.GET.get('type')
    paytypem=request.GET.get('paytypem')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    page=request.GET.get('page')
    paytypeid=request.GET.get('paytypeid')
    company_id=request.GET.get('company_id')
    company_name=request.GET.get('company_name')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    searchlist={}
    if paytype:
        searchlist['paytype']=paytype
        paytype=int(paytype)
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if account:
        searchlist['account']=account
    if mobile:
        searchlist['mobile']=mobile
    if company_id:
        searchlist['company_id']=company_id
    if company_name:
        searchlist['company_name']=company_name
        company_name=company_name.encode('utf-8')
    if paytypem:
        searchlist['paytypem']=paytypem
        paytypem=paytypem.encode('utf-8')
    if paytypeid:
        searchlist['paytypeid']=paytypeid
        paytypename=zzm.getftypename(paytypeid)
    searchurl=urllib.urlencode(searchlist)
    paytypelist=zzm.getpaytypelist(paytype=paytype)['list']
    paytypemlist=zzm.getpaytypemlist()
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    outfeelist=zzm.getoutfeelist(frompageCount=frompageCount,limitNum=limitNum,type=paytype,gmt_begin=gmt_begin,gmt_end=gmt_end,paytypeid=paytypeid,company_id=company_id,company_name=company_name,account=account,mobile=mobile,paytypem=paytypem)
    listcount=0
    listall=outfeelist['list']
    listcount=outfeelist['count']
    sumfee=outfeelist['sumfee']
    pcount=outfeelist['pcount']
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
    return render_to_response('mobile/outfee.html',locals())

def addchongzhi(request):
    company_id=request.GET.get('company_id')
    account=zzm.getcompanyaccount(company_id)
    request_url=request.META.get('HTTP_REFERER','/')
    paytypelist=zzm.getpaytypelist()['list']
    paytypemlist=zzm.getpaytypemlist()
    error1='账号和手机号任意填写一项'
    return render_to_response('mobile/addchongzhi.html',locals())

def addchongzhiok(request):
    request_url=request.GET.get('request_url')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    ftype=request.GET.get('ftype')
    fee=request.GET.get('fee')
    paywid=request.GET.get('paywid')
    payfrom=request.GET.get('payfrom')
    paytype=request.GET.get('paytype')
    bz=request.GET.get('bz')
    error=''
    errors='此处不能为空'
    if not account and not mobile:
        error1='账号和手机号任意填写一项'
        error=1
    if not fee:
        error2=errors
        error=1
    if error:
        paytypelist=zzm.getpaytypelist()['list']
        return render_to_response('mobile/addchongzhi.html',locals())
    gmt_date=datetime.date.today()
    gmt_created=datetime.datetime.now()
    company_id=zzm.getcompany_id(account,mobile)
    if paywid:
        argument=[]
        argument=[company_id,fee,ftype,gmt_created,paywid,paytype,payfrom]
        sql='update pay_mobileWallet set company_id=%s,fee=%s,ftype=%s,gmt_modified=%s,paytype=%s,payfrom=%s,bz=%s where id=%s'
    else:
        argument=[company_id,fee,ftype,gmt_date,gmt_created,gmt_created,paytype,payfrom,bz]
        sql='insert into pay_mobileWallet(company_id,fee,ftype,gmt_date,gmt_created,gmt_modified,paytype,payfrom,bz) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    zzm.dbc.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)

def chongzhichart(request):
    paytypelist=zzm.getpaytypelist()['list']
    ftype=request.GET.get('ftype')
    if not ftype:
        ftype=5
    ftypename=zzm.getftypename(ftype)
    return render_to_response('mobile/chongzhichart.html',locals())

def sunfeechart(request):
    sqlarg=''
    argument=[]
    datall=request.GET.get('datall')
    if ',' in datall:
        datallist=datall.split(',')
        ftype=datallist[0]
        #ftype="49,50,51,5"
        gmt_begin=datallist[1]
        gmt_end=datallist[2]
        argument=[ftype,gmt_begin,gmt_end]
        sqlarg+=' and gmt_date>=%s and gmt_date<=%s'
    else:
        ftype=datall
        #ftype="49,50,51,5"
        argument=[ftype]
    sql='select sum(fee) from pay_mobileWallet where ftype in (%s)'+sqlarg
    result=dbc.fetchnumberdb(sql,argument)
    return HttpResponse(str(result))

def chongzhicharturl(request):
    gmt_begin=''
    gmt_end=''
    datall=request.GET.get('datall')
    if ',' in datall:
        datallist=datall.split(',')
        ftype=datallist[0]
        gmt_begin=datallist[1]
        gmt_end=datallist[2]
    else:
        ftype=datall
#    ftype=request.GET.get('ftype')
#    gmt_begin=request.GET.get('datebegin')
#    gmt_end=request.GET.get('dateend')
    ftypename=zzm.getftypename(ftype)
    #ftype="49,50,51,5"
    chartinfeelist=zzm.getchartinfee(ftype=ftype,gmt_begin=gmt_begin,gmt_end=gmt_end)
    return render_to_response('mobile/chongzhicharturl.html',locals())

def blance(request):
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    page=request.GET.get('page')
    paytypeid=request.GET.get('paytypeid')
    company_name=request.GET.get('company_name')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    order=request.GET.get('order')
    searchlist={}
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if paytypeid:
        paytypename=zzm.getftypename(paytypeid)
        searchlist['paytypeid']=paytypeid
    if company_name:
        searchlist['company_name']=company_name
        company_name=company_name.encode('utf-8')
    if account:
        searchlist['account']=account
    if mobile:
        searchlist['mobile']=mobile
    searchurl=urllib.urlencode(searchlist)
    paytypelist=zzm.getpaytypelist()['list']
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    baoblancelist=zzm.qianbaoblancelist(frompageCount=frompageCount,limitNum=limitNum,gmt_begin=gmt_begin,gmt_end=gmt_end,paytypeid=paytypeid,company_name=company_name,account=account,mobile=mobile,order=order)
    listcount=0
    listall=baoblancelist['list']
    listcount=baoblancelist['count']
    countin=baoblancelist['countin']
    countall=baoblancelist['countall']
#    sumfee=outfeelist['sumfee']
#    pcount=outfeelist['pcount']
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
    return render_to_response('mobile/blance.html',locals())
def getcompanyid(request):
    tourl=request.GET.get('tourl')
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('mobile/shop/getcompanyid.html',locals())
def getfromaccounttocompanyid(request):
    request_url=request.META.get('HTTP_REFERER','/')
    account=request.GET.get('account')
    tourl=request.GET.get('tourl')
    if account:
        sql="select company_id from company_account where account=%s"
        result=dbc.fetchonedb(sql,[account])
        company_id=0
        if result:
            company_id=result[0]
        else:
            return HttpResponse("无此账号："+str(account))
    else:
        return render_to_response('mobile/shop/getcompanyid.html',locals())
    return HttpResponseRedirect(tourl+"&company_id="+str(company_id)+"&account="+str(account))
def addshop_product(request):
    account=request.GET.get('account')
    company_id=request.GET.get('company_id')
    #request_url=request.META.get('HTTP_REFERER','/')
    request_url="shop_product.html?paytype=11"
    return render_to_response('mobile/shop/addshop_product.html',locals())
def addshop_reflush(request):
    #request_url=request.META.get('HTTP_REFERER','/')
    request_url="shop_product.html?paytype=42"
    account=request.GET.get('account')
    company_id=request.GET.get('company_id')
    return render_to_response('mobile/shop/addshop_reflush.html',locals())
def delshop_product(request):
    request_url=request.META.get('HTTP_REFERER','/')
    sid=request.GET.get('sid')
    sql='delete from shop_showphone where id=%s'
    dbc.updatetodb(sql,[sid])
    return HttpResponseRedirect(request_url)
def delshop_reflush(request):
    request_url=request.META.get('HTTP_REFERER','/')
    sid=request.GET.get('sid')
    sql='delete from shop_reflush where id=%s'
    dbc.updatetodb(sql,[sid])
    return HttpResponseRedirect(request_url)
def updateshop_product(request):
    request_url=request.META.get('HTTP_REFERER','/')
    sid=request.GET.get('sid')
    sql='select company_id,gmt_begin,gmt_end from shop_showphone where id=%s'
    result=dbc.fetchonedb(sql,sid)
    if result:
        company_id=result[0]
        start_time=formattime(result[1])
        timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if not start_time:
            start_time=timenow
        end_time=formattime(result[2])
        if not end_time:
            end_time=timenow
    return render_to_response('mobile/shop/addshop_product.html',locals())
def updateshop_reflush(request):
    request_url=request.META.get('HTTP_REFERER','/')
    sid=request.GET.get('sid')
    sql='select company_id,gmt_begin,gmt_end from shop_reflush where id=%s'
    result=dbc.fetchonedb(sql,sid)
    if result:
        company_id=result[0]
        start_time=formattime(result[1])
        timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if not start_time:
            start_time=timenow
        end_time=formattime(result[2])
        if not end_time:
            end_time=timenow
    return render_to_response('mobile/shop/addshop_reflush.html',locals())
def addshop_productok(request):
    request_url=request.GET.get('request_url')
    company_id=request.GET.get('company_id')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sid=request.GET.get('sid')
    error=''
    errors='此处不能为空'
    if not company_id:
        error1=errors
        error=1
    if not gmt_begin:
        error2=errors
        error=2
    if not gmt_end:
        error3=errors
        error=3
    if error:
        return render_to_response('mobile/shop/addshop_product.html',locals())
    argument=[company_id,gmt_begin,gmt_end]
    if sid:
        argument.append(sid)
        sql='update shop_showphone set company_id=%s,gmt_begin=%s,gmt_end=%s where id=%s'
    else:
        argument.append(timenow)
        sql='insert into shop_showphone(company_id,gmt_begin,gmt_end,gmt_created) values(%s,%s,%s,%s)'
    dbc.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)
def addshop_reflushok(request):
    request_url=request.GET.get('request_url')
    company_id=request.GET.get('company_id')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sid=request.GET.get('sid')
    error=''
    errors='此处不能为空'
    if not company_id:
        error1=errors
        error=1
    if not gmt_begin:
        error2=errors
        error=2
    if not gmt_end:
        error3=errors
        error=3
    if error:
        return render_to_response('mobile/shop/addshop_reflush.html',locals())
    argument=[company_id,gmt_begin,gmt_end]
    if sid:
        argument.append(sid)
        sql='update shop_reflush set company_id=%s,gmt_begin=%s,gmt_end=%s where id=%s'
    else:
        argument.append(timenow)
        sql='insert into shop_reflush(company_id,gmt_begin,gmt_end,gmt_created) values(%s,%s,%s,%s)'
    dbc.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)
def shop_product(request):
    page=request.GET.get('page')
    paytype=request.GET.get('paytype')
    is_checked=request.GET.get('is_checked')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    keywords=request.GET.get('keywords')
    searchlist={}
    if paytype:
        searchlist['paytype']=paytype
        paytypename=zzm.getftypename(paytype)
    if is_checked:
        searchlist['is_checked']=is_checked
        if is_checked=='0':
            check_name="未审核"
        if is_checked=='1':
            check_name="已审核"
        if is_checked=='2':
            check_name="交易关闭"
    if account:
        searchlist['account']=account
    if mobile:
        searchlist['mobile']=mobile
    if keywords:
        searchlist['keywords']=keywords
    
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if paytype=='9':
        shop_productlist=zzms.getshop_product_ranklist(frompageCount=frompageCount,limitNum=limitNum,paytype='10431004',is_checked=is_checked,account=account,mobile=mobile,keywords=keywords)
    else: 
        shop_productlist=zzms.getshop_productlist(frompageCount=frompageCount,limitNum=limitNum,account=account,mobile=mobile)
    if paytype=="42":
        shop_productlist=zzms.getshop_reflushlist(frompageCount=frompageCount,limitNum=limitNum,account=account,mobile=mobile)
    listcount=0
    listall=shop_productlist['list']
    listcount=shop_productlist['count']
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
    if paytype=='42':
        return render_to_response('mobile/shop/shop_reflush.html',locals())
    if paytype=='9':
        return render_to_response('mobile/shop/shop_product_rank.html',locals())
    else:
        return render_to_response('mobile/shop/shop_showphone.html',locals())
def shop_baoming(request):
    page=request.GET.get('page')
    paytype=request.GET.get('paytype')
    searchlist={}
    if paytype:
        searchlist['paytype']=paytype
    else:
        paytype=16
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    shop_baoming=zzms.getshop_baoming(frompageCount=frompageCount,limitNum=limitNum,paytype=paytype)
    listcount=0
    listall=shop_baoming['list']
    listcount=shop_baoming['count']
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
    return render_to_response('mobile/shop/shop_baoming.html',locals())
def update_prorank(request):
    request_url=request.META.get('HTTP_REFERER','/')
    prorankid=request.GET.get('prorankid')
    sql='select product_id,name,start_time,end_time,is_checked,gmt_modified,company_id,apply_account,buy_time from products_keywords_rank where id=%s'
    result=dbc.fetchonedb(sql,prorankid)
    if result:
        pro_id=result[0]
        pro_title=zzm.getproduct_title(pro_id)
        name=result[1]
        start_time=formattime(result[2])
        timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if not start_time:
            start_time=timenow
        end_time=formattime(result[3])
        if not end_time:
            end_time=timenow
        is_checked=result[4]
        checklist2=getoptionlist(int(is_checked),['未审核','已审核','交易关闭'])
        gmt_modified=formattime(result[5])
        company_id=result[6]
        company_name=zzm.getcompany_name(company_id)
        company_account=result[7]
        buy_time=formattime(result[8])
    return render_to_response('mobile/shop/update_prorank.html',locals())
def update_prorankok(request):
    request_url=request.GET.get('request_url')
    prorankid=request.GET.get('prorankid')
    if prorankid:
        is_checked=request.GET.get('is_checked')
        name=request.GET.get('name')
        start_time=request.GET.get('start_time')
        end_time=request.GET.get('end_time')
        sql='update products_keywords_rank set is_checked=%s,name=%s,start_time=%s,end_time=%s where id=%s'
        dbc.updatetodb(sql,[is_checked,name,start_time,end_time,prorankid])
        return HttpResponseRedirect(request_url)
def del_prorank(request):
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
def delshop_product_wxtg(request):
    request_url=request.META.get('HTTP_REFERER','/')
    shoproid=request.GET.get('shoproid')
    if shoproid:
        sql='delete from shop_product_wxtg where id=%s'
        dbc.updatetodb(sql,shoproid)
    return HttpResponseRedirect(request_url)
def upshop_product2(request):
    is_ok=request.GET.get('is_ok')
    auto_id=request.GET.get('auto_id')
    if is_ok=='1':
        is_ok='0'
    else:
        is_ok='1'
    sql='update shop_product_wxtg set is_check=%s where id=%s'
    dbc.updatetodb(sql,[is_ok,auto_id])
    return HttpResponse('1')

#砍价产品
def kanjia_prolist(request):
    sql="select name,price,number,lastprice,cut_price,end_time,havenumber,id from subject_kanjia_pro"
    result=dbc.fetchalldb(sql)
    listall=[]
    if result:
        for list in result:
            #0元剩余名额
            number=list[2]
            sqlc="select count(0) from subject_kanjia_baoming where pro_id=%s and price_now<=0"
            resultc=dbc.fetchonedb(sqlc,[list[7]])
            xbcount=resultc[0]
            havenumber=int(number)-xbcount
            
            sqlc="select count(0) from subject_kanjia_baoming where pro_id=%s"
            resultc=dbc.fetchonedb(sqlc,[list[7]])
            bcount=resultc[0]
            
            l={'id':list[7],'name':list[0],'price':list[1],'number':list[2],'lastprice':list[3],'cut_price':list[4],'end_time':formattime(list[5],1),'havenumber':havenumber,'bcount':bcount}
            listall.append(l)
    return render_to_response('mobile/kanjia/index.html',locals())

#砍价报名表
def kanjia_baoming(request):
    page=request.GET.get('page')
    pro_id=request.GET.get('pro_id')
    searchlist={}
    if pro_id:
        searchlist['pro_id']=pro_id
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    kanjiabaoming=zzm.getkanjiabaoming(frompageCount=frompageCount,limitNum=limitNum,pro_id=pro_id)
    listcount=0
    listall=kanjiabaoming['list']
    listcount=kanjiabaoming['count']
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
    return render_to_response('mobile/kanjia/baoming.html',locals())
#砍价历史
def kanjia_history(request):
    page=request.GET.get('page')
    baoming_id=request.GET.get('baoming_id')
    searchlist={}
    if baoming_id:
        searchlist['baoming_id']=baoming_id
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    kanjiabaoming=zzm.getkanjiacutlist(frompageCount=frompageCount,limitNum=limitNum,baoming_id=baoming_id)
    listcount=0
    listall=kanjiabaoming['list']
    listcount=kanjiabaoming['count']
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
    return render_to_response('mobile/kanjia/history.html',locals())
