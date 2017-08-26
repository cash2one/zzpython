def getdaohangtype(pingyin):
    #获得缓存
    zz91daohang_getdaohangtype=cache.get("zz91daohang_getdaohangtype"+str(pingyin))
    if zz91daohang_getdaohangtype:
        return zz91daohang_getdaohangtype 
    sql='select sid from daohang where pingyin=%s'
    #cursor.execute(sql,[pingyin])
    #ldbresult=cursor.fetchone()
    ldbresult=dbc.fetchonedb(sql,[pingyin])
    if ldbresult:
        #设置缓存
        cache.set("zz91daohang_getdaohangtype"+str(pingyin),ldbresult[0],60*5)
        return ldbresult[0]
def gettagslabel(id):
    #获得缓存
    zz91daohang_gettagslabel=cache.get("zz91daohang_gettagslabel"+str(id))
    if zz91daohang_gettagslabel:
        return zz91daohang_gettagslabel 
    sql='select tags from tags where id=%s'
    #cursor_tags.execute(sql,[id])
    #result=cursor_tags.fetchone()
    result=dbt.fetchonedb(sql,[id])
    if result:
        #设置缓存
        cache.set("zz91daohang_gettagslabel"+str(id),result[0],60*5)
        return result[0]
def gettagscategorycode(tags_id):
    sql="select category_products_main_code,pingyin from tags_category where tags_id=%s"
    #cursor_tags.execute(sql,[tags_id])
    #arrtags=cursor_tags.fetchone()
    arrtags=dbt.fetchonedb(sql,[tags_id])
    if (arrtags):
        return {'category_products_main_code':arrtags[0],'pingyin':arrtags[1]}
def getnav(tags_id):
    nav=gettagscategorycode(tags_id)
    if nav:
        navlist=str(nav['category_products_main_code'])
        navlen=len(navlist)
        if navlen==4:
            return "<a href='/tags-"+navlist[0:4]+"/'>"+getprolabel(navlist[0:4])+"</a>"
        if navlen==8:
            return "<a href='/tags-"+navlist[0:4]+"/'>"+getprolabel(navlist[0:4])+"</a>&nbsp;/&nbsp;<a href='/tags-"+navlist[0:8]+"/'>"+getprolabel(navlist[0:8])+"</a>"
        if navlen==12:
            return "<a href='/tags-"+navlist[0:4]+"/'>"+getprolabel(navlist[0:4])+"</a>&nbsp;/&nbsp;<a href='/tags-"+navlist[0:8]+"/'>"+getprolabel(navlist[0:8])+"</a>&nbsp;/&nbsp;<a href='/tags-"+navlist[0:12]+"/'>"+getprolabel(navlist[0:12])+"</a>"
        if navlen==16:
            return "<a href='/tags-"+navlist[0:4]+"/'>"+getprolabel(navlist[0:4])+"</a>&nbsp;/&nbsp;<a href='/tags-"+navlist[0:8]+"/'>"+getprolabel(navlist[0:8])+"</a>&nbsp;/&nbsp;<a href='/tags-"+navlist[0:12]+"/'>"+getprolabel(navlist[0:12])+"</a>&nbsp;/&nbsp;<a href='/tags-"+navlist[0:16]+"/'>"+getprolabel(navlist[0:16])+"</a>"
def getmoreproperty(listmore,text,value):
    if (value!="" and value!=None):
        value=value.strip()
        listmore.append({'property':text,'content':value})
    return listmore
#获得留言数
def getquestioncount(company_id):
    sqlg="select qcount from inquiry_count where company_id=%s"
    #cursor.execute(sqlg,company_id)
    #phoneresult=cursor.fetchone()
    phoneresult=dbc.fetchonedb(sqlg,company_id)
    if phoneresult:
        return phoneresult[0]
    else:
        return None
def getprolabel(code):
    sql="select label,code from category_products where code='"+code+"'"
    #cursor.execute(sql)
    #result=cursor.fetchone()
    result=dbc.fetchonedb(sql)
    if result:
        label=result[0]
        if not label:
            return ""
        return label
#获得城市信息
def getnavareavalue(code):
    sql="select label,code from category where code='"+code+"'"
    #cursor.execute(sql)
    #result=cursor.fetchone()
    result=dbc.fetchonedb(sql)
    if result:
        area2=result[0]
        return result
def getcategorylabel(code):
    if code:
        sql="select label from category where code='"+code+"'"
        #cursor.execute(sql)
        #result=cursor.fetchone()
        result=dbc.fetchonedb(sql)
        if result:
            return result[0]
#----判断是否样品
def getyangflag(products_id):
    sql="select a.sample_id from sample_relate_product as a left join sample as b on a.sample_id=b.id where product_id=%s and b.is_del=0"
    #cursor.execute(sql,[products_id])
    #productlist = cursor.fetchone()
    productlist=dbc.fetchonedb(sql,[products_id])
    if productlist:
        return productlist[0]
#----获得拿样价
def gettakeprice(sample_id):
    sql='select take_price from sample where id=%s'
    #cursor.execute(sql,sample_id)
    #result = cursor.fetchone()
    result=dbc.fetchonedb(sql,sample_id)
    if result:
        return result[0]
