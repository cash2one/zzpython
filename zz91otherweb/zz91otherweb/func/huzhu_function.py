#-*- coding:utf-8 -*-
class huzhu_zhishi:
    def __init__(self):
        self.dbc=dbt
    def getarticallist(self,frompageCount,limitNum,typeid=''):
        argument=[]
        sqlarg=' from bbs_zhishi where id>0'
        if typeid:
            sqlarg+=' and typeid=%s'
            argument.append(typeid)
        sqlc='select count(0)'+sqlarg
        sql='select id,typeid,title,click,keywords,gmt_created'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sqlc,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            typeid=result[1]
            typename=''
            if typeid:
                typename=self.gettypename(typeid)
            title=result[2]
            click=result[3]
            keywords=result[4]
            gmt_created=formattime(result[5])
            list={'id':id,'typeid':typeid,'typename':typename,'title':title,'click':click,'keywords':keywords,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count}
    
    def getarttypelist(self,frompageCount,limitNum):
        sql='select id,typename,sortrank from bbs_zstype order by id limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            typename=result[1]
            sortrank=result[2]
            list={'id':id,'typename':typename,'sortrank':sortrank}
            listall.append(list)
        return listall
    def gettypename(self,typeid):
        sql='select typename from bbs_zstype where id=%s'
        result=self.dbc.fetchonedb(sql,[typeid])
        if result:
            return result[0]

