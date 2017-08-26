#-*- coding:utf-8 -*-
class newsource:
    def __init__(self):
        self.dbo=dbo
    def getsource_type(self):
        sql=''
    def getsource_list(self):
        sql=''

class zz91news:
    def __init__ (self):
        self.dbn=dbn
    def delnews(self,id):
        #sql='delete from dede_arctiny where id=%s'
        #self.dbn.updatetodb(sql,[id])
        cl = SphinxClient()
        cl.SetServer ( "search.zz91server.com", 9317 )
        dellist={}
        sql="insert into dede_archives_1 select * from dede_archives where id=%s and not exists(select id from dede_archives_1 where id=dede_archives.id)"
        self.dbn.updatetodb(sql,[id])
        sql='delete from dede_archives where id=%s'
        self.dbn.updatetodb(sql,[id])
        res = cl.UpdateAttributes ( 'news', [ 'deleted' ], {int(id):[1]} )
        #sql='delete from dede_addonarticle where aid=%s'
        #self.dbn.updatetodb(sql,[id])
    def delnewstype(self,id):
        sql='delete from dede_arctype where id=%s'
        self.dbn.updatetodb(sql,id)
    def updatetype(self,typename,sortrank,typeid):
        sql='update dede_arctype set typename=%s,sortrank=%s where id=%s'
        self.dbn.updatetodb(sql,[typename,sortrank,typeid])
    def addtype(self,typename,sortrank,reid,topid):
        sql='insert into dede_arctype(typename,sortrank,reid,topid) values(%s,%s,%s,%s)'
        self.dbn.updatetodb(sql,[typename,sortrank,reid,topid])
    def updatenews(self,title,shorttitle,sortrank,litpic,click,writer,typeid,typeid2,body,redirecturl,id):
        sql='update dede_archives set title=%s,shorttitle=%s,sortrank=%s,litpic=%s,click=%s,writer=%s,typeid=%s,typeid2=%s where id=%s'
        self.dbn.updatetodb(sql,[title,shorttitle,sortrank,litpic,click,writer,typeid,typeid2,id])
        sql1='update dede_addonarticle set body=%s,redirecturl=%s where aid=%s'
        self.dbn.updatetodb(sql1,[body,redirecturl,id])
    def quickupdate(self,strattlist,title,keywords,shorttitle,id):
        sql='update dede_archives set flag=%s,title=%s,keywords=%s,shorttitle=%s where id=%s'
        self.dbn.updatetodb(sql,[strattlist,title,keywords,shorttitle,id])
    def addnews(self,title,shorttitle,litpic,click,writer,typeid,typeid2,body,pubdate,redirecturl):
        sortrank=int(time.time())
        sql='insert into dede_arctiny(typeid,typeid2,mid,senddate,sortrank) values(%s,%s,%s,%s,%s)'
        self.dbn.updatetodb(sql,[typeid,typeid2,1,sortrank,sortrank])
        sql2='select id from dede_arctiny where sortrank=%s'
        result=self.dbn.fetchonedb(sql2,sortrank)
        if result:
            id=result[0]
            sql3='insert into dede_archives(id,title,shorttitle,litpic,click,writer,typeid,typeid2,pubdate,sortrank) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.dbn.updatetodb(sql3,[id,title,shorttitle,litpic,click,writer,typeid,typeid2,pubdate,sortrank])
            sql4='insert into dede_addonarticle(aid,body,redirecturl) values(%s,%s,%s)'
            self.dbn.updatetodb(sql4,[id,body,redirecturl])
    
    #----资讯列表(搜索引擎)
    def getnewslist(self,SPHINXCONFIG,keywords="",frompageCount="",limitNum="",typeid="",typeid2="",allnum="",arg='',flag='',type='',MATCH=""):
#        if keywords:
#            keywords=keywords.upper()
#        if '%' in keywords:
#            keywords=keywords.replace('%','%%')
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        if MATCH!="":
            cl.SetMatchMode ( SPH_MATCH_ANY )
        else:
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if (typeid):
            cl.SetFilter('typeid',typeid)
        if (typeid2):
            cl.SetFilter('typeid2',[typeid2])
        cl.SetFilter('typeid',[235,184],True)
        if MATCH!="":
            cl.SetSortMode( SPH_SORT_EXTENDED ,'@weight DESC,pubdate desc' )
        else:
            cl.SetSortMode( SPH_SORT_ATTR_DESC ,'pubdate' )
        if (allnum):
            cl.SetLimits (frompageCount,limitNum,allnum)
        else:
            cl.SetLimits (frompageCount,limitNum)
        if (keywords):
            if flag:
                res = cl.Query ('@(title,description) '+keywords+'&@(flag) "p"','news')
            else:
                if arg==1:
                    res = cl.Query ('@(title,description) '+keywords,'news')
                else:
                    res = cl.Query ('@(title) '+keywords,'news')
        else:
            if flag:
                res = cl.Query ('@(flag) "p"','news')
            else:
                res = cl.Query ('','news')
        listall_news=[]
        listcount_news=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    subcontent=self.getsubcontent(id,20)
                    newsurl=self.get_newstype(id)
                    weburl="http://news.zz91.com"
                    if newsurl:
                        if newsurl["url2"]:
                            weburl+="/"+newsurl["url2"]
                        weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                    attrs=match['attrs']
                    title=attrs['ptitle']
