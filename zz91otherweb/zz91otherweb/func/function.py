#-*- coding:utf-8 -*-
#----栏目读取
class tylelist():
    def __init__(self):
        self._reid = 0
        self._wtype=1
    def gettylelist(self,wtype=1,reid=0):
        sql="select id,typename,sortrank from webtype where wtype=%s,reid=%s"
        cursor.execute(sql,[wtype,reid])
        returnlist=cursor.fetchall()

#----获得栏目列表
def getwebtypelist(frompageCount,limitNum,reid='',wtype=''):
    sql1='select count(0) from webtype'
    if reid:
        sql1=sql1+' where reid='+reid
    else:
        sql1=sql1+' where wtype='+str(wtype)
    count=fetchnumberdb(sql1,cursor)
    listall=[]
    sql='select id,typename,sortrank from webtype'
    if reid:
        sql=sql+' where reid='+reid
    else:
        sql=sql+' where wtype='+str(wtype)
    sql=sql+' order by sortrank,id desc limit '+str(frompageCount)+','+str(limitNum)
    resultlist=fetchalldb(sql,cursor)
    if resultlist:
        for result in resultlist:
            id=result[0]
            nexttype=getnexttype(id)
            if nexttype:
                has_son=1
            else:
                has_son=0
            websitelist=getwebsitelist(0,7,'',id)
            listweb=[]
            if websitelist:
                listweb=websitelist['list']
            list={'id':id,'typename':result[1],'sortrank':result[2],'websitelist':listweb,'has_son':has_son}
            listall.append(list)
    return {'list':listall,'count':count}

def getindextypelist(wtype):
    listall=[]
    sql='select id,typename from webtype where wtype='+str(wtype)
    resultlist=fetchalldb(sql,cursor)
    if resultlist:
        for result in resultlist:
            listall2=[]
            id=result[0]
            resultlist2=getnexttype(id)
            list={'id':id,'typename':result[1],'typelist':resultlist2}
            if listall2:
                list['typelist']=listall2
            listall.append(list)
    return listall

def getpage404list(frompageCount,limitNum,wtype=''):
    sql1='select count(0) from page404'
    if wtype:
        sql1=sql1+' where wtype='+str(wtype)
    count=fetchnumberdb(sql1,cursor)
    listall=[]
    sql='select id,url,wtype from page404'
    if wtype:
        sql=sql+' where wtype='+str(wtype)
    sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
    resultlist=fetchalldb(sql,cursor)
    if resultlist:
        for result in resultlist:
            id=result[0]
            listweb=[]
            list={'id':id,'url':result[1],'wtype':result[2]}
            listall.append(list)
    return {'list':listall,'count':count}

def getalltypelist(wtype):
    listall=[]
    sql='select id,typename from webtype where wtype='+str(wtype)
    resultlist=fetchalldb(sql,cursor)
    if resultlist:
        for result in resultlist:
            listall2=[]
            id=result[0]
            resultlist2=getnexttype(id)
            if resultlist2:
                for result2 in resultlist2:
                    listall3=[]
                    id2=result2['id']
                    listall3=getnexttype(id2)
                    list2={'id':id2,'typename':result2['typename'],'typelist':''}
                    if listall3:
                        list2['typelist']=listall3
                    listall2.append(list2)
            list={'id':id,'typename':result[1],'typelist':''}
            if listall2:
                list['typelist']=listall2
            listall.append(list)
    return listall

#----根据栏目id查出下一级栏目
def getnexttype(typeid):
    listall=[]
    sql='select id,typename from webtype where reid='+str(typeid)
    resultlist=fetchalldb(sql,cursor)
    if resultlist:
        for result in resultlist:
            id=result[0]
            websitelist=getwebsitelist(0,7,'',id)
            listweb=[]
            if websitelist:
                listweb=websitelist['list']
            list={'id':id,'typename':result[1],'listweb':''}
            if listweb:
                list['listweb']=listweb
            listall.append(list)
    return listall