def getproductsinfo(pdtid,cursor,keywords):
    keywords=keywords.replace('\\','')
    keywords=keywords.replace('/','')
    keywords=keywords.replace('/','')
    keywords=keywords.replace('(','')
    keywords=keywords.replace(')','')
    keywords=keywords.replace('+','')
    sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%Y/%m/%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit,p.quantity,DATE_FORMAT(p.expire_time,'%Y-%m-%d'),DATEDIFF(p.expire_time,CURDATE()) as yxtime,p.quantity_unit,f.label,c.address,DATE_FORMAT(c.regtime,'%Y-%m-%d'),c.area_code,p.check_status,p.tags,p.source,p.specification,p.impurity,p.color,p.useful,p.appearance,p.manufacture,p.origin,p.tags FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code left outer join category_products as f on p.category_products_main_code=f.code where p.id="+str(pdtid)+""
    #cursor.execute(sql)
    #productlist = cursor.fetchone()
    productlist=dbc.fetchonedb(sql)
    if productlist:
        arrpdt_kind={'kindtxt':'','kindclass':''}
        pdt_kind=productlist[3]
        viptype=str(productlist[9])
        if (str(pdt_kind) == '1'):
            arrpdt_kind['kindtxt']='求购'
            arrpdt_kind['kindclass']='buy'
        else:
            arrpdt_kind['kindtxt']='供应'
            arrpdt_kind['kindclass']='sell'
        arrviptype={'vippic':'','vipname':'','vipclass':'','vipsubname':'','vipcheck':'','com_fqr':'','zstNum':'','ldb':''}
        if (viptype == '10051000'):
            arrviptype['vippic']=None
            arrviptype['vipname']='普通会员'
        if (viptype == '10051001'):
            arrviptype['vippic']='http://img.zz91.com/zz91images/recycle.gif'
            arrviptype['vipname']='再生通'
            arrviptype['vipclass']='zst_logo'
        if (viptype == '100510021000'):
            arrviptype['vippic']='http://img.zz91.com/zz91images/pptSilver.gif'
            arrviptype['vipname']='银牌品牌通'
            arrviptype['vipclass']='ypppt_logo'
        if (viptype == '100510021001'):
            arrviptype['vippic']='http://img.zz91.com/zz91images/pptGold.gif'
            arrviptype['vipname']='金牌品牌通'
            arrviptype['vipclass']='jpppt_logo'
        if (viptype == '100510021002'):
            arrviptype['vippic']='http://img.zz91.com/zz91images/pptDiamond.gif'
            arrviptype['vipname']='钻石品牌通'
            arrviptype['vipclass']='zsppt_logo'
        if (viptype == '10051003'):
            arrviptype['vippic']=''
            arrviptype['vipname']='来电宝客户'
            arrviptype['vipclass']='ldb_logo'
        if (viptype == '10051000'):
            arrviptype['vipcheck']=None
        else:
            arrviptype['vipcheck']=1
        #来电宝客户
        company_id=productlist[0]
        if company_id:
            sqll="select id from crm_company_service where company_id=%s and crm_service_code in(1007,1008,1009,1010) and apply_status=1"
            #cursor.execute(sqll,[company_id])
            #ldbresult=cursor.fetchone()
            ldbresult=dbc.fetchonedb(sqll,[company_id])
            if ldbresult:
                sqlg="select front_tel from phone where company_id="+str(company_id)+" and expire_flag=0"
                #cursor.execute(sqlg)
                #phoneresult=cursor.fetchone()
                phoneresult=dbc.fetchonedb(sqlg)
                if phoneresult:
                    arrviptype['ldb']={'ldbphone':phoneresult[0]}
                else:
                    arrviptype['ldb']=None
            else:
                arrviptype['ldb']=None
        arrviptype['vipsubname'] = productlist[7]
        arrviptype['com_fqr']=''
        com_province=productlist[10]
        if (com_province==None):
            com_province=''
        pdt_images=""
        area_code=productlist[21]
        #地区信息
        if (area_code):
            sqld="select label from category where code='"+str(area_code[:-4])+"'"
            #cursor.execute(sqld)
            #arealabel = cursor.fetchone()
            arealabel=dbc.fetchonedb(sqld)
            if arealabel:
                if arealabel[0]:
                    com_province=arealabel[0]+' '+com_province
                    
        arrcompinfo=None
        bindweixin=None
        sqld="select qq,account from company_account where company_id=%s"
        #cursor.execute(sqld,[productlist[0]])
        #compqq = cursor.fetchone()
        compqq=dbc.fetchonedb(sqld,[productlist[0]])
        if compqq:
            qq=compqq[0]
            if qq:
                qq=qq.strip()
            if (qq==""):
                qq=None
            if (qq):
                arrcompinfo={'qq':qq}
            account=compqq[1]
            #bindweixin=isbindweixin(account)
        #价格范围判断
        allprice=""
        min_price=productlist[11]
        if (min_price==None):
            min_price=''
        else:
            min_price=str(min_price)
            if (min_price!='0.0'):
                allprice=allprice+min_price
        max_price=productlist[12]
        if (max_price==None):
            max_price=''
        else:
            max_price=str(max_price)
            if (max_price!='0.0' and max_price!=min_price):
                allprice=allprice+'-'+max_price
        price_unit=productlist[13]
        #
        if (price_unit==None):
            price_unit=''
        else:
            if (allprice!=''):
                allprice=allprice+price_unit
                
        total_quantity=productlist[14]
        quantity_unit=productlist[17]
        if (quantity_unit==None):
            quantity_unit=''
        if (total_quantity=='' or total_quantity==' ' or total_quantity==None):
            total_quantity=None
        else:
            total_quantity=total_quantity+quantity_unit

        procatetype=productlist[18]
        if (procatetype!=None):
            procatetype=procatetype.replace('|',' ')
            procatetype=procatetype.replace('\\',' ')
            procatetype=procatetype.replace('/',' ')
            procatetype=procatetype.replace('(',' ')
            procatetype=procatetype.replace(')',' ')

        
        
        #----
        sql1="select pic_address from products_pic where product_id="+str(productlist[2])+" and check_status=1 order by is_default desc,id desc"
        #cursor.execute(sql1)
        #productspic = cursor.fetchone()
        productspic=dbc.fetchonedb(sql1)
        if productspic:
            pdt_images=productspic[0]
        else:
            pdt_images=""
        if (pdt_images == '' or pdt_images == '0'):
            pdt_images='../cn/img/noimage.gif'
        else:
            pdt_images='http://img3.zz91.com/122x93/'+pdt_images+''
        #发起人标志
        zs=None
        cxcompany=None
        if (company_id!=None):
            sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001001' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
            #cursor.execute(sql1)
            #fqrflag = cursor.fetchone()
            fqrflag=dbc.fetchonedb(sql1)
            if fqrflag:
                fqr=1
            else:
                fqr=None
            
            #诚信会员
            sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001005' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
            #cursor.execute(sql1)
            #cxflag = cursor.fetchone()
            cxflag=dbc.fetchonedb(sql1)
            if cxflag:
                cxcompany=1
            else:
                cxcompany=None

            #终生会员
            sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001003' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
            #cursor.execute(sql1)
            #zsflag = cursor.fetchone()
            zsflag=dbc.fetchonedb(sql1)
            if zsflag:
                zs=1
            else:
                zs=None
            zst_year=0
            #年限
            sql2="select sum(zst_year) from crm_company_service where company_id="+str(company_id)+" and apply_status=1"
            #cursor.execute(sql2)
            #zstNumvalue = cursor.fetchone()
            zstNumvalue=dbc.fetchonedb(sql2)
            if zstNumvalue:
                zst_year=zstNumvalue[0]
            arrviptype['zstNum']=zst_year
        else:
            fqr=None
        #供求更多属性
        sqlm="select property,content from product_addproperties where pid=%s"
        #cursor.execute(sqlm,[productlist[2]])
        #resultmore=cursor.fetchall()
        resultmore=dbc.fetchalldb(sqlm,[productlist[2]])
        listmore=[]
        if resultmore:
            for ll in resultmore:
                if (ll[1]!=None):
                    contentp=ll[1].strip()
                    if (contentp==""):
                        contentp=None
                else:
                    contentp=None
                list={'property':ll[0],'content':contentp}
                listmore.append(list)
        source=productlist[24]
        listmore=getmoreproperty(listmore,'货源地',source)
        origin=productlist[31]
        listmore=getmoreproperty(listmore,'来源产品',origin)
        specification=productlist[25]
        listmore=getmoreproperty(listmore,'产品规格',specification)
        impurity=productlist[26]
        listmore=getmoreproperty(listmore,'杂质含量',impurity)
        color=productlist[27]
        listmore=getmoreproperty(listmore,'颜色',color)
        useful=productlist[28]
        listmore=getmoreproperty(listmore,'用途',useful)
        appearance=productlist[29]
        listmore=getmoreproperty(listmore,'外观',appearance)
        manufacture=productlist[30]
        listmore=getmoreproperty(listmore,'加工说明',getcategorylabel(manufacture))
        
        #询盘量
        questioncount=None
        if company_id:
            questioncount=getquestioncount(company_id)
        tagslist=[]
        tags=productlist[32]
        if tags:
            tagsarray=tags.split(",")
            for i in tagsarray:
                l={'label':i,'label_hex':getjiami(i)}
                tagslist.append(l)
        yangflag=getyangflag(pdtid)
        #拿样价
        takeprice=''
        if yangflag:
            takeprice=gettakeprice(yangflag)
        
        
        
        pdt_name=productlist[4]
        list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
        ,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5],'pdt_detailfull':productlist[5]
        ,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype,'check_status':productlist[22]
        ,'pdt_images':pdt_images,'pdt_price':allprice
        ,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'fqr':fqr
        ,'cxcompany':cxcompany,'total_quantity':total_quantity,'procatetype':procatetype
        ,'zs':zs,'xianhuoid':'','questioncount':questioncount,'tagslist':tagslist
        ,'arrcompinfo':arrcompinfo,'listmore':listmore,'bindweixin':bindweixin,'yangflag':yangflag,'takeprice':takeprice}
    else:
        list1=None
        
    #list1=getproid(pdtid)
    if (list1 == None):
        return None
    else:
        pdt_images=list1['pdt_images']
        if (pdt_images=='../cn/img/noimage.gif'):
            list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
        pdt_detail=filter_tags(list1['pdt_detail'])
        pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
        docs=[pdt_detail]
        list1['pdt_detail']=subString(pdt_detail,30)+'...'
        """
        sqlxx="select id from products_spot where product_id=%s"
        cursor.execute(sqlxx,[pdtid])
        result=cursor.fetchone()
        if result:
            list1['xianhuoid']=result[0]
        else:
            list1['xianhuoid']=None
        """
        pdt_name=list1['pdt_name']
        docs=[pdt_name]
        pdt_name=pdt_name.replace(keywords,'<em>'+keywords+'</em>')
        #for k in keywords:
            #pdt_name=pdt_name.replace(k,'<em>'+k+'</em>')
        list1['pdt_name']=pdt_name    
        
    return list1
