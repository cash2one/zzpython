#-*- coding:utf-8 -*-
class zzhuzhu:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #最新互助信息 翻页
    def getbbslist(self,kname='',frompageCount=0,limitNum=1,category_id='',fromtime='',endtime='',datetype='',check_status='',company_id='',htype="",bbs_post_assist_id=""):
        catelist=self.getbbs_categorys(category_id)
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetFilter('is_del',[0])
        if category_id:
            cl.SetFilter('bbs_post_category_id',catelist)
        if check_status:
            cl.SetFilter('check_status',[int(check_status)])
        else:
            cl.SetFilter('check_status',[1,2])
        if company_id:
            cl.SetFilter('company_id',[int(company_id)])
        if fromtime and endtime:
            cl.SetFilterRange('reply_time',fromtime,endtime)
        if bbs_post_assist_id:
            cl.SetFilter('bbs_post_assist_id',[int(bbs_post_assist_id)])
        if htype:
            if (htype=="hot"):
                cl.SetSortMode( SPH_SORT_EXTENDED,"reply_count desc,reply_time desc" )
            if (htype=="new"):
                cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
            if (htype=="guanzhu"):
                cl.SetSortMode( SPH_SORT_EXTENDED,"notice_count desc,reply_time desc" )
        else:
            cl.SetSortMode( SPH_SORT_EXTENDED,"reply_time desc,post_time desc" )
        """
        if (datetype==1):
            cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc,reply_time desc" )
        if (datetype in (2,3)):
            cl.SetSortMode( SPH_SORT_EXTENDED,"reply_count desc" )
        """
        cl.SetLimits (frompageCount,limitNum,20000)
        if (kname):
            res = cl.Query ('@(title,tags) '+kname,'huzhu')
        else:
            res = cl.Query ('','huzhu')
        listall=[]
        listcount=0
        if res:
            if res.has_key('matches'):
                listcount=res['total_found']
                tagslist=res['matches']
                i=0
                for match in tagslist:
                    id=match['id']
                    bbscontent=self.getbbscontent(id)
                    if bbscontent:
                        bbscontent['num']=i
                        if not bbscontent['title']:
                            bbscontent['title']=bbscontent['content']
                        if limitNum==1:
                            bbscontent['count']=listcount
                            bbscontent['txt']='最新互助问答信息'
                            
                            return bbscontent
                        i+=1
                        listall.append(bbscontent)
        if limitNum==1:
            return ''
        return {'list':listall,'count':listcount}
    #--发布者 回复者
    def getusername(self,company_id):
        if company_id==0:
            return '再生君'
        uusername=cache.get("mobile_username"+str(company_id))
        if uusername:
            return uusername
        nickname=None
        """
        sqlu="select nickname,account from bbs_user_profiler where company_id=%s"
        ulist = self.dbc.fetchonedb(sqlu,[company_id])
        if ulist:
            nickname= ulist[0]
            account=ulist[1]
            if (nickname==None or nickname==account):
                sqlu="select contact from company_account where company_id=%s"
                ulist = self.dbc.fetchonedb(sqlu,[company_id])
                if ulist:
                    nickname=ulist[0]
        
        """
        sqlu="select contact from company_account where company_id=%s"
        ulist = self.dbc.fetchonedb(sqlu,[company_id])
        if ulist:
            nickname=ulist[0]
        else:
            nickname=''
        cache.set("mobile_username"+str(company_id),nickname,60*60*24)
        return nickname
    #--回复数
    def gethuzhureplaycout(self,bbs_post_id):
        sqlr="select count(0) from bbs_post_reply where bbs_post_id=%s and is_del='0' and check_status in ('1','2')"
        rlist = self.dbc.fetchonedb(sqlr,str(bbs_post_id))
        if rlist:
            return rlist[0]
    #--我的回复数
    def getmyhuzhureplaycout(self,account):
        sqlr="select count(0) from bbs_post_reply where account=%s and check_status in ('1','2')"
        rlist = self.dbc.fetchonedb(sqlr,str(account))
        if rlist:
            return rlist[0]
    #----获得昵称
    def getcompanynickname(self,company_id):
        sql='select nickname from bbs_user_profiler where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #----获得互助关注行业
    def gethuzhuguanzhu(self,company_id):
        sql='select guanzhu from bbs_user_profiler where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
        else:
            return ""
    def addmyzhuzhuguanzhu(self,myguanzhu,company_id,account):
        sqla="select id from bbs_user_profiler where company_id=%s"
        result=self.dbc.fetchonedb(sqla,[company_id])
        tt=""
        if myguanzhu:
            for t in myguanzhu:
                tt=tt+t+","
            myguanzhu=tt[:-1]
        else:
            myguanzhu=""
        gmt_created=gmt_modified=datetime.datetime.now()
        if result:
            sql='update bbs_user_profiler set guanzhu=%s,gmt_modified=%s where company_id=%s'
            self.dbc.updatetodb(sql,[str(myguanzhu),gmt_modified,company_id])
        else:
            value=[company_id,account,str(myguanzhu),gmt_created,gmt_modified]
            sql='insert into bbs_user_profiler (company_id,account,guanzhu,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)'
            self.dbc.updatetodb(sql,value)
    #替换可拨打电话
    def replacetel(self,content):
        if content:
            rpl1=re.findall('[0-9\ ]+',content)
            for r1 in rpl1:
                if len(r1)>10 and len(r1)<=12:
                    if 'tel:' in r1:
                        content=content
                    else:
                        content=content.replace(r1,'<a href="tel:'+r1+'">'+r1+'</a>')
        return content
    def replaceurl(self,content):
        return remove_content_a(content)
        if content:
            regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)
            s=regex.findall(content)
            for l in s:
                if 'http://' in l:
                    content=content
                else:
                    content=content.replace(l,"<a href=javascript:openurlblank('"+l+"?&')>"+l+"</a>")
        return content
        #s=regex.sub('<a href=>'+content+'</a>',content)#去掉CDATA
    #----回复列表
    def replylist(self,postid,frompageCount,limitNum):
        sql="select account,title,content,gmt_created,company_id,id from bbs_post_reply where bbs_post_id=%s and is_del='0' and check_status in ('1','2') and bbs_post_reply_id=0 order by gmt_created desc limit %s,%s"
        alist = self.dbc.fetchalldb(sql,[postid,frompageCount,limitNum])
        listall_reply=[]
        if alist:
            i=0
            for list in alist:
                reply_id=list[5]
                accountr=list[0]
                company_id=list[4]
                nicknamer=self.getusername(company_id)
                facepic=self.getfacepic(company_id)
                titler=list[1]
                contentr=list[2]
                contentr=self.replaceurl(contentr)
                contentr=self.replacetel(contentr)
                gmt_createdr=formattime(list[3],0)
                relist=self.replyreplylist(reply_id,0,10)
                i+=1
                list={'reply_id':reply_id,'facepic':facepic,'title':titler,'nickname':nicknamer,'content':contentr,'posttime':gmt_createdr,'replylist':relist,'i':frompageCount+i,'post_id':postid,'company_id':company_id}
                listall_reply.append(list)
        return listall_reply
    #----回复回复
    def replyreplylist(self,replyid,frompageCount,limitNum):
        sql="select account,title,content,gmt_created,company_id,id,tocompany_id from bbs_post_reply where bbs_post_reply_id=%s and is_del='0' and check_status in ('1','2') order by gmt_created desc limit %s,%s"
        alist = self.dbc.fetchalldb(sql,[str(replyid),frompageCount,limitNum])
        listall={'list':'','count':''}
        listall_reply=[]
        i=0
        if alist:
            for list in alist:
                reply_id=list[5]
                accountr=list[0]
                company_id=list[4]
                tocompany_id=list[6]
                nicknamer=self.getusername(company_id)
                tonickname=self.getusername(tocompany_id)
                facepic=self.getfacepic(company_id)
                tofacepic=self.getfacepic(tocompany_id)
                titler=list[1]
                contentr=list[2]
                contentr=self.replaceurl(contentr)
                contentr=self.replacetel(contentr)
                gmt_createdr=formattime(list[3],0)
                i+=1
                list={'reply_id':reply_id,'facepic':facepic,'tofacepic':tofacepic,'title':titler,'nickname':nicknamer,'content':contentr,'posttime':gmt_createdr,'company_id':company_id,'tonickname':tonickname,'tocompany_id':tocompany_id,'i':i}
                listall_reply.append(list)
        listall['list']=listall_reply
        if i>10:
            listall['count']=1
        else:
            listall['count']=None
        return listall
    def getprofilerid(self,account):
        sql="select id from bbs_user_profiler where account=%s"
        newcode=self.dbc.fetchonedb(sql,[account])
        if (newcode == None):
            return '0'
        else:
            return newcode[0]
    #获得头像
    def getfacepic(self,company_id):
        sql="select picture_path from bbs_user_profiler where company_id=%s"
        newcode=self.dbc.fetchonedb(sql,[company_id])
        if (newcode == None):
            return 'http://static.m.zz91.com/aui/images/noavatar.gif'
        else:
            if newcode[0]:
                return 'http://img3.zz91.com/200x15000/'+newcode[0]
            else:
                return 'http://static.m.zz91.com/aui/images/noavatar.gif'
    def getbbslistone(self):
        sql="select id,title from bbs_post where is_del=0 and check_status in (1,2) order by id desc "
        bbslist=self.dbc.fetchonedb(sql)
        if bbslist:
            return {'id':bbslist[0],'title':bbslist[1]}
        else:
            return ''
    def getbbscontent(self,id,showcontent=""):
        bbscontent=cache.get("mobile_bbspostcontent"+str(id)+"-"+str(showcontent))
        if (bbscontent==None):
            sql="select content,account,company_id,reply_time,title,post_time,notice_count,recommend_count,collect_count,visited_count,bbs_post_category_id from bbs_post where id=%s"
            alist = self.dbc.fetchonedb(sql,[id])
            if alist:
                content=alist[0]
                if alist[0]:
                    content=subString(filter_tags(alist[0]),150)
                contentall=""
                if showcontent:
                    contentall=alist[0]
                    contentall=remove_script(contentall)
                    #contentall=remove_content_a(contentall)
                company_id=alist[2]
                #黑名单客户
                if company_id:
                    sql="select id from company where is_block=1 and id=%s"
                    result=self.dbc.fetchonedb(sql,[company_id])
                    if result:
                        return None
                username=self.getusername(alist[2])
                title=alist[4]
                gmt_time=str(formattime(alist[5],0))
                reply_time=str(formattime(alist[3],0))
                #头像
                facepic=self.getfacepic(company_id)
                piclist=self.getbbspiclist("bbs_post",id)
                
                recommend_count=alist[7]
                if not recommend_count:
                    recommend_count=0
                visited_count=alist[9]
                if not visited_count:
                    visited_count=0
                notice_count=alist[6]
                if not notice_count:
                    notice_count=0
                collect_count=alist[8]
                if not collect_count:
                    collect_count=0
                if not title:
                    title=""
                bbs_post_category_id=alist[10]
                if bbs_post_category_id==106:
                    title=""
                replycount=self.gethuzhureplaycout(id)
                bbscontent={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'nickname':username,'replycount':replycount,'reply_time':reply_time,'notice_count':notice_count,'recommend_count':recommend_count,'collect_count':collect_count,'visited_count':visited_count,'company_id':company_id,'facepic':facepic,'piclist':piclist,'contentall':contentall,'bbs_post_category_id':bbs_post_category_id}
                cache.set("mobile_bbspostcontent"+str(id)+"-"+str(showcontent),bbscontent,60*30)
        return bbscontent
    #置顶信息
    def gettopbbslist(self,code):
        if code:
            sql="select link from data_index where category_code=%s  order by id desc limit 0,3"
            bbslist=self.dbc.fetchalldb(sql,[code])
            if bbslist:
                listall=[]
                for list in bbslist:
                    link=list[0]
                    bbsid=link.replace("http://huzhu.zz91.com/detail/","").replace(".html","")
                    clist=self.getbbscontent(bbsid)
                    listall.append(clist)
                return listall
            else:
                return None
        else:
            return None
    #获得互助图片
    def getbbspiclist(self,source,source_id):
        sql="select path from other_piclist where source_id=%s and source=%s"
        bbslist=self.dbc.fetchalldb(sql,[source_id,source])
        if bbslist:
            listall=[]
            for list in bbslist:
                path=list[0]
                picurl={'file_path':'http://img3.zz91.com/300x15000/'+path}
                listall.append(picurl)
            return listall
        return []
    #----互助加点击数
    def huzhuclick_add(self,id):
        sql="update bbs_post set visited_count=visited_count+1 where id=%s"
        dbc.updatetodb(sql,[id])
    #是否已经关注
    def isnotice(self,content_id,company_id,type):
        if company_id:
            sql="select id,state from bbs_post_notice_recommend where content_id=%s and company_id=%s and type=%s order by gmt_modified desc"
            result=dbc.fetchonedb(sql,[content_id,company_id,type])
            if result:
                state=result[1]
                return state
            else:
                return 1
        else:
            return 1
    #朋友圈列表
    def getquanlist(self,company_id,frompageCount,limitNum):
        sql="select a.id from bbs_post as a inner join company_addressbook as b on a.company_id=b.forcompany_id and (b.company_id=%s or a.company_id=%s) and a.check_status=1 and a.is_del=0 order by a.gmt_created desc limit %s,%s"
        result=self.dbc.fetchalldb(sql,[company_id,company_id,frompageCount,limitNum])
        listall=[]
        if result:
            for list in result:
                id=list[0]
                bbscontent=self.getbbscontent(id)
                if bbscontent:
                    if not bbscontent['title']:
                        bbscontent['title']=bbscontent['content']
                replylist=self.replylist(id,0,10)
                bbscontent['replylist']=replylist
                listall.append(bbscontent)
        return listall
    #获取小类
    def getbbs_post_categorys(self,cid):
        if (cid==106 or cid==1 or not cid):
            navlist=[{'name':'最新商机','category_id':cid,'htype':'new','bbs_post_assist_id':''},{'name':'热门关注','category_id':cid,'htype':'guanzhu','bbs_post_assist_id':''},{'name':'热门回复','category_id':cid,'htype':'hot','bbs_post_assist_id':''}]
            return navlist
        sql="select id,name from bbs_post_categorys where parent_id=%s and state=0"
        result=self.dbc.fetchalldb(sql,[cid])
        listall=[]
        if result:
            for list in result:
                id=list[0]
                name=list[1]
                l={'category_id':cid,'name':name,'bbs_post_assist_id':id,'htype':''}
                listall.append(l)
        return listall
    def getbbs_categorys(self,cid):
        listall=cache.get("app_getbbs_categorys"+str(cid))
        if listall:
            return listall
        listall=[]
        if cid:
            sql="select id from bbs_post_categorys where parent_id=%s and state=0"
            result=self.dbc.fetchalldb(sql,[cid])
            listall.append(int(cid))
            if result:
                for list in result:
                    id=int(list[0])
                    listall.append(id)
                    sql1="select id from bbs_post_categorys where parent_id=%s and state=0"
                    result1=self.dbc.fetchalldb(sql1,[id])
                    if result1:
                        for list1 in result1:
                            id1=int(list1[0])
                            listall.append(id1)
        cache.set("app_getbbs_categorys"+str(cid),listall,60*60*24)
        return listall