#-*- coding:utf-8 -*-
from datetime import timedelta,date
class ztrade:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #----生意管家 供求管理
    def getmyproductslist(self,frompageCount="",limitNum="",company_id="",checkStatus=""):
        if not checkStatus:
            checkStatus=1
        sql1="select count(0) from products where company_id=%s and check_status=%s and is_del=0"
        alist=self.dbc.fetchonedb(sql1,[company_id,checkStatus])
        if alist:
            listcount=alist[0]
        sql="select id,title,real_time,refresh_time from products where company_id=%s and check_status=%s and is_del=0 order by refresh_time desc limit "+str(frompageCount)+","+str(frompageCount+limitNum)+""
        alist=self.dbc.fetchalldb(sql,[company_id,checkStatus])
        listall=[]
        num=0
        for list in alist:
            num+=1
            rlist={'proid':list[0],'protitle':list[1],'gmt_created':formattime(list[3]),'real_time':formattime(list[2],1),'refresh_time':formattime(list[3],0),'num':num}
            listall.append(rlist)
        return {'list':listall,'count':listcount}
    #公司供求信息 翻页
    def getcompanyproductslist(self,frompageCount,limitNum,kname='',company_id='',pdt_type=''):
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], spconfig['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if company_id:
            cl.SetFilter('company_id',[int(company_id)])
        if pdt_type:
            cl.SetFilter('pdt_kind',[int(pdt_type)])
        cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
        cl.SetLimits (frompageCount,limitNum,20000)
        if (kname):
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        else:
            res = cl.Query ('','offersearch_new,offersearch_new_vip')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                for match in tagslist:
                    id=match['id']
                    list=self.getcompinfo(id,kname)
                    listall.append(list)
                listcount=res['total_found']
        return {'list':listall,'count':listcount}
    def getcompinfo(self,pdtid,keywords,company_id=''):
#        isbuycontact=None
#        if company_id:
#            isbuycontact=self.getbuycontact(company_id,pdtid)
        productsinfo=cache.get("productsinfo"+str(pdtid))
        productsinfo=None
        if (productsinfo==None):
            sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%%Y/%%m/%%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code where p.id=%s;"
            productlist = self.dbc.fetchonedb(sql,pdtid)
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
                    arrviptype['vippic']='http://m.zz91.com/images/recycle.gif'
                    arrviptype['vipname']='再生通'
                if (viptype == '100510021000'):
                    arrviptype['vippic']='http://m.zz91.com/images/pptSilver.gif'
                    arrviptype['vipname']='银牌品牌通'
                if (viptype == '100510021001'):
                    arrviptype['vippic']='http://m.zz91.com/images/pptGold.gif'
                    arrviptype['vipname']='金牌品牌通'
                if (viptype == '100510021002'):
                    arrviptype['vippic']='http://m.zz91.com/images/pptDiamond.gif'
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
                if (price_unit==None):
                    price_unit=''
                else:
                    if (allprice!=''):
                        allprice=allprice+price_unit
                #----
                sql1="select pic_address from products_pic where product_id=%s and check_status=1"
                productspic = self.dbc.fetchonedb(sql1,productlist[2])
                if productspic:
                    pdt_images=productspic[0]
                else:
                    pdt_images=""
                if (pdt_images == '' or pdt_images == '0'):
                    pdt_images='../cn/img/noimage.gif'
                else:
                    pdt_images='http://img3.zz91.com/135x135/'+pdt_images+''
                
                ldbtel=self.getldbphone(productlist[0])
                    
                list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
                ,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5]
                ,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype
                ,'pdt_images':pdt_images,'pdt_price':allprice
                ,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'ldbtel':ldbtel}
            else:
                list1=None
                
            #list1=getproid(pdtid)
            if (list1 == None):
                return None
            else:
                pdt_images=list1['pdt_images']
                if (pdt_images=='../cn/img/noimage.gif'):
                    list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
                pdt_detail=list1['pdt_detail']
                pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
                docs=[pdt_detail]
                list1['pdt_detail']=subString(pdt_detail,50)+'...'
                
                pdt_name=list1['pdt_name']
                docs=[pdt_name]
                list1['pdt_name']=pdt_name
            productsinfo=list1
            cache.set("productsinfo"+str(pdtid),list1,1)