def getcompinfo(pdtid,cursort,keywords):
    list1=cache.get("daohang_compinfo"+str(pdtid))
    if not list1:
        sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%Y/%m/%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code where p.id="+str(pdtid)+""
        #cursort.execute(sql)
        #productlist = cursort.fetchone()
        productlist=dbc.fetchonedb(sql)
        if productlist:
            arrpdt_kind={'kindtxt':'','kindclass':''}
            pdt_kind=productlist[3]
            viptype=str(productlist[9])
            if (str(pdt_kind) == '1'):
                arrpdt_kind['kindtxt']='求购'
                arrpdt_kind['kindclass']='buy'
            else:
                arrpdt_kind['kindtxt']='供应'
                arrpdt_kind['kindclass']='sell'
            arrviptype={'vippic':'','vipname':'','vipsubname':'','vipcheck':'','com_fqr':''}
            if (viptype == '10051000'):
                arrviptype['vippic']=None
                arrviptype['vipname']='普通会员'
            if (viptype == '10051001'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/recycle.gif'
                arrviptype['vipname']='再生通'
            if (viptype == '100510021000'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/pptSilver.gif'
                arrviptype['vipname']='银牌品牌通'
            if (viptype == '100510021001'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/pptGold.gif'
                arrviptype['vipname']='金牌品牌通'
            if (viptype == '100510021002'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/pptDiamond.gif'
                arrviptype['vipname']='钻石品牌通'
            if (viptype == '10051000'):
                arrviptype['vipcheck']=None
            else:
                arrviptype['vipcheck']=1
            arrviptype['vipsubname'] = productlist[7]
            arrviptype['com_fqr']=''
            com_province=productlist[10]
            if (com_province==None):
                com_province=''
            pdt_images=""
            sql1="select pic_address from products_pic where product_id="+str(productlist[2])+" and check_status=1"
            #cursort.execute(sql1)
            #productspic = cursort.fetchone()
            productspic=dbc.fetchonedb(sql1)
            if productspic:
                pdt_images=productspic[0]
            else:
                pdt_images=""
            if (pdt_images == '' or pdt_images == '0'):
                pdt_images='../cn/img/noimage.gif'
            else:
                pdt_images='http://img3.zz91.com/118x85/'+pdt_images+''
            list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
            ,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5]
            ,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype
            ,'pdt_images':pdt_images,'pdt_price':productlist[8]
            ,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1}
        else:
            list1=None
            
        #list1=getproid(pdtid)
        if (list1 == None):
            return None
        else:
            pdt_images=list1['pdt_images']
            if (pdt_images=='../cn/img/noimage.gif'):
                list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
            pdt_detail=stripTags(list1['pdt_detail'])
            pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
            docs=[pdt_detail]
            list1['pdt_detail']=subString(pdt_detail,150)+'...'
            
            pdt_name=list1['pdt_name']
            #pdt_name=getlightkey(keywords,pdt_name)
            docs=[pdt_name]
            if (keywords!="" and keywords!=None):
                pdt_name=pdt_name.replace(keywords,"<font color=red>"+keywords+"</font>")
            #pdt_name=pdt_name.replace(keywords,'<font color=#F30/>'+keywords+'</font>')
            list1['pdt_name']=pdt_name
            cache.set("daohang_compinfo"+str(pdtid),list1,60*60)    
    return list1
##过滤HTML中的标签
def stripTags(s):
    intag = [False]
    def chk(c):
        if intag[0]:
            intag[0] = (c != '>')
            return False
        elif c == '<':
            intag[0] = True
            return False
        return True
    return ''.join(c for c in s if chk(c))
def getnum_str(numstr,nowcode,num):
    if (str(numstr)=='None' or str(numstr)==''):
        return num
    else:
        nstr=numstr.split(',')
        for i in nstr:
            ii=i.split(':')
            if (len(ii)>=1):
                if (str(ii[0])==nowcode):
                    num= int(ii[1])
    return num
#关键字加亮
def getlightkey(keywords,content):
    content=stripTags(content)
    p=""
    for a in keywords:
        #if (content.find(a)>0):
        #p=p+a.decode('utf-8')+content
        content=content.replace(str(a),"<font color=red>"+str(a)+"</font>")
    return content
#关键字加亮  搜索引擎
def getlightkeywords(cl,docs,words,index):
    opts = {'before_match':'<font color=red>', 'after_match':'</font>', 'chunk_separator':' ... ', 'limit':400, 'around':15}
    tagscrl = cl.BuildExcerpts(docs, index, words, opts)
    if tagscrl:
        return tagscrl[0]
    else:
        return docs
#判断是否为HEX码
def gethextype(keywords):
    zwtype=0
    zwflag=0
    strvalue="abcdef0123456789"
    for a in keywords:
        if (a >= u'\u4e00' and a<=u'\u9fa5'):
            zwflag=zwflag+1
    if zwflag>0:
        zwtype=1
    zwflag=0
    if zwtype==0:
        for a in keywords:
            if (strvalue.find(a)==-1):
                zwflag=zwflag+1
        if zwflag>0:
            zwtype=1
    if zwtype==1:
        return False
    else:
        return True
def subString(string,length): 
    if string:  
        if length >= len(string):   
            return string   
        result = ''  
        i = 0  
        p = 0  
        while True:   
            ch = ord(string[i])   
            #1111110x   
            if ch >= 252:   
                p = p + 6  
            #111110xx   
            elif ch >= 248:   
                p = p + 5  
            #11110xxx   
            elif ch >= 240:   
                p = p + 4  
            #1110xxxx   
            elif ch >= 224:   
                p = p + 3  
            #110xxxxx   
            elif ch >= 192:
                p = p + 2  
            else:   
                p = p + 1       
            if p >= length:   
                break;
            else:   
                i = p   
        return string[0:i]
        pass
    else:
        return string
def _key_to_file(key):
    path = str(int(int(key) / 1000))
    return '/usr/data/offerlist/'+path+'/'
def getproid(id):
    fname = _key_to_file(id)
    if not (os.path.exists(fname+str(id)+'.pkl')):
        return None
    else:
        pkl_file = open(fname+str(id)+'.pkl','rb')
        return pickle.load(pkl_file)
        pkl_file.close()

#加密
def getjiami(strword):
    return strword.encode('utf8','ignore').encode("hex")
def getjiemi(strword):
    return strword.decode("hex").decode('utf8','ignore')
def gettagsName(id):
    listall=cache.get("daohang_tagsName"+str(id))
    if listall:
        return listall
    sql="select tags from tags where old_id=%s"
    #cursor_tags.execute(sql,id)
    #arrtags=cursor_tags.fetchone()
    arrtags=dbt.fetchonedb(sql,id)
    if (arrtags):
        tagsName=arrtags[0].encode('utf-8')
        cache.set("tags_tagsName"+str(id),tagsName,60*60)
        return tagsName
    else:
        sql="select tags from tags where id=%s"
        #cursor_tags.execute(sql,id)
        #arrtags=cursor_tags.fetchone()
        arrtags=dbt.fetchonedb(sql,id)
        if (arrtags):
            tagsName=arrtags[0].encode('utf-8')
            cache.set("daohang_tagsName"+str(id),tagsName,60*60)
            return tagsName
#记录点击次数
def tagschickNum(keywords):
    sql="update tags set search_count=search_count+1 where tags=%s"
    #cursor_tags.execute(sql,[keywords])
    #conn_tags.commit()
    dbt.updatetodb(sql,[keywords])
    

#广告
def getadlist(pkind,keywords):
    kname_hex=''
    if keywords:
        kname_hex=getjiami(keywords)
    listdir=cache.get("daohang_adlist"+str(pkind)+str(kname_hex))
    if not listdir:
        keystr="|1:"+keywords+"|"
        sql="select ad_content,ad_target_url,id from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and search_exact='"+str(keystr)+"' and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
        #cursor_ads.execute(sql,pkind)
        #alist = cursor_ads.fetchone()
        alist=dba.fetchonedb(sql,pkind)
        if alist:
            listdir={'url':'http://gg.zz91.com/hit?a='+str(alist[2]),'picaddress':alist[0]}
            cache.set("daohang_adlist"+str(pkind)+str(kname_hex),listdir,60*60)
    return listdir
#企业报价条数
def getpricelist_company_count(kname):
    company_price=SPHINXCONFIG['name']['company_price']['name']
    serverid=SPHINXCONFIG['name']['company_price']['serverid']
    port=SPHINXCONFIG['name']['company_price']['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    cl.SetLimits (0,1,1)
    try:
        res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'',company_price)
        if res:
            return res['total_found']
        return 0
    except:
        return 0
def getpricealllist(kname="",num=""):
    pricelist=SPHINXCONFIG['name']['pricelist']['name']
    serverid=SPHINXCONFIG['name']['pricelist']['serverid']
    port=SPHINXCONFIG['name']['pricelist']['port']
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,postdate desc" )
    if num:
        limitnum=num
    else:
        limitnum=30
    cl.SetLimits (0,limitnum,limitnum)
    if (kname!="" and kname):
        res = cl.Query ('@(title,typename,label,label1,label2,spec,spec1,spec2,area,area1,area2) '+kname+'',pricelist)
    else:
        res = cl.Query ('',pricelist)
    listall=[]
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            
            for match in tagslist:
                id=match['id']
                sql="select postdate,label,label1,label2,spec,spec1,spec2,area,area1,area2,price1,price2,price3,price4,price5,price6,unit,price,priceid,title from price_list where id=%s"
                #cursor.execute(sql,[id])
                #alist = cursor.fetchone()
                alist=dbc.fetchonedb(sql,[id])
                if alist:
                    postdate=alist[0]
                    label=alist[1]
                    purl=None
                    pcompcount=""
                    if label:
                        pcompcount=getpricelist_company_count(label)
                        if pcompcount==0:
                            purl=None
                        else:
                            purl="http://jiage.zz91.com/s/"+getjiami(label)+"-1/"
                    if label==None:
                        label=""
                    label1=alist[2]
                    if label1==None:
                        label1=""
                    label2=alist[3]
                    if label2==None:
                        label2=""
                    spec=alist[4]
                    if spec==None:
                        spec=""
                    spec1=alist[5]
                    if spec1==None:
                        spec1=""
                    spec2=alist[6]
                    if spec2==None:
                        spec2=""
                    area=alist[7]
                    if area==None:
                        area=""
                    area1=alist[8]
                    if area1==None:
                        area1=""
                    area2=alist[9]
                    if area2==None:
                        area2=""
                    price1=alist[10]
                    price2=alist[11]
                    price3=alist[12]
                    price4=alist[13]
                    price5=alist[14]
                    price6=alist[15]
                    unit=alist[16]
                    if unit==None:
                        unit=""
                    price=alist[17]
                    if not price:
                        price=""
                    priceid=alist[18]
                    title=alist[19]
                    list={'id':id,'priceid':priceid,'title':title,'postdate':postdate,'label':label,'label1':label1,'label2':label2,'spec':spec,'spec1':spec1,'spec2':spec2,'area':area,'area1':area1,'area2':area2,'price':price,'price1':price1,'price2':price2,'price3':price3,'price4':price4,'price5':price5,'price6':price6,'unit':unit,'pcompcount':pcompcount,'purl':purl}
                    listall.append(list)
                    
    return listall
                    
def newtagslist(kname,num):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listall=cache.get("daohang_newtagslist"+str(kname_hex)+str(num))
    if not listall:
        #-------------最新标签
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"search_count desc" )
        cl.SetLimits (0,num)
        
        if (kname):
            res = cl.Query ('@tname '+kname,'tagslist')
        else:
            res = cl.Query ('','tagslist')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                ii=1
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    tags=attrs['tags']
                    tags=tags.replace("/","")
                    list1={'kname':tags,'id':id,'classid':ii,'kname_hex':tags.encode("hex")}
                    listall.append(list1)
                    ii+=1
                    if (ii>2):
                        ii=1
                cache.set("daohang_newtagslist"+str(kname_hex)+str(num),listall,60*20)
    return listall
#相关供求类别
def getcategorylist(kname='',limitcount=''):
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    #cl.SetSortMode( SPH_SORT_EXTENDED,"sort desc" )
    if (limitcount!=''):
        cl.SetLimits (0,limitcount,limitcount)
    if (kname!=""):
        res = cl.Query (''+kname,'category_products')
    else:
        res = cl.Query ('','category_products')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                label=attrs['plabel']
                code=attrs['pcode']
                list1={'id':id,'code':code,'label':label,'label_hex':label.encode("hex")}
                listall.append(list1)
            return listall
#------供求列表右边报价固定导航
def getrightpricenav(code):
    navlist1=[]
    nav1={'label':'废铜','url':'http://jiage.zz91.com/feitong/'}
    navlist1.append(nav1)
    nav1={'label':'废铁','url':'http://jiage.zz91.com/feitie/'}
    navlist1.append(nav1)
    nav1={'label':'废钢','url':'http://jiage.zz91.com/feigang1/'}
    navlist1.append(nav1)
    nav1={'label':'废铝','url':'http://jiage.zz91.com/feilv/'}
    navlist1.append(nav1)
    nav1={'label':'废镍','url':'http://jiage.zz91.com/feinie/'}
    navlist1.append(nav1)
    nav1={'label':'废不锈钢','url':'http://jiage.zz91.com/feibuxiugang/'}
    navlist1.append(nav1)
    nav1={'label':'废钼钛','url':'http://jiage.zz91.com/feimutai/'}
    navlist1.append(nav1)
    nav1={'label':'国外废金属','url':'http://jiage.zz91.com/guowaifeijinshu/'}
    navlist1.append(nav1)
    nav1={'label':'江浙沪','url':'http://jiage.zz91.com/jiangzhehu/'}
    navlist1.append(nav1)
    nav1={'label':'山东','url':'http://jiage.zz91.com/shandong/'}
    navlist1.append(nav1)
    nav1={'label':'广东','url':'http://jiage.zz91.com/guangdong/'}
    navlist1.append(nav1)
    nav1={'label':'临沂','url':'http://jiage.zz91.com/linyi1/'}
    navlist1.append(nav1)
    nav1={'label':'清远','url':'http://jiage.zz91.com/qingyuan/'}
    navlist1.append(nav1)
    
    navlist2=[]
    nav1={'label':'PP','url':'http://jiage.zz91.com/pp/'}
    navlist2.append(nav1)
    nav1={'label':'PVC','url':'http://jiage.zz91.com/pvc/'}
    navlist2.append(nav1)
    nav1={'label':'PMMA','url':'http://jiage.zz91.com/PMMA/'}
    navlist2.append(nav1)
    nav1={'label':'EVA','url':'http://jiage.zz91.com/EVA/'}
    navlist2.append(nav1)
    nav1={'label':'HDPE','url':'http://jiage.zz91.com/HDPE/'}
    navlist2.append(nav1)
    nav1={'label':'LDPE','url':'http://jiage.zz91.com/LDPE/'}
    navlist2.append(nav1)
    nav1={'label':'TPU','url':'http://jiage.zz91.com/TPU/'}
    navlist2.append(nav1)
    nav1={'label':'PET','url':'http://jiage.zz91.com/PET/'}
    navlist2.append(nav1)
    nav1={'label':'ABS','url':'http://jiage.zz91.com/ABS/'}
    navlist2.append(nav1)
    nav1={'label':'PC','url':'http://jiage.zz91.com/PC/'}
    navlist2.append(nav1)
    nav1={'label':'GPPS','url':'http://jiage.zz91.com/GPPS/'}
    navlist2.append(nav1)
    nav1={'label':'余姚','url':'http://jiage.zz91.com/yuyao/'}
    navlist2.append(nav1)
    nav1={'label':'再生料','url':'http://jiage.zz91.com/suliaozaishengliaojiagehangqing/'}
    navlist2.append(nav1)
    nav1={'label':'新料出厂','url':'http://jiage.zz91.com/chuchangjia/'}
    navlist2.append(nav1)
    nav1={'label':'新料市场','url':'http://jiage.zz91.com/shichangjia/'}
    navlist2.append(nav1)
    
    navlist3=[]
    nav1={'label':'油价快报','url':'http://jiage.zz91.com/youjia/'}
    navlist3.append(nav1)
    nav1={'label':'废纸价格','url':'http://jiage.zz91.com/feizhigedijiage/'}
    navlist3.append(nav1)
    nav1={'label':'废橡胶价格','url':'http://jiage.zz91.com/guoneixiangjiao/'}
    navlist3.append(nav1)
    nav1={'label':'综合废料','url':'http://jiage.zz91.com/hangqingzongshu/'}
    navlist3.append(nav1)
                    
    if (code=='1000' or code=='1005' or code=='1007'):
        return navlist1
    if (code=='1001' or code=='1006' or code=='1003' or code=='1010' or code=='1011'):
        return navlist2
    if (code=='1002' or code=='1004' or code=='1008' or code=='1009'):
        return navlist3
def getpricelist(kname="",num=""):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listdir=cache.get("daohang_pricelist"+str(kname_hex)+str(num))
    if not listdir:
        #------最新报价信息
        price=SPHINXCONFIG['name']['price']['name']
        serverid=SPHINXCONFIG['name']['price']['serverid']
        port=SPHINXCONFIG['name']['price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
        if num:
            limitnum=num
        else:
            limitnum=30
        cl.SetLimits (0,limitnum)
        if (kname!="" and kname):
            res = cl.Query ('@(title,tags) '+kname+'',price)
        else:
            res = cl.Query ('',price)
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_baojia=[]
                for match in tagslist:
                    td_id=match['id']
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    fulltitle=title
                    #title=getlightkeywords(cl,[title],kname,'price')
                    gmt_time=attrs['gmt_time']
                    list1={'td_title':title,'fulltitle':fulltitle,'td_id':td_id,'td_time':gmt_time}
                    listall_baojia.append(list1)
                    havelist=listall_baojia
            listcount_baojia=res['total_found']
            if (listcount_baojia==0):
                havelist=None
                res = cl.Query ('','price')
                if res:
                    if res.has_key('matches'):
                        tagslist=res['matches']
                        listall_baojia=[]
                        for match in tagslist:
                            td_id=match['id']
                            attrs=match['attrs']
                            title=attrs['ptitle']
                            fulltitle=title
                            #title=getlightkeywords(cl,[title],kname,'price')
                            gmt_time=attrs['gmt_time']
                            list1={'td_title':title,'fulltitle':fulltitle,'td_id':td_id,'td_time':gmt_time}
                            listall_baojia.append(list1)
                    listcount_baojia=0
            listdir={'list':listall_baojia,'count':listcount_baojia,'havelist':havelist}
            cache.set("daohang_pricelist"+str(kname_hex)+str(num),listdir,60*20)
    return listdir
#企业报价
def getpricelist_company(kname="",num=""):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listdir=cache.get("daohang_pricelist_company"+str(kname_hex)+str(num))
    if not listdir:
        #------最新报价信息
        company_price=SPHINXCONFIG['name']['company_price']['name']
        serverid=SPHINXCONFIG['name']['company_price']['serverid']
        port=SPHINXCONFIG['name']['company_price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,post_time desc" )
        if num:
            limitnum=num
        else:
            limitnum=30
        cl.SetLimits (0,limitnum)
        res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'',company_price)
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_baojia=[]
                for match in tagslist:
                    td_id=match['id']
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    #title=getlightkeywords(cl,[title],kname,'company_price')
                    gmt_time=attrs['ppost_time']
                    price_unit=attrs['price_unit']
                    min_price=attrs['min_price']
                    max_price=attrs['max_price']
                    product_id=attrs['product_id']
                    #if (price=="" or price=="none"):
                    price=min_price+"-"+max_price+price_unit
                    #td_time=gmt_time.strftime('%Y-%m-%d')
                    list1={'td_title':title,'td_id':td_id,'product_id':product_id,'td_time':gmt_time,'price':price,'url':'http://jiage.zz91.com/cdetail/'+str(td_id)+'.html'}
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
            listdir={'list':listall_baojia,'count':listcount_baojia}
            cache.set("daohang_pricelist_company"+str(kname_hex)+str(num),listdir,60*20)
    return listdir
def getbbslist(kname="",num=""):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listdir=cache.get("daohang_bbslist"+str(kname_hex)+str(num))
    if not listdir:
        #最新互助信息
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,post_time desc" )
        if num:
            limitnum=num
        else:
            limitnum=30
        cl.SetLimits (0,limitnum,limitnum)
        res = cl.Query ('@(title,tags) '+kname,'huzhu')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                for match in tagslist:
                    td_id=match['id']
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    gmt_time=attrs['ppost_time']
                    sql="select content,account,company_id,reply_time from bbs_post where id=%s"
                    #cursor.execute(sql,td_id)
                    #alist = cursor.fetchone()
                    alist=dbc.fetchonedb(sql,td_id)
                    if alist:
                        #havepic=havepicflag(alist[0])
                        havepic=0
                        content=subString(filter_tags(alist[0]),50)
                        #username=getusername(alist[2])
                        username=""
                    else:
                        content=""
                        havepic=0
                        username=""
                    #replycount=gethuzhureplaycout(td_id)
                    replycount=0
                    list1={'td_title':subString(title,60),'td_title_f':title,'td_id':td_id,'td_time':gmt_time,'replycount':replycount,'content':content,'havepic':havepic,'username':username}
                    listall_news.append(list1)
                    havelist=listall_news
            listcount_news=res['total_found']
            listdir={'list':listall_news,'count':listcount_news,'havelist':havelist}
            cache.set("daohang_bbslist"+str(kname_hex)+str(num),listdir,60*60)
    return listdir    
def getofferlist(kname="",ckind="",num=""):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listdir=cache.get("daohang_offerlist"+str(kname_hex)+str(ckind)+str(num))
    if not listdir:
        #-----------供求信息
        port = settings.SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetFilter('check_status',[1])
        if ckind:
            cl.SetFilter('pdt_kind',[int(ckind)])
        cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
        if num:
            limitnum=num
        else:
            limitnum=50
        cl.SetLimits (0,1000,1000)
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                testcom_id=0
                pcount=0
                for match in tagslist:
                    id=match['id']
                    com_id=match['attrs']['company_id']
                    viptype=match['attrs']['viptype']
                    refresh_time=float(match['attrs']['refresh_time'])
                    pdt_date=float(match['attrs']['pdt_date'])
                    if (testcom_id==com_id):
                        pcount+=1
                    else:
                        pcount=0
                    list1=[id,pcount,viptype,refresh_time,pdt_date]
                    
                    #list1=getcompinfo(pdtid,cursor,kname)
                    listall.append(list1)
                    testcom_id=com_id
                #根据轮回排序
                listallvip=sorted(listall, key=lambda d:d[1])
                #根据日期排序
                changeflag=0
                listallvip1=[]
                listallvip2=[]
                m=0
                for i in listallvip:
                    m+=1
                    if (changeflag==int(i[1])):
                        list1=[i[0],i[1],i[2],i[3],i[4]]
                        listallvip2.append(list1)
                        if (len(listallvip)==m):
                            listallvip1+=listallvip2
                    else:
                        listallvip2=sorted(listallvip2, key=lambda a:a[4],reverse=True)
                        listallvip1+=listallvip2
                        listallvip2=[]
                        list1=[i[0],i[1],i[2],i[3],i[4]]
                        listallvip2.append(list1)
                        if (len(listallvip)==m):
                            listallvip1+=listallvip2
                    changeflag=int(i[1])
                listallvip=listallvip1
                
                #根据会员类型排序
                changeflag=0
                changeflag1=0
                listallvip1=[]
                listallvip2=[]
                m=0
                strchangeflag=''
                for i in listallvip:
                    m+=1
                    if ((changeflag==int(i[4]) and changeflag1==int(i[1])) or changeflag==0):
                        list1=[i[0],i[1],i[2],i[3],i[4]]
                        listallvip2.append(list1)
                        #strchangeflag+='|'+str(changeflag)+'*'+str(int(i[4]))
                        if (len(listallvip)==m):
                            listallvip1+=listallvip2
                    else:
                        listallvip2=sorted(listallvip2, key=lambda a:a[2],reverse=True)
                        listallvip1+=listallvip2
                        listallvip2=[]
                        list1=[i[0],i[1],i[2],i[3],i[4]]
                        listallvip2.append(list1)
                        if (len(listallvip)==m):
                            listallvip1+=listallvip2
                    changeflag=int(i[4])
                    changeflag1=int(i[1])
                listallvip=listallvip1
                
                #根据发布时间排序
                changeflag=0
                changeflag1=0
                changeflag2=0
                listallvip1=[]
                listallvip2=[]
                m=0
                for i in listallvip:
                    m+=1
                    if ((changeflag==int(i[2]) and changeflag1==int(i[1]) and changeflag2==int(i[4])) or changeflag==0):
                        list1=[i[0],i[1],i[2],i[3],i[4]]
                        listallvip2.append(list1)
                        if (len(listallvip)==m):
                            listallvip1+=listallvip2
                    else:
                        listallvip2=sorted(listallvip2, key=lambda d:d[3],reverse=True)
                        listallvip1+=listallvip2
                        listallvip2=[]
                        list1=[i[0],i[1],i[2],i[3],i[4]]
                        listallvip2.append(list1)
                        if (len(listallvip)==m):
                            listallvip1+=listallvip2
                    changeflag=int(i[2])
                    changeflag1=int(i[1])
                    changeflag2=int(i[4])
                listallvip=listallvip1
            #列出供求信息列表
            listall=[]
            for match in listallvip[0:limitnum]:
                list1=getproductsinfo(match[0],cursor,kname)
                listall.append(list1)
            listcount=res['total_found']
            listdir={'list':listall,'count':listcount}
            cache.set("daohang_offerlist"+str(kname_hex)+str(ckind)+str(num),listdir,60*60)
    return listdir
    
def newcustmerprice(kname):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listall=cache.get("daohang_newcustmerprice"+str(kname_hex))
    if not listall:
        #-------------最新产品企业报价
        company_price=SPHINXCONFIG['name']['company_price']['name']
        serverid=SPHINXCONFIG['name']['company_price']['serverid']
        port=SPHINXCONFIG['name']['company_price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
        cl.SetLimits (0,20,20)
        res = cl.Query ('@title '+kname,company_price)
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    title=subString(title,12)
                    gmt_time=attrs['ppost_time']
                    price=subString(attrs['price'],12)
                    list1={'pdt_name':title,'id':id,'pdt_price':price}
                    listall.append(list1)
                cache.set("daohang_newcustmerprice"+str(kname_hex),listall,60*60)
    return listall
            
#类别列表
def getindexcategorylist(code,showflag):
    l=len(code)
    listall_cate=cache.get("daohang_indexcategroy"+str(code))
    if not listall_cate:
        sql="select label,code from category_products where code like '"+str(code)+"____' order by sort asc"
        #cursor.execute(sql)
        listall_cate=[]
        #catelist=cursor.fetchall()
        catelist=dbc.fetchalldb(sql)
        for a in catelist:
            if (showflag==1):
                sql1="select label from category_products where code like '"+str(a[1])+"____' order by sort asc"
                #cursor.execute(sql1)
                listall_cate1=[]
                #catelist1=cursor.fetchall()
                catelist1=dbc.fetchalldb(sql1)
                for b in catelist1:
                    list1={'label':b[0],'label_hex':getjiami(b[0])}
                    listall_cate1.append(list1)
            else:
                listall_cate1=None
            list={'label':a[0],'label_hex':getjiami(a[0]),'code':a[1],'catelist':listall_cate1}
            listall_cate.append(list)
            cache.set("daohang_indexcategroy"+str(code),listall_cate,60*60000)
    return listall_cate
def getcategory_productsname(code):
    sql="select label from category_products where code=%s"
    #cursor.execute(sql,[code])
    #catelist=cursor.fetchone()
    catelist=dbc.fetchonedb(sql,[code])
    if catelist:
        return catelist[0]
    
#---标签库首页有图片的最新供求列表
def getindexofferlist_pic(kname="",pdt_type="",limitcount="",company_id=""):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listall_offerlist=cache.get("daohang_indexofferlistpic"+str(kname_hex)+str(pdt_type)+str(limitcount)+str(company_id))
    listall_offerlist=None
    if not listall_offerlist:
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," company_id desc,refresh_time desc" )
        cl.SetLimits (0,limitcount,limitcount)
        if (pdt_type!=None and pdt_type!=""):
            cl.SetFilter('pdt_kind',[int(pdt_type)])
        if company_id:
            cl.SetFilter('company_id',[int(company_id)])
        cl.SetFilterRange('havepic',1,100)
        if (kname==None or kname==""):
            res = cl.Query ('','offersearch_new,offersearch_new_vip')
        else:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                listall_offerlist=[]
                for match in itemlist:
                    pid=match['id']
                    attrs=match['attrs']
                    pdt_date=attrs['pdt_date']
                    pdt_kind=attrs['pdt_kind']
                    kindtxt=''
                    if (pdt_kind=='1'):
                        kindtxt="供应"
                    if (pdt_kind=='2'):
                        kindtxt="求购"
                    title=subString(attrs['ptitle'],40)
                    sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc"
                    #cursor.execute(sql1,[pid])
                    #productspic = cursor.fetchone()
                    productspic=dbc.fetchonedb(sql1,[pid])
                    if productspic:
                        pdt_images=productspic[0]
                    else:
                        pdt_images=""
                    if (pdt_images == '' or pdt_images == '0'):
                        pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                    else:
                        pdt_images='http://img3.zz91.com/100x100/'+pdt_images+''
                    list={'id':pid,'title':title,'gmt_time':pdt_date,'kindtxt':kindtxt,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images}
                    listall_offerlist.append(list)
                cache.set("daohang_indexofferlistpic"+str(kname_hex)+str(pdt_type)+str(limitcount)+str(company_id),listall_offerlist,60*60)
    return listall_offerlist
def getcompanyindexcomplist(kname,num):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listall_company=cache.get("daohang_indexcompanylist"+str(kname_hex)+str(num))
    listall_company=None
    if not listall_company:
        #-------------最新加入企业
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC, gmt_start desc" )
        cl.SetLimits (0,num,num)
        #cl.SetFilter('apply_status',[1])
    
        nowdate=date.today()-timedelta(days=360)
        nextday=date.today()+timedelta(days=1)
        formatnowdate=time.mktime(nowdate.timetuple())
        formatnextday=time.mktime(nextday.timetuple())
        #cl.SetFilterRange('gmt_start',int(formatnowdate),int(formatnextday))
        
        if (kname):
            res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
        else:
            res = cl.Query ('','company')
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                listall_company=[]
                for match in itemlist:
                    id=match['id']
                    attrs=match['attrs']
                    comname=attrs['compname']
                    business=attrs['pbusiness']
                    area_province=attrs['parea_province']
                    domain_zz91=attrs['domain_zz91']
                    company_id=id
                    if company_id:
                        sqll="select id from crm_company_service where company_id=%s and crm_service_code in(1007,1008,1009,1010) and apply_status=1"
                        #cursor.execute(sqll,[company_id])
                        #ldbresult=cursor.fetchone()
                        ldbresult=dbc.fetchonedb(sqll,[company_id])
                        if ldbresult:
                            ldbflag=1
                        else:
                            ldbflag=None
                    if domain_zz91:
                        domain_zz91=domain_zz91.strip()
                    if domain_zz91=="":
                        url="http://company.zz91.com/compinfo"+str(id)+".htm"
                        urllx="http://company.zz91.com/compinfo"+str(id)+".htm"
                    else:
                        url="http://"+domain_zz91+".zz91.com"
                        urllx="http://"+domain_zz91+".zz91.com/lxfs.htm"
                    if ldbflag==1:
                        url="http://www.zz91.com/ppc/index"+str(id)+".htm"
                        urllx="http://www.zz91.com/ppc/contact"+str(id)+".htm"
                    oneofferpic=getindexofferlist_pic(limitcount=1,company_id=id)
                    if oneofferpic:
                        oneofferpic=oneofferpic[0]
                    list={'id':id,'comname':comname,'business':business,'area_province':area_province,'domain_zz91':domain_zz91,'url':url,'urllx':urllx,'oneofferpic':oneofferpic,'ldbflag':ldbflag}
                    listall_company.append(list)
                cache.set("daohang_indexcompanylist"+str(kname_hex)+str(num),listall_company,60*60)
    return listall_company
def englishlist():
    pinyin=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    return pinyin    
#-------------------------
def getdaohanglist(sid):
    listall=cache.get("daohang_daohanglist"+str(sid))
    if not listall:
        sql="select id,label,pingyin,templates,ord,sid from daohang where sid="+str(sid)+" order by ord asc"
        #cursor.execute(sql)
        listall=[]
        #complist=cursor.fetchall()
        complist=dbc.fetchalldb(sql)
        for a in complist:
            list={'id':a[0],'sid':a[5],'label':a[1],'pingyin':a[2],'templates':a[3],'ord':a[4]}
            listall.append(list)
        if listall:
            cache.set("daohang_daohanglist"+str(sid),listall,60*60)
    return listall
#----------#获得查看更多栏
def getdaohanglist1(sid,num):
    sql="select label,pingyin from daohang where sid in (%s) order by ord asc limit 0,%s"
    #cursor.execute(sql,[sid,num])
    listall=[]
    #complist=cursor.fetchall()
    complist=dbc.fetchalldb(sql,[sid,num])
    for a in complist:
        list={'label':a[0],'pingyin':a[1]}
        listall.append(list)
    return listall
def getmdaohanglist():
    listall=cache.get("daohang_mdaohanglist")
    if not listall:
        sql="select id,label,pingyin,templates,ord,sid from daohang where id<22 order by id"
        #cursor.execute(sql)
        listall=[]
        #complist=cursor.fetchall()
        complist=dbc.fetchalldb(sql)
        for a in complist:
            list={'id':a[0],'sid':a[5],'label':a[1],'pingyin':a[2],'templates':a[3],'ord':a[4]}
            listall.append(list)
        if listall:
            cache.set("daohang_mdaohanglist",listall,60*60)
    return listall
def getdaohanglist_child(sid):
    listall=cache.get("daohang_daohanglist_child"+str(sid))
    if not listall:
        sql="select id,label,pingyin,templates,ord,sid,keywords2 from daohang where sid="+str(sid)+" order by ord asc"
        #cursor.execute(sql)
        listall=[]
        #complist=cursor.fetchall()
        complist=dbc.fetchalldb(sql)
        for a in complist:
            childlist=getdaohanglist(a[0])
            keywords2=a[6]
            priceInfo=getpricelist_daohang(kname=keywords2,limitcount=10,titlelen=100)
            list={'id':a[0],'sid':a[5],'label':a[1],'pingyin':a[2],'templates':a[3],'ord':a[4],'childlist':childlist,'priceInfo':priceInfo,'keywords2':keywords2}
            listall.append(list)
        if listall:
            cache.set("daohang_daohanglist_child"+str(sid),listall,60*60)
    return listall
def gettagslist(kname,num):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listall=cache.get("daohang_tagslist"+str(kname_hex)+str(num))
    if not listall:
        #-------------标签列表
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," search_count desc" )
        cl.SetLimits (0,num,num)
        res = cl.Query ('@tname '+kname,'tagslist')
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                listall=[]
                i=1
                for match in itemlist:
                    attrs=match['attrs']
                    id=attrs['tid']
                    tname=str(attrs['tags'])
                    list={'id':id,'name':tname,'n':i}
                    listall_tagslist.append(list)
                    i+=1
                    if (i>3):
                        i=1
                cache.set("daohang_tagslist"+str(kname_hex)+str(num),listall,60*60)
    return listall

def gettagstypelist(code,frompageCount="",limitNum="",num=""):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_EXTENDED2 )
    cl.SetSortMode( SPH_SORT_EXTENDED," search_count desc" )
    cl.SetLimits (frompageCount,limitNum,num)
    codelen=len(code)
    if codelen==4:
        sfild="@main_code1"
    if codelen==8:
        sfild="@main_code2"
    if codelen==12:
        sfild="@main_code3"
    if codelen==16:
        sfild="@category_products_main_code"
    res = cl.Query (sfild+" "+str(code),'tagslist')
    listall=[]
    listcount=0
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            for match in itemlist:
                attrs=match['attrs']
                id=attrs['tid']
                tname=str(attrs['tags'])
                tagscategory=gettagscategorycode(id)
                list={'id':id,'name':tname,'pingyin':tagscategory['pingyin'],'category_products_main_code':tagscategory['category_products_main_code'],'main_code':tagscategory['category_products_main_code'][0:4]}
                listall.append(list)
            listcount=res['total_found']
    return {'list':listall,'count':listcount}
