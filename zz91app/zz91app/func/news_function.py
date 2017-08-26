#-*- coding:utf-8 -*-
class zznews:
    #----初始化ast数据库
    def __init__(self):
        self.dbn=dbn
        self.dbc=dbc
    def getnewscolumn(self):
        #获得缓存
        zz91app_getnewscolumn=cache.get("zz91app_getnewscolumn")
        if zz91app_getnewscolumn:
            return zz91app_getnewscolumn
        sql='select id,typename,keywords from dede_arctype where reid=184 and id not in (190,191,192,193,194,195,196,235) order by sortrank limit 0,8'
        resultlist=self.dbn.fetchalldb(sql)
        if resultlist:
            listall=[]
            numb=0
            for result in resultlist:
                numb=numb+1
                id=result[0]
                typename=result[1].decode('utf8','ignore')
                url=result[2]
                newslist=self.getnewslist(frompageCount=0,limitNum=5,typeid=[id])
                list={'typeid':id,'typename':typename,'url':url,'numb':numb,'newslist':newslist}
                listall.append(list)
            #设置缓存
            cache.set("zz91app_getnewscolumn",listall,60*10)
            return listall
    #----资讯列表(搜索引擎)
    def getnewslist(self,keywords="",frompageCount="",limitNum="",typeid="",typeid2="",allnum="",arg='',flag='',type='',MATCH="",hot=''):
        cl = SphinxClient()
        news=spconfig['name']['news']['name']
        serverid=spconfig['name']['news']['serverid']
        port=spconfig['name']['news']['port']
        cl.SetServer ( serverid, port )
        if MATCH!="":
            cl.SetMatchMode ( SPH_MATCH_ANY )
        else:
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        
        if (typeid):
            if typeid==['196']:
                keywords="p"
                typeid=""
            elif typeid==['195']:
                return self.getcompanynews(frompageCount,limitNum)
            else:
                cl.SetFilter('typeid',typeid)
        if (typeid2):
            cl.SetFilter('typeid2',[typeid2])
        cl.SetFilter('deleted',[0])
        if hot==1:
            #一个月内容的热门资讯
            today=datetime.date.today()   
            oneday=datetime.timedelta(days=7)   
            day7=today-oneday
            cl.SetFilterRange('pubdate',date_to_int(day7),date_to_int(today))
            flag="p"
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
                res = cl.Query ('@(title,description) '+keywords+'&@(flag) "'+str(flag)+'"',news)
            else:
                if arg==1:
                    res = cl.Query ('@(title,description) '+keywords,news)
                else:
                    res = cl.Query ('@(title) '+keywords,news)
        else:
            if flag:
                res = cl.Query ('@(flag) "'+str(flag)+'"',news)
            else:
                res = cl.Query ('',news)
        listall_news=[]
        listcount_news=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    subcontent=self.getsubcontent(id,160).decode('utf8','ignore')
                    subcontent=subcontent.replace('　','')
                    subcontent=subcontent.replace('\n','')
                    subcontent=subcontent.replace('\r','')
                    subcontent=subcontent.replace('\t','')
                    subcontent=subcontent.replace('\\r\\n\\r\\n\\t','')
                    subcontent=subcontent.replace('\\','')
                    
                    
                    murl="http://app.zz91.com/news/newsdetail"+str(id)+".htm"
                    attrs=match['attrs']
                    title=attrs['ptitle'].decode('utf8','ignore')
                    click=attrs['click']
                    pubdate=attrs['pubdate']
                    pic=attrs['litpic']
                    litpic=pic
                    if pic!="" and pic:
                        if "http://" in pic:
                            if ("img1.zz91") in pic:
                                listpic="http://img3.zz91.com/200x200"+pic.replace("http://img1.zz91.com","")
                            else:
                                litpic="http://pyapp.zz91.com/app/changepic.html?url=" +pic+"&width=300&height=300"
                        else:
                            litpic="http://pyapp.zz91.com/app/changepic.html?url=http://news.zz91.com/" +pic+"&width=300&height=300"
                    else: 
                        #litpic="http://img0.zz91.com/front/images/global/noimage.gif"
                        litpic=None
                    pubdate2=time.strftime('%Y-%m-%d', time.localtime(pubdate))
                    list1={'title':title,'click':click,'id':id,'pubdate':pubdate2,'murl':murl,'litpic':litpic,'subcontent':subcontent}
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
        if limitNum==1:
            return ''
        return {'list':listall_news,'count':listcount_news}
    def getsubcontent(self,id,len):
        #获得缓存
        #zz91app_getsubcontent=cache.get("zz91app_getsubcontent"+str(id)+str(len))
        #if zz91app_getsubcontent:
            #return zz91app_getsubcontent
        sql="select body from dede_addonarticle where aid=%s"
        alist = self.dbn.fetchonedb(sql,[id])
        content=""
        if alist:
            content=alist[0]
            if content:
                content=content.replace("　", "")
                content=subString(filter_tags(content),len)
            #设置缓存
            #cache.set("zz91app_getsubcontent"+str(id)+str(len),content,60*10)
        return content
        """
        sql='select description from dede_archives where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            body=result[0]
            if body:
                return body[:len]
            else:
                return ""
        """
    #获得一条资讯
    def getonenews(self):
        sql='select id,title from dede_archives order by id desc'
        result=self.dbn.fetchonedb(sql)
        if result:
            return {'id':result[0],'title':result[1]}
        else:
            return ''
    #获取新闻栏目名称(一期)
    def get_typename(self,id):
        #获得缓存
        zz91app_get_typename=cache.get("zz91app_get_typename"+str(id))
        if zz91app_get_typename:
            return zz91app_get_typename
        sql='select typename from dede_arctype where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            #设置缓存
            cache.set("zz91app_get_typename"+str(id),result[0],60*10)
            return result[0]
    #获得新闻栏目id列表
    def getcolumnid(self):
        sql='select id from dede_arctype where reid=184 and id not in (190,191,192,193,194,195,196,235) order by sortrank limit 0,8'
        resultlist=self.dbn.fetchalldb(sql)
        if resultlist:
            listall=[]
            for result in resultlist:
                listall.append(result[0])
            return listall
        
    #获得类别列表
    def getcolumnlist(self):
        sql='select id,typename from dede_arctype where reid=184 and id not in (190,191,192,193,194,195,196,235) order by sortrank limit 0,20'
        resultlist=self.dbn.fetchalldb(sql)
        if resultlist:
            listall=[]
            for result in resultlist:
                list={'id':result[0],'typename':result[1]}
                listall.append(list)
            return listall
    
    #最新图片新闻
    def get_newsimgsone(self):
        cursor_news = conn_news.cursor()
        sql="select id,title,pubdate from dede_archives where flag='p' order by pubdate desc limit 0,9"
        cursor_news.execute(sql)
        alist = cursor_news.fetchone()
        list=None
        if alist:
            id=alist[0]
            title=alist[1]
            contentlist=getnewscontent(id,cursor_news)
            if contentlist:
                content=contentlist['content']
                result=get_img_url(content)
                mobileweburl="http://m.zz91.com/news/newsdetail"+str(id)+".htm?type=news"
                if result:
                    imglll=result[0]
                    if "uploads/media/img_news" in imglll:
                        img_url="http://news.zz91.com"+imglll
                    else:
                        img_url=imglll
                else:
                    img_url=""
                list={'id':id,'title':title,'picurl':img_url,'url':mobileweburl}
        cursor_news.close()
        return list
    #----最终页相关阅读(4大类别)(一期)
    def get_typenews(self,typeid="",typeid2=""):
        culvalue=[]
        sql="select id,title,click,litpic from dede_archives where id>0 "
        if typeid:
            sql+=" and typeid=%s"
            culvalue.append(typeid)
        if typeid2:
            sql+=" and typeid2=%s"
            culvalue.append(typeid2)
        sql+=" order by id desc limit 0,5"
        if culvalue!=[]:
            resultlist=self.dbn.fetchalldb(sql,culvalue)
        else:
            resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                subcontent=self.getsubcontent(result[0],80).decode('utf8','ignore')
                pic=result[3]
                if pic!="" and pic:
                    if "http://" in pic:
                        litpic="http://pyapp.zz91.com/app/changepic.html?url=" +pic+"&width=300&height=300"
                    else:
                        litpic="http://pyapp.zz91.com/app/changepic.html?url=http://news.zz91.com/" +pic+"&width=300&height=300"
                else: 
                    litpic=None
                list={'id':result[0],'title':result[1].decode('utf8','ignore'),'click':result[2],'subcontent':subcontent,'litpic':litpic}
                listall.append(list)
        return listall
    
    #----推荐资讯（app置顶资讯）
    def get_topnews(self,typeid="",typeid2=""):
        cl = SphinxClient()
        news=spconfig['name']['news']['name']
        serverid=spconfig['name']['news']['serverid']
        port=spconfig['name']['news']['port']
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        
        if (typeid):
            cl.SetFilter('typeid',[int(typeid)])
        if (typeid2):
            cl.SetFilter('typeid2',[typeid2])
        cl.SetFilter('deleted',[0])
        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'pubdate' )
        cl.SetLimits (0,3,3)
        res = cl.Query ('@(flag) "c"',news)
        listall_news=[]
        listcount_news=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    subcontent=self.getsubcontent(id,80).decode('utf8','ignore')
                    murl="http://app.zz91.com/news/newsdetail"+str(id)+".htm"
                    attrs=match['attrs']
                    title=attrs['ptitle'].decode('utf8','ignore')
                    click=attrs['click']
                    pubdate=attrs['pubdate']
                    pic=attrs['litpic']
                    if pic!="" and pic:
                        if "http://" in pic:
                            litpic="http://pyapp.zz91.com/app/changepic.html?url=" +pic+"&width=300&height=300"
                        else:
                            litpic="http://pyapp.zz91.com/app/changepic.html?url=http://news.zz91.com/" +pic+"&width=300&height=300"
                    else: 
                        litpic=None
                    pubdate2=time.strftime('%Y-%m-%d', time.localtime(pubdate))
                    list1={'title':title,'click':click,'id':id,'pubdate':pubdate2,'murl':murl,'litpic':litpic,'subcontent':subcontent}
                    listall_news.append(list1)
                listcount_news=res['total_found']
        return listall_news
    
    #----新闻最终页上一篇下一篇(一期)
    def getarticalup(self,id,typeid):
        #获得缓存
        zz91app_getarticalup=cache.get("zz91app_getarticalup"+str(id)+str(typeid))
        if zz91app_getarticalup:
            return zz91app_getarticalup
        sqlt="select id,title from dede_archives where typeid=%s and id>%s order by id limit 0,1"
        resultu = self.dbn.fetchonedb(sqlt,[typeid,id])
        if resultu:
            list={'id':resultu[0],'title':resultu[1]}
            #设置缓存
            cache.set("zz91app_getarticalup"+str(id)+str(typeid),list,60*10)
            return list
    def getarticalnx(self,id,typeid):
        #获得缓存
        zz91app_getarticalnx=cache.get("zz91app_getarticalnx"+str(id)+str(typeid))
        if zz91app_getarticalnx:
            return zz91app_getarticalnx
        sqlt="select id,title from dede_archives where typeid=%s and id<%s order by id desc limit 0,1"
        resultn = self.dbn.fetchonedb(sqlt,[typeid,id])
        if resultn:
            list={'id':resultn[0],'title':resultn[1]}
            #设置缓存
            cache.set("zz91app_getarticalnx"+str(id)+str(typeid),list,60*10)
            return list
    #新闻内容
    def getnewscontent(self,id):
        newscontent=cache.get("newscontent"+str(id))
        if (newscontent==None):
            sqlt="select title,pubdate,click from dede_archives where id=%s"
            alist = self.dbn.fetchonedb(sqlt,[id])
            title=""
            pubdate=""
            click=""
            if alist:
                title=alist[0]
                pubdate=int_to_strall(alist[1])
                click=alist[2]
            else:
                title=""
                pubdate="2016-01-29 06:45:01"
                click=0
            sql="select body from dede_addonarticle where aid=%s"
            alist = self.dbn.fetchonedb(sql,[id])
            content=""
            if alist:
                content=alist[0]
                #content=getreplacepic(content)
                content=replacepic(content)
            newscontent={'title':title,'pubdate':pubdate,'content':content,'click':click}
            cache.set("newscontent"+str(id),newscontent,60*60)
        return newscontent
    #----新闻加点击数
    def newsclick_add(self,id):
        sql="update dede_archives set click=click+1 where id=%s"
        self.dbn.updatetodb(sql,[id])
    #----读取企业新闻
    def getcompanynews(self,fromcount,limitcount):
        #获得缓存
        zz91app_getcompanynews=cache.get("zz91app_getcompanynews")
        if zz91app_getcompanynews:
            return zz91app_getcompanynews
        sql="select count(0) from esite_news"
        listcount = self.dbc.fetchonedb(sql)[0]
        sql="select a.id,a.company_id,a.title,a.post_time,b.domain_zz91 from esite_news as a left join company as b on a.company_id=b.id order by id desc limit "+str(fromcount)+","+str(limitcount)+""
        result = self.dbc.fetchalldb(sql)
        listall=[]
        if result:
            for list in result:
                id=list[0]
                company_id=list[1]
                title=list[2]
                title10=title[:10]
                post_time=list[3]
                short_time=getMonth(post_time)+"-"+getDay(post_time)
                domain_zz91=list[4]
                list={'id':id,'title':title,'domain_zz91':domain_zz91,'pubdate':getMonth(post_time)+"-"+getDay(post_time),'short_time':short_time,'title10':title10}
                listall.append(list)
        #设置缓存
        cache.set("zz91app_getcompanynews",{'list':listall,'count':listcount},60*10)
        return {'list':listall,'count':listcount}
    #我的关注
    def getmyguanzhu(self,company_id=""):
        listall=[]
        if mid:
            sql="select tags,typeid,navname from myguanzhu where company_id=%s order by id asc"
            resultlist=self.dbn.fetchalldb(sql,company_id)
            if resultlist:
                listall=[]
                for result in resultlist:
                    typename=result[0]
                    typeid=result[1]
                    navname=result[2]
                    piclist=zzn.getnewspiclist(keywords=typename,limitNum=1,company_id=company_id,typeid=[int(typeid)],navname=navname)
                    list={'typename':typename,'piclist':piclist}
                    listall.append(list)
        return listall
    #获取滚动图片
    def getnewspiclist(self,keywords="",typeid="",typeid2="",type="",flag="",limitNum="",company_id="",navname=""):
        listall=[]
        if navname=="news":
            cl = SphinxClient()
            news=spconfig['name']['news']['name']
            serverid=spconfig['name']['news']['serverid']
            port=spconfig['name']['news']['port']
            cl.SetServer ( serverid, port )
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
            if (typeid2):
                cl.SetFilter('typeid2',[typeid2])
            
            cl.SetSortMode( SPH_SORT_EXTENDED ,'pubdate desc' )
            if (limitNum):
                cl.SetLimits (0,limitNum,limitNum)
            else:
                cl.SetLimits (0,5,5)
            if (keywords):
                res = cl.Query ('@(title,description,typename,typename1) '+keywords+'&@(flag) "p"',news)
            else:
                if flag:
                    res = cl.Query ('@(flag) p+'+flag+'',news)
                else:
                    res = cl.Query ('@(flag) "p"',news)
            noreadcount=self.getnoreadcount(keywords=keywords,typeid=typeid,company_id=company_id)
            if res:
                if res.has_key('matches'):
                    tagslist=res['matches']
                    for match in tagslist:
                        id=match['id']
                        attrs=match['attrs']
                        pic=attrs['litpic']
                        if pic!="" and pic:
                            litpic=pic
                            
                        else: 
                            litpic=None
                        title=attrs['ptitle']
                        pubdate=attrs['pubdate']
                        pubdate2=time.strftime('%m/%d', time.localtime(pubdate))
                        
                        list={'id':id,'pic':litpic,'title':title,'pubdate':pubdate2,'noreadcount':noreadcount}
                        if limitNum==1:
                            return list
                        listall.append(list)
        if navname=="huzhu":
            port = spconfig['port']
            cl = SphinxClient()
            cl.SetServer ( spconfig['serverid'], port )
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
            cl.SetSortMode( SPH_SORT_EXTENDED ,'post_time desc' )
            cl.SetFilter('is_del',[0])
            cl.SetFilter('check_status',[1,2])
            
            if (limitNum):
                cl.SetLimits (0,limitNum,limitNum)
            else:
                cl.SetLimits (0,5,5)
            if (keywords):
                res = cl.Query ('@(title,tags) '+keywords,"huzhu")
            else:
                res = cl.Query ('',"huzhu")
        return listall
    #未读信息量
    def getnoreadcount(self,keywords="",typeid="",typeid2="",company_id=""):
        if company_id:
            value=[company_id]
            sql="select maxnewstime,navname from myguanzhu where company_id=%s"
            if (keywords):
                sql+=" and tags=%s"
                value.append(keywords)
            result=self.dbn.fetchonedb(sql,value)
            
            if result:
                pubdate=result[0]
                navname=result[1]
                if navname=="news":
                    cl = SphinxClient()
                    news=spconfig['name']['news']['name']
                    serverid=spconfig['name']['news']['serverid']
                    port=spconfig['name']['news']['port']
                    cl.SetServer ( serverid, port )
                    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
                    cl.SetSortMode( SPH_SORT_EXTENDED ,'pubdate desc' )
                    if (typeid):
                        cl.SetFilter('typeid',typeid)
                    if pubdate:
                        cl.SetFilterRange('pubdate',int(pubdate),4070880000)
                    cl.SetLimits (0,1)
                    if (keywords):
                        res = cl.Query ('@(title,description,typename,typename1) '+keywords,news)
                    else:
                        res = cl.Query ('',news)
                    return res['total_found']
                elif navname=="huzhu":
                    port = spconfig['port']
                    cl = SphinxClient()
                    cl.SetServer ( spconfig['serverid'], port )
                    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
                    cl.SetSortMode( SPH_SORT_EXTENDED ,'post_time desc' )
                    cl.SetFilter('is_del',[0])
                    cl.SetFilter('check_status',[1,2])
                    
                    if pubdate:
                        cl.SetFilterRange('post_time',int(pubdate),4070880000)
                    cl.SetLimits (0,1)
                    if (keywords):
                        res = cl.Query ('@(title,tags) '+keywords,"huzhu")
                    else:
                        res = cl.Query ('',"huzhu")
                    return res['total_found']
        return 0
    #获得资讯数和关注数
    def getnewstitlecount(self,keywords,company_id=""):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetFilter('is_del',[0])
        cl.SetFilter('check_status',[1,2])
        cl.SetLimits (0,1)
        if (keywords):
            res = cl.Query ('@(title,tags) '+keywords,"huzhu")
        else:
            res = cl.Query ('',"huzhu")
        newscount=res['total_found']
        sql="select count(0) from myguanzhu where tags=%s"
        result=self.dbn.fetchonedb(sql,[keywords])
        gzcount=result[0]
        isguanzhu=None
        if company_id:
            sql="select id from myguanzhu where tags=%s and company_id=%s"
            result=self.dbn.fetchonedb(sql,[keywords,company_id])
            if result:
                isguanzhu=1
        return {'newscount':newscount,'gzcount':gzcount,'isguanzhu':isguanzhu}
    
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