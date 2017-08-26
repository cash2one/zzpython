#-*- coding:utf-8 -*-
import datetime

class zznews:
    #----初始化ast数据库
    def __init__(self):
        self.dbn=dbn
    def getnewscolumn(self,reid="",typeid="",deviceId=""):
        if str(reid)=="0" or not reid:
            return None
        sql='select id,typename,keywords,typedir from dede_arctype where id>0'
        if reid:
            sql+=' and reid='+str(reid)
        else:
            sql+=' and reid=0'
        sql=sql+' order by sortrank asc limit 0,100'
        resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        if resultlist:
            typedir=""
            numb=0
            for result in resultlist:
                nowdir=None
                if typeid:
                    if str(typeid)==str(result[0]):
                        nowdir=1
                numb=numb+1
                id=result[0]
                typename=result[1]
                url=result[2]
                url="../list/list1.html"
                typedir=result[3]
                typedir=typedir.replace("{cmspath}/a/","")
                pageParam={'typeid':id}
                list={'typename':typename,'url':url,'pageParam':pageParam}
                listall.append(list)
            return listall
    def getcolumnall(self,mid=""):
        sql="select id,typename from dede_arctype where reid=0"
        resultlist=self.dbn.fetchalldb(sql)
        listall={}
        for list in resultlist:
            id=list[0]
            typename=list[1]
            sqlc="select id,typename from dede_arctype where reid=%s"
            result=self.dbn.fetchalldb(sqlc,[id])
            child=[]
            for list1 in result:
                id1=list1[0]
                myflag=None
                if mid:
                    sqld="select id from myguanzhu where mid=%s and typeid=%s"
                    resultd=self.dbn.fetchonedb(sqld,[mid,id1])
                    if resultd:
                        myflag=1
                typename1=list1[1]
                url="../list/list1.html"
                pageParam={'typeid':id1}
                l={'id':id1,'typename':typename1,'url':url,'pageParam':pageParam,'myflag':myflag}
                child.append(l)
            ll={str(id):{'id':id,'typename':typename,'list':child}}
            listall.update(ll)
        if mid:
            sql="select id,tags from myguanzhu where typeid=0 and mid=%s"
            result=self.dbn.fetchalldb(sql,[mid])
            if result:
                child=[]
                for list in result:
                    pageParam={'typeid':0}
                    typename1=list[1]
                    url="../list/list1.html"
                    myflag=1
                    l={'id':0,'typename':typename1,'url':url,'pageParam':pageParam,'myflag':myflag}
                    child.append(l)
                ll={str(0):{'id':0,'typename':'其他','list':child}}
                listall.update(ll)
        return listall
    #我的关注
    def getmyguanzhu(self,mid=""):
        listall=[]
        if mid:
            sql="select tags,typeid from myguanzhu where mid=%s order by id asc"
            resultlist=self.dbn.fetchalldb(sql,mid)
            if resultlist:
                listall=[]
                for result in resultlist:
                    typename=result[0]
                    typeid=result[1]
                    piclist=self.getnewspiclist(keywords=typename,limitNum=1,mid=mid,typeid=[int(typeid)])
                    list={'typename':typename,'piclist':piclist,'typeid':typeid}
                    listall.append(list)
        return listall
    #获取我的定制
    def getmyorderlist(self):
        sql='select id,typename,keywords from dede_arctype order by id asc limit 0,100'
        resultlist=self.dbn.fetchalldb(sql)
        if resultlist:
            listall=[]
            numb=2
            for result in resultlist:
                numb=numb+1
                id=result[0]
                typename=result[1]
                url=result[2]
                list={'id':id,'typeid':id,'typename':typename,'url':url,'numb':numb}
                listall.append(list)
            return listall
    def getchildtypelist(self,typeid):
        sqlc="select id,typename from dede_arctype where reid=%s"
        result=self.dbn.fetchalldb(sqlc,[typeid])
        child=[]
        for list1 in result:
            id1=list1[0]
            child.append(id1)
        return child
    #获取滚动图片
    def getnewspiclist(self,keywords="",typeid="",typeid2="",type="",flag="",limitNum="",mid=""):
        cl = SphinxClient()
        news=spconfig['name']['dacong']['name']
        serverid=spconfig['name']['dacong']['serverid']
        port=spconfig['name']['dacong']['port']
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        
        if (typeid):
            if typeid==[0]:
                arr=0
            else:
                typenewid=self.getchildtypelist(typeid[0])
                if not typenewid:
                    typenewid=typeid
                cl.SetFilter('typeid',typenewid)
        
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
        listall=[]
        noreadcount=self.getnoreadcount(keywords=keywords,typeid=typeid,mid=mid)
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
                    title=title.replace("_养生之道网","")
                    pubdate=attrs['pubdate']
                    pubdate2=time.strftime('%m/%d', time.localtime(pubdate))
                    
                    list={'id':id,'pic':litpic,'title':title,'pubdate':pubdate2,'noreadcount':noreadcount}
                    if limitNum==1:
                        return list
                    listall.append(list)
        return listall
    #未读信息量
    def getnoreadcount(self,keywords="",typeid="",typeid2="",mid=""):
        if mid:
            value=[mid]
            sql="select maxnewstime from myguanzhu where mid=%s"
            """
            if (typeid):
                sql+=" and typeid in (%s)"
                value.append(typeid[0])
            """
            if (keywords):
                sql+=" and tags=%s"
                value.append(keywords)
            result=self.dbn.fetchonedb(sql,value)
            
            if result:
                pubdate=result[0]
                cl = SphinxClient()
                news=spconfig['name']['dacong']['name']
                serverid=spconfig['name']['dacong']['serverid']
                port=spconfig['name']['dacong']['port']
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
        return 0
    #获得资讯数和关注数
    def getnewstitlecount(self,keywords,mid=""):
        cl = SphinxClient()
        news=spconfig['name']['dacong']['name']
        serverid=spconfig['name']['dacong']['serverid']
        port=spconfig['name']['dacong']['port']
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED ,'pubdate desc' )
        cl.SetLimits (0,1)
        if (keywords):
            res = cl.Query ('@(title,description,typename,typename1) '+keywords,news)
        else:
            res = cl.Query ('',news)
        newscount=res['total_found']
        sql="select count(0) from myguanzhu where tags=%s"
        result=self.dbn.fetchonedb(sql,[keywords])
        gzcount=result[0]
        isguanzhu=None
        if mid:
            sql="select id from myguanzhu where tags=%s and mid=%s"
            result=self.dbn.fetchonedb(sql,[keywords,mid])
            if result:
                isguanzhu=1
        return {'newscount':newscount,'gzcount':gzcount,'isguanzhu':isguanzhu}
    #----资讯列表(搜索引擎)
    def getnewslist(self,keywords="",frompageCount="",limitNum="",typeid="",typeid2="",allnum="",arg='',flag='',type='',MATCH=""):
        cl = SphinxClient()
        news=spconfig['name']['dacong']['name']
        serverid=spconfig['name']['dacong']['serverid']
        port=spconfig['name']['dacong']['port']
        cl.SetServer ( serverid, port )
        if MATCH!="":
            cl.SetMatchMode ( SPH_MATCH_ANY )
        else:
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        
        if (typeid):
            if typeid==[0]:
                arr=0
            else:
                cl.SetFilter('typeid',typeid)
        if (typeid2):
            cl.SetFilter('typeid2',[typeid2])
        if MATCH!="":
            cl.SetSortMode( SPH_SORT_EXTENDED ,'@weight DESC,pubdate desc' )
        else:
            if (type=="hot"):
                cl.SetSortMode( SPH_SORT_EXTENDED ,'click desc' )
            elif (type=="like"):
                cl.SetSortMode( SPH_SORT_EXTENDED ,'scount desc' )
            else:
                cl.SetSortMode( SPH_SORT_EXTENDED ,'pubdate desc' )
        if (allnum):
            cl.SetLimits (frompageCount,limitNum,allnum)
        else:
            cl.SetLimits (frompageCount,limitNum)
        if (keywords):
            if flag:
                res = cl.Query ('@(title,description,typename,typename1) '+keywords+'&@(flag) "'+flag+'"',news)
            else:
                if arg==1:
                    res = cl.Query ('@(title,typename,typename1) '+keywords,news)
                else:
                    res = cl.Query ('@(title,typename,typename1) '+keywords,news)
        else:
            if flag:
                res = cl.Query ('@(flag) '+flag+'',news)
            else:
                res = cl.Query ('',news)
        listall_news=[]
        listcount_news=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    subcontent=self.getsubcontent(id,400)
                    arrcontent=self.getnewscontent(id)
                    pic=attrs['litpic']
                    
                    if pic!="" and pic:
                        litpic=pic
                    else: 
                        litpic=None
                    picone=litpic
                    picmore=None
                    content=None
                    if arrcontent:
                        content=arrcontent['content']
                        """
                        piclist=self.getcontentpic(content)
                        if piclist:
                            if len(piclist)>=3:
                                picmore=piclist[0:30]
                                ll=[]
                                i=1
                                for l in picmore:
                                    if l and "http" in l:
                                        if requests.get(l).status_code=="404":
                                            a=0
                                        else:
                                            l=l.replace("&width=300&height=300","&width=100&height=100")
                                            ll.append(l)
                                            i+=1
                                        if i>4:
                                            break
                                picmore=ll
                            else:
                                picone=litpic
                        else:
                            picone=litpic
                        """
                        
                    murl="/app/newsdetail"+str(id)+".htm"
                    
                    title=attrs['ptitle']
                    if arrcontent:
                        click=arrcontent['click']
                        pcount=arrcontent['pcount']
                        fcount=arrcontent['fcount']
                        
                        typename=arrcontent['typename']
                        typeid=arrcontent['typeid']
                        typedir=arrcontent['typedir']
                        source=arrcontent['source']
                        pubdate=attrs['pubdate']
                        pubdate2=time.strftime('%m/%d', time.localtime(pubdate))
                        list1={'title':title,'picone':picone,'picmore':picmore,'click':click,'id':id,'pubdate':pubdate2,'pcount':pcount,'fcount':fcount,'typename':typename,'typedir':typedir,'murl':murl,'litpic':litpic,'subcontent':subcontent.decode('utf-8','ignore'),'source':source}
                        if type:
                            if keywords:
                                if keywords in title:
                                    #title=search_strong(keywords,title)
                                    list1['title']=title
                        listall_news.append(list1)
                        if limitNum==1:
                            return list1
                listcount_news=res['total_found']
        if limitNum==1:
            return ''
        return {'list':listall_news,'count':listcount_news+1}
    def getcontentpic(self,html):
        if html:
            html=html.replace("data-original=","src=").replace("IMG",'img').replace("SRC",'src')
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
    #获取文章内容
    def getsubcontent(self,id,len):
        sql="select body from dede_addonarticle where aid=%s"
        alist = self.dbn.fetchonedb(sql,[id])
        content=""
        if alist:
            content=alist[0]
            if content:
                content=remove_content_value(subString(filter_tags(content),len))
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
    #获取新闻栏目名称(一期)
    def get_typename(self,id):
        sql='select typename,typedir from dede_arctype where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            return {'typename':result[0],'typedir':result[1]}
    #获取新闻栏目名称(一期)
    def get_typeid(self,typedir):
        sql='select id from dede_arctype where typedir=%s'
        result=self.dbn.fetchonedb(sql,[typedir])
        if result:
            return result[0]
    def get_typereid(self,typeid):
        sql='select reid from dede_arctype where id=%s'
        result=self.dbn.fetchonedb(sql,[typeid])
        if result:
            return result[0]
    def get_typedir(self,typeid):
        sql='select typedir from dede_arctype where id=%s'
        result=self.dbn.fetchonedb(sql,[typeid])
        if result:
            return result[0]
    #获得新闻栏目id列表
    def getcolumnid(self):
        sql='select id,typename,keywords from dede_arctype where reid=184 order by sortrank limit 0,8'
        resultlist=self.dbn.fetchalldb(sql)
        if resultlist:
            listall=[]
            for result in resultlist:
                listall.append(result[0])
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
            contentlist=self.getnewscontent(id,cursor_news)
            if contentlist:
                content=contentlist['content']
                result=get_img_url(content)
                mobileweburl="http://m.zz91.com/sex/newsdetail"+str(id)+".htm?type=news"
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
    def get_typenews(self,typeid="",typeid2="",num=""):
        culvalue=[]
        sql="select id,title from dede_archives where id>0 "
        if typeid:
            sql+=" and typeid=%s"
            culvalue.append(typeid)
        if typeid2:
            sql+=" and typeid2=%s"
            culvalue.append(typeid2)
        sql+=" order by id desc "
        if num:
            sql+=" limit 0,"+str(num)
        else:
            sql+=" limit 0,10"
        if culvalue!=[]:
            resultlist=self.dbn.fetchalldb(sql,culvalue)
        else:
            resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'title':result[1]}
                listall.append(list)
        return listall
    
    #----新闻最终页上一篇下一篇(一期)
    def getarticalup(self,id,typeid):
        sqlt="select id,title from dede_archives where typeid=%s and id>%s order by id limit 0,1"
        resultu = self.dbn.fetchonedb(sqlt,[typeid,id])
        if resultu:
            list={'id':resultu[0],'title':resultu[1]}
            return list
    def getarticalnx(self,id,typeid):
        sqlt="select id,title from dede_archives where typeid=%s and id<%s order by id desc limit 0,1"
        resultn = self.dbn.fetchonedb(sqlt,[typeid,id])
        if resultn:
            list={'id':resultn[0],'title':resultn[1]}
            return list
    def get_newslittlecontent(self,id):
        pcount=0
        fcount=0
        sqlp="select count(0) from dede_feedback where aid=%s"
        plist = self.dbn.fetchonedb(sqlp,[id])
        if plist:
            pcount=plist[0]
        sqlp="select count(0) from dede_member_stow where aid=%s"
        plist = self.dbn.fetchonedb(sqlp,[id])
        if plist:
            fcount=plist[0]
        sqlt="select title,pubdate,click,typeid from dede_archives where id=%s"
        alist = self.dbn.fetchonedb(sqlt,[id])
        title=""
        pubdate=""
        click=""
        if alist:
            title=alist[0]
            pubdate=int_to_strall(alist[1])
            pubdate2=time.strftime('%m/%d', time.localtime(alist[1]))
            click=alist[2]
            typeid=alist[3]
            typename=self.get_typename(typeid)['typename']
            newscontent={'title':title.decode('utf-8','ignore'),'pubdate':pubdate2,'click':click,'pcount':pcount,'fcount':fcount,'typename':typename}
            return newscontent
    #新闻内容
    def getnewscontent(self,id,mid=""):
        newscontent=cache.get("dacong_newscontent"+str(id))
        newscontent=None
        if (newscontent==None):
            sqlt="select title,pubdate,click,typeid,source,litpic from dede_archives where id=%s"
            alist = self.dbn.fetchonedb(sqlt,[id])
            title=""
            pubdate=""
            click=""
            typename=""
            if alist:
                title=remove_content_value(alist[0])
                pubdate=int_to_strall(alist[1])
                click=alist[2]
                typeid=alist[3]
                #typedir=self.get_typedir(typeid)
                typevalue=self.get_typename(typeid)
                if typevalue:
                    typename=typevalue['typename']
                    typedir=typevalue['typedir']
                source=alist[4]
                litpic=alist[5]
                sql="select body,cstyle from dede_addonarticle where aid=%s"
                alist = self.dbn.fetchonedb(sql,[id])
                content=""
                if alist:
                    content=alist[0]
                    cstyle=alist[1]
                    #content=getreplacepic(content)
                    #content=replacepic(content)
                sql="select url from zhuaqu_url where aid=%s"
                alist = self.dbn.fetchonedb(sql,[id])
                oldurl=""
                if alist:
                    oldurl=alist[0]
                newscontent={'title':title.decode('utf-8','ignore'),'pubdate':pubdate,'content':content.decode('utf-8','ignore'),'typename':typename,'typeid':typeid,'typedir':typedir,'click':click,'source':source,'oldurl':oldurl,'cstyle':cstyle,'litpic':litpic}
                cache.set("dacong_newscontent"+str(id),newscontent,60*60)
        if newscontent:
            pcount=0
            fcount=0
            #评论数
            sqlp="select count(0) from dede_feedback where aid=%s"
            plist = self.dbn.fetchonedb(sqlp,[id])
            if plist:
                pcount=plist[0]
            #收藏数
            sqlp="select count(0) from dede_member_stow where aid=%s"
            plist = self.dbn.fetchonedb(sqlp,[id])
            if plist:
                fcount=plist[0]
            #是否已经收藏
            haveshouchan=None
            if mid:
                sqlp="select id from dede_member_stow where mid=%s and aid=%s"
                plist = self.dbn.fetchonedb(sqlp,[mid,id])
                if plist:
                    haveshouchan=1
            #类别文章数
            typeid=newscontent['typeid']
            typenamecount=0
            if typeid:
                sql="select count(0) from dede_archives where typeid=%s"
                plist = self.dbn.fetchonedb(sql,[typeid])
                if plist:
                    typenamecount=plist[0]
            tags=newscontent['typename']
            haveguanzhu=None
            if mid and tags:
                sql="select id from myguanzhu where mid=%s and tags=%s"
                result=dbn.fetchonedb(sql,[mid,tags])
                if result:
                    haveguanzhu=1
            newscontent['typenamecount']=typenamecount
            newscontent['pcount']=pcount
            newscontent['fcount']=fcount
            newscontent['haveshouchan']=haveshouchan
            newscontent['haveguanzhu']=haveguanzhu
        return newscontent
    #----新闻加点击数
    def newsclick_add(self,id):
        sql="update dede_archives set click=click+1 where id=%s"
        self.dbn.updatetodb(sql,[id])
    
    #---订阅
    def saveorder(self,deviceId,tid,action):
        gmt_created=datetime.datetime.now()
        if action=="0":
            sql="delete from myorder where deviceId=%s,tid=%s"
            self.dbn.updatetodb(sql,[deviceId,tid])
        else:
            sql="select * from myorder where deviceId=%s,tid=%s"
            alist = self.dbn.fetchonedb(sqlt,[deviceId,tid])
            if not alist:
                sql="insert into myorder(deviceId,tid,gmt_created) values(%s,%s,%s)"
                self.dbn.updatetodb(sql,[deviceId,tid,gmt_created])
