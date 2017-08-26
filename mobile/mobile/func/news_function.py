#-*- coding:utf-8 -*-
class zz91news:
    def __init__ (self):
        self.dbn=dbn
    #获得新闻栏目id列表
    def getcolumnid(self):
        sql='select id,typename,keywords from dede_arctype where reid=184 order by sortrank limit 0,20'
        resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            listall.append(result[0])
        return listall
    def delnews(self,id):
        sql='delete from dede_arctiny where id=%s'
        self.dbn.updatetodb(sql,id)
        sql='delete from dede_archives where id=%s'
        self.dbn.updatetodb(sql,id)
        sql='delete from dede_addonarticle where aid=%s'
        self.dbn.updatetodb(sql,id)
    def delnewstype(self,id):
        sql='delete from dede_arctype where id=%s'
        self.dbn.updatetodb(sql,id)
    def updatetype(self,typename,sortrank,typeid):
        sql='update dede_arctype set typename=%s,sortrank=%s where id=%s'
        self.dbn.updatetodb(sql,[typename,sortrank,typeid])
    def addtype(self,typename,sortrank,reid,topid):
        sql='insert into dede_arctype(typename,sortrank,reid,topid) values(%s,%s,%s,%s)'
        self.dbn.updatetodb(sql,[typename,sortrank,reid,topid])
    def updatenews(self,title,shorttitle,litpic,click,writer,typeid,typeid2,body,id):
        sql='update dede_archives set title=%s,shorttitle=%s,litpic=%s,click=%s,writer=%s,typeid=%s,typeid2=%s where id=%s'
        self.dbn.updatetodb(sql,[title,shorttitle,litpic,click,writer,typeid,typeid2,id])
        sql1='update dede_addonarticle set body=%s where aid=%s'
        self.dbn.updatetodb(sql1,[body,id])
    def quickupdate(self,strattlist,title,keywords,shorttitle,id):
        sql='update dede_archives set flag=%s,title=%s,keywords=%s,shorttitle=%s where id=%s'
        self.dbn.updatetodb(sql,[strattlist,title,keywords,shorttitle,id])
    def addnews(self,title,shorttitle,litpic,click,writer,typeid,typeid2,body,pubdate):
        sortrank=int(time.time())
        sql='insert into dede_arctiny(typeid,typeid2,mid,senddate,sortrank) values(%s,%s,%s,%s,%s)'
        self.dbn.updatetodb(sql,[typeid,typeid2,1,sortrank,sortrank])
        sql2='select id from dede_arctiny where sortrank=%s'
        result=self.dbn.fetchonedb(sql2,sortrank)
        if result:
            id=result[0]
            sql3='insert into dede_archives(id,title,shorttitle,litpic,click,writer,typeid,typeid2,pubdate,sortrank) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.dbn.updatetodb(sql3,[id,title,shorttitle,litpic,click,writer,typeid,typeid2,pubdate,sortrank])
            sql4='insert into dede_addonarticle(aid,body) values(%s,%s)'
            self.dbn.updatetodb(sql4,[id,body])
    
    #----资讯列表(搜索引擎)
    def getnewslist(self,keywords="",frompageCount="",limitNum="",typeid="",typeid2="",allnum="",arg='',flag='',type='',MATCH="",num="",has_txt="",sortby='',company_id='',hot=''):