#标签总数
def gettagsallcout():
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetLimits (0,1)
    res = cl.Query ('','tagslist')
    if res:
        listcount=res['total_found']
    return listcount
#企业总数
def getcompanyallcout(vip=""):
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    if vip:
        cl.SetFilter('apply_status',[1])
    cl.SetLimits (0,1)
    res = cl.Query ('','company')
    listcount=0
    if res:
        listcount=res['total_found']
        if not listcount:
            listcount=0
    return format(int(listcount*1.1),",")
#供求总数
def getproallcout():
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetLimits (0,1)
    res = cl.Query ('','offersearch_new,offersearch_new_vip')
    if res:
        listcount=res['total_found']
    return format(int(listcount*1.1),",")
#--获取资讯url
#def get_newstype(id,cursor_news):
def get_newstype(id):
    listdir=cache.get("daohang_newstype"+str(id))
    if not listdir:
        sql='select typeid,typeid2 from dede_archives where id=%s'
        #cursor_news.execute(sql,[id])
        #result=cursor_news.fetchone()
        result=dbn.fetchonedb(sql,[id])
        if result:
            typeid=result[0]
            typeid2=result[1]
            sql2='select typename,keywords from dede_arctype where id=%s'
            #cursor_news.execute(sql2,[typeid])
            #result2=cursor_news.fetchone()
            result2=dbn.fetchonedb(sql2,[typeid])
            if result2:
                listdir={'typename':result2[0],'url':result2[1],'typeid':typeid,'typeid2':typeid2,'url2':''}
                if typeid2!='0':
                    sql3='select keywords from dede_arctype where id=%s'
                    #cursor_news.execute(sql3,[typeid2])
                    #result3=cursor_news.fetchone()
                    result3=dbn.fetchonedb(sql3,[typeid2])
                    if result3:
                        listdir['url2']=result3[0]
                cache.set("daohang_newstype"+str(id),listdir,60*60)
    return listdir