#----获得栏目详细内容
def gettypedetail(id):
    sql='select id,typename,sortrank,reid,topid from webtype where id=%s'
    result=fetchonedb(sql,cursor,[id])
    list={'id':'','typename':'','sortrank':'','retypename':'','toptypename':''}
    if result:
        reid=result[3]
        retypename=''
        if reid:
            retypename=gettypename(reid)
        topid=result[4]
        toptypename=''
        if topid:
            toptypename=gettypename(topid)
        list={'id':result[0],'typename':result[1],'sortrank':result[2],'retypename':retypename,'toptypename':toptypename}
    return list
def gettypename(id):
    sql='select typename from webtype where id=%s'
    result=fetchonedb(sql,cursor,[id])
    if result:
        return result[0]
def gettypeid(typename):
    sql='select id from webtype where typename=%s'
    result=fetchonedb(sql,cursor,[typename])
    if result:
        return result[0]
#----获得网站列表
def getwebsitelist(frompageCount,limitNum,recycle='',typeid='',recommend='',reid='',topid='',wtype='',title=''):
    nexttype=[]
    sql1='select count(a.id) from website as a left join webtype as b on a.typeid=b.id where a.isdelete=0'
    if recycle:
        sql1=sql1.replace('isdelete=0', 'isdelete=1')
    if typeid:
        sql1=sql1+' and (a.typeid='+str(typeid)
        sql1=sql1+' or b.topid='+str(typeid)
        sql1=sql1+' or b.reid='+str(typeid)+')'
    if wtype:
        sql1=sql1+' and a.wtype='+str(wtype)
    if title:
        sql1=sql1+u' and a.name like "%'+title+'%"'
    if recommend:
        sql1=sql1+' and a.recommend='+str(recommend)
    count=fetchnumberdb(sql1,cursor)
    listall=[]
    sql='select a.id,a.typeid,a.name,a.url,a.pic,a.gmt_created,a.sortrank,a.recommend,a.content from website as a left join webtype as b on a.typeid=b.id where a.isdelete=0'
    if recycle:
        sql=sql.replace('isdelete=0', 'isdelete=1')
    if typeid:
        sql=sql+' and (a.typeid='+str(typeid)
        sql=sql+' or b.topid='+str(typeid)
        sql=sql+' or b.reid='+str(typeid)+')'
    if wtype:
        sql=sql+' and a.wtype='+str(wtype)
    if title:
        sql=sql+u' and a.name like "%'+title+'%"'
    if recommend:
        sql=sql+' and a.recommend='+str(recommend)
    sql=sql+' order by sortrank,id desc limit '+str(frompageCount)+','+str(limitNum)
    resultlist=fetchalldb(sql,cursor)
    if resultlist:
        for result in resultlist:
            typeid1=result[1]
            typedetail=gettypedetail(typeid1)
            typename=typedetail['typename']
            retypename=typedetail['retypename']
            toptypename=typedetail['toptypename']
            url=result[3]
            shorturl=''
            if url:
                shorturl=url[:40]
            list={'id':result[0],'typeid':typeid1,'typename':typename,'retypename':retypename,'toptypename':toptypename,'name':result[2],'url':url,'shorturl':shorturl,'pic':result[4],'gmt_created':formattime(result[5],1),'sortrank':result[6],'recommend':result[7],'content':result[8]}
            listall.append(list)
    return {'list':listall,'count':count}
def getwebdetail(id):
    sql='select id,typeid,name,url,pic,gmt_created,sortrank,recommend,wtype,content from website where id=%s'
    result=fetchonedb(sql,cursor,[id])
    list=[]
    if result:
        typeid=result[1]
        typename=gettypename(typeid)
        list={'id':result[0],'typeid':typeid,'typename':typename,'name':result[2],'url':result[3],'pic':result[4],'gmt_created':formattime(result[5],1),'sortrank':result[6],'recommend':result[7],'wtype':result[8],'content':result[9]}
    return list