#------以下是dedecms数据
    #--根据dede_member_stow表的id获得mid与aid
    def getmidaid(self,id):
        sql="select mid, aid from dede_member_stow where id =%s"
        alist=self.dbn.fetchonedb(sql,[id])
        if alist:
            mid=alist[0]
            aid=alist[1]
            list={'mid':mid,'aid':aid}
            return list
    #--获得文章标题
    def getnewstitle(self,id):
        sql="select title from dede_archives where id=%s"
        alist=self.dbn.fetchonedb(sql,[id])
        if alist:
            title=alist[0]
            list={'title':remove_content_value(title)}
            return list
    #--根据mid获得发布人（member）信息
    def getmemberinfo(self,mid):
        sql="select mid,userid,uname,sex,face,mobile,marry from dede_member where mid=%s"
        alist=self.dbn.fetchonedb(sql,[mid])
        if alist:
            mid=alist[0]
            userid=alist[1]
            uname=alist[2]
            sex=alist[3]
            face=alist[4]
            mobile=alist[5]
            marry=alist[6]
            list={'mid':mid,'userid':userid,'uname':uname,'sex':sex,'face':face,'mobile':mobile,'marry':marry}
            return list
    #获得小图
    def getlitpic(self,aid):
        sql="select litpic from dede_archives where id=%s"
        result=self.dbn.fetchonedb(sql,[aid])
        if result:
            if result[0]:
                return result[0]
    #获得收藏夹列表(根据userid获得)
    def get_memebe_stom(self,mid="",frompageCount="",limitNum="",allnum=''):
        argument=[mid]
        sql1="select count(*) from dede_member_stow where mid=%s"
        sql="select id,mid,aid,title,addtime from dede_member_stow where mid=%s order by id desc limit "+str(frompageCount)+","+str(limitNum)+""
        listall=[]
        count=self.dbn.fetchnumberdb(sql1,argument)
        resultlist=self.dbn.fetchalldb(sql,argument)
        if resultlist:
            for result in resultlist:
                id=result[0]
                mid=result[1]
                aid=result[2]
                title=result[3]
                addtime=int_to_strall(result[4])
                #content=self.get_newslittlecontent(aid)
                litpic=self.getlitpic(aid)
                
                list={'id':id,'mid':mid,'aid':aid,'title':title,'addtime':addtime,'litpic':litpic}
                listall.append(list)
        return {'list':listall,'count':count}
    #获得标签列表
    def get_tagslist(self,frompageCount="",limitNum="",allnum='',mid=''):
        argument=[]
        sql1="select count(*) from dede_tagindex"
        sql="select id,tag,typeid,count from dede_tagindex order by count desc limit "+str(frompageCount)+","+str(limitNum)+""
        listall=[]
        count=self.dbn.fetchnumberdb(sql1,argument)
        resultlist=self.dbn.fetchalldb(sql,argument)
        if resultlist:
            for result in resultlist:
                id=result[0]
                tag=result[1]
                typeid=result[2]
                ncount=result[3]
                newsgz=self.getnewstitlecount(tag,mid=mid)
                newscount=0
                gzcount=0
                if newsgz:
                    newscount=newsgz['newscount']
                    gzcount=newsgz['gzcount']
                    isguanzhu=newsgz['isguanzhu']
                
                list={'id':id,'tag':tag,'typeid':typeid,'count':ncount,'newscount':newscount,'gzcount':gzcount,'isguanzhu':isguanzhu}
                listall.append(list)
        return {'list':listall,'count':count}
            
    #过获得评论表
    def get_feedback(self,aid=None,mid=None,frompageCount="",limitNum="",allnum='',deviceId=""):
        argument=[]
        sqlarg=''
        if aid:
            sqlarg+=' and aid=%s'
            argument.append(aid)
        if mid:
            sqlarg+=' and mid=%s'
            argument.append(mid)
        sql1="select count(*) from dede_feedback where id>0 "+sqlarg
        sql='select id,aid,mid,msg,bad,good,dtime from dede_feedback where id>0 '+sqlarg+' order by id desc  limit %s,%s'
        count=self.dbn.fetchnumberdb(sql1,argument)
        argument.append(frompageCount)
        argument.append(limitNum)
        resultlist=self.dbn.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                aid=result[1]
                mid=result[2]
                msg=result[3]
                
                bad=result[4]
                good=result[5]
                dtime=int_to_strall(result[6])
                feedbackname="网友"
                
                if mid:
                    memberinfo=self.getmemberinfo(mid)
                    if memberinfo:
                        feedbackname=memberinfo['uname']
                        face=memberinfo['face']
                    else:
                        feedbackname="网友"
                        face=None
                list={'id':id,'aid':aid,'bad':bad,'good':good,'msg':msg,'feedbackname':feedbackname,'dtime':dtime,'face':face}
                listall.append(list)
        return {'list':listall,'count':count}
    #最近浏览
    def get_history(self,mid=None,frompageCount="",limitNum="",allnum=''):
        argument=[]
        sqlarg=''
        if mid:
            sqlarg=' and mid=%s'
            argument.append(mid)
        sql1="select count(*) from view_history where id>0"+sqlarg
        sql='select id,aid,mid,gmt_created from view_history where id>0'+sqlarg+' order by id desc limit %s,%s'
        count=self.dbn.fetchnumberdb(sql1,argument)
        argument.append(frompageCount)
        argument.append(limitNum)
        resultlist=self.dbn.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                aid=result[1]
                mid=result[2]
                gmt_created=result[3]
                content=self.getnewstitle(aid)
                litpic=self.getlitpic(aid)
                title=''
                if content:
                    title=content['title']
                if title:
                    addtime=formattime(gmt_created,0)
                    list={'id':id,'aid':aid,'content':content,'litpic':litpic,'title':title,'addtime':addtime}
                    listall.append(list)
        return {'list':listall,'count':count}
    #获得我的订阅表
    def get_myorder(self,deviceId):
        sql='select mid,tid from myorder where deviceId=%s'
        resultlist=self.dbn.fetchalldb(sql,[deviceId])
        listall=[]
        if resultlist:
            for result in resultlist:
                mid=result[0]
                tid=result[1]
                sql1='select typename,tempindex,id from dede_arctype where id=%s'
                t_res=self.dbn.fetchonedb(sql1,[tid])
                if t_res:
                    typename=t_res[0]
                    tempindex=t_res[1]
                    id=t_res[2]
                    list={'typename':typename,'id':id}
                    listall.append(list)
        return listall
                
    #插入至留言溥
    def insert_guestbook(self,mid,gid,title,uname,email,qq,tel,ip,dtime,msg):
        sql='insert into dede_member_guestbook(mid,gid,title,uname,email,qq,tel,ip,dtime,msg) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.dbn.updatetodb(sql,[mid,gid,title,uname,email,qq,tel,ip,dtime,msg])
        
    #插入至最近浏览
    def insert_viewhistory(self,mid,aid,deviceId=""):
        gmt_created=datetime.datetime.now()
        sql="select id from view_history where aid=%s and mid=%s"
        result=self.dbn.fetchonedb(sql,[aid,mid])
        if result:
            a=1
            #sqlt="update view_history set gmt_created=%s where id=%s"
            #self.dbn.updatetodb(sqlt,[result[0]])
        else:
            sql='insert into view_history(mid,aid,gmt_created,deviceId) values(%s,%s,%s,%s)'
            self.dbn.updatetodb(sql,[mid,aid,gmt_created,deviceId])
    #获得用户信息
    def getuserinfo(self,mid="",deviceId=""):
        sql="select mid,userid,pwd,uname,sex,face,marry,mobile from dede_member where deviceId=%s"
        result=self.dbn.fetchonedb(sql,[deviceId])
        list=None
        if result:
            gmt_modified=datetime.datetime.now()
            token = hashlib.md5(result[2]+result[1]+str(gmt_modified))
            token = token.hexdigest()[8:-8]
            list={'mid':result[0],
                  'userid':result[1],
                  'pwd':result[2],
                  'uname':result[3],
                  'sex':result[4],
                  'face':result[5],
                  'marry':result[6],
                  'mobile':result[7],
                  'token':token,
                }
        return list
    #更新token
    def savetoken(self,mid,token,appid):
        gmt_modified=datetime.datetime.now()
        sql="select mid from member_appinfo where mid=%s"
        mlist=dbn.fetchonedb(sql,[mid])
        if mlist:
            sql="update member_appinfo set appid=%s,token=%s,gmt_modified=%s where mid=%s"
            dbn.updatetodb(sql,[appid,token,gmt_modified,mid])
        else:
            sql="insert into member_appinfo(mid,appid,token,gmt_modified) values(%s,%s,%s,%s)"
            dbn.updatetodb(sql,[mid,appid,token,gmt_modified])
        return 1