#----资讯列表
def getnewslist(keywords="",frompageCount="",limitNum="",typeid="",allnum="",typeid2="",contentflag=""):
    cursor_news = conn_news.cursor()
    news=SPHINXCONFIG['name']['news']['name']
    serverid=SPHINXCONFIG['name']['news']['serverid']
    port=SPHINXCONFIG['name']['news']['port']
#    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    if (typeid):
        cl.SetFilter('typeid',typeid)
    if (typeid2):
        cl.SetFilter('typeid2',[typeid2])
    cl.SetSortMode( SPH_SORT_EXTENDED,'@weight DESC,@id desc' )
    if (allnum):
        cl.SetLimits (frompageCount,limitNum,allnum)
    else:
        cl.SetLimits (frompageCount,limitNum)
    if (keywords):
        res = cl.Query ('@(title,description) '+keywords,news)
    else:
        res = cl.Query ('',news)
    listall_news=[]
    listcount_news=0
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            for match in tagslist:
                id=match['id']
                newsurl=get_newstype(id)
                weburl="http://news.zz91.com"
                if newsurl:
                    if newsurl["url2"]:
                        weburl+="/"+newsurl["url2"]
                    weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
#                newsurl='news'
                attrs=match['attrs']
                fulltitle=attrs['ptitle']
                
                title=subString(fulltitle,100)
