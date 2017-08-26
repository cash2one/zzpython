#-*- coding:utf-8 -*-

class zz91products:
    def __init__(self):
        self.dbc=dbc
    def getproductslist(self,frompageCount,limitNum,check_status=''):
        argument=[]
        #DATEDIFF(CURDATE(),gmt_created)>7
        sqlarg=' from products where gmt_modified>"2016-8-28"'
        if check_status:
            sqlarg+=' and check_status=%s'
            argument.append(check_status)
        sqlc='select count(0)'+sqlarg
        sql='select id,title,products_type_code,gmt_created'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sqlc,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            title=result[1]
            products_type_code=result[2]
            if products_type_code=="10331000":
                products_type="供应"
            if products_type_code=="10331001":
                products_type="求购"
            gmt_created=formattime(result[3])
            ispic=self.getexitspic(id)
            list={'id':id,'title':title,'products_type':products_type,'products_type_code':products_type_code,'gmt_created':gmt_created,'ispic':ispic}
            listall.append(list)
        return {'list':listall,'count':count}
    #类别列表
    def getindexcategorylist(self,code,showflag):
        catelist=cache.get("mobile_catec"+str(code))
        if (catelist==None):
            if (showflag==2):
                sql="select label,code,pinyin from category_products where code like %s order by sort asc"
            else:
                sql="select label,code,pinyin from category_products where code like %s"'"____"'" order by sort asc"
            #cursor.execute(sql,[str(code)])
            listall_cate=[]
            #catelist=cursor.fetchall()
            catelist=dbc.fetchalldb(sql,[str(code)])
            numb=0
            for a in catelist:
                numb=numb+1
                if (showflag==1):
                    sql1="select label,pinyin,code from category_products where code like '"+str(a[1])+"____' order by sort asc"
                    #cursor.execute(sql1)
                    listall_cate1=[]
                    #catelist1=cursor.fetchall()
                    catelist1=dbc.fetchalldb(sql1)
                    for b in catelist1:
                        pinyin=b[1]
                        if pinyin:
                            pinyin=pinyin.lower()
                        list1={'label':b[0],'code':b[2],'pinyin':pinyin}
                        listall_cate1.append(list1)
                else:
                    listall_cate1=None
                pinyin=a[2]
                if pinyin:
                    pinyin=pinyin.lower()
                list={'label':a[0],'code':a[1],'catelist':listall_cate1,'numb':numb,'pinyin':pinyin}
                listall_cate.append(list)
            cache.set("mobile_catec"+str(code),listall_cate,60*6)
        else:
            listall_cate=catelist
        
        return listall_cate
    def getcategory_name(self,code):
        sql='select label from category_products where code=%s'
        result=self.dbc.fetchonedb(sql,[code])
        if result:
            return result[0]
    #加工说明
    def getcategorylist(self,code):
        sql="select code,label from category where parent_code=%s"
        result=self.dbc.fetchalldb(sql,[code])
        listall=[]
        if result:
            for list in result:
                l={'code':list[0],'label':list[1]}
                listall.append(l)
        return listall
    #未通过原因
    def getunpass_reason(self):
        sql="select content from description_template where template_code=%s"
        result=self.dbc.fetchalldb(sql,['10341001'])
        listall=[]
        if result:
            for list in result:
                l={'content':list[0]}
                listall.append(l)
        return listall
    def getexitspic(self,proid):
        sql="select pic_address from products_pic where product_id=%s"
        result=self.dbc.fetchonedb(sql,[proid])
        if result:
            return result[0]
    #供求图片
    def getcategorylist(self,proid):
        sql="select * from products_pic where product_id=%s"
        result=dict_dbc.fetchalldb(sql,[proid])
        return result
    #支付订单
    def getpayorderlist(self,frompageCount,limitNum,out_trade_no="",mobile='',contact='',trade_no=''):
        argument=[]
        sqlarg=' from pay_order where id>0'
        if out_trade_no:
            sqlarg+=' and out_trade_no=%s'
            argument.append(out_trade_no)
        if trade_no:
            sqlarg+=' and trade_no=%s'
            argument.append(trade_no)
        if contact:
            sqlarg+=' and contact=%s'
            argument.append(contact)
        if mobile:
            sqlarg+=' and mobile=%s'
            argument.append(mobile)
        sqlc='select count(0)'+sqlarg
        sql='select * '+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sqlc,argument)
        resultlist=dict_dbc.fetchalldb(sql,argument)
        listall=[]
        for list in resultlist:
            gmt_created=formattime(list['gmt_created'])
            list['gmt_created']=gmt_created
            listall.append(list)
        return {'list':listall,'count':count}
    #公司信息
    def getcompanydetail(self,proid):
        sql="select company_id from products where id=%s"
        result=self.dbc.fetchonedb(sql,[proid])
        if result:
            company_id=result[0]
            if company_id:
                sql="select * from company where id=%s"
                company=dict_dbc.fetchonedb(sql,[company_id])
                return company
                #sql="select * from company_account where company_id=%s"
                #company_account=dict_dbc.fetchalldb(sql,[company_id])
                