#        productsinfo['isbuycontact']=isbuycontact
        return productsinfo
    #---获得来电宝电话
    def getldbphone(self,company_id):
        if company_id:
            sqlg="select front_tel,tel from phone where company_id=%s and expire_flag=0"
            phoneresult=self.dbc.fetchonedb(sqlg,[company_id])
            if phoneresult:
                tel=phoneresult[1]
                tel=tel.replace("-",",,,")
                return {'front_tel':phoneresult[0],'tel':tel}
            else:
                return None
        else:
            return None
    #----供求列表
    def getofferlist(self,kname="",pdt_type="",limitNum="",havepic="",frompageCount="",company_id=''):
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], spconfig['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
        if frompageCount:
            cl.SetLimits (frompageCount,limitNum,10000)
        else:
            cl.SetLimits (0,limitNum,limitNum)
        if company_id:
            cl.SetFilter('company_id',[company_id])
        if pdt_type:
            cl.SetFilter('pdt_kind',[int(str(pdt_type))])
        if havepic:
            cl.SetFilterRange('havepic',1,100)
        if kname:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        else:
            res = cl.Query ('','offersearch_new_vip')
        listcount=0
        listall_offerlist=[]
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                num=0
                for match in itemlist:
                    num+=1
                    pid=match['id']
                    attrs=match['attrs']
                    company_id=attrs['company_id']
                    parea=''
#                    parea=getproducts_area(company_id)
                    
                    pdt_date=int_to_str(attrs['refresh_time'])
                    short_time=pdt_date[5:]
                    
                    products_detail=''
#                    products_detail=getproducts_detail(pid)
                    pic_address=''
                    '''
                    productspic=getpic_address(pid)
                    if productspic:
                        pdt_images=productspic
                    else:
                        pdt_images=""
                    if (pdt_images == '' or pdt_images == '0'):
                        pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                    else:
                        pdt_images='http://img3.zz91.com/100x100/'+pdt_images+''
                    pic_address=pdt_images'''
                    title=subString(attrs['ptitle'],40)
#                    title=getlightkeywords(cl,[title],kname,"offersearch_new")
                    list={'id':pid,'title':title,'gmt_time':pdt_date,'short_time':short_time,'fulltitle':attrs['ptitle'],'pic_address':pic_address,'products_detail':products_detail,'parea':parea,'num':num}
                    listall_offerlist.append(list)
            listcount=res['total_found']
        return {'list':listall_offerlist,'count':listcount}
    def getreportcheck(self,company_id,forcompany_id):
        sql='select check_status from pay_report where company_id=%s and forcompany_id=%s order by id desc'
        result=self.dbc.fetchonedb(sql,[company_id,forcompany_id])
        if result:
            return result[0]
    def getreportischeck(self,forcompany_id):
        sql='select id from pay_report where forcompany_id=%s and check_status=1 order by id desc'
        result=self.dbc.fetchonedb(sql,[forcompany_id])
        if result:
            return result[0]
        #--获得公司id
    def getcompanyid(self,account):
        sql="select company_id from  company_account where account=%s"
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    def getpro_report(self,company_id,forcompany_id,product_id,content):
        gmt_date=datetime.date.today()
        gmt_created=datetime.datetime.now()
        argument=[company_id,forcompany_id,product_id,content,gmt_date,gmt_created]
        sql='insert into pay_report(company_id,forcompany_id,product_id,content,gmt_date,gmt_created) values(%s,%s,%s,%s,%s,%s)'
        self.dbc.updatetodb(sql,argument)
    #----判断是否为再生通
    def getiszstcompany(self,company_id):
        if company_id:
            sqll="select id from crm_company_service where company_id=%s and crm_service_code='1000' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
            zstresult=self.dbc.fetchonedb(sqll,[company_id])
            if zstresult:
                return 1
            else:
                return None
        else:
            return None
    #获得供求信息
    def getproductdetail(self,id):
        sql="select company_id,title,details,location,provide_status,total_quantity,price_unit,quantity_unit,quantity,source"
        sql=sql+",specification,origin,impurity,color,useful,appearance,manufacture,min_price,max_price,tags,refresh_time,expire_time,products_type_code,price"
        sql=sql+" from products where id=%s and (is_pause=0 and check_status=1 and is_del=0)"
        plist=self.dbc.fetchonedb(sql,str(id))
        if plist:
            company_id=plist[0]
            title=plist[1]
            if not title:
                title=""
            details=plist[2]
            details=filter_tags(details)
            location=plist[3]
            if (location):
                if (location.strip()==''):
                    location=None
            provide_status=plist[4]
            total_quantity=plist[5]
            
            quantity_unit=plist[7]
            quantity=plist[8]
            if plist[9]:
                source=plist[9].strip()
            else:
                source=""
            if source:
                if (source.strip()==''):
                    source=None
            specification=plist[10]
            origin=plist[11]
            impurity=plist[12]
            color=plist[13]
            useful=plist[14]
            appearance=plist[15]
            manufacture=plist[16]
            
            price_unit=plist[6]
            min_price=plist[17]
            max_price=plist[18]
            price=plist[23]
            if not price:
                price=''
                if (min_price!=None and min_price!='' and str(min_price)!='0.0'):
                    price+=str(min_price)+'-'
                if (max_price!=None and max_price!='' and str(max_price)!='0.0'):
                    price+=str(max_price)
            if price and price_unit:
                if '元' not in price:
                    price=price+str(price_unit)
            tags=plist[19]
            refresh_time=formattime(plist[20],3)
            
            datetoday=datetime.datetime.now()
            expire_time=plist[21]
            if (str(expire_time)=='9999-12-31 23:59:59'):
                expire_time="长期有效"
            elif (expire_time==None or expire_time==""):
                expire_time=None
            elif expire_time<datetoday:
                expire_time='<font color="red">信息已过期</font>'
            else:
                if (expire_time!="长期有效"):
                    expire_time=formattime(expire_time,0)
            products_type_code=plist[22]
            if products_type_code=='10331000':
                title='供应'+title
            elif products_type_code=='10331001':
                title='求购'+title
            sqlc="select name,business,regtime,address,introduction,membership_code from company where id=%s"
            clist=self.dbc.fetchonedb(sqlc,company_id)
            if clist:
                compname=clist[0]
                business=clist[1]
                regtime=clist[2]
                address=clist[3]
                introduction=clist[4]
                viptype=clist[5]
                arrviptype={'vippic':'','vipname':'','vipcheck':'','ldb':''}
                if (viptype == '10051000'):
                    arrviptype['vippic']=None
                    arrviptype['vipname']='普通会员'
                if (viptype == '10051001'):
                    arrviptype['vippic']='http://m.zz91.com/images/recycle.gif'
                    arrviptype['vipname']='再生通'
                if (viptype == '100510021000'):
                    arrviptype['vippic']='http://m.zz91.com/images/pptSilver.gif'
                    arrviptype['vipname']='银牌品牌通'
                if (viptype == '100510021001'):
                    arrviptype['vippic']='http://m.zz91.com/images/pptGold.gif'
                    arrviptype['vipname']='金牌品牌通'
                if (viptype == '100510021002'):
                    arrviptype['vippic']='http://m.zz91.com/images/pptDiamond.gif'
                    arrviptype['vipname']='钻石品牌通'
                if (viptype == '10051003'):
                    arrviptype['vippic']=''
                    arrviptype['vipname']='来电宝客户'
                if (viptype == '10051000'):
                    arrviptype['vipcheck']=None
                else:
                    arrviptype['vipcheck']=1
                #来电宝客户
                sqll="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code in(1007,1008,1009,1010) and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
                ldbresult=self.dbc.fetchonedb(sqll)
                if ldbresult:
                    sqlg="select front_tel,tel from phone where company_id="+str(company_id)+" and expire_flag=0"
                    phoneresult=self.dbc.fetchonedb(sqlg)
                    if phoneresult:
                        arrviptype['ldb']={'ldbphone':phoneresult[0],'ldbtel':phoneresult[1]}
                    else:
                        arrviptype['ldb']=None
                else:
                    arrviptype['ldb']=None
            sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
            sqlc=sqlc+",sex,position,qq "
            sqlc=sqlc+"from company_account where company_id=%s"
            alist=self.dbc.fetchonedb(sqlc,company_id)
            if alist:
                contact=alist[0]
                tel_country_code=alist[1]
                if (str(tel_country_code)=='None'):
                    tel_country_code=""
                tel_area_code=alist[2]
                if (str(tel_area_code)=='None'):
                    tel_area_code=""
                tel=alist[3]
                mobile=alist[4]
                mobilelist=[]
                mobile1=""
                if (mobile):
                    mobile=mobile.strip()
                    mobile1=mobile[0:11]
                    if len(mobile)>21:
                        mobilelist=re.findall('[\d]+',mobile)
                fax_country_code=alist[5]
                fax_area_code=alist[6]
                fax=alist[7]
                email=alist[8]
                sex=alist[9]
                position=alist[10]
                if (position==None):
                    position=""
                position=position.strip()
                qq=alist[11]
            sql1="select pic_address from products_pic where product_id=%s and check_status=1"
            productspic=self.dbc.fetchalldb(sql1,id)
            piclist=[]
            if productspic:
                for p in productspic:
                    pimages=p[0]
                    if (pimages == '' or pimages == '0' or pimages==None):
                        pdt_images='../cn/img/noimage.gif'
                        pdt_images_big='../cn/img/noimage.gif'
                    else:
                        pdt_images="http://img3.zz91.com/135x135/"+pimages+""
                        pdt_images_big="http://img3.zz91.com/300x300/"+pimages+""
                    picurl={'images':pdt_images,'images_big':pdt_images_big}
                    piclist.append(picurl)
            if price and '元' in price:
                price_unit=''
            if quantity and '吨' in quantity:
                quantity_unit=''
            list={'pdtid':id,'company_id':company_id,'title':title,'refresh_time':refresh_time,'expire_time':expire_time,'details':details,'location':location,'provide_status':provide_status,'total_quantity':total_quantity,'price':price,'price_unit':price_unit,'quantity_unit':quantity_unit,'quantity':quantity,'source':source,'specification':specification,'origin':origin,'impurity':impurity,'color':color,'useful':useful,'appearance':appearance,'manufacture':manufacture,'min_price':min_price,'max_price':max_price,'tags':tags,'compname':compname,'business':business,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'mobilelist':mobilelist,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'piclist':piclist,'viptype':arrviptype,'products_type_code':products_type_code}
            return list
    #----相关供求类别(你是不是还想找?)
    def getcategorylist(self,kname='',limitcount=''):
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], spconfig['port'] )
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
    #----报价列表
    def getprlist(self,frompageCount,limitNum,maxcount=100000,kname='',category_id='',assist_id='',categoryname='',arg=''):
        price=spconfig['name']['price']['name']
        serverid=spconfig['name']['price']['serverid']
        port=spconfig['name']['price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
        if category_id:
            cl.SetFilter('type_id',category_id)
        if assist_id:
            cl.SetFilter('assist_type_id',assist_id)
        if arg=='1':
            cl.SetGroupBy( 'type_id',SPH_GROUPBY_ATTR )
        elif arg=='2':
            cl.SetGroupBy( 'assist_type_id',SPH_GROUPBY_ATTR )
        cl.SetLimits (frompageCount,limitNum,maxcount)
        listall_baojia=[]
        listcount_baojia=0
        js=0
        if kname:
            kname=kname.replace("|"," ")
            querysty='@(title,tags) '+kname
            res = cl.Query (querysty,price)
        else:
            res = cl.Query ('',price)
        if res:
#            return res
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    td_id=match['id']
                    url='/detail/'+str(td_id)+'.html'
                    mobileurl='/priceviews/?id='+str(td_id)
                    attrs=match['attrs']
                    type_id=attrs['type_id']
                    title=attrs['ptitle']
                    ptitle=re.sub('[\d]+月[\d]+日','',title)
                    ptitle=re.sub('价格','',ptitle)
                    ptitle=re.sub('地区','',ptitle)
                    area=''
                    if kname:
                        area=re.sub(kname.encode('utf-8'),'',ptitle)
                    assist_type_id=attrs['assist_type_id']
                    company_numb=0
                    gmt_time=attrs['gmt_time']
                    list1={'mobileurl':mobileurl,'td_title':title,'ptitle':ptitle,'area':area,'fulltitle':title,'td_id':td_id,'td_time':gmt_time,'url':url,'categoryid':type_id,'assist_type_id':assist_type_id}
                    js=js+1
                    if js%2==0:
                        evennumber=1
                    else:
                        evennumber=0
                    list1['evennumber']=evennumber
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
        return {'list':listall_baojia,'count':listcount_baojia}
    #------企业报价
    def getpricelist_company(self,kname='',frompageCount='',limitNum='',maxcount=100000):
        company_price=spconfig['name']['company_price']['name']
        serverid=spconfig['name']['company_price']['serverid']
        port=spconfig['name']['company_price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if kname:
            res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'',company_price)
        else:
            res = cl.Query ('',company_price)
        listall_baojia=[]
        listcount_baojia=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    td_id=match['id']
                    mobileurl='/compriceviews/?id='+str(td_id)
                    attrs=match['attrs']
                    fulltitle=attrs['ptitle']
                    company_id=attrs['company_id']
                    companyname=''
#                    companyname=self.getcompanynamecomid(company_id)
                    province=attrs['province']
                    city=attrs['city']
                    title=subString(fulltitle,60)
#                    title=getlightkeywords(cl,[title],kname,"company_price")
                    gmt_time=attrs['ppost_time']
                    price_unit=attrs['price_unit']
                    min_price=attrs['min_price']
                    max_price=attrs['max_price']
                    #if (price=="" or price=="none"):
                    price=min_price+"-"+max_price+price_unit
                    company_numb=''
#                    company_numb=self.getpricelist_company_count(title)
                    #td_time=gmt_time.strftime('%Y-%m-%d')
                    companyurl=''
                    domain_zz91=self.getdomain_zz91(company_id)
                    if domain_zz91:
                        companyurl="http://"+domain_zz91+".zz91.com"
                    else:
                        companyurl="http://company.zz91.com/compinfo"+str(company_id)+".htm"
                    list1={'mobileurl':mobileurl,'td_title':title,'province':province,'city':city,'company_numb':company_numb,'companyurl':companyurl,'companyname':companyname,'company_id':company_id,'fulltitle':fulltitle,'td_id':td_id,'td_time':gmt_time,'price':price,'url':'http://price.zz91.com/companyprice/priceDetails'+str(td_id)+'.htm'}
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
        return {'list':listall_baojia,'count':listcount_baojia}
    def getdomain_zz91(self,id):
        sql='select domain_zz91 from company where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    #置顶广告
    def keywordstopcompany(self,product_id):
        sql="select id from products_keywords_rank where product_id=%s and start_time<'"+str(date.today()+timedelta(days=1))+"' and end_time>'"+str(date.today())+"' and is_checked=1 and type in ('10431004','手机站关键字排名') and not exists(select id from products where id=products_keywords_rank.product_id and is_pause=1) order by start_time asc"
        results = self.dbc.fetchonedb(sql,[product_id])
        return results
    #----类别列表
    def getindexcategorylist(self,code,showflag):
        catelist=cache.get("cate1"+str(code))
        if (catelist==None):
            if (showflag==2):
                sql="select label,code from category_products where code like %s order by sort asc"
            else:
                sql="select label,code from category_products where code like %s"'"____"'" order by sort asc"
            catelist=self.dbc.fetchalldb(sql,[str(code)])
            listall_cate=[]
            numb=0
            for a in catelist:
                numb=numb+1
                if (showflag==1):
                    sql1="select label from category_products where code like '"+str(a[1])+"____' order by sort asc"
                    catelist1=self.dbc.fetchalldb(sql1)
                    listall_cate1=[]
                    for b in catelist1:
                        list1={'label':b[0]}
                        listall_cate1.append(list1)
                else:
                    listall_cate1=None
                list={'label':a[0],'code':a[1],'catelist':listall_cate1,'numb':numb}
                listall_cate.append(list)
            cache.set("cate1"+str(code),listall_cate,60*60000)
        else:
            listall_cate=catelist
        
        return listall_cate