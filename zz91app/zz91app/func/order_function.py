#-*- coding:utf-8 -*-
class zzorder:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getordercount(self,company_id,type):
        sql='select count(0) from app_custom where company_id=%s and is_views=0 and type=%s'
        result=self.dbc.fetchnumberdb(sql,[company_id,type])
        return result
    def getorderlist(self,company_id,type):
        #获得缓存
        #zz91app_getorderlist=cache.get("zz91app_getorderlist"+str(company_id)+str(type))
        #if zz91app_getorderlist:
            #return zz91app_getorderlist
        count=self.getordercount(company_id,type)
        sql='select did from app_custom where company_id=%s and type=%s'
        resultlist=self.dbc.fetchalldb(sql,[company_id,type])
        listall=[]
        for result in resultlist:
            did=result[0]
            if type==1:
                companykeyword=self.getcompanykeyword(did)
                list=self.getindexofferlist(kname=companykeyword)
            else:
                pricecatename=self.getpricecatename(did)
                list=self.getpricelist(keywords=pricecatename)
            listall.append(list)
        #设置缓存
        #cache.set("zz91app_getorderlist"+str(company_id)+str(type),{'list':listall,'count':count},60*10)
        return {'list':listall,'count':count}
    #----商机定制主类
    def getcompanykeyword(self,id):
        #获得缓存
        #zz91app_getcompanykeyword=cache.get("zz91app_getcompanykeyword"+str(id))
        #if zz91app_getcompanykeyword:
            #return zz91app_getcompanykeyword
        sql="select title from data_index where id=%s"
        datalist=self.dbc.fetchonedb(sql,[id])
        if datalist:
            #设置缓存
            #cache.set("zz91app_getcompanykeyword"+str(id),datalist[0],60*10)
            return datalist[0]
    #--价格分类
    def getpricecatename(self,id):
         #获得缓存
        zz91app_getpricecatename=cache.get("zz91app_getpricecatename"+str(id))
        if zz91app_getpricecatename:
            return zz91app_getpricecatename
        sql="select name from price_category where id=%s"
        alist=self.dbc.fetchonedb(sql,[id])
        if alist:
            #设置缓存
            cache.set("zz91app_getpricecatename"+str(id),alist[0],60*10)
            return alist[0]
    #----最新供求
    def getindexofferlist(self,kname='',pdt_type='',company_id='',limitcount=1):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
        cl.SetLimits (0,limitcount,limitcount)
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
        if pdt_type:
            cl.SetFilter('pdt_kind',[int(pdt_type)])
        #if company_id:
            #cl.SetFilter('company_id',[int(company_id)])
        cl.SetFilterRange('havepic',1,100)
        if kname:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_ppc')
        else:
            res = cl.Query ('','offersearch_ppc')
        listcount=0
        listall_offerlist=[]
        if res:
            if res.has_key('matches'):
                listcount=res['total_found']
                itemlist=res['matches']
                for match in itemlist:
                    id=match['id']
                    list1=getcompinfo(id,kname,company_id)
                    listall_offerlist.append(list1)
        if limitcount==1:
            return None
        else:
            return {'list':listall_offerlist,'count':listcount}
    #----最新供求
    def getindexofferlist_ios(self,limitcount=1):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
        cl.SetLimits (0,limitcount,limitcount)
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
        if kname:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        else:
            res = cl.Query ('','offersearch_new,offersearch_new_vip')
        listcount=0
        listall_offerlist=[]
        if res:
            if res.has_key('matches'):
                listcount=res['total_found']
                itemlist=res['matches']
                for match in itemlist:
                    id=match['id']
                    list1=getcompinfo(id,kname,company_id)
                    listall_offerlist.append(list1)
        if limitcount==1:
            return None
        else:
            return {'list':listall_offerlist,'count':listcount}
    
    #报价列表 翻页
    def getpricelist(self,keywords="",frompageCount=0,limitNum=1,category_id="",allnum=10000,assist_type_id=""):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if (category_id):
            cl.SetFilter('type_id',category_id)
        if (assist_type_id):
            cl.SetFilter('assist_type_id',[assist_type_id])
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_time desc" )
        cl.SetLimits (frompageCount,limitNum,allnum)
        if (keywords):
            res = cl.Query ('@(title,tags) '+keywords,'price')
        else:
            res = cl.Query ('','price')
        listall=[]
        listcount=0
        if res:
            if res.has_key('matches'):
                listcount=res['total_found']
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    sql="select content,tags from price where id=%s and is_checked=1"
                    alist = self.dbc.fetchonedb(sql,id)
                    content=""
                    tags=""
                    if alist:
                        content=subString(filter_tags(alist[0]),50)
                        tags=alist[1]
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    gmt_time=attrs['gmt_time']
                    list1={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'tags':tags}
                    if limitNum==1:
                        list1['count']=listcount
                        return list1
                    listall.append(pricecontent)
        if limitNum==1:
            return ''
        else:
            return {'list':listall,'count':listcount}