class zz91huzhu:
    def __init__(self):
        self.db_huzhu=dbc
    def updatedb(self,is_del,postid):
        gmt_created=datetime.datetime.now()
        sql='update bbs_post set is_del=%s,gmt_modified=%s where id=%s'
        self.db_huzhu.updatetodb(sql,[is_del,gmt_created,postid])
    def update_bbs_post(self,bbs_post_category_id,title,content,check_status,gmt_created,postsource,litpic,postid):
        content_query=filter_tags(content)
        gmt_modified=datetime.datetime.now()
        sql='update bbs_post set bbs_post_category_id=%s,title=%s,content=%s,content_query=%s,check_status=%s,gmt_modified=%s,postsource=%s where id=%s'
        self.db_huzhu.updatetodb(sql,[bbs_post_category_id,title,content,content_query,check_status,gmt_modified,postsource,postid])
        if litpic:
            sql1='update bbs_post_upload_file set file_path=%s where bbs_post_id=%s'
            self.db_huzhu.updatetodb(sql,[litpic,postid])
    def add_bbs_post(self,company_id,account,bbs_post_category_id,title,content,check_status,gmt_created,postsource,litpic):
        content_query=filter_tags(content)
        gmt_modified=datetime.datetime.now()
        sql='insert into bbs_post(company_id,account,bbs_post_category_id,title,content,content_query,check_status,gmt_created,gmt_modified,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_huzhu.updatetodb(sql,[company_id,account,bbs_post_category_id,title,content,content_query,check_status,gmt_created,gmt_modified,postsource])
        if litpic:
            sql1='select max(id) from bbs_post'
            result=self.db_huzhu.fetchonedb(sql1)
            if result:
                bbs_post_id=result[0]
                sql2='insert into bbs_post_upload_file(company_id,account,bbs_post_id,file_path,gmt_created) values(%s,%s,%s,%s,%s)'
                self.db_huzhu.updatetodb(sql2,[company_id,account,bbs_post_id,litpic,gmt_created])

    def addbbs_post_invite(self,checktitle,checktype):
        sql='insert into bbs_post_invite(bbs_post_id,guanzhu_id,gmt_created) values(%s,%s,%s)'
        gmt_created=datetime.datetime.now()
        for postid in checktitle:
            for ctype in checktype:
                sql1='select id from bbs_post_invite where bbs_post_id=%s and guanzhu_id=%s'
                result=self.db_huzhu.fetchonedb(sql1,[postid,ctype])
                if not result:
                    self.db_huzhu.updatetodb(sql,[postid,ctype,gmt_created])
    #展会直播列表
    def getzhibolist(self,frompageCount,limitNum,searchlist=""):
        argument=[]
        sqlarg=' from subject_zhibo where id>0'
        ztype=searchlist.get("ztype")
        if ztype:
            sqlarg+=' and ztype=%s'
            argument.append(ztype)
        sqlc='select count(0)'+sqlarg
        sql='select id,content,gmt_created,title '+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.db_huzhu.fetchnumberdb(sqlc,argument)
        resultlist=self.db_huzhu.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            content=result[1]
            title=result[3]
            if not title:
                title=''
            gmt_created=formattime(result[2])
            list={'id':id,'content':content,'gmt_created':gmt_created,'title':title}
            listall.append(list)
        return {'list':listall,'count':count}
    def getpushlist(self,frompageCount,limitNum,guanzhu_id=''):
        sql1='select count(0) from bbs_post_invite where id>0'
        sql='select bbs_post_id,guanzhu_id from bbs_post_invite where id>0'
        argument=[]
        if guanzhu_id:
            sql1=sql1+' and guanzhu_id=%s'
            sql=sql+' and guanzhu_id=%s'
            argument.append(guanzhu_id)
        sql=sql+' order by id desc'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=self.db_huzhu.fetchnumberdb(sql1,argument)
        else:
            count=self.db_huzhu.fetchnumberdb(sql1)
        if argument:
            resultlist=self.db_huzhu.fetchalldb(sql,argument)
        else:
            resultlist=self.db_huzhu.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                bbs_post_id=result[0]
                guanzhu_id=result[1]
                guanzhu_name=''
                if guanzhu_id==1:
                    guanzhu_name='废金属'
                elif guanzhu_id==2:
                    guanzhu_name='废塑料'
                elif guanzhu_id==3:
                    guanzhu_name='综合废料'
                bbs_post_detail=self.getbbs_post_detail(bbs_post_id)
                if bbs_post_detail:
                    check_status=bbs_post_detail['check_status']
                    check_name=bbs_post_detail['check_name']
                    visited_count=bbs_post_detail['visited_count']
                    reply_count=bbs_post_detail['reply_count']
                    reply_time=bbs_post_detail['reply_time']
                    postsource=bbs_post_detail['postsource']
                    company_id=bbs_post_detail['company_id']
                    account=bbs_post_detail['account']
                    title=bbs_post_detail['title']
                    content=bbs_post_detail['content']
                    content_query=''
                    if bbs_post_detail.has_key('content_query'):
                        content_query=bbs_post_detail['content_query']
                    bbs_post_category=bbs_post_detail['bbs_post_category']
                    bbs_post_category_id=bbs_post_detail['bbs_post_category_id']
                    gmt_created=bbs_post_detail['gmt_created']
                    list={'id':bbs_post_id,'check_status':check_status,'check_name':check_name,'visited_count':visited_count,'reply_count':reply_count,'reply_time':reply_time,'postsource':postsource,'company_id':company_id,'account':account,'title':title,'content':content,'content_query':content_query,'bbs_post_category':bbs_post_category,'bbs_post_category_id':bbs_post_category_id,'gmt_created':gmt_created,'guanzhu_id':guanzhu_id,'guanzhu_name':guanzhu_name}
                    listall.append(list)
#                    return bbs_post_detail
        return {'list':listall,'count':count}

    def getbbs_post_detail(self,id):
        sql='select id,company_id,account,bbs_user_profiler_id,bbs_post_category_id,title,content,gmt_created,check_status,visited_count,reply_count,reply_time,postsource,content_query from bbs_post where id=%s'
        result=self.db_huzhu.fetchonedb(sql,[id])
        listall=[]
        if result:
