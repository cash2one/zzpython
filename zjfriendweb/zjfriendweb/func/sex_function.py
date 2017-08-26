#-*- coding:utf-8 -*-
import datetime
def subString(string,length):   
    if length >= len(string):   
        return string   
    result = ''  
    i = 0  
    p = 0  
    while True:   
        ch = ord(string[i])   
        #1111110x   
        if ch >= 252:   
            p = p + 6  
        #111110xx   
        elif ch >= 248:   
            p = p + 5  
        #11110xxx   
        elif ch >= 240:   
            p = p + 4  
        #1110xxxx   
        elif ch >= 224:   
            p = p + 3  
        #110xxxxx   
        elif ch >= 192:
            p = p + 2  
        else:   
            p = p + 1       
        if p >= length:   
            break;
        else:   
            i = p   
    return string[0:i]
    pass
class zznews:
    #----初始化ast数据库
    def __init__(self):
        self.dbn=dbn
    def getnewscolumn(self,reid="",typeid="",deviceId=""):
        sql='select id,typename,keywords,typedir from dede_arctype where id>0'
        if reid:
            sql+=' and reid='+str(reid)
        else:
            sql+=' and reid=0'
        if deviceId:
            sql=sql+' and exists(select tid from myorder where tid=dede_arctype.id and deviceId="'+str(deviceId)+'")'
            sql=sql+' order by id asc limit 0,100'
        resultlist=self.dbn.fetchalldb(sql)
        if resultlist:
            typedir=""
            numb=0
            listall=[{'id':0,'typeid':0,'typename':'推荐','numb':0,'url':'','typedir':'','nowdir':''}]
            for result in resultlist:
                nowdir=None
                if typeid:
                    if str(typeid)==str(result[0]):
                        nowdir=1
                numb=numb+1
                id=result[0]
                typename=result[1]
                url=result[2]
                typedir=result[3]
                typedir=typedir.replace("{cmspath}/a/","")
                list={'id':id,'typeid':id,'typename':typename,'url':url,'numb':numb,'typedir':typedir,'nowdir':nowdir}
                listall.append(list)
            return listall
    def getmyorderlist(self):
        sql='select id,typename,keywords from dede_arctype where id not in (1,6,16,21,31,26) order by id asc limit 0,100'
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
    #----资讯列表(搜索引擎)
    def getnewslist(self,keywords="",frompageCount="",limitNum="",typeid="",typeid2="",allnum="",arg='',flag='',type='',MATCH=""):
        cl = SphinxClient()
        news=spconfig['name']['sex']['name']
        serverid=spconfig['name']['sex']['serverid']
        port=spconfig['name']['sex']['port']
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
            cl.SetSortMode( SPH_SORT_EXTENDED ,'pubdate desc' )
        if (allnum):
            cl.SetLimits (frompageCount,limitNum,allnum)
        else:
            cl.SetLimits (frompageCount,limitNum)
        if (keywords):
            if flag:
                res = cl.Query ('@(title,description) '+keywords+'&@(flag) "p"',news)
            else:
                if arg==1:
                    res = cl.Query ('@(title,description) '+keywords,news)
                else:
                    res = cl.Query ('@(title) '+keywords,news)
        else:
            if flag:
                res = cl.Query ('@(flag) "p"',news)
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
                    picone=None
                    picmore=None
                    content=None
                    if arrcontent:
                        content=arrcontent['content']
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
                        
                    murl="http://apptest.zz91.com/sex/newsdetail"+str(id)+".htm"
                    
                    title=attrs['ptitle']
                    click=arrcontent['click']
                    pcount=arrcontent['pcount']
                    fcount=arrcontent['fcount']
                    pubdate=attrs['pubdate']
                    typename=arrcontent['typename']
                    typeid=arrcontent['typeid']
                    typedir=arrcontent['typedir']
                    
                    pubdate2=time.strftime('%m/%d', time.localtime(pubdate))
                    list1={'title':title,'picone':picone,'picmore':picmore,'click':click,'id':id,'pubdate':pubdate2,'pcount':pcount,'fcount':fcount,'typename':typename,'typedir':typedir,'murl':murl,'litpic':litpic,'subcontent':subcontent.decode('utf-8','ignore')}
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
    def getsubcontent(self,id,len):
        sql="select body from dede_addonarticle where aid=%s"
        alist = self.dbn.fetchonedb(sql,[id])
        content=""
        if alist:
            content=alist[0]
            if content:
                content=subString(filter_tags(content),len)
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
    def getnewscontent(self,id):
        newscontent=cache.get("newscontent"+str(id))
        newscontent=None
        if (newscontent==None):
            #评论数
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
            typename=""
            if alist:
                title=alist[0]
                pubdate=int_to_strall(alist[1])
                click=alist[2]
                typeid=alist[3]
                #typedir=self.get_typedir(typeid)
                typevalue=self.get_typename(typeid)
                if typevalue:
                    typename=typevalue['typename']
                    typedir=typevalue['typedir']
            sql="select body from dede_addonarticle where aid=%s"
            alist = self.dbn.fetchonedb(sql,[id])
            content=""
            if alist:
                content=alist[0]
                content=content.replace("text-align: center", "")
                #content=getreplacepic(content)
                #content=replacepic(content)
            newscontent={'title':title.decode('utf-8','ignore'),'pubdate':pubdate,'content':content.decode('utf-8','ignore'),'typename':typename,'typeid':typeid,'typedir':typedir,'click':click,'pcount':pcount,'fcount':fcount}
            cache.set("newscontent"+str(id),newscontent,60*60)
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
            list={'title':title}
            return list
    #--根据mid获得发布人（member）信息
    def getmemberinfo(self,mid):
        sql="select mid,userid,uname,sex,face from dede_member where mid=%s"
        alist=self.dbn.fetchonedb(sql,[mid])
        if alist:
            mid=alist[0]
            userid=alist[1]
            uname=alist[2]
            sex=alist[3]
            face=alist[4]
            list={'mid':mid,'userid':userid,'uname':uname,'sex':sex,'face':face}
            return list
        
    #获得收藏夹列表(根据userid获得)
    def get_memebe_stom(self,mid="",frompageCount="",limitNum="",allnum=''):
        argument=[mid]
        sql1="select count(*) from dede_member_stow where mid=%s"
        sql="select id,mid,aid,title from dede_member_stow where mid=%s order by id desc limit "+str(frompageCount)+","+str(limitNum)+""
        listall=[]
        count=self.dbn.fetchnumberdb(sql1,argument)
        resultlist=self.dbn.fetchalldb(sql,argument)
        if resultlist:
            for result in resultlist:
                id=result[0]
                mid=result[1]
                aid=result[2]
                title=result[3]
                content=self.get_newslittlecontent(aid)
                
                list={'id':id,'mid':mid,'aid':aid,'title':title,'content':content}
                listall.append(list)
        return {'list':listall,'count':count}
            
            
    #过获得评论表
    def get_feedback(self,aid=None,mid=None,frompageCount="",limitNum="",allnum=''):
        argument=[]
        sqlarg=''
        if aid:
            sqlarg=' and aid=%s'
            argument.append(aid)
        if mid:
            sqlarg=' and mid=%s'
            argument.append(mid)
        sql1="select count(*) from dede_feedback where id>0"+sqlarg
        sql='select id,aid,mid,msg,bad,good from dede_feedback where id>0'+sqlarg+' limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbn.fetchnumberdb(sql1,argument)
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
                feedbackname=self.getmemberinfo(mid)['uname']
                list={'id':id,'aid':aid,'bad':bad,'good':good,'msg':msg,'feedbackname':feedbackname}
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
        sql='select id,aid,mid from view_history where id>0'+sqlarg+' limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbn.fetchnumberdb(sql1,argument)
        resultlist=self.dbn.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                aid=result[1]
                mid=result[2]
                content=self.get_newslittlecontent(aid)
                list={'id':id,'aid':aid,'content':content}
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
        sql="select id from view_history where aid=%s and deviceId=%s"
        result=self.dbn.fetchonedb(sql,[aid,deviceId])
        if result:
            a=1
            #sqlt="update view_history set gmt_created=%s where id=%s"
            #self.dbn.updatetodb(sqlt,[result[0]])
        else:
            sql='insert into view_history(mid,aid,gmt_created,deviceId) values(%s,%s,%s,%s)'
            self.dbn.updatetodb(sql,[mid,aid,gmt_created,deviceId])