#                title=getlightkeywords(cl,[title],keywords,"news")
                
                pubdate=attrs['pubdate']
                pubdate2=timestamp_datetime2(pubdate)
#                havepic=havepicflag(content)
                #littlecontent=subString(filter_tags(content),60)
                list1={'title':title,'fulltitle':fulltitle,'id':id,'pubdate':pubdate2,'newsurl':newsurl,'weburl':weburl}
                listall_news.append(list1)
            listcount_news=res['total_found']
    return {'list':listall_news,'count':listcount_news}

def timestamp_datetime2(value):
    format = '%Y-%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt


#----供求地区详情
def getproducts_area(company_id):
    listdir=cache.get("daohang_products_area"+str(company_id))
    if not listdir:
        sql='select label from category where code=(select area_code from company where id=%s)'
        #cursor.execute(sql,[company_id])
        #result1=cursor.fetchone()
        result1=dbc.fetchonedb(sql,[company_id])
        if result1:
            listdir={'source':result1[0]}
            cache.set("daohang_products_area"+str(company_id),listdir,60*60)
        return listdir

#----供应详情2条
def getproducts_detail(product_id):
    listdir=cache.get("daohang_products_detail"+str(product_id))
    if not listdir:
        sql='select quantity,quantity_unit,price,price_unit,refresh_time from products where id=%s'
        #cursor.execute(sql,[product_id])
        #result=cursor.fetchone()
        result=dbc.fetchonedb(sql,[product_id])
        if result:
            price=result[2]
            if price=="" or price==" ":
                price=None
            if price=="0.0":
                price=None
            listdir={'quantity':result[0],'quantity_unit':result[1],'price':price,'price_unit':result[3],'refresh_time':result[4]}
            cache.set("daohang_products_detail"+str(product_id),listdir,60*60)
    return listdir