#                    if re.findall('^[A-Z]+',keywords):
#                    else:
#                        title=re.sub(keywords,'<font color="red">'+keywords+'</font>',title)
                    click=attrs['click']
                    pubdate=attrs['pubdate']
                    pic=attrs['litpic']
                    if pic!="" and pic:
                        litpic="http://news.zz91.com/" +pic
                    else: 
                        litpic="http://img0.zz91.com/front/images/global/noimage.gif"
                    #litpic=''
                    pubdate2=time.strftime('%Y-%m-%d', time.localtime(pubdate))
                    list1={'title':title,'click':click,'id':id,'pubdate':pubdate2,'weburl':weburl,'litpic':litpic,'subcontent':subcontent}
                    if type:
                        if keywords in title or arg==1 or arg==2:
                            listall_news.append(list1)
                            title=search_strong(keywords,title)
                            list1['title']=title
                    else:
                        listall_news.append(list1)
                    if limitNum==1:
                        return list1
                listcount_news=res['total_found']
        return {'list':listall_news,'count':listcount_news}
    def getsubcontent(self,id,len):
        sql='select description from dede_archives where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            body=result[0]
            return body[:len]
        
    #----获取资讯url
    def get_newstype(self,id):
        sql='select typeid,typeid2 from dede_archives where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            typeid=result[0]
            typeid2=result[1]
            sql2='select typename,keywords from dede_arctype where id=%s'
            result2=self.dbn.fetchonedb(sql2,[typeid])
            if result2:
                list={'typename':result2[0],'url':result2[1],'typeid':typeid,'typeid2':typeid2,'url2':'','typename2':''}
                if typeid2!='0':
                    sql3='select keywords,typename from dede_arctype where id=%s'
                    result3=self.dbn.fetchonedb(sql3,[typeid2])
                    if result3:
                        list['url2']=result3[0]
                        list['typename2']=result3[1]
                return list
    def get_typetags(self,url):
        sql1='select typename from dede_arctype where keywords=%s'
        result=self.dbn.fetchonedb(sql1,[url])
        listall=[]
        if result:
            keywords=result[0]
            sql='select id,typename from dede_arctype where keywords=%s'
            resultlist=self.dbn.fetchalldb(sql,[keywords])
            if resultlist:
                for result in resultlist:
                    typename=result[1]
                    list={'id':result[0],'typename':typename,'typename_hex':getjiami(typename),}
                    listall.append(list)
        return listall

    def gettypelist(self):
        listall=[]
        sql='select id,typename,sortrank from dede_arctype where topid=0 order by sortrank,id desc'
        resultlist=self.dbn.fetchalldb(sql)
        if resultlist:
            for result in resultlist:
                id=result[0]
                nexttype=self.getnexttype(id)
                typename=result[1]
                sortrank=result[2]
                list={'id':result[0],'typename':typename,'sortrank':sortrank,'nexttype':nexttype}
                listall.append(list)
        return {'list':listall}
    def getnexttype(self,reid):
        listall=[]
        sql='select id,typename,sortrank from dede_arctype where reid=%s order by sortrank'
        resultlist=self.dbn.fetchalldb(sql,[reid])
        if resultlist:
            for result in resultlist:
                typename=result[1]
                sortrank=result[2]
                list={'id':result[0],'typename':typename,'sortrank':sortrank}
                listall.append(list)
        return listall
    def gettypedetail(self,id):
        sql='select id,typename,sortrank from dede_arctype where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            list={'id':result[0],'typename':result[1],'sortrank':result[2]}
            return list
    #----资讯列表(数据库)
    def get_news_all(self,frompageCount,limitNum,pubdate='',pubdate2='',writer='',flag='',title='',typeid='',typeid2='',isdel=""):
        argument=[]
        if isdel:
            sql1='select count(0) from dede_archives_1 where id>0'
            sql='select id,title,pubdate,click,writer,flag,shorttitle,keywords from dede_archives_1 where id>0'
        else:
            sql1='select count(0) from dede_archives where id>0'
            sql='select id,title,pubdate,click,writer,flag,shorttitle,keywords from dede_archives where id>0'
        if pubdate:
            argument.append(pubdate)
            sql1=sql1+' and pubdate>=%s'
            sql=sql+' and pubdate>=%s'
        if pubdate2:
            argument.append(pubdate2)
            sql1=sql1+' and pubdate<=%s'
            sql=sql+' and pubdate<=%s'
        if writer:
            argument.append(writer)
            sql1=sql1+' and writer=%s'
            sql=sql+' and writer=%s'
        if flag:
            argument.append(flag)
            sql1=sql1+' and find_in_set(%s,flag)'
            sql=sql+' and find_in_set(%s,flag)'
        if typeid:
#            argument.append(typeid)
            sql1=sql1+' and typeid='+typeid
            sql=sql+' and typeid='+typeid
        if typeid2:
