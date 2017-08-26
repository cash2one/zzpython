# -*- coding: utf-8 -*-  
class zzcaigou:
    def __init__(self):
        self.db=db
#所有资讯
    def getcaigoulist(self,frompageCount="",limitNum=""):
        argument=[]
        sqlcount="select count(0) as count from caigou where id>0"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select id,title,detail,contact,email,mobile,tel,company_name,company_address,gmt_created,gmt_modified,check_status from caigou where id>0 limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        for list in listall:
            time1=list.get('gmt_created')
            if time1:
                list['gmt_created']=formattime(time1,flag=2)
            time2=list.get('gmt_modified')
            if time2:
                list['gmt_modified']=formattime(time2,flag=2)
        return {'count':count,'list':listall}
