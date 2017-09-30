#-*- coding:utf-8 -*-
listfield=['label','label1','spec','spec1','spec2','price','area','area1','area2','price1','price2','price3','price4','price5','price6','unit','qushi','qushi1','othertext','othertext1','num']
class zz91price:
    def __init__(self):
        from zz91db_ast import companydb
        self.dbc=companydb()
    def getpriceattrpinyin(self,label):
        sql='select pinyin from price_category_attr where label=%s'
        result=self.dbc.fetchonedb(sql,[label])
        if result:
            return result[0]
        return ''
    def getpriceattrlabel(self,id):
        sql='select label from price_category_attr where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
        return ''
    def getpricecategorylabel(self,id):
        sql='select name from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
        return ''
    def getpricefielddetail(self,id):
        sql='select price_category_id,name,field,sortrank,assist_type_id from price_category_field where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        list={'price_category_id':'','price_category_label':'','assist_type_id':'','assist_type_label':'','name':'','field':'','sortrank':''}
        if result:
            price_category_id=result[0]
            price_category_label=self.getpricecategorylabel(price_category_id)
            name=result[1]
            field=result[2]
            sortrank=result[3]
            assist_type_id=result[4]
            assist_type_label=self.getpricecategorylabel(assist_type_id)
            list={'price_category_id':price_category_id,'price_category_label':price_category_label,'assist_type_id':assist_type_id,'assist_type_label':assist_type_label,'name':name,'field':field,'sortrank':sortrank}
        return list
    def getpriceattrdetail(self,id):
        sql='select id,parent_id,price_category_id,label,pinyin,sortrank,page_type from price_category_attr where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        list={'parent_id':'','parent_label':'','price_category_id':'','price_category_label':'','label':'','pinyin':'','sortrank':''}
        if result:
            id=result[0]
            parent_id=result[1]
            price_category_id=result[2]
            parent_label=self.getpriceattrlabel(parent_id)
            price_category_label=self.getpricecategorylabel(price_category_id)
            label=result[3]
            pinyin=result[4]
            sortrank=result[5]
            page_type=result[6]
            list={'parent_id':parent_id,'parent_label':parent_label,'price_category_id':price_category_id,'price_category_label':price_category_label,'label':label,'pinyin':pinyin,'sortrank':sortrank,'page_type':page_type}
        return list
    def getpricectattrlist(self,frompageCount='',limitNum='',price_cid='',parent_id=''):
        sql1='select count(0) from price_category_attr where id>0'
        sql='select id,parent_id,price_category_id,label,pinyin,sortrank,page_type from price_category_attr where id>0'
        argument=[]
        if price_cid:
            sql1=sql1+' and price_category_id=%s'
            sql=sql+' and price_category_id=%s'
            argument.append(price_cid)
        if parent_id:
            sql1=sql1+' and parent_id=%s'
            sql=sql+' and parent_id=%s'
            argument.append(parent_id)
        count=self.dbc.fetchnumberdb(sql1,argument)
        sql=sql+' order by sortrank,id desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            parent_id=result[1]
            price_category_id=result[2]
            parent_label=self.getpriceattrlabel(parent_id)
            price_category_label=self.getpricecategorylabel(price_category_id)
            label=result[3]
            pinyin=result[4]
            sortrank=result[5]
            page_type=result[6]
            list={'id':id,'parent_id':parent_id,'parent_label':parent_label,'price_category_id':price_category_id,'price_category_label':price_category_label,'label':label,'pinyin':pinyin,'sortrank':sortrank,'page_type':page_type}
            listall.append(list)
        return {'list':listall,'count':count}
    def getpricectattrlist2(self,frompageCount=0,limitNum=100):
        listall=[]
#        listallcache=cache.get("priceattrlist2")
#        if not listall:
        sql='select id,parent_id,price_category_id,label,pinyin,sortrank,page_type from price_category_attr group by label'
        sql+=' order by sortrank,label'
        sql+=' limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql)
        for result in resultlist:
            id=result[0]
            parent_id=result[1]
            price_category_id=result[2]
            label=result[3]
            pinyin=result[4]
            sortrank=result[5]
            page_type=result[6]
            list={'id':id,'parent_id':parent_id,'price_category_id':price_category_id,'label':label,'pinyin':pinyin,'sortrank':sortrank,'page_type':page_type}
            listall.append(list)
