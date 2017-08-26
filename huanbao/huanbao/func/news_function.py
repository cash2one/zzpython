# -*- coding: utf-8 -*-  
class zznews:
    def __init__(self):
        self.db=db
#所有资讯
    def getnewslist(self,frompageCount="",limitNum="",index=""):
        argument=[]
        type=''
        clo_name=''
        if index=='0' or index is None:
            sqlcount="select count(0) as count from news where id>0"
            count=db.fetchonedb(sqlcount,argument)['count']
            sqllist="select id,title,title_index,category_code,description,details,details_query,tags,html_path,news_source,gmt_publish,gmt_created,gmt_modified from news where id>0 limit "+str(frompageCount)+","+str(limitNum)+""
            listall=db.fetchalldb(sqllist,argument)
        else:
            if index=='1':
                argument.append('10001000')
                type='hbxw'
                clo_name='环保新闻'
            elif index=='2':
                argument.append('10001001')
                type='zcfg'
                clo_name='政策法规'
            elif index=='3':
                argument.append('10001002')
                type='hqbg'
                clo_name='市场/行情报告'
            elif index=='4':
                argument.append('10001003')
                type='gcal'
                clo_name='工程/案例'
            elif index=='5':
                argument.append('10001004')
                type='qyjs'
                clo_name='前沿技术'
            elif index=='6':
                argument.append('10001005')
                type='zjlw'
                clo_name='专家/论文'
            elif index=='7':
                argument.append('10001006')
                type='ssbk'
                clo_name='上市板块'
            sqlcount="select count(0) as count from news where category_code=%s"
            count=db.fetchonedb(sqlcount,argument)['count']
            sqllist="select id,title,title_index,category_code,description,details,details_query,tags,html_path,news_source,gmt_publish,gmt_created,gmt_modified from news where category_code=%s limit "+str(frompageCount)+","+str(limitNum)+""
            listall=db.fetchalldb(sqllist,argument)
        for list in listall:
            time1=list.get('gmt_publish')
            list['gmt_publish']=formattime(time1,flag=1)
            time2=list.get('gmt_created')
            list['gmt_created']=formattime(time2,flag=1)
            time3=list.get('gmt_modified')
            list['gmt_modified']=formattime(time3,flag=1)
        return {'count':count,'list':listall,'type':type,'clo_name':clo_name}
    
    def addnews(self,request=""):
        sql="select code,name from news_category where code like '________'"
        result=db.fetchalldb(sql)
        return result
    
    def modnews(self,request=""):
        id=request.GET.get('id')
        sql="select * from news where id=%s"
        result=db.fetchonedb(sql,[id])
        sqls="select code,name from news_category where code like '________'"
        result1=db.fetchalldb(sqls)
        return {'result':result,'result1':result1}
    
    def savenews(self,request=""):
        id=request.POST.get('id')
        time=datetime.datetime.now()
        print time
        title=request.POST.get('title')
        title_index=request.POST.get('title_index')
        category_code=request.POST.get('category_code')
        description=request.POST.get('description')
        details=request.POST.get('details')
        details_query=request.POST.get('details_query')
        tags=request.POST.get('tags')
        html_path=request.POST.get('html_path')
        news_source=request.POST.get('news_source')
        news_source_url=request.POST.get('news_source_url')
        pause_status=request.POST.get('pause_status')
        gmt_publish=request.POST.get('gmt_publish')
        gmt_modified=request.POST.get('gmt_modified')
        uid=request.session.get('user_id',default=None)
        sql='select username,realname from user where id=%s'
        result=db.fetchonedb(sql,[uid])
        admin_account=result.get('username')
        admin_name=result.get('realname')
        if not id:
            sqls='insert into news(title,title_index,category_code,description,details,details_query,tags,html_path,news_source,gmt_created,admin_account,admin_name,news_source_url,pause_status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result1=db.updatetodb(sqls,[title,title_index,category_code,description,details,details_query,tags,html_path,news_source,time,admin_account,admin_name,news_source_url,pause_status])
        elif id:
            sqls='update news set title=%s,title_index=%s,category_code=%s,description=%s,details=%s,details_query=%s,tags=%s,html_path=%s,news_source=%s,gmt_modified=%s,admin_account=%s,admin_name=%s,news_source_url=%s,pause_status=%s where id=%s'
            result1=db.updatetodb(sqls,[title,title_index,category_code,description,details,details_query,tags,html_path,news_source,time,admin_account,admin_name,news_source_url,pause_status,id])
    
    def delnews(self,request="",check_box_list=""):
        id=request.GET.get('id')
        if id:
            sql='delete from news where id=%s'
            result=db.updatetodb(sql,[id])
        if check_box_list:
            for id in check_box_list:
                sql='delete from news where id=%s'
                result=db.updatetodb(sql,[id])
        
    def detailsnews(self,request=""):
        id=request.GET.get('id')
        sql='select id,title,title_index,category_code,description,details,details_query,tags,html_path,news_source,view_count,gmt_created from news where id=%s'
        result=db.fetchonedb(sql,[id])
        sql1='update news set view_count=view_count+1 where id=%s'
        result1=db.updatetodb(sql1,[id])
        time=result['gmt_created']
        result['gmt_created']=formattime(time,flag=2)
        return result