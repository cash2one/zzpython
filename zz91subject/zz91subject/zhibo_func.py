#-*- coding:utf-8 -*-
class zhibofun:
    def __init__(self):
        self.dbc=dbc
        self.dbn=dbn
    #展会直播列表
    def getzhibolist(self,frompageCount,limitNum,ztype="",orderflag="",bbs_post_id=''):
        argument=[]
        sqlarg=' from subject_zhibo where id>0 '
        if bbs_post_id:
            sqlarg+=' and bbs_post_id=%s'
            argument.append(bbs_post_id)
        if ztype:
            sqlarg+=' and ztype=%s'
            argument.append(ztype)
        sqlc='select count(0)'+sqlarg
        sql='select id,content,gmt_created,title'+sqlarg
        if (str(orderflag)=="1"):
            sql+=' order by gmt_created desc '
        else:
            sql+=' order by gmt_created asc '
        sql+='limit %s,%s'
        count=self.dbc.fetchnumberdb(sqlc,argument)
        argument.append(frompageCount)
        argument.append(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            content=result[1]
            if content:
                content=content.replace("http://img1.zz91.com","http://img3.zz91.com/600x600")
            gmt_created=result[2]
            title=result[3]
            imglist=self.get_img_url(content)
            imgone=None
            if imglist:
                imgone=imglist[0]
            gmtdate=formattime(gmt_created,1)
            gmthoure=gmt_created.strftime('%H:%M')
            litcontent=subString(filter_tags(content),200)
            list={'id':id,'title':title,'litcontent':litcontent,'gmtdate':gmtdate,'gmthoure':gmthoure,'imgone':imgone}
            listall.append(list)
        return {'list':listall,'count':count}
    #---回复列表
    def replylist(self,postid,frompageCount,limitNum):
        visited_count=0
        sql="select visited_count from bbs_post where id=%s"
        result=dbc.fetchonedb(sql,[postid])
        if result:
            visited_count=result[0]
        rcount=0
        sql="select count(0) from bbs_post_reply where bbs_post_id=%s and is_del='0' and check_status in ('1','2') "
        result=dbc.fetchonedb(sql,[postid])
        if result:
            rcount=result[0]
        sql="select account,title,content,gmt_created,company_id,id,tocompany_id from bbs_post_reply where bbs_post_id=%s and is_del='0' and check_status in ('1','2') order by gmt_created desc limit %s,%s"
        alist=dbc.fetchalldb(sql,[postid,frompageCount,limitNum])
        listall_reply=[]
        if alist:
            i=0
            for list in alist:
                reply_id=list[5]
                accountr=list[0]
                company_id=list[4]
                nicknamer=self.getusername(company_id)
                titler=list[1]
                contentr=list[2]
                #contentr=replacetel(contentr)
                contentr=self.replaceurl(contentr)
                gmt_createdr=formattime(list[3],0)
                relist=""
                tocompany_id=list[6]
                tonickname=""
                if str(tocompany_id)!="0":
                    tonickname=self.getusername(tocompany_id)
                    if tonickname:
                        nicknamer=nicknamer+" 回复  "+tonickname
                #relist=self.replyreplylist(reply_id,0,10)
                i+=1
                list={'reply_id':reply_id,'title':titler,'nickname':nicknamer,'content':contentr,'posttime':gmt_createdr,'replylist':relist,'i':frompageCount+i,'post_id':postid,'company_id':company_id}
                listall_reply.append(list)
        return {'list':listall_reply,'visited_count':visited_count,'count':rcount}
    #----回复回复
    def replyreplylist(self,replyid,frompageCount,limitNum):
        sql="select account,title,content,gmt_created,company_id,id,tocompany_id from bbs_post_reply where bbs_post_reply_id=%s and is_del='0' and check_status in ('1','2') order by gmt_created desc limit %s,%s"
        alist=dbc.fetchalldb(sql,[str(replyid),frompageCount,limitNum])
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
                titler=list[1]
                contentr=list[2]
                #contentr=replacetel(contentr)
                contentr=self.replaceurl(contentr)
                gmt_createdr=formattime(list[3],0)
                i+=1
                list={'reply_id':reply_id,'title':titler,'nickname':nicknamer,'content':contentr,'posttime':gmt_createdr,'company_id':company_id,'tonickname':tonickname,'tocompany_id':tocompany_id,'i':i}
                listall_reply.append(list)
        listall['list']=listall_reply
        if i>10:
            listall['count']=1
        else:
            listall['count']=None
        return listall
    #--发布者 回复者
    def getusername(self,company_id):
        nickname=None
        sqlu="select contact from company_account where company_id=%s"
        ulist=dbc.fetchonedb(sqlu,[company_id])
        if ulist:
            nickname=ulist[0]
        return nickname
    def replaceurl(self,content):
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
                if "http://" in l:
                    content=content
                else:
                    content=content.replace(l,"<a href='"+l+"'>"+l+"</a>")
        return content
    #----互助加点击数
    def huzhuclick_add(self,id):
        sql="update bbs_post set visited_count=visited_count+1 where id=%s"
        dbc.updatetodb(sql,[id])
        return 1
    def getaccount(self,company_id):
        sql="select account from company_account where company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
        else:
            return ''
    #----回复帖子
    def huzhu_replay(self,request):
        bbs_post_id = request.POST.get('bbs_post_id')
        replyid=request.POST.get('replyid')
        tocompany_id = request.POST.get('tocompany_id')
        title=request.POST.get('title')
        content = request.POST.get('content')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        company_id = request.POST.get('company_id')
        username=self.getaccount(company_id)
        
        if (content and content!=""):
            value=[company_id,tocompany_id,username,title,bbs_post_id,content,0,1,gmt_created,gmt_modified,1,replyid]
            sql="insert into bbs_post_reply(company_id,tocompany_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,postsource,bbs_post_reply_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,value)
            sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
            dbc.updatetodb(sql,[gmt_modified,gmt_modified,bbs_post_id])
    #再生汇签到客户
    def zsh_qiandaolist(self,frompageCount,limitNum,ztype=''):
        sql="select id,zheng_no,companyname,contact,business,qiandaotime from zsh_list where ztype=%s and isqiandao=1"
        sql=sql+' order by qiandaotime desc limit %s,%s'
        result=dbc.fetchalldb(sql,[ztype,frompageCount,limitNum])
        listall=[]
        if result:
            for list in result:
                id=list[0]
                zheng_no=list[1]
                companyname=list[2]
                contact=list[3]
                business=list[4]
                qiandaotime=formattime(list[5],0)
                l={'id':id,'zheng_no':zheng_no,'companyname':companyname,'contact':contact,'business':business,'qiandaotime':qiandaotime}
                listall.append(l)
        return listall
    #----新闻列表
    def getnewslist(self,keywords="",frompageCount='',limitNum='',typeid="",typeid2=""):
        sql='select id,title,pubdate,litpic from dede_archives where id>0'
        argument=[]
        if typeid:
            sql+=" and typeid=%s"
            argument.append(typeid)
        if typeid2:
            sql+=" and typeid2=%s"
            argument.append(typeid2)
        sql+=" order by pubdate desc"
        sql+=" limit %s,%s"
        argument.append(frompageCount)
        argument.append(limitNum)
        result=dbn.fetchalldb(sql,argument)
        listall_news=[]
        for list in result:
            id=list[0]
            title=list[1]
            pubdate=list[2]
            content=self.getnewcontent(id)
            imglist=self.get_img_url(content)
            imgone=None
            if imglist:
                imgone=imglist[0]
                if "zz91.com" not in imgone and "http" not in imgone:
                    imgone=imgone.replace("uploads/uploads/","")
                    imgone="http://imgnews.zz91.com"+imgone
            newsurl=self.get_newstype(id=id)
            weburl=''
            if newsurl:
                weburl="/"+newsurl["url"]+"/"+str(id)+".html"
            litcontent=subString(filter_tags(content),500)
            list1={'title':title,'litcontent':litcontent,'id':id,'pubdate':int_to_str2(pubdate),'imgone':imgone,'weburl':weburl}
            listall_news.append(list1)
        return listall_news
    #新闻内容
    def getnewcontent(self,id,nohtml=''):
        sql='select body from dede_addonarticle where aid=%s'
        result1=dbn.fetchonedb(sql,id)
        if result1:
            body=result1[0]
            if nohtml:
                body=filter_tags(body)
            return body
    #----获取资讯url
    def get_newstype(self,id='',typeid=''):
        
        if id:
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
            