def getpic_address(product_id):
    listdir=cache.get("daohang_pic_address"+str(product_id))
    if not listdir:
        sql='select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc'
        #cursor.execute(sql,[product_id])
        #ldbresult=cursor.fetchone()
        ldbresult=dbc.fetchonedb(sql,[product_id])
        if ldbresult:
            listdir=ldbresult[0]
            cache.set("daohang_pic_address"+str(product_id),listdir,60*60)
    return listdir

def offerlist(kname="",pdt_type="",limitcount="",havepic="",fromlimit=""):
    #-------------供求列表
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
    if (fromlimit):
        cl.SetLimits (fromlimit,limitcount+fromlimit,limitcount+fromlimit)
    else:
        cl.SetLimits (0,limitcount,limitcount)
    if (pdt_type!="" and pdt_type!=None):
        cl.SetFilter('pdt_kind',[int(str(pdt_type))])
    if (havepic):
        cl.SetFilterRange('havepic',1,100)
    if (kname=='' or kname==None):
        res = cl.Query ('','offersearch_new_vip')
    else:
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            listall_offerlist=[]
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
                parea=getproducts_area(company_id)
                
                
                pdt_date=timestamp_datetime2(attrs['refresh_time'])
                short_time=pdt_date[5:]
                
                products_detail=getproducts_detail(pid)
                
                productspic=getpic_address(pid)
                if productspic:
                    pdt_images=productspic
                else:
                    pdt_images=""
                if (pdt_images == '' or pdt_images == '0'):
                    pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                else:
                    pdt_images='http://img3.zz91.com/100x100/'+pdt_images+''
                pic_address=pdt_images
                #pdt_date=pdt_date.strftime( '%-Y-%-m-%-d-%-H-%-M')
#                sql="select refresh_time from products where id="+str(pid)+""
#                cursor.execute(sql)
#                productlist = cursor.fetchone()
#                if productlist:
#                    pdt_date=productlist[0].strftime( '%-Y-%-m-%-d')
                """
                pfromdate=date.today()
                pfromdate_int=int(time.mktime(pfromdate.timetuple()))
                pdt_date=pfromdate_int-pdt_date
                
                pdtnum=date.today()-timedelta(seconds=3)
                
                pdt_date=(datetime.datetime.now()-datetime.timedelta(seconds=20)).strftime( '%-Y-%-m-%-d')
                """
                title=subString(attrs['ptitle'],40)
                
#                title=getlightkeywords(cl,[title],kname,"offersearch_new")
                
                list={'id':pid,'title':title,'gmt_time':pdt_date,'short_time':short_time,'fulltitle':attrs['ptitle'],'pic_address':pic_address,'products_detail':products_detail,'arg':arg,'parea':parea}
                listall_offerlist.append(list)
            return listall_offerlist

def getpricelist_daohang(kname="",assist_type_id="",limitcount="",searchname="",titlelen="",hangqing=""):
    #------最新报价信息
    if (titlelen==""):
        titlelen=35
    price=SPHINXCONFIG['name']['price']['name']
    serverid=SPHINXCONFIG['name']['price']['serverid']
    port=SPHINXCONFIG['name']['price']['port']
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_EXTENDED )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    cl.SetLimits (0,limitcount,limitcount)
    if(assist_type_id!=None and assist_type_id!=""):
        if (hangqing=="1"):
            cl.SetFilter('type_id',[217,216,220])
        else:
            cl.SetFilter('assist_type_id',[assist_type_id])
    if (kname==None):
        res = cl.Query ('',price)
    else:
        res = cl.Query ('@(title,tags) '+kname,price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_baojia=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=subString(attrs['ptitle'],titlelen)
#                title=getlightkeywords(cl,[title],kname,"price")
                gmt_time=attrs['gmt_time']
                #td_time=gmt_time.strftime('%Y-%m-%d')
                list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle']}
                listall_baojia.append(list1)
            listcount_baojia=res['total_found']
            return listall_baojia
def getbbslist_daohang(kname,limitcount):
    kname_hex=''
    if kname:
        kname_hex=getjiami(kname)
    listall=cache.get("daohang_bbslist_daohang"+str(kname_hex)+str(limitcount))
    if not listall:
        #最新互助信息
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_EXTENDED )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight desc,post_time desc" )
        cl.SetLimits (0,limitcount,limitcount)
        res = cl.Query ('@(title,tags) '+kname,'huzhu')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    gmt_time=attrs['ppost_time']
                    list1={'title':title,'id':id,'gmt_time':gmt_time}
                    listall.append(list1)
                cache.set("daohang_bbslist_daohang"+str(kname_hex)+str(limitcount),listall,60*20)
    return listall
