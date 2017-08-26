#-*- coding:utf-8 -*-
class zznews:
    def __init__(self):
        self.db=db
#所有数据
    def getnewslist(self,frompageCount="",limitNum=""):
        argument=[]
        sqlcount="select count(0) as count from bz_article"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select aid,subject,keyword,content from bz_article limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}