#        if keywords:
#            keywords=keywords.upper()
#        if '%' in keywords:
#            keywords=keywords.replace('%','%%')
        news=SPHINXCONFIG['name']['news']['name']
        serverid=SPHINXCONFIG['name']['news']['serverid']
        port=SPHINXCONFIG['name']['news']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        if MATCH!="":
            cl.SetMatchMode ( SPH_MATCH_ANY )
        else:
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetFilter('typeid',[392],exclude=1)
        if company_id:
            #我的关注
            myguanzhu=self.getmyguanzhu(company_id)
            if myguanzhu:
                typeid=[]
                for l in myguanzhu:
                    typeid.append(l['typeid'])
                cl.SetFilter('typeid',typeid)
            else:
                if typeid:
                    cl.SetFilter('typeid',typeid)
                if typeid2 and typeid2!="" and typeid2!=[]:
                    cl.SetFilter('typeid2',typeid2)
                flag=1
                cl.SetSortMode( SPH_SORT_EXTENDED ,"click desc" )
        else:
            if typeid:
                cl.SetFilter('typeid',typeid)
            if typeid2 and typeid2!="" and typeid2!=[]:
                cl.SetFilter('typeid2',typeid2)
        cl.SetFilter('deleted',[0])
        if hot:
            #一个月内容的热门资讯
            today=datetime.date.today()   
            oneday=datetime.timedelta(days=7)   
            day7=today-oneday
            cl.SetFilterRange('pubdate',date_to_int(day7),date_to_int(today))
        if MATCH!="":
            cl.SetSortMode( SPH_SORT_EXTENDED ,'@weight DESC,pubdate desc' )
        else:
            if sortby:
                cl.SetSortMode( SPH_SORT_EXTENDED ,sortby )
            else:
                cl.SetSortMode( SPH_SORT_ATTR_DESC ,'pubdate' )
        if num:
            cl.SetLimits (0,num,num)
        else:
            if (allnum):
                cl.SetLimits (frompageCount,limitNum,allnum)
            else:
                cl.SetLimits (frompageCount,limitNum)
        if (keywords):
            if flag:
                res = cl.Query ('@(title,description,typename,typename1) '+keywords+'&@(flag) "p"',news)
            else:
                if arg==1:
                    res = cl.Query ('@(title,description,typename,typename1) '+keywords,news)
                else:
                    res = cl.Query ('@(title,typename,typename1) '+keywords,news)
        else:
            if flag:
                res = cl.Query ('@(flag) "p"',news)
            else:
                res = cl.Query ('',news)
        listall_news=[]
        listcount_news=0
        numb=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    content=''
                    contentall=''
                    if has_txt:
                        content=self.getnewcontent(id)
                        contentall=content
                        content=subString(filter_tags(content),200)
                    
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    click=attrs['click']
                    pubdate=attrs['pubdate']
                    litpic=attrs['litpic']
                    goodpost=attrs['goodpost']
                    typeid=attrs['typeid']
                    newsurl=self.get_newstype(typeid=typeid)
                    weburl=""
                    if newsurl:
                        weburl="/news/"+newsurl["url"]+"/"+str(id)+".html"
                    else:
                        weburl="/news/search/"+str(id)+".html"
                    imgurl=''
                    litpic=None
                    if not litpic:
                        imgurl=self.get_img_url(contentall)
                        if imgurl:
                            litpic=imgurl[0]
                    if litpic:
                        if "zz91.com" not in litpic and "http" not in litpic:
                            litpic=litpic.replace("uploads/uploads/","")
                            litpic="http://imgnews.zz91.com"+litpic
                    if litpic:
                        has_pic=1
                    else: 
                        litpic="http://img0.zz91.com/front/images/global/noimage.gif"
                        has_pic=''
                    #litpic=''
                    pubdate1=time.strftime('%m-%d', time.localtime(pubdate))
                    pubdate2=time.strftime('%Y-%m-%d', time.localtime(pubdate))
                    title=title.replace('&nbsp;','')
                    numb+=1
                    #收藏数
                    favoritecount=self.getfavoritecount(id)
                    dianzhancount=self.getzhancount(id)
                    list1={'typeid':typeid,'favoritecount':favoritecount,'title':title,'click':click,'id':id,'pubdate1':pubdate1,'pubdate':pubdate2,'weburl':weburl,'litpic':litpic,'has_pic':has_pic,'content':content,'goodpost':dianzhancount}
                    if keywords:
                        listall_news.append(list1)
                        if keywords.upper() in title.upper() or arg==1 or arg==2:
                            title=search_strong(keywords,title)
                            list1['title']=title
                    else:
                        listall_news.append(list1)
                    if limitNum==1 or num==1:
                        return list1
                listcount_news=res['total_found']
        if num:
            return listall_news
        else:
            return {'list':listall_news,'count':listcount_news}
    def getsubcontent(self,id,len):
        sql='select description from dede_archives where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            body=result[0]
            return body[:len]
    #是否收藏
    def isfavorite(self,content_id,favorite_type_code,company_id):
        if content_id and favorite_type_code and company_id:
            sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
            clist=dbc.fetchonedb(sql,[favorite_type_code,content_id,company_id])
            if clist:
                return 1
            else:
                return 0
        else:
            return 0
    #我的收藏夹
    def myfavorite(self,company_id,frompageCount="",limitNum=""):
        sql="select content_id from myfavorite where company_id=%s and favorite_type_code=%s order by gmt_created desc limit "+str(frompageCount)+','+str(limitNum)
        mlist=dbc.fetchalldb(sql,[company_id,'10091012'])
        listall=[]
        for list in mlist:
            id=list[0]
            list=self.getnewsdetail(id)
            list['body']=''
            list['content']=list['minbody']
            list['isfavorite']=1
            #ll={'id':list['id'],'conent':list['minbody'],'title':list['title'],'weburl':list['weburl']}
            listall.append(list)
        return listall
    #----获取资讯url
    def get_newstype(self,id='',typeid=''):
        
        if id:
            #catelist=cache.get("newstype"+str(id))
            #if catelist:
            #    return catelist
            sql='select typeid,typeid2 from dede_archives where id=%s'
            result=self.dbn.fetchonedb(sql,[id])
            if result:
                typeid=result[0]
                typeid2=result[1]
        else:
            typeid2="0"
        sql2='select typename,keywords from dede_arctype where id=%s'
        result2=self.dbn.fetchonedb(sql2,[typeid])
        if result2:
            url1=result2[1]
            
            if url1=="guonei":
                url1="cjxw"
            if url1=="guoji":
                url1="cjxw"
            if url1=="hangye":
                url1="hydt"
            if url1=="pinlun":
                url1="hydt"
            list={'typename':result2[0],'url':url1,'typeid':typeid,'typeid2':typeid2,'url2':'','typename2':''}
            if typeid2!='0':
                sql3='select keywords,typename from dede_arctype where id=%s'
                result3=self.dbn.fetchonedb(sql3,[typeid2])
                if result3:
                    list['url2']=result3[0]
                    list['typename2']=result3[1]
            #cache.set("newstype"+str(id),list,60*60)
            return list
    #类别名称
    def gettypenameid(self,keywords):
        sql='select id,typename from dede_arctype where keywords=%s'
        result=dbn.fetchonedb(sql,[keywords])
        if result:
            id=result[0]
            typename=result[1]
            list={'id':id,'typename':typename}
            return list
    def get_typetags(self,url):
        listall=cache.get("news_typetags"+str(url))
        if not catelist:
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
                    cache.set("news_typetags"+str(url),listall,60*60)
        return listall
    def gettypelist(self,frompageCount,limitNum,reid='',keywords='',has_news='',fromnews='',has_txt='',typeid='',typeid2=''):
        #获得缓存
        zz91news_gettypelist=cache.get("zz91news_gettypelist"+str(reid)+str(keywords)+str(has_news))
        if zz91news_gettypelist:
            return zz91news_gettypelist 
        listall=[]
        argument=[]
        sqlarg=' from dede_arctype '
        if reid:
            if 'where' in sqlarg:
                sqlarg+=' and reid=%s'
            else:
                sqlarg+=' where reid=%s'
            argument.append(reid)
        if keywords:
            if 'where' in sqlarg:
                sqlarg+=' and keywords=%s'
            else:
                sqlarg+=' where keywords=%s'
            argument.append(keywords)
        sql='select id,typename,sortrank,keywords'+sqlarg
        sql+=' order by sortrank,id limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbn.fetchalldb(sql,argument)
        for result in resultlist:
            id=result[0]
            nexttype=self.getnexttype(id)
            typename=result[1]
            typename_hex=''
            if typename:
                typename_hex=getjiami(typename)
            sortrank=result[2]
            keywords=result[3]
            newslist=[]
            if has_news:
                if reid==183:
                    typeid=typeid
                    typeid2=id