#            id=result[0]
            company_id=result[1]
            account=result[2]
            bbs_user_profiler_id=result[3]
            bbs_post_category_id=result[4]
            bbs_post_category=self.getbbs_post_category(bbs_post_category_id)
            title=result[5]
            content=result[6]
            gmt_created=date_to_str(result[7])
            check_status=result[8]
            check_name=''
            if check_status=='0':
                check_name='未审核'
            elif check_status=='1':
                check_name='已审核'
            elif check_status=='2':
                check_name='已读'
            elif check_status=='3':
                check_name='退回'
            visited_count=result[9]
            reply_count=result[10]
            reply_time=result[11]
            if reply_time:
                reply_time=date_to_strall(reply_time)
            postsourcen=result[12]
            content_query=result[13]
            if content_query:
                if len(content_query)>50:
                    content_query=content_query[:50]+'...'
            postsource=''
            if postsourcen==0:
                postsource='pc'
            elif postsourcen==1:
                postsource='手机站'
            elif postsourcen==4:
                postsource='app'
            list={'id':id,'check_status':check_status,'check_name':check_name,'visited_count':visited_count,'reply_count':reply_count,'reply_time':reply_time,'postsource':postsource,'company_id':company_id,'account':account,'title':title,'content':content,'content_query':content_query,'bbs_user_profiler_id':bbs_user_profiler_id,'bbs_post_category':bbs_post_category,'bbs_post_category_id':bbs_post_category_id,'gmt_created':gmt_created}
            return list
    
    def getbbspostlist(self,frompageCount,limitNum,typeid='',check_status='',ispush='',is_del='',account=''):
        sql1='select count(0) from bbs_post where is_del=0'
        sql='select id,company_id,account,bbs_user_profiler_id,bbs_post_category_id,title,content,gmt_created,check_status,visited_count,reply_count,reply_time,postsource,content_query from bbs_post where is_del=0'
        argument=[]
        if typeid:
            sql1=sql1+' and bbs_post_category_id=%s'
            sql=sql+' and bbs_post_category_id=%s'
            argument.append(typeid)
        if check_status:
            sql1=sql1+' and check_status=%s'
            sql=sql+' and check_status=%s'
            argument.append(check_status)
        if account:
            sql1=sql1+' and account=%s'
            sql=sql+' and account=%s'
            argument.append(account)
        if is_del:
            sql1=sql1.replace('is_del=0','is_del=1')
            sql=sql.replace('is_del=0','is_del=1')
        if ispush=='1':
            sql1=sql1+' and EXISTS(select bbs_post_id from bbs_post_invite where bbs_post.id=bbs_post_invite.bbs_post_id)'
            sql=sql+' and EXISTS(select bbs_post_id from bbs_post_invite where bbs_post.id=bbs_post_invite.bbs_post_id)'
        elif ispush=='0':
            sql1=sql1+' and not EXISTS(select bbs_post_id from bbs_post_invite where bbs_post.id=bbs_post_invite.bbs_post_id)'
            sql=sql+' and not EXISTS(select bbs_post_id from bbs_post_invite where bbs_post.id=bbs_post_invite.bbs_post_id)'
