#-*- coding:utf-8 -*- 
from django.shortcuts import render_to_response
from settings import pyuploadpath,pyimgurl,spconfig
from django.http import HttpResponse,HttpResponseRedirect
import MySQLdb,re,random,time
import memcache
connother = MySQLdb.connect(host='192.168.110.2', user='zz91news', passwd='4ReLhW3QLyaaECzU',db='zz91weixin',charset='utf8')
cursorother=connother.cursor()
connothernews = MySQLdb.connect(host='192.168.110.2', user='zz91news', passwd='4ReLhW3QLyaaECzU',db='zz91news',charset='utf8')
cursorothernews=connothernews.cursor()
#mc2 = memcache.Client(['192.168.110.114:11211'],debug=0)
#connother = MySQLdb.connect(host='192.168.2.40', user='root', passwd='10534jun',db='zz91weixin',charset='utf8')
#cursorother=connother.cursor()
#connothernews = MySQLdb.connect(host='192.168.2.40', user='root', passwd='10534jun',db='zz91news',charset='utf8')
#cursorothernews=connothernews.cursor()
#随机出来的类型
type_list={'joke':'joke','job':'job','news':'news'}
#新闻最终页
def otherdetail(request,id=''):
    click_add(id)
    type=request.GET.get('type')
    luck_one=get_one_random(id,type)
    aboutnews=get_aboutnews(type)
    return render_to_response('order/otherdetail.html',locals())

#最终页相关阅读
def get_aboutnews(arg=''):
    typeid=''
    sql="select id,title from artical where typeid=%s order by id desc limit 0,5"
    if arg=='job':
        typeid=1
    if arg=='joke':
        typeid=2
    cursorother.execute(sql,[typeid])
    resultlist=cursorother.fetchall()
    listall=[]
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'title':result[1]}
            listall.append(list)
    return listall

#职场和笑话 视图
def jobjoke(request):

    luck_one=luckcheck("hhhh")

    return render_to_response('order/jobjoke.html',locals())
#职场和笑话 视图
def luckcheck(weixinid):
    time3d=int(time.time()-3600*24*3)
    #weixinid=request.session.get("weixinid",None)
    #templist=cache.get(weixinid)
    #if (templist==None):
    rand_list=get_id_random()
        #分别从各种类型里面获取一定数量的随机值,然后拼接起来,最后在获取一个随机值
        #cache.set(weixinid,rand_list,60*60*3)
    #else:
        #rand_list=templist
    one_random=rand_list[random.randint(1, len(rand_list)-1)]
    id=one_random['id']
    type=one_random['type']
    luck_one=get_one_random(id,type)
    return luck_one
#获得职场和笑话的随机值
def get_id_random():
    sql_joke="select id from artical where typeid=2 order by rand() limit 20"
    cursorother.execute(sql_joke)
    resultlist=cursorother.fetchall()
    listall=[]
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'type':'joke'}
            listall.append(list)
    sql_job="select id from artical where typeid=1 order by rand() limit 30"
    cursorother.execute(sql_job)
    resultlist=cursorother.fetchall()
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'type':'job'}
            listall.append(list)
    """
    sql_news='select id from dede_archives order by rand() limit 2'
    cursorothernews.execute(sql_news)
    resultlist=cursorothernews.fetchall()
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'type':'news'}
            listall.append(list)
    """
    return listall

#获取最后随机数的信息
def get_one_random(id,arg=''):
    if arg in ['joke','job']:
        sql="select id,title,body,flag,click,pubdate from artical where id=%s"
    if arg =='news':
        one_new=get_one_new(id)
        content=getreplacepic(one_new['body'])
        one_new['flag']=0
        one_new['body']=content
        return one_new
    cursorother.execute(sql,[id])
    result=cursorother.fetchone()
    if result:
        content=getreplacepic(result[2])
        list={'id':result[0],'title':result[1],'body':content,'flag':1,'type':arg,'click':result[4],'pubdate':timestamp_datetime(result[5])}
        flag=result[3]
        if flag in ['p','g'] and arg=='joke':
            list['p']='p'
        if arg=='job' or flag in ['a','t']:
            list['a']='a'
        return list

def getreplacepic(content):
    if content:
        co=content.replace("/uploads/uploads/media/","http://pyapp.zz91.com/app/changepic.html?height=300&width=300&url=http://newsimg.zz91.com/uploads/uploads/media/")
        return co

#日期格式转换(一期)
def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def get_one_result(sql,arg=''):
    cursorother.execute(sql)
    result=cursorother.fetchone()
    if result:
        return result
#职场列表
def get_list(sql,arg=''):
    cursorother.execute(sql)
    resultlist=cursorother.fetchall()
    if resultlist:
        listall=[]
        for result in resultlist:
            list={'id':result[0],'title':result[1],'body':result[2]}
            flag=result[3]
            if flag in ['p','g'] and arg=='joke':
                list['p']='p'
            if arg=='job' or flag in ['a','t']:
                list['a']='a'
            listall.append(list)
        return listall

#读一条新闻
def get_one_new(id):
    sql='select body from dede_addonarticle where aid=%s'
    cursorothernews.execute(sql,[id])
    resultlist=cursorothernews.fetchone()
    if resultlist:
        content=resultlist[0]
        sql='select id,title,pubdate,click,keywords from dede_archives where id=%s'
        cursorothernews.execute(sql,[id])
        result=cursorothernews.fetchone()
        if result:
            pubdate=timestamp_datetime(result[2])
            list={'id':result[0],'title':result[1],'pubdate':pubdate,'click':result[3],'body':content,'a':'a','news':1}
            return list
#时间戳转为正常时间
def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def click_add(id):
    sql="update artical set click=click+1 where id=%s"
    cursorother.execute(sql,[id])
    connother.commit()
    