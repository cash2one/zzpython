#-*- coding:utf-8 -*-

class zprice:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getprice_clist(self,parent_id):
        sql='select name,id,pinyin from price_category where parent_id =%s and showflag=1'
        resultlist=self.dbc.fetchalldb(sql,[parent_id])
        listall=[]
        i=0
        
        for result in resultlist:
            trstr=""
            i+=1
            if i % 5==0:
                trstr="</tr><tr>"
            list={'name':result[0],'id':result[1],'pinyin':result[2].lower(),'trstr':trstr}
            listall.append(list)
            
        return listall
    def getcategory_label(self,category_id):
        sql='select name from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[category_id])
        if result:
            return result[0]
    def getcategory_pinyin(self,pinyin):
        sql='select id from price_category where pinyin=%s'
        result=self.dbc.fetchonedb(sql,[pinyin])
        if result:
            return result[0]
    def parent_id(self,id):
        sql='select parent_id from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getpricecatepinyin(self,id):
        sql='select pinyin from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            if result[0]:
                return result[0].lower()
    def getpricecategory(self,id):
        sql="select type_id,assist_type_id from price where id=%s"
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return {'type_id':result[0],'assist_type_id':result[1]}
    #----报价列表 页
    def getpricelist(self,keywords="",frompageCount="",limitNum="",category_id="",allnum="",assist_type_id="",arg=""):
        price=spconfig['name']['price']['name']
        serverid=spconfig['name']['price']['serverid']
        port=spconfig['name']['price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if arg==1:
            if category_id:
                cl.SetFilter('type_id',category_id,False)
            if assist_type_id:
                cl.SetFilter('assist_type_id',assist_type_id,True)
        elif arg==2:
            if category_id:
                cl.SetFilter('type_id',category_id,True)
            if assist_type_id:
                cl.SetFilter('assist_type_id',assist_type_id,False)
        else:
            if category_id:
                cl.SetFilter('type_id',category_id)
            if assist_type_id:
                cl.SetFilter('assist_type_id',assist_type_id)
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_time desc" )
        cl.SetLimits (frompageCount,limitNum,allnum)
        if keywords:
            res = cl.Query ('@(title,tags,search_label) '+keywords,price)
        else:
            res = cl.Query ('',price)
        listall_news=[]
        listcount_news=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                icout=0
                for match in tagslist:
                    id=match['id']
                    icout+=1
                    pricecontent=cache.get("pricecontent"+str(id))
                    if (pricecontent==None):
                        sql="select content,tags from price where id=%s and is_checked=1"
                        alist = self.dbc.fetchonedb(sql,[id])
                        content=""
                        tags=""
                        if alist:
                            content=subString(filter_tags(alist[0]),50)
                            tags=alist[1]
                        attrs=match['attrs']
                        title=attrs['ptitle']
                        typeid=attrs['type_id']
                        assistid=attrs['assist_type_id']
                        gmt_time=attrs['gmt_time']
                        list1={'title':title,'id':id,'typeid':typeid,'assistid':assistid,'gmt_time':gmt_time,'content':content,'tags':tags}
                        pricecontent=list1
                        cache.set("pricecontent"+str(id),pricecontent,60*60)
                    
                    listall_news.append(pricecontent)
                listcount_news=res['total_found']
        return {'list':listall_news,'count':listcount_news}
    def getbbslist(self,kname="",num=""):
        #最新互助信息
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
        if num:
            limitnum=num
        else:
            limitnum=30
        cl.SetLimits (0,limitnum,limitnum)
        if kname:
            res = cl.Query ('@(title,tags) '+kname,'huzhu')
            listall_news=[]
            listcount_news=0
            havelist=None
            if res:
                if res.has_key('matches'):
                    tagslist=res['matches']
                    for match in tagslist:
                        td_id=match['id']
                        attrs=match['attrs']
                        title=attrs['ptitle']
                        gmt_time=attrs['ppost_time']
                        list1={'td_title':subString(title,60),'td_title_f':title,'td_id':td_id,'td_time':gmt_time}
                        listall_news.append(list1)
                        havelist=listall_news
                listcount_news=res['total_found']
                if (listcount_news==0):
                    res = cl.Query ('','huzhu')
                    if res:
                        if res.has_key('matches'):
                            tagslist=res['matches']
                            for match in tagslist:
                                td_id=match['id']
                                attrs=match['attrs']
                                title=attrs['ptitle']
                                gmt_time=attrs['ppost_time']
                                list1={'td_title':subString(title,60),'td_title_f':title,'td_id':td_id,'td_time':gmt_time}
                                listall_news.append(list1)
                        listcount_news=0
            return {'list':listall_news,'count':listcount_news,'havelist':havelist}
    def offerlist(self,kname="",pdt_type="",limitcount="",havepic="",fromlimit=""):
        #-------------供求列表
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
        if (fromlimit):
            cl.SetLimits (fromlimit,limitcount+fromlimit,limitcount+fromlimit)
        else:
            cl.SetLimits (0,limitcount,limitcount)
        cl.SetFilter('is_pause',[0])
        cl.SetFilter('is_del',[0])
        if (pdt_type!="" and pdt_type!=None):
            cl.SetFilter('pdt_kind',[int(str(pdt_type))])
        if (havepic):
            cl.SetFilterRange('havepic',1,100)
        if (kname=='' or kname==None):
            res = cl.Query ('','offersearch_new_vip')
        else:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        listall_offerlist=[]
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                numb=0
                arg=''
                for match in itemlist:
                    numb=numb+1
                    if numb==1:
                        arg='l'
                    if numb==2:
                        arg='r'
                    pid=match['id']
                    attrs=match['attrs']
                    company_id=attrs['company_id']
                    
#                    pdt_date=int_to_str(attrs['refresh_time'])
#                    short_time=pdt_date[5:]
                    
                    title=subString(attrs['ptitle'],40)
                    
                    list={'id':pid,'title':title,'gmt_time':'','short_time':'','fulltitle':attrs['ptitle'],}
                    listall_offerlist.append(list)
        return listall_offerlist
    #报价频道 网上报价
    def getwebprice(self,priceid):
        sql="select product_name,quote,area,company_name,company_id from price_data where price_id=%s"
        returnlist=self.dbc.fetchalldb(sql,[priceid])
        html="<table><tr><td>品名</td><td>价格</td><td>地区</td></tr>"
        for list in returnlist:
            product_name=list[0]
            quote=list[1]
            area=list[2]
            company_name=list[3]
            company_id=list[4]
            html+="<tr>"
            html+="<td>"+product_name+"</td>"
            html+="<td>"+quote+"</td>"
            html+="<td>"+area+"</td>"
            html+="</tr>"
        html+="</table>"
        return html