def getseolist():
    listall=cache.get("daohang_seolist11")
    if not listall:
        strseo="回收丝锥|http://wzjs.zz91.com/,"
        strseo=strseo+"回收废钨钢|http://feiwugang.zz91.com/,"
        strseo=strseo+"回收高速钢|http://mojugang.zz91.com/,"
        strseo=strseo+"回收废钛|http://feitai.zz91.com/,"
        strseo=strseo+"废电路板|http://lantianxianluban.zz91.net/,"
        strseo=strseo+"增强尼龙|http://wx-hengrun.zz91.com/,"
        strseo=strseo+"供应玻璃纤维|http://laoyc.zz91.com/,"
        strseo=strseo+"数控刀片回收|http://zygjs.zz91.com/,"
        strseo=strseo+"三边封袋|http://zhangxf.zz91.com/,"
        strseo=strseo+"四氧化锇|http://cj.zz91.com/,"
        strseo=strseo+"碎牛皮|http://kaiyuanpige.zz91.com/,"
        strseo=strseo+"爆竹生产厂家|http://lhbzc.zz91.com/,"
        strseo=strseo+"白色开花料|http://kaihualiao.zz91.com/"
        seolist=strseo.split(",")
        listall=[]
        for a in seolist:
            alist=a.split("|")
            label=alist[0]
            url=alist[1]
            list={'label':label,'url':url}
            listall.append(list)
        cache.set("daohang_seolist11",listall,3600*24)
    return listall
#微门户关键词
def getcplist(keywords,limitcount):
    kname_hex=''
    if keywords:
        kname_hex=getjiami(keywords)
    listall=cache.get("daohang_cplist"+str(kname_hex)+str(limitcount))
    if not listall:
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        #cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
        cl.SetLimits (0,limitcount,limitcount)
        res = cl.Query ('@(label) '+keywords,'daohangkeywords')
        listall=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    label=attrs['plabel']
                    pingyin=attrs['ppinyin']
                    list={'label':label,'pingyin':pingyin}
                    listall.append(list)
        """
        sql="select label,pingyin from daohang where type=1 and sid=3738 limit 0,200"
        cursor.execute(sql)
        cplist=cursor.fetchall()
        listall=[]
        if cplist:
            for list in cplist:
                list={'label':list[0],'pingyin':list[1]}
                listall.append(list)
        """
        if listall:
            cache.set("daohang_cplist"+str(kname_hex)+str(limitcount),listall,60*20)
    return listall
def getHour():
    return str(datetime.datetime.now())[11:13] 
def getshowadflag():
    thour=getHour()
    if (int(thour)>=18 or int(thour)<7):
        showad=1
    else:
        showad=None
    return showad
##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    if htmlstr:
        s=re_cdata.sub('',htmlstr)#去掉CDATA
        s=re_script.sub('',s) #去掉SCRIPT
        s=re_style.sub('',s)#去掉style
        s=re_br.sub('\n',s)#将br转换为换行
        s=re_h.sub('',s) #去掉HTML 标签
        s=re_comment.sub('',s)#去掉HTML注释
        #去掉多余的空行
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=replaceCharEntity(s)#替换实体
        s=s.replace(" ","")
        return s
    else:
        return htmlstr

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
   
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr
#加密
def getjiami(strword):
    return strword.encode('utf8','ignore').encode("hex")
def getjiemi(strword):
    return strword.decode("hex").decode('utf8','ignore')
#获得明感字符
def getmingganword(s):
    sql="select id,updateflag,content from data_feifacontent where id=1"
    result=dbc.fetchonedb(sql)
    if not result:
        r=requests.get("http://pyapp.zz91.com/feifa.html")
        content=r.text
        sql="insert into data_feifacontent(id,content,updateflag) values(%s,%s,%s)"
        dbc.updatetodb(sql,[1,content,0])
    else:
        updateflag=result[1]
        if str(updateflag)=="1":
            r=requests.get("http://pyapp.zz91.com/feifa.html?a=0")
            content=r.text
            sql="update data_feifacontent set content=%s where id=1"
            dbc.updatetodb(sql,[content])
        else:
            content=result[2]
    lines=eval(content)
    list=[]
    if lines:
        for line in lines:
            line=line['k']
            line=line.strip('\n').strip()
            if line in s:
                return line
                break
            list.append(line)
    if s in list:
        return s
    if "激情" in s:
        return 2
    if "乱伦" in s:
        return 2
    
    return None
#--判断手机端还是pc
def mobileuseragent(agent):
    data=["Nokia",#诺基亚，有山寨机也写这个的，总还算是手机，Mozilla/5.0 (Nokia5800 XpressMusic)UC AppleWebkit(like Gecko) Safari/530  
    "SAMSUNG",#三星手机 SAMSUNG-GT-B7722/1.0+SHP/VPP/R5+Dolfin/1.5+Nextreaming+SMM-MMS/1.2.0+profile/MIDP-2.1+configuration/CLDC-1.1  
    "MIDP-2",#j2me2.0，Mozilla/5.0 (SymbianOS/9.3; U; Series60/3.2 NokiaE75-1 /110.48.125 Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML like Gecko) Safari/413  
    "CLDC1.1",#M600/MIDP2.0/CLDC1.1/Screen-240X320  
    "SymbianOS",#塞班系统的，  
    "MAUI",#MTK山寨机默认ua  
    "UNTRUSTED/1.0",#疑似山寨机的ua，基本可以确定还是手机  
    "Windows CE",#Windows CE，Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)  
    "iPhone",#iPhone是否也转wap？不管它，先区分出来再说。Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; zh-cn) AppleWebKit/532.9 (KHTML like Gecko) Mobile/8B117  
    "iPad",#iPad的ua，Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; zh-cn) AppleWebKit/531.21.10 (KHTML like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10  
    "Android",#Android是否也转wap？Mozilla/5.0 (Linux; U; Android 2.1-update1; zh-cn; XT800 Build/TITA_M2_16.22.7) AppleWebKit/530.17 (KHTML like Gecko) Version/4.0 Mobile Safari/530.17  
    "BlackBerry",#BlackBerry8310/2.7.0.106-4.5.0.182  
    "UCWEB",#ucweb是否只给wap页面？ Nokia5800 XpressMusic/UCWEB7.5.0.66/50/999  
    "ucweb",#小写的ucweb貌似是uc的代理服务器Mozilla/6.0 (compatible; MSIE 6.0;) Opera ucweb-squid  
    "BREW",#很奇怪的ua，例如：REW-Applet/0x20068888 (BREW/3.1.5.20; DeviceId: 40105; Lang: zhcn) ucweb-squid  
    "J2ME",#很奇怪的ua，只有J2ME四个字母  
    "YULONG",#宇龙手机，YULONG-CoolpadN68/10.14 IPANEL/2.0 CTC/1.0  
    "YuLong",#还是宇龙  
    "COOLPAD",#宇龙酷派YL-COOLPADS100/08.10.S100 POLARIS/2.9 CTC/1.0  
    "TIANYU",#天语手机TIANYU-KTOUCH/V209/MIDP2.0/CLDC1.1/Screen-240X320  
    "TY-",#天语，TY-F6229/701116_6215_V0230 JUPITOR/2.2 CTC/1.0  
    "K-Touch",#还是天语K-Touch_N2200_CMCC/TBG110022_1223_V0801 MTK/6223 Release/30.07.2008 Browser/WAP2.0  
    "Haier",#海尔手机，Haier-HG-M217_CMCC/3.0 Release/12.1.2007 Browser/WAP2.0  
    "DOPOD",#多普达手机  
    "Lenovo",# 联想手机，Lenovo-P650WG/S100 LMP/LML Release/2010.02.22 Profile/MIDP2.0 Configuration/CLDC1.1  
    "LENOVO",# 联想手机，比如：LENOVO-P780/176A  
    "HUAQIN",#华勤手机  
    "AIGO-",#爱国者居然也出过手机，AIGO-800C/2.04 TMSS-BROWSER/1.0.0 CTC/1.0  
    "CTC/1.0",#含义不明  
    "CTC/2.0",#含义不明  
    "CMCC",#移动定制手机，K-Touch_N2200_CMCC/TBG110022_1223_V0801 MTK/6223 Release/30.07.2008 Browser/WAP2.0  
    "DAXIAN",#大显手机DAXIAN X180 UP.Browser/6.2.3.2(GUI) MMP/2.0  
    "MOT-",#摩托罗拉，MOT-MOTOROKRE6/1.0 LinuxOS/2.4.20 Release/8.4.2006 Browser/Opera8.00 Profile/MIDP2.0 Configuration/CLDC1.1 Software/R533_G_11.10.54R  
    "SonyEricsson",# 索爱手机，SonyEricssonP990i/R100 Mozilla/4.0 (compatible; MSIE 6.0; Symbian OS; 405) Opera 8.65 [zh-CN]  
    "GIONEE",#金立手机  
    "HTC",#HTC手机  
    "ZTE",#中兴手机，ZTE-A211/P109A2V1.0.0/WAP2.0 Profile  
    "HUAWEI",#华为手机，  
    "webOS",#palm手机，Mozilla/5.0 (webOS/1.4.5; U; zh-CN) AppleWebKit/532.2 (KHTML like Gecko) Version/1.0 Safari/532.2 Pre/1.0  
    "GoBrowser",#3g GoBrowser.User-Agent=Nokia5230/GoBrowser/2.0.290 Safari  
    "IEMobile",#Windows CE手机自带浏览器，  
    "WAP2.0"]#支持wap 2.0的
    #agent=request.META['HTTP_USER_AGENT']
    for list in data:
        if list in agent:
            return 1