#            cache.set("priceattrlist2",listall,60*60000)
#        else:
#            listall=listallcache
        return listall
    def getpricecategorylist(self,parent_id=""):
        listall=[]
        listallcache=cache.get("getpricecategorylist"+str(parent_id))
        if not listallcache:
            if parent_id:
                sql='select id,name,pinyin from price_category where parent_id=%s'
                resultlist=self.dbc.fetchalldb(sql,[parent_id])
            else:
                sql='select id,name,pinyin from price_category where parent_id=0'
                resultlist=self.dbc.fetchalldb(sql)
            for result in resultlist:
                id=result[0]
                name=result[1]
                pinyin=result[2]
                nextclist=self.getpricenextcategory(id)
                listall2=[]
                for clist in nextclist:
                    id2=clist['id']
                    name2=clist['name']
                    pinyin2=clist['pinyin']
                    nextclist2=self.getpricenextcategory(id2)
                    listall3=[]
                    for clist2 in nextclist2:
                        id3=clist2['id']
                        name3=clist2['name']
                        pinyin3=clist2['pinyin']
                        nextclist3=self.getpricenextcategory(id3)
                        listall4=[]
                        for clist3 in nextclist3:
                            id4=clist3['id']
                            name4=clist3['name']
                            pinyin4=clist3['pinyin']
                            nextclist4=self.getpricenextcategory(id4)
                            listall5=[]
                            for clist4 in nextclist4:
                                id5=clist4['id']
                                name5=clist4['name']
                                pinyin5=clist4['pinyin']
                                nextclist5=self.getpricenextcategory(id5)
                                list5={'id':id5,'name':name5,'pinyin':pinyin5,'nextclist':nextclist5}
                                listall5.append(list5)
                            
                            list4={'id':id4,'name':name4,'pinyin':pinyin4,'nextclist':listall5}
                            listall4.append(list4)
                        list3={'id':id3,'name':name3,'pinyin':pinyin3,'nextclist':listall4}
                        listall3.append(list3)
                    list2={'id':id2,'name':name2,'pinyin':pinyin2,'nextclist':listall3}
                    listall2.append(list2)
                list={'id':id,'name':name,'pinyin':pinyin,'nextclist':listall2}
                listall.append(list)
            cache.set("getpricecategorylist"+str(parent_id),listall,60*60000)
        else:
            listall=listallcache
        return listall
    def getpricenextcategory(self,parent_id):
        listall=[]
        listallcache=cache.get("getpricenextcategory"+str(parent_id))
        if listallcache:
            listall=listallcache
        else:
            sql='select id,name,pinyin from price_category where parent_id=%s'
            resultlist=self.dbc.fetchalldb(sql,[parent_id])
            for result in resultlist:
                id=result[0]
                name=result[1]
                pinyin=result[2]
                list={'id':id,'name':name,'pinyin':pinyin}
                listall.append(list)
            cache.set("getpricenextcategory"+str(parent_id),listall,60*60000)
        return listall
    def getpricenextcategory2(self,id):
        listall=[]
        listallcache=cache.get("getpricenextcategory2"+str(id))
        if listallcache:
            listall=listallcache
        else:
            nextclist=self.getpricenextcategory(id)
            for clist in nextclist:
                id2=clist['id']
                name2=clist['name']
                pinyin2=clist['pinyin']
                nextclist2=self.getpricenextcategory(id2)
                list={'id':id2,'name':name2,'pinyin':pinyin2,'nextclist':nextclist2}
                listall.append(list)
            cache.set("getpricenextcategory2"+str(id),listall,60*60000)
        return listall
    def getpricectfieldlist(self,frompageCount='',limitNum='',price_category_id='',assist_type_id=""):
        sql1='select count(0) from price_category_field where id>0'
        sql='select id,price_category_id,name,field,sortrank,assist_type_id from price_category_field where id>0'
        argument=[]
        if price_category_id:
            sql1=sql1+' and price_category_id=%s'
            sql=sql+' and price_category_id=%s'
            argument.append(price_category_id)
        if assist_type_id:
            sql1=sql1+' and assist_type_id=%s'
            sql=sql+' and assist_type_id=%s'
            argument.append(assist_type_id)
        count=self.dbc.fetchnumberdb(sql1,argument)
        sql=sql+' order by sortrank,id limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            price_category_id=result[1]
            assist_type_id=result[5]
            assist_type_label=self.getpricecategorylabel(assist_type_id)
            price_category_label=self.getpricecategorylabel(price_category_id)
            name=result[2]
            field=result[3]
            sortrank=result[4]
            list={'id':id,'price_category_id':price_category_id,'price_category_label':price_category_label,'assist_type_id':assist_type_id,'assist_type_label':assist_type_label,'name':name,'field':field,'sortrank':sortrank}
            listall.append(list)
        return {'list':listall,'count':count}
    def getpricetablelist(self,frompageCount='',limitNum='',searchlist=''):
        postdate_min=searchlist.get('postdate_min')
        postdate_max=searchlist.get('postdate_max')
        gmt_modified_min=searchlist.get('gmt_modified_min')
        gmt_modified_max=searchlist.get('gmt_modified_max')
        type_id=searchlist.get('type_id')
        priceid=searchlist.get('priceid')
        assist_type_id=searchlist.get('assist_type_id')
        sqls=''
        argument=[]
        if postdate_min:
            sqls+=' and postdate > %s'
            argument.append(postdate_min)
        if postdate_max:
            sqls+=' and postdate < %s'
            argument.append(postdate_max)
        if gmt_modified_min:
            sqls+=' and gmt_modified > %s'
            argument.append(gmt_modified_min)
        if gmt_modified_max:
            sqls+=' and gmt_modified < %s'
            argument.append(gmt_modified_max)
        if type_id:
            sqls+=' and type_id=%s'
            argument.append(type_id)
        if priceid:
            sqls+=' and priceid=%s'
            argument.append(priceid)
        if assist_type_id:
            sqls+=' and assist_type_id=%s'
            argument.append(assist_type_id)
        sql='select id,priceid,typename,title,type_id,assist_type_id,label,label1,label2,spec,spec1,spec2,price,area,area1,area2,price1,price2,price3,price4,price5,price6,unit,qushi,qushi1,postdate,othertext,othertext1,num,gmt_modified from price_list where id>0 '+sqls+' order by id desc limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from price_list where id>0 '+sqls+''
        resultlist=self.dbc.fetchalldb(sql,argument)
        count=self.dbc.fetchonedb(sqlc,argument)[0]
        listall=[]
        for result in resultlist:
            id=result[0]
            priceid=result[1]
            if priceid is None:
                priceid=''
            typename=result[2]
            if typename is None:
                typename=''
            title=result[3]
            if title is None:
                title=''
            type_id=result[4]
            if type_id is None:
                type_name=''
            else:
                type_name=self.getpricecategorylabel(type_id)
            assist_type_id=result[5]
            if assist_type_id is None:
                assist_type_name=''
            else:
                assist_type_name=self.getpricecategorylabel(assist_type_id)
            label=result[6]
            if label is None:
                label=''
            label1=result[7]
            if label1 is None:
                label1=''
            label2=result[8]
            if label2 is None:
                label2=''
            spec=result[9]
            if spec is None:
                spec=''
            spec1=result[10]
            if spec1 is None:
                spec1=''
            spec2=result[11]
            if spec2 is None:
                spec2=''
            price=result[12]
            if price is None:
                price=''
            area=result[13]
            if area is None:
                area=''
            area1=result[14]
            if area1 is None:
                area1=''
            area2=result[15]
            if area2 is None:
                area2=''
            price1=result[16]
            if price1 is None:
                price1=''
            price2=result[17]
            if price2 is None:
                price2=''
            price3=result[18]
            if price3 is None:
                price3=''
            price4=result[19]
            if price4 is None:
                price4=''
            price5=result[20]
            if price5 is None:
                price5=''
            price6=result[21]
            if price6 is None:
                price6=''
            unit=result[22]
            if unit is None:
                unit=''
            qushi=result[23]
            if qushi is None:
                qushi=''
            qushi1=result[24]
            if qushi1 is None:
                qushi1=''
            postdate=result[25]
            if postdate is None:
                postdate=''
            else:
                postdate=formattime(postdate,flag=2)
            othertext=result[26]
            if othertext is None:
                othertext=''
            othertext1=result[27]
            if othertext1 is None:
                othertext1=''
            num=result[28]
            if num is None:
                num=''
            gmt_modified=result[29]
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            list={'id':id,'priceid':priceid,'typename':typename,'title':title,'type_name':type_name,'assist_type_name':assist_type_name,'label':label,'label1':label1,'label2':label2,'spec':spec,'spec1':spec1,'spec2':spec2,'price':price,'area':area,'area1':area1,'area2':area2,'price1':price1,'price2':price2,'price3':price3,'price4':price4,'price5':price5,'price6':price6,'unit':unit,'qushi':qushi,'qushi1':qushi1,'postdate':postdate,'othertext':othertext,'othertext1':othertext1,'num':num,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}