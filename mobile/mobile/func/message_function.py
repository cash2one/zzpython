#-*- coding:utf-8 -*-
class zzmessage:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #----系统推送消息数量
    def getmessagecount(self,company_id):
        sql="select count(0) from app_message where company_id in (0,%s) and not exists(select mid from app_message_view where mid=app_message.id and company_id=%s and is_views=1)"
        count=self.dbc.fetchnumberdb(sql,[company_id,company_id])
        
        return count
    #更新消息状态
    def updatemessages(self,mid,company_id,allcompany="",type=""):
        #更新monggodb
        collection=dbmongo.appmessages
        collection.update({"id": int(mid)}, {"$set": {"isview": 1}});
        sql="select id from app_message_view where mid=%s and company_id=%s"
        result=dbc.fetchonedb(sql,[mid,company_id])
        if result:
            sqlu="update app_message_view set is_views=1 where mid=%s and company_id=%s"
            dbc.updatetodb(sqlu,[mid,company_id])
        else:
            gmt_created=datetime.datetime.now()
            sqlu="insert into app_message_view (mid,company_id,gmt_created,is_views) values(%s,%s,%s,%s)"
            dbc.updatetodb(sqlu,[mid,company_id,gmt_created,1])
        
        
    #一键更新未读
    def updatemessagesall(self,company_id,mtype=""):
        #更新monggodb
        #collection=dbmongo.appmessages
        #if company_id:
            #collection.update({"company_id": int(company_id)}, {"$set": {"isview": 1}});
        if (str(mtype)!="0"):
            sql="update app_message set is_views=1 where company_id=%s and is_views=0"
            if mtype:
                sql+=" and mtype="+str(mtype)
            dbc.updatetodb(sql,[company_id])
        #更新系统消息
        if str(mtype)=="0":
            sql1='select id from app_message where company_id=0 and not exists(select mid from app_message_view where mid=app_message.id and company_id=%s and is_views=1)'
            """
            result=dbc.fetchalldb(sql1,[company_id])
            if result:
                for list in result:
                    self.updatemessages(list[0],company_id)
            """
        
    #----系统推送消息列表
    def getmessagelist(self,company_id="",frompageCount=0,limitNum=20,isviews=None,mtype=""):
        if str(mtype)=="0":
            company_id=0
        sql1='select count(0) from app_message where company_id=%s'
        result1=self.dbc.fetchonedb(sql1,[company_id])
        if result1:
            count=result1[0]
        else:
            count=0
        sql="select id,title,url,content,company_id,gmt_created from app_message where company_id=%s"
        if isviews=="1":
            sql+=" and is_views=1"
            #sql+=" and exists(select id from app_message_view where mid=app_message.id and is_views=1)"
        if isviews=="0":
            sql+=" and is_views=0"
        if  mtype:
            sql+=" and mtype="+str(mtype)
            #sql+=" and not exists(select id from app_message_view where mid=app_message.id and is_views=1)"
        sql+=" order by id desc limit %s,%s"
        resultlist=self.dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
        
        listall=[]
        for result in resultlist:
            id=result[0]
            title=result[1]
            url=result[2]
            url=url.replace("?","awena")
            url=url.replace("&","aanda")
            content=result[3]
            gmt_created=formattime(result[5],3)
            isviews=self.getmessageview(id,company_id)
            list={'id':id,'title':title,'url':url,'content':content,'gmt_created':gmt_created,'isviews':isviews}
            listall.append(list)
        return {'list':listall,'count':count}
    def getnoviewmessagecount(self,company_id="",mtype=""):
        collection=dbmongo.appmessages
        searchlist={}
        if not mtype:
            mtype=0
        count=0
        if company_id and mtype!=0:
            #searchlist["company_id"]={"$in":[int(company_id)]}
            #searchlist["type"]=int(mtype)
            #searchlist["isview"]=0
            count=0
            sql="select count(0) from app_message where company_id=%s and is_views=0 and mtype=%s"
            result=self.dbc.fetchonedb(sql,[company_id,mtype])
            if result:
                count=result[0]
        #count=collection.find(searchlist).count()
        if mtype==0:
            sql1='select count(0) from app_message where company_id=0 and not exists(select id from app_message_view where mid=app_message.id and company_id=%s and is_views=1)'
            result1=self.dbc.fetchonedb(sql1,[company_id])
            if result1:
                count1=int(result1[0])
            else:
                count1=0
            if count:
                count=count+count1
            else:
                count=count1
        return count
    #----系统推送消息列表
    def getmessagelistmongo(self,company_id="",frompageCount=0,limitNum=20,isviews=None,mtype=0):
        collection=dbmongo.appmessages
        searchlist={}
        if not mtype:
            mtype=0
        if company_id:
            searchlist["company_id"]={"$in":[int(company_id),0]}
            searchlist["type"]=int(mtype)
        if isviews=="1":
            searchlist["isview"]=1
        if isviews=="0":
            searchlist["isview"]=0
        
        count=collection.find(searchlist).count()
        resultlist=collection.find(searchlist).sort("id",-1).skip(frompageCount).limit(limitNum)
        """
        sql1='select count(0) from app_message where company_id in (%s,0) '
        result1=self.dbc.fetchonedb(sql1,[company_id])
        if result1:
            count=result1[0]
        else:
            count=0
        sql="select id,title,url,content,company_id,gmt_created from app_message where company_id in (%s,0)"
        if isviews=="1":
            sql+=" and exists(select id from app_message_view where mid=app_message.id and is_views=1)"
        if isviews=="0":
            sql+=" and not exists(select id from app_message_view where mid=app_message.id and is_views=1)"
        sql+=" order by id desc limit %s,%s"
        resultlist=self.dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
        
        listall=[]
        for result in resultlist:
            id=result[0]
            title=result[1]
            url=result[2]
            url=url.replace("?","awena")
            url=url.replace("&","aanda")
            content=result[3]
            gmt_created=formattime(result[5],3)
            isviews=self.getmessageview(id,company_id)
            list={'id':id,'title':title,'url':url,'content':content,'gmt_created':gmt_created,'isviews':isviews}
            listall.append(list)
        """
        listall=[]
        for result in resultlist:
            id=result['id']
            title=result['title']
            url=result['url']
            url=url.replace("?","awena")
            url=url.replace("&","aanda")
            content=result['content']
            gmt_created=formattime(result['gmt_created'],3)
            #isview=result['isview']
            isviews=self.getmessageview(id,company_id)
            list={'id':id,'title':title,'url':url,'content':content,'gmt_created':gmt_created,'isviews':isviews}
            listall.append(list)
        return {'list':listall,'count':count,'testlist':searchlist}
    #----是否查看
    def getmessageview(self,mid,company_id):
        sql='select id from app_message_view where company_id=%s and is_views=1 and mid=%s'
        resultlist=self.dbc.fetchonedb(sql,[company_id,mid])
        listall=[]
        if resultlist:
            return 1
        else:
            return None
             
    def getmessagelist1(self,company_id):
        sql1='select count(0) from app_message_view where company_id=%s and is_views=0'
        count=self.dbc.fetchnumberdb(sql1,company_id)
        sql='select id,mid,is_views,gmt_created from app_message_view where company_id=%s and is_views=0'
        resultlist=self.dbc.fetchalldb(sql,company_id)
        listall=[]
        for result in resultlist:
            id=result[0]
            mid=result[1]
            messagedetail=self.getmessagedetail(mid)
            is_views=result[2]
            gmt_created=formattime(result[3],3)
            list={'id':id,'mid':mid,'is_views':is_views,'messagedetail':messagedetail,'gmt_created':gmt_created}
            listall.append(list)
        return {'count':count,'list':listall,'txt':'系统推送消息'}
    def getmessagedetail(self,id):
        sql='select title,url,gmt_created,content from app_message where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        list=None
        if result:
            title=result[0]
            url=result[1]
            gmt_created=formattime(result[2],3)
            content=result[3]
            list={'title':title,'url':url,'gmt_created':gmt_created,'content':content}
        return list
    
    
    
    #判断当前用户是否选取了主营行业类别
    def has_industry_code(self,company_id):
        sql='select industry_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result[0]  and result[0]!=0 and result[0]!='0':
            return 1
        else:
            return None
    #如果没有主营行业类别则进行选取行业类别(10个)
    def get_ten_lei(self):
        sql="select code,label from category where parent_code='1000'"
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                code=result[0]
                label=result[1]
                list={"code":code,"label":label}
                listall.append(list)
            return {'list':listall}
    #获得主营行业类别
    def getindustrycode(self,company_id):
        sql='select industry_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #获得相对应行业的推送供求
    def getapppushlist(self,industry_code):
        sql='select id,code,title,weburl,content,gmt_created from app_push_tuijian where code=%s order by id desc limit 0,9'
        resultlist=self.dbc.fetchalldb(sql,[industry_code])
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                industry_code=result[1]
                title=result[2]
                weburl=result[3]
                content=result[4]
                gmt_created=formattime(result[5],2)
                list={"id":id,"industry_code":industry_code,"title":title,"weburl":weburl,"content":content,"gmt_created":gmt_created}
                listall.append(list)
            return {'list':listall}
    #聊天列表
    def getchatlist(self,frompageCount="",limitNum="",company_id=""):
        sqlarg=""
        sql="select count(0) from app_chat where find_in_set('"+str(company_id)+"',chat_group)"
        listcount=0
        alist=self.dbc.fetchonedb(sql)
        if alist:
            listcount=alist[0]
        sql="select chat_group,chat_content,gmt_modified,chat_count from app_chat where find_in_set('"+str(company_id)+"',chat_group) order by gmt_modified desc limit "+str(frompageCount)+","+str(limitNum)+""
        result=self.dbc.fetchalldb(sql)
        listall=[]
        if result:
            for list in result:
                chat_group=list[0]
                chatarr=chat_group.split(",")
                chat_content=list[1]
                chat_count=list[3]
                
                
                forcompany_id=0
                for a in chatarr:
                    if a!=company_id:
                        forcompany_id=a
                if forcompany_id!=0:
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
                    lista={'company_id':forcompany_id,'contact':contact,'position':position,'compname':compname,'faceurl':faceurl,'chat_content':chat_content,'chat_count':chat_count}
                    listall.append(lista)
                
        return {'list':listall,'count':listcount}
    #读数据库留言
    def getxunpanlist(self,frompageCount=0,limitNum=10,company_id='',sendtype=''):
        sqlarg=''
        argument=[]
        account=getcompanyaccount(company_id)
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
        count=dbc.fetchnumberdb(sql1,argument)
        resultlist=dbc.fetchalldb(sql,argument)
        listall=[]
        gmt_modified=datetime.datetime.now()
        for result in resultlist:
            id=result[0]
            chatgroup=result[1]
            if chatgroup:
                chatarr=chatgroup.replace("-",",")
                
                sqla="select chat_count,id from app_chat where chat_group=%s"
                resultq=dbc.fetchonedb(sqla,[chatarr])
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
                        dbc.updatetodb(sqlb,[gmt_modified,chat_countarr,cid]);
            
            list=getleavewords(id)
            listall.append(list)
        return {'list':listall,'count':count}
        
        