#            argument.append(typeid)
            sql1=sql1+' and typeid2='+typeid2
            sql=sql+' and typeid2='+typeid2
        if title:
#            argument.append(title)
            sql1=sql1+' and title like "%'+title+'%"'
            sql=sql+' and title like "%'+title+'%"'
        sql=sql+' order by id desc'
        if limitNum:
            sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        result1=self.dbn.fetchonedb(sql1,argument)
        if result1:
            count=result1[0]
        else:
            count=0
        resultlist=self.dbn.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            js=0
            for result in resultlist:
                id=result[0]
                title=result[1]
                intdate=result[2]
                click=result[3]
                writer=result[4]
                flag=result[5]
                shorttitle=result[6]
                keywords=result[7]
                if flag:
                    flaglist=flag.split(',')
                    flagnamestr=''
                    for fl in flaglist:
                        flagname=self.getflagname(fl)
                        flagnamestr=flagnamestr+' '+flagname
                pubdate=int_to_str(intdate)
                newsurl=self.get_newstype(id)
                weburl="http://news.zz91.com"
                typeid=''
                typeid2=''
                typename=''
                typename2=''
                if newsurl:
                    typeid=newsurl['typeid']
                    typename=newsurl['typename']
                    typeid2=newsurl['typeid2']
                    if newsurl["url2"]:
                        typename2=newsurl['typename2']
                        weburl+="/"+newsurl["url2"]
                    weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                list={'id':id,'intdate':intdate,'pubdate':pubdate,'title':title,'weburl':weburl,'click':click,'writer':writer,'flaglist':'','flagnamestr':'','js':js,'typeid':typeid,'typeid2':typeid2,'typename':typename,'typename2':typename2,'shorttitle':shorttitle,'keywords':keywords}
                if flag:
                    list['flaglist']=flaglist
                    list['flagnamestr']=flagnamestr
                listall.append(list)
                js=js+1
        return {'list':listall,'count':count,'sql':sql}
    def getattlist(self):
        sql='select sortid,att,attname from dede_arcatt order by sortid'
        resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'att':result[1],'attname':result[2]}
                listall.append(list)
        return listall
    def getflagname(self,att):
        sql='select attname from dede_arcatt where att=%s'
        result=self.dbn.fetchonedb(sql,att)
        if result:
            return result[0]
    def getnewsdetail(self,id):
        sql='select body,redirecturl from dede_addonarticle where aid=%s'
        result1=self.dbn.fetchonedb(sql,id)
        if result1:
            body=result1[0]
            redirecturl=result1[1]
        else:
            return ''
        sql='select title,typeid,typeid2,flag,litpic,writer,click,shorttitle from dede_archives where id=%s'
        result=self.dbn.fetchonedb(sql,id)
        if result:
            title=result[0]
            typeid=result[1]
            typename=self.gettypename(typeid)
            typeid2=result[2]
            typename2=''
            if typeid2!='0':
                typename2=self.gettypename(typeid2)
            flag=result[3]
            litpic=result[4]
            writer=result[5]
            click=result[6]
            shorttitle=result[7]
            list={'body':body,'redirecturl':redirecturl,'title':title,'typeid':typeid,'typename':typename,'typeid2':typeid2,'typename2':typename2,'flag':flag,'litpic':litpic,'writer':writer,'click':click,'shorttitle':shorttitle}
            return list
    def gettypename(self,id):
        if id:
            sql='select typename from dede_arctype where id=%s'
            result=self.dbn.fetchonedb(sql,[id])
            if result:
                return result[0]
        
    #zz91一键删除
    def delallzz91(self,checkid):
        cl = SphinxClient()
        cl.SetServer ( "search.zz91server.com", 9317 )
        dellist={}
        for id in checkid:
            #sql1="delete from dede_arctiny where id=%s"
            #self.dbn.updatetodb(sql1,[id])
            sql="insert into dede_archives_1 select * from dede_archives where id=%s and not exists(select id from dede_archives_1 where id=dede_archives.id)"
            self.dbn.updatetodb(sql,[id])
            sql2="delete from dede_archives where id=%s"
            self.dbn.updatetodb(sql2,[id])
            dellist.update({int(id):[1]})
            #sql3="delete from dede_addonarticle where aid=%s"
            #self.dbn.updatetodb(sql3,[id])
            res = cl.UpdateAttributes ( 'news', [ 'deleted' ], {int(id):[1]} )
        return res
    #zz91一键恢复
    def backallnews(self,checkid):
        cl = SphinxClient()
        cl.SetServer ( "search.zz91server.com", 9317 )
        dellist={}
        for id in checkid:
            sql="insert into dede_archives select * from dede_archives_1 where id=%s and not exists(select id from dede_archives where id=dede_archives_1.id)"
            self.dbn.updatetodb(sql,[id])
            sql2="delete from dede_archives_1 where id=%s"
            self.dbn.updatetodb(sql2,[id])
            dellist.update({int(id):[0]})
            res = cl.UpdateAttributes ( 'news', [ 'deleted' ], {int(id):[0]} )
        return
    
        