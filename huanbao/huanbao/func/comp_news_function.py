# -*- coding: utf-8 -*-  
class zznews:
    def __init__(self):
        self.db=db

    def getcompnews(self,frompageCount="",limitNum=""):
        argument=[]
        sqlcount="select count(0) as count from comp_news where id>0"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select id,cid,account,category_code,title,details,pause_status,check_status,delete_status,check_person,gmt_publish,gmt_created,gmt_modified,view_count,tags from comp_news where id>0 limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}