#                    typeid=[]
                else:
                    typeid=id
                    typeid2=typeid2
                if fromnews:
                    newslist=self.get_news_all(frompageCount=fromnews,limitNum=has_news,typeid=typeid,typeid2=typeid2,has_txt=has_txt)['list']
                else:
                    newslist=self.get_news_all(frompageCount=0,limitNum=has_news,typeid=typeid,typeid2=typeid2,has_txt=has_txt)
            list={'id':result[0],'typename':typename,'typename_hex':typename_hex,'sortrank':sortrank,'nexttype':nexttype,'keywords':keywords,'newslist':newslist}
            listall.append(list)
        #设置缓存
        cache.set("zz91news_gettypelist"+str(reid)+str(keywords)+str(has_news),listall,60*10) 
        return listall
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
        result=self.dbn.fetchone(sql,[id])
        if result:
            list={'id':result[0],'typename':result[1],'sortrank':result[2]}
            return list
    #----资讯列表(数据库)
    def get_news_all(self,frompageCount,limitNum,pubdate='',pubdate2='',flag='',title='',typeid='',typeid2='',has_txt='',kwd=''):
        #获得缓存
        zz91news_get_news_all=cache.get("zz91news_get_news_all"+str(pubdate2)+str(flag)+str(typeid))
        zz91news_get_news_all=None
        if zz91news_get_news_all:
            return zz91news_get_news_all 
        argument=[]
        sql1='select count(0) from dede_archives where id>0'
        sql='select id,title,sortrank,click,writer,shorttitle,keywords,litpic,filename,description from dede_archives where id>0'
        if pubdate:
            argument.append(pubdate)
            sql1=sql1+' and senddate>=%s'
            sql=sql+' and senddate>=%s'
        if pubdate2:
            argument.append(pubdate2)
            sql1=sql1+' and senddate<=%s'
            sql=sql+' and senddate<=%s'
        if flag:
            if ',' in flag:
                sql1=sql1+' and flag=%s'
                sql=sql+' and flag=%s'
            else:
                sql1=sql1+' and find_in_set(%s,flag)'
                sql=sql+' and find_in_set(%s,flag)'
            argument.append(flag)
        if typeid:
            argument.append(typeid)
            sql1=sql1+' and typeid=%s'
            sql=sql+' and typeid=%s'
        if typeid2:
            argument.append(typeid2)
            sql1=sql1+' and typeid2=%s'
            sql=sql+' and typeid2=%s'
        if title:
#            argument.append(title)
            sql1=sql1+' and title like "%'+title+'%"'
            sql=sql+' and title like "%'+title+'%"'
        sql=sql+' order by id desc'
        if limitNum:
            sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbn.fetchnumberdb(sql1,argument)
        resultlist=self.dbn.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            js=0
            for result in resultlist:
                id=result[0]
                title=result[1]
                title12=title[:12]
                title15=title[:15]
                title16=title[:16]
                title20=title[:20]
                intdate=result[2]
                click=result[3]
                writer=result[4]
                shorttitle=result[5]
                keywords=result[6]
                litpic=result[7]
                filename=result[8]
                description=result[9]
                kwds=''
                kwds_hex=''
                if kwd and keywords:
                    kwdslist=keywords.split(',')[:kwd]
                    if kwd>1:
                        kwds=','.join(kwdslist)
                    else:
                        kwds=kwdslist[0]
                        kwds_hex=getjiami(kwds)
                pubdate=intdate
#                pubdate=int_to_str(intdate)
                pubdate1=time.strftime('%m-%d', time.localtime(pubdate))
                pubdate2=time.strftime('%Y-%m-%d', time.localtime(pubdate))
                newsurl=self.get_newstype(id=id)
                weburl=""
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
                        #weburl+="/"+newsurl["url2"]
                    #weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                    weburl="/"+newsurl["url"]+"/"+str(id)+".html"
                content=''
                if has_txt:
                    if description:
                        content=filter_tags(description)
                        content=subString(str(content),has_txt)
                    #content=self.getnewsbody(id,has_txt)
                list={'id':id,'intdate':intdate,'pubdate':pubdate,'pubdate1':pubdate1,'pubdate2':pubdate2,'title':title,'title12':title12,'title15':title15,'title16':title16,'title20':title20,'weburl':weburl,'click':click,'writer':writer,'flaglist':'','flagnamestr':'','js':js,'typeid':typeid,'typeid2':typeid2,'typename':typename,'typename2':typename2,'shorttitle':shorttitle,'keywords':keywords,'litpic':litpic,'content':content,'kwds':kwds,'kwds_hex':kwds_hex,'filename':filename}
                #if flag:
                    #list['flaglist']=flaglist
                    #list['flagnamestr']=flagnamestr
                if limitNum==1:
                    return list
                listall.append(list)
                js=js+1
        #设置缓存
        cache.set("zz91news_get_news_all"+str(pubdate2)+str(flag)+str(typeid),listall,60*10) 
        return {'list':listall,'count':count}
    #新闻内容
    def getnewsbody(self,id,has_txt):
        sql='select description from dede_archives where id=%s'
        resultlist=self.dbn.fetchonedb(sql,id)
        if resultlist:
            content=resultlist[0]
            if content:
                content=content[:has_txt]
                return content
    #收藏数
    def getfavoritecount(self,id):
        sql="select count(0) from myfavorite where content_id=%s and favorite_type_code='10091012'"
        result=dbc.fetchonedb(sql,[id])
        return result[0]
    #点赞数
    def getzhancount(self,id):
        sql="select count(0) from dianzhan where aid=%s"
        result=dbn.fetchonedb(sql,[id])
        return result[0]
    def getattlist(self):
        catelist=cache.get("news_attlist")
        if catelist:
            return catelist
        sql='select sortid,att,attname from dede_arcatt order by sortid'
        resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'att':result[1],'attname':result[2]}
                listall.append(list)
        cache.set("news_attlist",listall,60*60000)
        return listall
    def getflagname(self,att):
        sql='select attname from dede_arcatt where att=%s'
        result=self.dbn.fetchonedb(sql,att)
        if result:
            return result[0]
    #新闻内容
    def getnewcontent(self,id,nohtml=''):
        sql='select body from dede_addonarticle where aid=%s'
        result1=self.dbn.fetchonedb(sql,id)
        if result1:
            body=result1[0]
            if nohtml:
                body=filter_tags(body)
            return body
    def getnewsdetail(self,id):
        #获得缓存
        #zz91news_getnewsdetail=cache.get("zz91news_getnewsdetail"+str(id))
        #if zz91news_getnewsdetail:
            #return zz91news_getnewsdetail 
        sql='select body,redirecturl from dede_addonarticle where aid=%s'
        result1=self.dbn.fetchonedb(sql,id)
        if result1:
            body=result1[0]
            redirecturl=result1[1]
            if redirecturl:
                list={'redirecturl':redirecturl}
                return list
            minbody=filter_tags(body)
            minbody=minbody.replace("    ","").strip().lstrip().rstrip().replace("　","")
            minbody=subString(minbody,200)
            
        else:
            return ''
        sql='select title,typeid,typeid2,flag,litpic,writer,click,shorttitle,pubdate,keywords,goodpost from dede_archives where id=%s'
        result=self.dbn.fetchonedb(sql,id)
        if result:
            title=result[0]
            typeid=result[1]
            typename=self.gettypename(typeid)
            typeid2=str(result[2])
            typename2=''
            if not typeid2:
                typeid2="0"
            if typeid2!='0':
                typename2=self.gettypename(typeid2)
            flag=result[3]
            litpic=result[4]
            #图片替换url
            imgurl=self.get_img_url(body)
            if imgurl:
                litpic=imgurl[0]
                for pp in imgurl:
                    if "zz91.com" not in pp and "http" not in pp:
                        pic=pp.replace("uploads/uploads/","")
                        pic="http://imgnews.zz91.com"+pic
                        body=body.replace(pp,pic)
                            
                        
            if litpic:
                if "zz91.com" not in litpic and "http" not in litpic:
                    litpic=litpic.replace("uploads/uploads/","")
                    litpic="http://imgnews.zz91.com"+litpic
            if litpic!="" and litpic:
                has_pic=1
            else: 
                has_pic=''
            writer=result[5]
            click=result[6]
            shorttitle=result[7]
            pubdate=int_to_strall(result[8])
            keywords=result[9]
            goodpost=result[10]
            kwdlist=[]
            newsurl=self.get_newstype(typeid=typeid)
            weburl=""
            if newsurl:
                weburl="/news/"+newsurl["url"]+"/"+str(id)+".html"
            else:
                weburl="/news/search/"+str(id)+".html"
            if keywords:
                if ',' in keywords:
                    keywordlist=keywords.split(',')
                    for kwd in keywordlist:
                        kwd_hex=getjiami(kwd)
                        listdir={'kwd_hex':kwd_hex,'kwd_name':kwd}
                        kwdlist.append(listdir)
                else:
                    kwd_hex=getjiami(keywords)
                    listdir={'kwd_hex':kwd_hex,'kwd_name':keywords}
                    kwdlist.append(listdir)
            #收藏数
            favoritecount=self.getfavoritecount(id)
            dianzhancount=self.getzhancount(id)
            list={'body':body,'favoritecount':favoritecount,'title':title,'typeid':typeid,'typename':typename,'typeid2':typeid2,'typename2':typename2,'flag':flag,'litpic':litpic,'writer':writer,'click':click,'shorttitle':shorttitle,'pubdate':pubdate,'kwdlist':kwdlist,'goodpost':dianzhancount,'minbody':minbody,'has_pic':has_pic,'weburl':weburl,'id':id,'keywords':keywords}
            #设置缓存
            cache.set("zz91news_getnewsdetail"+str(id),list,60*10)
            return list
    def gettypename(self,id):
        sql='select typename from dede_arctype where id=%s'
        result=self.dbn.fetchonedb(sql,id)
        if result:
            return result[0]
    def gettypenameurl(self,id):
        sql='select typename,keywords from dede_arctype where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            listdir={'typename':result[0],'keywords':result[1]}
            return listdir
    #新闻最终页上一篇下一篇(一期)
    def getarticalup(self,id,typeid,typeid2,detail_url):
        #获得缓存
        zz91news_getarticalup=cache.get("zz91news_getarticalup"+str(id)+str(typeid)+str(typeid2)+str(detail_url))
        if zz91news_getarticalup:
            return zz91news_getarticalup 
        sqlt="select id,title from dede_archives where typeid=%s and typeid2=%s and id>%s order by id limit 0,1"
        resultu = self.dbn.fetchonedb(sqlt,[typeid,typeid2,id])
        if resultu:
            idu=resultu[0]
            titleu=resultu[1]
            titleu=titleu.replace(" ","")
            titleu=titleu[:20]
            newsurl=self.get_newstype(idu)
            weburl='/'+detail_url+'/newsdetail1'+str(idu)+'.htm'
            list={'idu':idu,'titleu':titleu,'weburl':weburl}
            #设置缓存
            cache.set("zz91news_getarticalup"+str(id)+str(typeid)+str(typeid2)+str(detail_url),list,60*10)
            return list
    def getarticalnx(self,id,typeid,typeid2,detail_url):
        #获得缓存
        zz91news_getarticalnx=cache.get("zz91news_getarticalnx"+str(id)+str(typeid)+str(typeid2)+str(detail_url))
        if zz91news_getarticalnx:
            return zz91news_getarticalnx 
        sqlt="select id,title from dede_archives where typeid=%s and typeid2=%s and id<%s order by id desc limit 0,1"
        resultn = self.dbn.fetchonedb(sqlt,[typeid,typeid2,id])
        if resultn:
            idn=resultn[0]
            titlen=resultn[1]
            titlen=titlen.replace(" ","")
            titlen=titlen[:20]
            newsurl=self.get_newstype(idn)
            weburl='/'+detail_url+'/newsdetail1'+str(idn)+'.htm'
            list={'idn':idn,'titlen':titlen,'weburl':weburl}
            #设置缓存
            cache.set("zz91news_getarticalnx"+str(id)+str(typeid)+str(typeid2)+str(detail_url),list,60*10)
            return list
    #订阅类别
    def getguanzhu(self,company_id=""):
        sql="select id,typename,typedir from dede_arctype where isdefault=0"
        resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        for list in resultlist:
            id=list[0]
            typename=list[1]
            typedir=list[2]
            myflag=None
            if company_id:
                sqld="select id from myguanzhu where company_id=%s and typeid=%s"
                resultd=self.dbn.fetchonedb(sqld,[company_id,id])
                if resultd:
                    myflag=1
            l={'id':id,'typename':typename,'myflag':myflag,'typedir':typedir}
            listall.append(l)
        if company_id:
            sql="select id,tags from myguanzhu where typeid=0 and company_id=%s"
            result=self.dbn.fetchalldb(sql,[company_id])
            if result:
                myflag=1
                for list in result:
                    id=list[0]
                    typename=list[1]
                    l={'id':id,'typename':typename,'myflag':myflag,'typedir':''}
                    listall.append(l)
        return listall
    #我的关注
    def getmyguanzhu(self,company_id=""):
        listall=[]
        if company_id:
            sql="select tags,typeid from myguanzhu where company_id=%s order by id asc"
            resultlist=self.dbn.fetchalldb(sql,company_id)
            if resultlist:
                listall=[]
                for result in resultlist:
                    typename=result[0]
                    typeid=result[1]
                    list={'typename':typename,'typeid':typeid}
                    listall.append(list)
        return listall
    #微门户关键词
    def getcplist(self,keywords,limitcount):
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"showcount desc" )
        cl.SetLimits (0,limitcount,limitcount)
        keywords=''
        if keywords=='':
            res = cl.Query ('','daohangkeywords')
        else:
            res = cl.Query ('@(label) '+keywords,'daohangkeywords')
        listall=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                i=1
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    label=attrs['plabel']
                    pingyin=attrs['ppinyin']
                    if pingyin!="":
                        list={'label':label,'pingyin':pingyin,'i':i}
                        listall.append(list)
                    if (i>=4):
                        i=1
                    i=i+1
        if listall==[]:
            res = cl.Query ('','daohangkeywords')
            if res:
                if res.has_key('matches'):
                    tagslist=res['matches']
                    listall_news=[]
                    for match in tagslist:
                        id=match['id']
                        attrs=match['attrs']
                        label=attrs['plabel']
                        pingyin=attrs['ppinyin']
                        if pingyin!="":
                            list={'label':label,'pingyin':pingyin}
                            listall.append(list)
        return listall
    #展会列表
    def getzhlist(self,frompageCount,limitNum,searchlist=""):
        sqlarg=' from exhibit as a left outer join category as b on a.plate_category_code=b.code left outer join category as c on c.code=a.exhibit_category_code left outer join category as d on a.area_code=d.code where a.id>0'
        argument=[]
        if searchlist.has_key("area_code"):
            area_code=searchlist['area_code']
            sqlarg+=' and a.area_code=%s'
            argument.append(area_code)
        if searchlist.has_key("name"):
            name=searchlist['name']
            sqlarg+=' and a.name like %s'
            argument.append('%'+name+'%')
        if searchlist.has_key("area"):
            area=searchlist['area']
            sqlarg+=' and a.area like %s'
            argument.append('%'+area+'%')
        if searchlist.has_key("plate_category_code"):
            plate_category_code=searchlist['plate_category_code']
            sqlarg+=' and a.plate_category_code=%s'
            argument.append(plate_category_code)
        if searchlist.has_key("exhibit_category_code"):
            exhibit_category_code=searchlist['exhibit_category_code']
            sqlarg+=' and a.exhibit_category_code=%s'
            argument.append(exhibit_category_code)
        if searchlist.has_key("noexpress"):
            noexpress=searchlist['noexpress']
            sqlarg+=' and DATEDIFF(CURDATE(),a.start_time)<=0'
        if searchlist.get("top"):
            sqlarg+=' and a.hz_categorylist like "%20121002%"'
        sql1='select count(0)'+sqlarg
        sql='select a.id,a.name,a.area_code,a.area,a.start_time,a.end_time,a.plate_category_code,a.exhibit_category_code,a.gmt_created,a.checked,a.tags,b.label as bktypename,c.label as hytypename,d.label as area_name,a.tags,a.allzhuban,a.photo_cover,a.content,a.redircturl '+sqlarg
        if searchlist.has_key("noexpress"):
            sql+=' order by a.start_time asc limit '+str(frompageCount)+','+str(limitNum)
        else:
            sql+=' order by a.start_time desc limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=dbc.fetchnumberdb(sql1,argument)
            resultlist=dbc.fetchalldb(sql,argument)
        else:
            count=dbc.fetchnumberdb(sql1)
            resultlist=dbc.fetchalldb(sql)
        listall=[]
        i=1
        for result in resultlist:
            id=result[0]
            name=result[1]
            area_code=result[2]
            area=result[3]
            start_time=formattime(result[4],1)
            intstarttime=date_to_int(result[4])
            nowint=date_to_int(datetime.datetime.now())
            haveday=0
            if intstarttime>nowint:
                haveday=(intstarttime-nowint)/(3600*24)
            end_time=formattime(result[5],1)
            plate_category_code=result[6]
            exhibit_category_code=result[7]
            gmt_created=formattime(result[8],0)
            checked=result[9]
            bktypename=result[11]
            hytypename=result[12]
            area_name=result[13]
            tags=result[14]
            allzhuban=result[15]
            photo_cover=result[16]
            redircturl=result[18]
            imgurl=''
            if not photo_cover:
                imgurl=self.get_img_url(result[17])
            if imgurl:
                photo_cover=imgurl[0]
            if not photo_cover:
                photo_cover='http://img0.zz91.com/front/images/global/noimage.gif'
            if area:
                area_name=area
            if checked==1:
                checkvalue='已审'
            else:
                checkvalue='<font color=red>未审</font>'
            hnum=i % 2
            i+=1
            list={'id':id,'name':name,'area_code':area_code,'area_name':area_name,'tags':tags,'allzhuban':allzhuban,'area':area,'start_time':start_time,'end_time':end_time,'bktypename':bktypename,'hytypename':hytypename,'gmt_created':gmt_created,'checkvalue':checkvalue,'hnum':hnum,'photo_cover':photo_cover,'haveday':haveday,'redircturl':redircturl}
            listall.append(list)
        return {'list':listall,'count':count}
    #获取内容图片
    def get_img_url(self,html):#获得图片url
        #html=html.lower()
        if html:
            html=html.replace("data-original=","src=").replace("IMG",'img').replace("SRC",'src').replace("data-src","src")
            re_py3=r'<img.*?src="(.*?)".*?>'
            urls_pat3=re.compile(re_py3)
            img_url3=re.findall(urls_pat3,html)
            if img_url3:
                return img_url3
            re_py3=r"<img.*?src='(.*?)'.*?>"
            urls_pat3=re.compile(re_py3)
            img_url3=re.findall(urls_pat3,html)
            if img_url3:
                return img_url3
            re_py3=r'<img.*?src=(.*?) .*?>'
            urls_pat3=re.compile(re_py3)
            img_url3=re.findall(urls_pat3,html)
            if img_url3:
                return img_url3
    def getcategorylabel(self,code):
        sql="select label from category where code=%s"
        result=dbc.fetchonedb(sql,[code])
        if result:
            return result[0]
        else:
            return ''