#            argument.append(ispush)
        sql=sql+' order by id desc'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=self.db_huzhu.fetchnumberdb(sql1,argument)
        else:
            count=self.db_huzhu.fetchnumberdb(sql1)
        if argument:
            resultlist=self.db_huzhu.fetchalldb(sql,argument)
        else:
            resultlist=self.db_huzhu.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                company_id=result[1]
                account=result[2]
                bbs_user_profiler_id=result[3]
                bbs_post_category_id=result[4]
                bbs_post_category=self.getbbs_post_category(bbs_post_category_id)
                title=result[5]
                content=result[6]
                gmt_created=date_to_str(result[7])
                check_status=result[8]
                check_name=''
                if check_status=='0':
                    check_name='未审核'
                elif check_status=='1':
                    check_name='已审核'
                elif check_status=='2':
                    check_name='已读'
                elif check_status=='3':
                    check_name='退回'
                visited_count=result[9]
                reply_count=result[10]
                reply_time=result[11]
                if reply_time:
                    reply_time=date_to_strall(reply_time)
                postsourcen=result[12]
                content_query=result[13]
                if content_query:
                    if len(content_query)>50:
                        content_query=content_query[:50]+'...'
                postsource=''
                if postsourcen==0:
                    postsource='pc'
                elif postsourcen==1:
                    postsource='手机站'
                else:
                    postsource='导入'
                weburl='http://m.zz91.com/huzhuview/'+str(id)+'.htm'
                list={'id':id,'weburl':weburl,'check_status':check_status,'check_name':check_name,'visited_count':visited_count,'reply_count':reply_count,'reply_time':reply_time,'postsource':postsource,'company_id':company_id,'account':account,'title':title,'content':content,'content_query':content_query,'bbs_user_profiler_id':bbs_user_profiler_id,'bbs_post_category':bbs_post_category,'bbs_post_category_id':bbs_post_category_id,'gmt_created':gmt_created}
                listall.append(list)
        return {'list':listall,'count':count}
    def getbbs_post_category(self,id):
        sql='select name from bbs_post_categorys where id=%s and state=0'
        result=self.db_huzhu.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getcategorylist(self):
        sql='select id,name from bbs_post_categorys where state=0 and parent_id=0 order by id desc'
        resultlist=self.db_huzhu.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'name':result[1]}
                listall.append(list)
        return listall
    def getbbs_post_title(self,id):
        sql='select title from bbs_post where id=%s'
        result=self.db_huzhu.fetchonedb(sql,[id])
        if result:
            return result[0]
        return ''
    def getreplylist(self,frompageCount='',limitNum='',postid='',account=''):
        sql1='select count(0) from bbs_post_reply where is_del=0'
        sql='select id,company_id,account,bbs_post_id,title,content,check_status,gmt_created,postsource from bbs_post_reply where is_del=0'
        argument=[]
        if postid:
            sql1=sql1+' and bbs_post_id=%s'
            sql=sql+' and bbs_post_id=%s'
            argument.append(postid)
        if account:
            sql1=sql1+' and account=%s'
            sql=sql+' and account=%s'
            argument.append(account)
        sql=sql+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=self.db_huzhu.fetchnumberdb(sql1,argument)
        else:
            count=self.db_huzhu.fetchnumberdb(sql1)
        if argument:
            resultlist=self.db_huzhu.fetchalldb(sql,argument)
        else:
            resultlist=self.db_huzhu.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                company_id=result[1]
                account=result[2]
                bbs_post_id=result[3]
                bbs_post_title=self.getbbs_post_title(bbs_post_id)
                title=result[4]
                content=result[5]
                if content:
                    if len(content)>50:
                        content=content[:50]+'...'
                check_status=result[6]
                check_name=''
                if check_status=='0':
                    check_name='未审核'
                elif check_status=='1':
                    check_name='已审核'
                elif check_status=='2':
                    check_name='已读'
                elif check_status=='3':
                    check_name='退回'
                gmt_created=date_to_strall(result[7])
                postsourcen=result[8]
                postsource=''
                if postsourcen==0:
                    postsource='pc'
                elif postsourcen==1:
                    postsource='手机站'
                else:
                    postsource='导入'
                list={'id':id,'company_id':company_id,'account':account,'bbs_post_id':bbs_post_id,'bbs_post_title':bbs_post_title,'title':title,'content':content,'check_status':check_status,'check_name':check_name,'gmt_created':gmt_created,'postsource':postsource}
                listall.append(list)
        return {'list':listall,'count':count}
    def getlitpic(self,bbs_post_id):
        sql='select file_path from bbs_post_upload_file where bbs_post_id=%s'
        result=self.db_huzhu.fetchonedb(sql,[bbs_post_id])
        if result:
            return result[0]
            
    def getbbs_post_detail(self,id):
        sql='select company_id,account,bbs_post_category_id,title,content,gmt_created,check_status,visited_count,reply_count,reply_time,postsource from bbs_post where is_del=0 and id=%s'
        result=self.db_huzhu.fetchonedb(sql,[id])
        if result:
            litpic=self.getlitpic(id)
            company_id=result[0]
            account=result[1]
            bbs_post_category_id=result[2]
            bbs_post_category=self.getbbs_post_category(bbs_post_category_id)
            title=result[3]
            content=result[4]
            gmt_created=date_to_str(result[5])
            check_status=result[6]
            check_name=''
            if check_status=='0':
                check_name='未审核'
            elif check_status=='1':
                check_name='已审核'
            elif check_status=='2':
                check_name='已读'
            elif check_status=='3':
                check_name='退回'
            visited_count=result[7]
            reply_count=result[8]
            reply_time=result[9]
            if reply_time:
                reply_time=date_to_strall(reply_time)
            postsourcen=result[10]
            postsource=''
            if postsourcen==0:
                postsource='pc'
            elif postsourcen==1:
                postsource='手机站'
            else:
                postsource='导入'
            list={'check_status':check_status,'litpic':litpic,'check_name':check_name,'visited_count':visited_count,'reply_count':reply_count,'reply_time':reply_time,'postsource':postsource,'company_id':company_id,'account':account,'title':title,'content':content,'bbs_post_category':bbs_post_category,'bbs_post_category_id':bbs_post_category_id,'gmt_created':gmt_created}
            return list