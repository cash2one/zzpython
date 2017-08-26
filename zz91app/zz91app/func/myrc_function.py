#-*- coding:utf-8 -*-
class zmyrc:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getviptype(self,company_id):
        sql='select membership_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #绑定的客户自动登录
    def weixinautologin(self,request,weixinid):
        if (weixinid and weixinid!=""):
            account=self.weixinbinding(weixinid)
            if account:
                company_id=self.getcompanyid(account)
                request.session.set_expiry(60*60*60)
                request.session['username']=account
                request.session['company_id']=company_id
                return 1
            else:
                return None
        else:
            return None
        #验证微信是否绑定
    def weixinbinding(self,weixinid):
        sql="select target_account from oauth_access where open_id=%s and target_account<>'0'"
        list=self.dbc.fetchonedb(sql,[weixinid]);
        if list:
            return list[0]
        else:
            return None
    #--获得公司id
    def getcompanyid(self,account):
        sql="select company_id from  company_account where account=%s"
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    #--获得登陆账号
    def getcompanyaccount(self,company_id):
        sql="select account from  company_account where company_id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #我的收藏夹
    def getfavoritelist(self,frompageCount="",limitNum="",company_id="",checkStatus=""):
        sqlarg=""
        if (checkStatus=="" or checkStatus==None):
            checkStatus=1
        print "checkStatus:",checkStatus
        if  checkStatus==1 or checkStatus=='1' :
            sqlarg=' (favorite_type_code=10091006 or favorite_type_code=10091000 or favorite_type_code=10091001 or favorite_type_code=10091007 ) '
        if  checkStatus=='2':
            sqlarg=" (favorite_type_code=10091002 or favorite_type_code=10091003) "
        if   checkStatus=='3':
            sqlarg=" favorite_type_code=10091004"
        if  checkStatus=='4':
            sqlarg=" favorite_type_code=10091005"
        if  checkStatus=='5':
            sqlarg=" favorite_type_code=10091012"
        sql="select count(0) from myfavorite where company_id=%s and"+sqlarg
        listall=None
        listcount=0
        alist=self.dbc.fetchonedb(sql,[company_id])
        if alist:
            listcount=alist[0]           
        sql2="select favorite_type_code,content_id,content_title,id from myfavorite where company_id=%s and "+sqlarg+" order by gmt_created desc limit "+str(frompageCount)+","+str(limitNum)+""
        aalist=self.dbc.fetchalldb(sql2,[company_id])
        listall=[]
        if alist:
            for list in aalist:
                favorite_type_code=list[0]
                content_id=list[1]
                content_title=list[2]
                id=list[3]
                favorite_url=None
                favorite_urls=None
                favorite_type=None
                if (favorite_type_code):
                    if (favorite_type_code=="10091006" or favorite_type_code=="10091000" or favorite_type_code=="10091001" or favorite_type_code=="10091007"):
                        favorite_type="供求信息"
                        favorite_url="/detail/?id="+str(content_id)
                        favorite_urls="/standard/productdetail/?pdtid="+str(content_id)
                    if (favorite_type_code=="10091002" or favorite_type_code=="10091003"):
                        favorite_type="公司信息"
                        favorite_url="/companyinfo/?company_id="+str(content_id)
                        favorite_urls="/standard/companyinfo/?company_id="+str(content_id)
                    if (favorite_type_code=="10091004" or favorite_type_code=="10091003"):
                        favorite_type="公司信息"
                        favorite_url="/companyinfo/?company_id="+str(content_id)
                        favorite_urls="/standard/companyinfo/?company_id="+str(content_id)
                    if (favorite_type_code=="10091004"):
                        favorite_type="报价信息"
                        favorite_url="/priceviews/?id="+str(content_id)
                        favorite_urls="/standard/priceviews/?id="+str(content_id)
                    if (favorite_type_code=="10091005"):
                        favorite_type="互助社区"
                        favorite_url="/huzhuview/"+str(content_id)+".htm"
                        favorite_urls="/standard/huzhuviews/"+str(content_id)+".htm"
                    if (favorite_type_code=="10091012"):
                        favorite_type="资讯"
                        favorite_url="/news/newsdetail"+str(content_id)+".html"
                        favorite_urls="/news/newsdetail"+str(content_id)+".html"
                
                
                lista={'id':id,'favorite_type_code':favorite_type_code,'favorite_type':favorite_type,'favorite_url':favorite_url,'favorite_urls':favorite_urls,'content_id':content_id,'content_title':content_title}
                listall.append(lista)
        return {'list':listall,'count':listcount}

    #保存定制
    def savecollect(self,company_id,keywords,gmt_created,collect_type,keywordslist=""):
        sql='select company_id from app_order where company_id=%s'
        alist=self.dbc.fetchonedb(sql,[company_id])
        if alist:
            if collect_type=='1':
                if keywords:
                    sql='update app_order set businesskeywords=%s,gmt_created=%s where company_id=%s'
                    self.dbc.updatetodb(sql,[keywords,gmt_created,company_id])
                if keywordslist:
                    sql='update app_order set businesskeywordslist=%s,gmt_created=%s where company_id=%s'
                    self.dbc.updatetodb(sql,[keywordslist,gmt_created,company_id])
            elif collect_type=='2':
                if keywords:
                    sql='update app_order set pricekeywords=%s,gmt_created=%s where company_id=%s'
                    self.dbc.updatetodb(sql,[keywords,gmt_created,company_id])
                if keywordslist:
                    sql='update app_order set pricekeywordslist=%s,gmt_created=%s where company_id=%s'
                    self.dbc.updatetodb(sql,[keywordslist,gmt_created,company_id])
        else:
            if collect_type=='1':
                if keywords:
                    sql='insert into app_order(businesskeywords,gmt_created,company_id) values(%s,%s,%s)'
                    self.dbc.updatetodb(sql,[keywords,gmt_created,company_id])
                if keywordslist:
                    sql='insert into app_order(businesskeywordslist,gmt_created,company_id) values(%s,%s,%s)'
                    self.dbc.updatetodb(sql,[keywordslist,gmt_created,company_id])
            elif collect_type=='2':
                if keywords:
                    sql='insert into app_order(pricekeywords,gmt_created,company_id) values(%s,%s,%s)'
                    self.dbc.updatetodb(sql,[keywords,gmt_created,company_id])
                if keywordslist:
                    sql='insert into app_order(pricekeywordslist,gmt_created,company_id) values(%s,%s,%s)'
                    self.dbc.updatetodb(sql,[keywordslist,gmt_created,company_id])
    #----商机定制主类
    def getcompanykeyword(self,id):
        sql="select title from data_index where id=%s"
        datalist=self.dbc.fetchonedb(sql,[id])
        if datalist:
            return datalist[0]
    #获得我的商机定制
    def get_mybusinesscollect(self,company_id):
        sql='select businesskeywords from app_order where company_id=%s'
        alist = self.dbc.fetchonedb(sql,[company_id])
        listall=[]
        if alist:
            keywords=alist[0]
            if keywords:
                keyword_list=keywords.split(',')
                for id in keyword_list:
                    keywd=self.getcompanykeyword(id)
                    listall.append({'keywords':keywd,'keywords_hex':getjiami(keywd)})
        if listall==[]:
            #从搜索关键字里读
            sql="select keywords from app_user_keywords where company_id=%s and ktype='trade'  order by id desc limit 0,5"
            alist = self.dbc.fetchonedb(sql,[company_id])
            listall=[]
            if alist:
                listall.append({'keywords':alist[0],'keywords_hex':getjiami(alist[0])})
            else:
                return None
        return listall
    #获得我的商机定制
    def get_mybusinesscollectid(self,company_id):
        sql='select businesskeywords from app_order where company_id=%s'
        alist = self.dbc.fetchonedb(sql,[company_id])
        listall=[]
        if alist:
            keywords=alist[0]
            if keywords:
                keyword_list=keywords.split(',')
                for id in keyword_list:
                    listall.append(id)
        return listall
    #获得我的商机定制
    def get_mypricecollectid(self,company_id):
        sql='select pricekeywords,pricekeywordslist from app_order where company_id=%s'
        alist = self.dbc.fetchonedb(sql,[company_id])
        listall=[]
        if alist:
            keywords=alist[0]
            keywordslist=alist[1]
            if keywordslist:
                keyword_list=keywordslist.split(',')
                for id in keyword_list:
                    listall.append(id)
                return listall
            if keywords:
                keyword_list=keywords.split(',')
                for id in keyword_list:
                    listall.append(id)
        return listall
    #获得我的行情定制
    def get_mypricecollect(self,company_id):
        sql='select pricekeywords,pricekeywordslist from app_order where company_id=%s'
        alist = self.dbc.fetchonedb(sql,[company_id])
        listall=[]
        if alist:
            keywords=alist[0]
            pricekeywords=alist[1]
            if pricekeywords:
                keyword_list=pricekeywords.split(',')
                for key in keyword_list:
                    list={'label':key}
                    listall.append(list)
                return listall
            if keywords:
                keyword_list=keywords.split(',')
                for id in keyword_list:
                    keywd=self.getpricecatename(id)
                    list={'label':keywd,'id':id}
                    listall.append(list)
        return listall
    
    #新版app我的行情定制
    def getmyorderprice(self,company_id):
        
        sql='select id,label,company_id,category_id,assist_id,keywords from app_order_price where company_id=%s'
        alistall = self.dbc.fetchalldb(sql,[company_id])
        listall=[]
        if alistall:
            for alist in alistall:
                list={'id':alist[0],
                      'label':alist[1],
                      'company_id':alist[2],
                      'category_id':alist[3],
                      'assist_id':alist[4],
                      'keywords':alist[5]}
                listall.append(list)
        """
        sql="select pricekeywords from app_order where company_id=%s"
        alistall = self.dbc.fetchonedb(sql,[company_id])
        if alistall:
            pricekeywords=alistall[0]
            if pricekeywords:
                keyword_list=pricekeywords.split(',')
                for id in keyword_list:
                    label=self.getpricecatename(id)
                    list={'id':0,
                      'label':label,
                      'company_id':company_id,
                      'category_id':id,
                      'assist_id':0,
                      'keywords':''}
                    listall.append(list)
        """
        return listall
    #新版app定制行情
    def savemyorderprice(self,list):
        company_id=list['company_id']
        label=list['label']
        category_id=list['category_id']
        assist_id=list['assist_id']
        keywords=list['keywords']
        gmt_created=datetime.datetime.now()
        value=[label,company_id,category_id,assist_id,keywords,gmt_created]
        sql="select id from app_order_price where company_id=%s and category_id=%s and label=%s and assist_id=%s and keywords=%s"
        alist = self.dbc.fetchonedb(sql,[company_id,category_id,label,assist_id,keywords])
        if not alist:
            sql="insert into app_order_price(label,company_id,category_id,assist_id,keywords,gmt_created) values(%s,%s,%s,%s,%s,%s)"
            result=self.dbc.updatetodb(sql,value)
            if result:
                return result[0]
            return '0'
        else:
            return None
    #新版app供求定制保存
    def savemyordertrade(self,list):
        company_id=list['company_id']
        otype=list['otype']
        timelimit=list['timelimit']
        keywordslist=list['keywordslist']
        provincelist=list['provincelist']
        gmt_created=datetime.datetime.now()
        value=[otype,company_id,timelimit,keywordslist,provincelist,gmt_created]
        sql="select id from app_order_trade where company_id=%s"
        alist = self.dbc.fetchonedb(sql,[company_id])
        if not alist:
            sql="insert into app_order_trade(type,company_id,timelimit,keywordslist,provincelist,gmt_created) values(%s,%s,%s,%s,%s,%s)"
            result=self.dbc.updatetodb(sql,value)
            if result:
                return result[0]
            return '0'
        else:
            sql="update app_order_trade set type=%s,timelimit=%s,keywordslist=%s,provincelist=%s where company_id=%s"
            result=self.dbc.updatetodb(sql,[otype,timelimit,keywordslist,provincelist,company_id])
            if result:
                return result[0]
            return '0'
    #新版app我的供求定制
    def getmyordertrade(self,company_id):
        sql='select id,type,company_id,timelimit,keywordslist,provincelist from app_order_trade where company_id=%s'
        alist = self.dbc.fetchonedb(sql,[company_id])
        list=None
        if alist:
            list={'id':alist[0],
                  'otype':alist[1],
                  'company_id':alist[2],
                  'timelimit':alist[3],
                  'keywordslist':alist[4],
                  'provincelist':alist[5]}
        return list
            
    #--价格分类
    def getpricecatename(self,id):
        sql="select name from price_category where id=%s"
        alist=self.dbc.fetchonedb(sql,[id])
        if alist:
            return alist[0]
    def getcate(self,categoryId):
        sql="select name,id from price_category where parent_id=%s and showflag=1"
        alist=self.dbc.fetchalldb(sql,str(categoryId))
        catestr=""
        if alist:
            listall=[]
            catestr="<table class='cate-tb-inner'><tr>"
            i=0
            for a in alist:
                id=a[1]
                name=a[0]
                list={'id':id,'name':name}
                mm=i % 2
                catestr=catestr+"<td><a href='/priceindex/?id="+str(id)+"&pname="+str(name)+"'><div class='c6'>"+str(name)+"</div></a></td>"
                if (str(mm) == "1"):
                    catestr=catestr+"</tr><tr>"
                i=i+1
            catestr=catestr+"</tr></table>"
        return catestr
    
    
                
    #----商机定制主类
    def getordercategorylistmain(self):
        sql="select label,code from data_index_category where code like '10161001____'"
        datalist=self.dbc.fetchalldb(sql)
        listall=[]
        for list in datalist:
            code=list[1]
            label=list[0]
            childlist=self.getordercategorylist(code)
            list1={'code':code,'label':label,'childlist':childlist}
            listall.append(list1)
        return listall
    #----定制商机子类别
    def getordercategorylist(self,code):
        sql="select title,id from data_index where category_code=%s order by sort asc"
        datalist=self.dbc.fetchalldb(sql,[code])
        listall=[]
        for list in datalist:
            title=list[0]
            id=list[1]
            list1={'title':title,'id':id}
            listall.append(list1)
        return listall
    #----更新弹窗
    def updateopenfloat(self,company_id,viewed):
        sql="select id from bbs_post_viewed where company_id=%s and bbs_post_id=0"
        resultlist=self.dbc.fetchonedb(sql,[company_id])
        gmt_created=datetime.datetime.now()
        if resultlist:
            sqlu="update bbs_post_viewed set is_viewed=%s,gmt_created=%s where company_id=%s and bbs_post_id=0"
            self.dbc.updatetodb(sqlu,[viewed,gmt_created,company_id])
        else:
            sqlu="insert into bbs_post_viewed(company_id,bbs_post_id,is_viewed,gmt_created) values(%s,%s,%s,%s)"
            self.dbc.updatetodb(sqlu,[company_id,0,viewed,gmt_created])
    #----获得昵称
    def getcompanynickname(self,company_id):
        sql='select nickname from bbs_user_profiler where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #--获得互助关注行业
    def gethuzhuguanzhu(self,company_id):
        sql='select guanzhu from bbs_user_profiler where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
        else:
            return ""
    #邀请问答
    def getbbs_invite(self,company_id):
        sql="select guanzhu from bbs_user_profiler where company_id=%s"
        returnlist=self.dbc.fetchonedb(sql,[company_id])
        if returnlist:
            guanzhu=returnlist[0]
        else:
            guanzhu=None
        if (guanzhu and guanzhu!=""):
            sql="select bbs_post_id,gmt_created from bbs_post_invite where guanzhu_id in (%s) and not exists(select post_id from bbs_invite where post_id=bbs_post_invite.bbs_post_id and company_id=%s and answercheck in (1,2,3)) and exists(select id from bbs_post where id=bbs_post_invite.bbs_post_id)"
            #sql="select a.id,a.title,a.company_id,a.content,b.gmt_created from bbs_post as a left join bbs_post_invite as b on a.id=b.bbs_post_id where b.guanzhu_id in (%s) and  not exists(select post_id from bbs_invite where post_id=a.id and company_id=%s and answercheck=1 and is_del=1)"
            sql=sql+"  limit 0,10 "
            returnlist=self.dbc.fetchalldb(sql,[guanzhu,company_id])
            listall=[]
            for list in returnlist:
                bbs_post_id=list[0]
                sqlb="select company_id,title,content from bbs_post where id=%s"
                returnone=self.dbc.fetchonedb(sqlb,[bbs_post_id])
                if returnone:
                    ccompany_id=returnone[0]
                    title=returnone[1]
                    nickname=self.getusername(ccompany_id)
                    if nickname==None:
                        nickname="匿名"
                    gmt_created=list[1]
    
                    is_viewed=None
                    sqlb="select is_viewed,answercheck,id from bbs_invite where company_id=%s and post_id=%s and answercheck in (0,1)"
                    returnone=self.dbc.fetchonedb(sqlb,[company_id,bbs_post_id])
                    if returnone:
                        is_viewed=returnone[0]
                        answercheck=returnone[1]
                        pid=returnone[2]
                        if answercheck==2:
                            is_viewed=2
                    else:
                        pid=0
                    
                    is_viewed=self.getpostviewed(company_id,bbs_post_id)
        
                    if is_viewed=="0":
                        is_viewed=None
                    
                    
                    ll={'id':pid,'post_id':bbs_post_id,'title':title,'company_id':company_id,'nickname':nickname,'gmt_created':formattime(gmt_created,2),'is_viewed':is_viewed}
                    listall.append(ll)
            return listall
    #--发布者 回复者
    def getusername(self,company_id):
        nickname=None
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
        else:
            sqlu="select contact from company_account where company_id=%s"
            ulist = self.dbc.fetchonedb(sqlu,[company_id])
            if ulist:
                nickname=ulist[0]
        return nickname
    #获得已读互助
    def getpostviewed(self,company_id,bbs_post_id):
        if company_id:
            sql="select id from bbs_post_viewed where company_id=%s and bbs_post_id=%s and is_viewed=1"
            resultlist=self.dbc.fetchonedb(sql,[company_id,bbs_post_id])
            if resultlist:
                return None
            else:
                return "1"
    #互助消息中心
    def getmessgelist(self,company_id,frompageCount,limitNum):
        mycompany_id=company_id
        sql1='select count(0) from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (a.company_id=%s or b.tocompany_id=%s)'
        result1=self.dbc.fetchonedb(sql1,[company_id,company_id])
        if result1:
            count=result1[0]
        else:
            count=0
        sql='select b.id,b.content,b.gmt_created,b.company_id,a.title,a.id,b.tocompany_id,a.reply_time from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (a.company_id=%s or b.tocompany_id=%s) order by a.reply_time desc limit %s,%s'
        resultlist=self.dbc.fetchalldb(sql,[company_id,company_id,frompageCount,limitNum])
        listall=[]
        if resultlist:
            for result in resultlist:
                company_id=result[3]
                post_id=result[5]
                reply_time=str(result[7])
                nickname=self.getusername(company_id)
                postviewed=self.getpostviewed(mycompany_id,post_id)
                list={'id':result[0],'title':result[1],'gmt_created':formattime(result[2],2),'nickname':nickname,'post_title':result[4],'company_id':company_id,'post_id':post_id,'postviewed':postviewed,'reply_time':reply_time}
                listall.append(list)
        return {'list':listall,'count':count}
    #我的回复
    def getmyquestion(self,company_id,frompageCount,limitNum):
        sql1='select count(0) from bbs_post where company_id=%s '
        result1=self.dbc.fetchonedb(sql1,[company_id])
        if result1:
            count=result1[0]
        else:
            count=0
        sql='select id,title,post_time,reply_count from bbs_post where company_id=%s  order by id desc limit %s,%s'
        resultlist=self.dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'title':result[1],'post_time':formattime(result[2],2),'reply_count':result[3]}
                listall.append(list)
        return {'list':listall,'count':count}
    #我的关注
    def getmygaunzhu(self,company_id,frompageCount,limitNum):
        sql1='select count(0) from bbs_post_notice_recommend where company_id=%s and type=1'
        result1=self.dbc.fetchonedb(sql1,[company_id])
        if result1:
            count=result1[0]
        else:
            count=0
        sql='select content_id,content_title,gmt_modified from bbs_post_notice_recommend where company_id=%s and type=1 order by id desc limit %s,%s'
        resultlist=self.dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'bbs_post_id':result[0],'title':result[1],'post_time':formattime(result[2],2)}
                listall.append(list)
        return {'list':listall,'count':count}
    #我的回复
    def getmyreply(self,company_id,frompageCount,limitNum):
        sql1='select count(0) from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (b.company_id=%s)'
        result1=self.dbc.fetchonedb(sql1,[company_id])
        if result1:
            count=result1[0]
        else:
            count=0
        sql='select b.id,b.content,b.gmt_created,a.company_id,a.title,a.reply_count,a.id from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (b.company_id=%s) order by b.gmt_created desc limit %s,%s'
        resultlist=self.dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
        listall=[]
        if resultlist:
            for result in resultlist:
                company_id=result[3]
                nickname=self.getusername(company_id)
                if nickname==None:
                    nickname="ZZ91管理员"
                reply_count=0
                if result[5]:
                    reply_count=result[5]
                list={'id':result[0],'post_id':result[6],'content':result[1],'gmt_created':formattime(result[2],2),'nickname':nickname,'post_title':result[4],'reply_count':reply_count}
                listall.append(list)
        return {'list':listall,'count':count}
    
    #询盘留言列表 翻页
    def getleavewordslist(self,frompageCount,limitNum,company_id,sendtype,group=""):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if (company_id):
            if sendtype=="1":
                cl.SetFilter('scomid',[int(company_id)])
            else:
                cl.SetFilter('rcomid',[int(company_id)])
            if group:
                cl.SetGroupBy( 'scomid',SPH_GROUPBY_ATTR )
            cl.SetSortMode( SPH_SORT_EXTENDED,"qid desc" )
            cl.SetLimits (frompageCount,limitNum,20000)
            res = cl.Query ('','question')
            if res:
                if res.has_key('matches'):
                    tagslist=res['matches']
                    listall=[]
                    for match in tagslist:
                        id=match['id']
                        list=self.getleavewords(id)
                        listall.append(list)
                    listcount=res['total_found']
        return {'list':listall,'count':listcount}
    def getchatlist(self,frompageCount=0,limitNum=1,company_id='',sendtype=''):
        sqlarg=''
        argument=[]
        account=getaccount(company_id)
        if company_id and str(company_id)!="0":
            if sendtype=="1":
                sqlarg+=' and sender_account=%s'
                argument.append(account)
            else:
                sqlarg+=' and receiver_account=%s'
                argument.append(account)
        else:
            return {'list':None,'count':0}
        sql1="select count(*) from inquiry where id>0 "+sqlarg
        sql="select id,conversation_group from inquiry where id>0 "+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        gmt_modified=datetime.datetime.now()
        for result in resultlist:
            id=result[0]
            chatgroup=result[1]
            if chatgroup:
                chatarr=chatgroup.replace("-",",")
                
                sqla="select chat_count,id from app_chat where chat_group=%s"
                resultq=self.dbc.fetchonedb(sqla,[chatarr])
                if resultq:
                    chat_count=resultq[0]
                    cid=resultq[1]
                    if chat_count:
                        #更新为已读
                        chat_countlist=eval(chat_count)
                        for ll in chat_countlist:
                            if str(ll)==str(company_id):
                                chat_countlist[ll]=0
                        chat_countarr=str(chat_countlist)
                        sqlb="update app_chat set gmt_modified=%s,chat_count=%s where id=%s"
                        self.dbc.updatetodb(sqlb,[gmt_modified,chat_countarr,cid]);
            
            list=self.getleavewords(id)
            listall.append(list)
        return {'list':listall,'count':count}
    #留言详细
    def getleavewords(self,qid):
        sql="select title,content,send_time,sender_account,id,is_viewed from inquiry where id=%s"
        alist=self.dbc.fetchonedb(sql,[qid])
        list=None
        if alist:
            companyarray=self.getcompanyname(alist[3])
            sqlt="update inquiry set is_viewed=1 where id=%s and is_viewed=0"
            self.dbc.updatetodb(sqlt,[alist[4]])
            list={'id':alist[4],'title':alist[0],'content':alist[1],'is_viewed':alist[5],'stime':formattime(alist[2],0),'companyarray':companyarray}
        return list
    #获得公司名称
    def getcompanyname(self,uname):
        sql="select company_id from company_account where account=%s"
        newcode=self.dbc.fetchonedb(sql,[uname])
        if (newcode):
            company_id=newcode[0]
            sqlc="select name from company where id=%s"
            clist=self.dbc.fetchonedb(sqlc,[company_id])
            if clist:
                return {'company_id':company_id,'companyname':clist[0]}
    #----生意管家 供求管理
    def getmyproductslist(self,frompageCount="",limitNum="",company_id="",checkStatus=""):
        if (checkStatus=="" or checkStatus==None):
            checkStatus=1
        checkStatus=str(checkStatus)
        if checkStatus=="3":
            sql="select count(0) from products where company_id=%s and is_pause=1 and is_del=0"
            alist=self.dbc.fetchonedb(sql,[company_id])
        else:
            sql="select count(0) from products where company_id=%s and check_status=%s and is_pause=0 and is_del=0"
            alist=self.dbc.fetchonedb(sql,[company_id,int(checkStatus)])
        if alist:
            listcount=alist[0]
        if checkStatus=="3":
            sql="select id,title,real_time,refresh_time,unpass_reason from products where company_id=%s and is_pause=1 and is_del=0 order by refresh_time desc limit "+str(frompageCount)+","+str(limitNum)+""
            alist=self.dbc.fetchalldb(sql,[company_id])
        else:
            sql="select id,title,real_time,refresh_time,unpass_reason from products where company_id=%s and check_status=%s and is_pause=0 and is_del=0 order by refresh_time desc limit "+str(frompageCount)+","+str(limitNum)+""
            alist=self.dbc.fetchalldb(sql,[company_id,int(checkStatus)])
        listall=[]
        if alist:
            for list in alist:
                unpass_reason=list[4]
                rlist={'proid':list[0],'protitle':list[1],'real_time':formattime(list[2],0),'refresh_time':formattime(list[3],0),'unpass_reason':unpass_reason}
    #            list=getcompinfo(proid,cursor,None)
                listall.append(rlist)
        return {'list':listall,'count':listcount}
    #我的企业报价
    def mycompanyprice(self,frompageCount="",limitNum="",company_id="",is_checked=""):
        argument=[company_id]
        sqlm=''
        if is_checked:
            sqlm=sqlm+"and a.is_checked=%s"
            argument.append(is_checked)
        sql="select count(0) from company_price as a where a.company_id=%s "+sqlm
        alist=self.dbc.fetchonedb(sql,argument)
        listcount=alist[0]
        sql="select a.product_id,a.title,a.price,a.price_unit,a.min_price,a.max_price,a.area_code,a.details,a.is_checked,a.post_time,b.label,a.company_id,c.label,a.category_company_price_code,d.name,a.id from company_price as a left join category as b on left(a.area_code,16)=b.code left join category as c on left(a.area_code,12)=c.code left join company as d on d.id=a.company_id where a.company_id=%s "+sqlm+" limit "+str(frompageCount)+","+str(limitNum)+""
        result=self.dbc.fetchalldb(sql,argument)
        listall=[]
        if result:
            for list in result:
                product_id=list[0]
                title=list[1]
                price=list[2]
                price_unit=list[3]
                min_price=list[4]
                max_price=list[5]
                rprice=''
                if price:
                    rprice=price
                if min_price:
                    rprice=min_price
                if max_price:
                    rprice=rprice+"-"+max_price
                price=rprice
                is_checked=list[6]
                if is_checked==1:
                    checktxt="已审核"
                else:
                    checktxt="<font color=red>未审核</font>"
                details=list[7]
                post_time=formattime(list[9],0)
                city=list[10]
                province=list[12]
                company_id=list[11]
                category_company_price_code=list[13]
                companyname=list[14]
                id=list[15]
                clabel=''
                sql2='select label from category_company_price where code=%s'
                alist2 = self.dbc.fetchonedb(sql2,[category_company_price_code])
                if alist2:
                    clabel=alist2[0]
                pricelist={'id':id,'product_id':product_id,'checktxt':checktxt,'title':title,'price':price,'price_unit':price_unit,'post_time':post_time,'city':city,'company_id':company_id,'province':province,'category_company_price_code':category_company_price_code,'companyname':companyname,'clabel':clabel}
                listall.append(pricelist)
        return {'list':listall,'count':listcount}
        
    def getcategoryname(self,code):
        #获得缓存
        zz91app_getcategoryname=cache.get("zz91app_getcategoryname"+str(code))
        if zz91app_getcategoryname:
            return zz91app_getcategoryname
        sql="select label from category_products where code=%s"
        catevalue=self.dbc.fetchonedb(sql,[code])
        if catevalue:
            #设置缓存
            cache.set("zz91app_getcategoryname"+str(code),catevalue[0],60*10)
            return catevalue[0]
    #----根据id查询1条供求
    def getmyproductsbyid(self,id):
        sql="select id,title,quantity,quantity_unit,price,price_unit,details,category_products_main_code,products_type_code,expire_time from products where id=%s"
        list=self.dbc.fetchonedb(sql,[id])
        if list:
            validity=list[9]
            vali="长期（一年内）"
            if validity=="-1":
                vali="长期（一年内）"
            if validity=="90":
                vali="三个月"
            if validity=="60":
                vali="二个月"
            if validity=="10":
                vali="十天"
            categoryname=self.getcategoryname(list[7])
            alist={'id':list[0],'title':list[1],'quantity':list[2],'quantity_unit':list[3],'price':list[4],'price_unit':list[5],'details':list[6],'categorycode':list[7],'categoryname':categoryname,'products_type_code':list[8],'validity':vali,'validitycode':formattime(validity,0)}
            return alist
    #产品图片
    def getmyproductspic(self,id):
        sql1="select pic_address,check_status,id from products_pic where product_id=%s"
        productspic=self.dbc.fetchalldb(sql1,[id])
        piclist=[]
        if productspic:
            for p in productspic:
                pimages=p[0]
                check_status=p[1]
                pid=p[2]
                if (pimages == '' or pimages == '0' or pimages==None):
                    pdt_images='../cn/img/noimage.gif'
                    pdt_images_big='../cn/img/noimage.gif'
                else:
                    pdt_images="http://img3.zz91.com/135x135/"+pimages+""
                    pdt_images_big="http://img3.zz91.com/800x800/"+pimages+""
                picurl={'images':pdt_images,'images_big':pdt_images_big,'check_status':check_status,'id':pid}
                piclist.append(picurl)
        return piclist
    #我的通讯录
    def getmyaddressbooklist(self,frompageCount="",limitNum="",company_id=""):
        sqlarg=""
        sql="select count(0) from company_addressbook where company_id=%s "+sqlarg
        listcount=0
        alist=self.dbc.fetchonedb(sql,[company_id])
        if alist:
            listcount=alist[0]           
        sql2="select forcompany_id,bz from company_addressbook where company_id=%s "+sqlarg+" order by id desc limit "+str(frompageCount)+","+str(limitNum)+""
        aalist=self.dbc.fetchalldb(sql2,[company_id])
        listall=[]
        if alist:
            for list in aalist:
                forcompany_id=list[0]
                contact=""
                position=""
                sql="select contact,sex,position from company_account where company_id=%s"
                alist=self.dbc.fetchonedb(sql,[forcompany_id])
                if alist:
                    contact=alist[0]
                    sex=alist[1]
                    position=alist[2]
                    if str(sex)=="0":
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="先生"
                    else:
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="女士"
                    if (position==None):
                        position=""
                    position=position.strip()
                compname=""
                sqlc="select name from company where id=%s"
                clist=self.dbc.fetchonedb(sqlc,[forcompany_id])
                if clist:
                    compname=clist[0]
                bz=list[1]
                faceurl=None
                sql="select picture_path from bbs_user_profiler where company_id=%s"
                piclist=dbc.fetchonedb(sql,[forcompany_id])
                faceurl=None
                if piclist:
                    if piclist[0]:
                        if piclist[0]:
                            faceurl="http://img3.zz91.com/100x100/"+piclist[0]
                lista={'company_id':forcompany_id,'contact':contact,'position':position,'compname':compname,'faceurl':faceurl}
                listall.append(lista)
        return {'list':listall,'count':listcount}
    