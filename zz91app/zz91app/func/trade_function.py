#-*- coding:utf-8 -*-

class zztrade:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getviptype(self,company_id):
        sql='select membership_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getreportcheck(self,company_id,forcompany_id,product_id):
        sql='select check_status from pay_report where company_id=%s and forcompany_id=%s and product_id=%s order by id desc'
        result=self.dbc.fetchonedb(sql,[company_id,forcompany_id,product_id])
        if result:
            return result[0]
    def getreportischeck(self,forcompany_id,product_id):
        sql='select id from pay_report where forcompany_id=%s and product_id=%s and check_status=1 order by id desc'
        result=self.dbc.fetchonedb(sql,[forcompany_id,product_id])
        if result:
            return result[0]
        #--获得公司id
    def getcompanyid(self,account):
        sql="select company_id from  company_account where account=%s"
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    def getcompanynamecomid(self,company_id):
        sql="select name from company where id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getpro_report(self,company_id,forcompany_id,product_id,content):
        gmt_date=datetime.date.today()
        gmt_created=datetime.datetime.now()
        argument=[company_id,forcompany_id,product_id,content,gmt_date,gmt_created]
        if (str(company_id)!="0" and str(forcompany_id)!="0"):
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
    def getproductdetail(self,id,isseeflag=""):
        productsinfo=cache.get("app_productdetail"+str(id))
        if productsinfo:
            return productsinfo
        
        sql="select company_id,title,details,location,provide_status,total_quantity,price_unit,quantity_unit,quantity,source"
        sql=sql+",specification,origin,impurity,color,useful,appearance,manufacture,min_price,max_price,tags,refresh_time,expire_time,products_type_code,category_products_main_code"
        sql=sql+" from products where id=%s and is_del=0"
        #is_pause=0 and check_status=1 and 
        plist=self.dbc.fetchonedb(sql,str(id))
        if plist:
            company_id=plist[0]
            title=plist[1]
            details=plist[2]
            if details:
                details=remove_script(details)
                details=remove_content_a(details)
                details=remove_content_value(details)
                details=details.replace("http://img1.zz91.com","http://img3.zz91.com/400x1500")
            details_text=filter_tags(details)
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
            if not min_price:
                min_price=0
            max_price=plist[18]
            if not max_price:
                max_price=0
            price=""
            if (min_price!=None and min_price!='' and str(min_price)!='0.0'):
                price=price+str(min_price)+'-'
            if (max_price!=None and max_price!='' and str(max_price)!='0.0'):
                price=price+str(max_price)
            if (price!="" and price_unit!=None and price_unit!=''):
                price=price+str(price_unit)
            if (price==''):
                price=None
                
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
            category_products_main_code=plist[23]
            productscategory1=self.getcategoryname(category_products_main_code[0:8])
            productscategory2=self.getcategoryname(category_products_main_code[0:12])
            procatetext=""
            if productscategory1:
                procatetext=productscategory1
            if productscategory2:
                procatetext=productscategory2
            productscategory=productscategory1+"->"+productscategory2
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
                sqll="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
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
                    if str(sex)=="0":
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="先生"
                    else:
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="女士"
                    position=alist[10]
                    if (position==None):
                        position=""
                    position=position.strip()
                    if arrviptype['vipcheck']==1 and arrviptype['ldb']==None:
                        a="高会号码不过滤"
                    else:
                        if introduction:
                            if mobile:
                                introduction=introduction.replace(mobile,"")
                            if mobile1:
                                introduction=introduction.replace(mobile1,"")
                    qq=alist[11]
                    if arrviptype['vipcheck']==1 and arrviptype['ldb']==None:
                        a="高会号码不过滤"
                    else:
                        if details:
                            if mobile:
                                details=details.replace(mobile,"")
                            if mobile1:
                                details=details.replace(mobile1,"")
                sql1="select pic_address from products_pic where product_id=%s"
                #and check_status=1
                productspic=self.dbc.fetchalldb(sql1,id)
                piclist=[]
                if productspic:
                    picnum=1
                    for p in productspic:
                        pimages=p[0]
                        if (pimages == '' or pimages == '0' or pimages==None):
                            pdt_images='../cn/img/noimage.gif'
                            pdt_images_big='../cn/img/noimage.gif'
                        else:
                            vadiolist=["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]
                            vadioflag=0
                            for pp in vadiolist:
                                if ("."+pp in pimages):
                                    vadioflag=1
                            if (vadioflag==1):
                                pdt_images="../../image/video.png"
                                pdt_images_big="http://img1.zz91.com/"+pimages+""
                            else:
                                pdt_images="http://img3.zz91.com/135x135/"+pimages+""
                                pdt_images_big="http://img3.zz91.com/300x300/"+pimages+""
                        
                        if (picnum==1):
                            firstpic=pdt_images_big
                        else:
                            firstpic=None
                        if (picnum==len(productspic)):
                            lastpic=pdt_images_big
                        else:
                            lastpic=None
                        
                        picurl={'images':pdt_images,'images_big':pdt_images_big,'picnum':picnum,'firstpic':firstpic,'lastpic':lastpic}
                        picnum+=1
                        piclist.append(picurl)
                if not piclist:
                    piclist=[{'images':'','images_big':'','picnum':'','firstpic':'','lastpic':''}]
                    #piclist=[]
                lenpiclist=len(piclist)
                if price and '元' in price:
                    price_unit=''
                if quantity and '吨' in quantity:
                    quantity_unit=''
                #供求更多属性
                sqlm="select property,content from product_addproperties where pid=%s and is_del='0'"
                resultmore=dbc.fetchalldb(sqlm,[id])
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
                        
                listmore=self.getmoreproperty(listmore,'货源地',source)
                listmore=self.getmoreproperty(listmore,'来源产品',origin)
                listmore=self.getmoreproperty(listmore,'产品规格',specification)
                listmore=self.getmoreproperty(listmore,'杂质含量',impurity)
                listmore=self.getmoreproperty(listmore,'颜色',color)
                listmore=self.getmoreproperty(listmore,'用途',useful)
                listmore=self.getmoreproperty(listmore,'外观',appearance)
                listmore=self.getmoreproperty(listmore,'加工说明',manufacture)
                propertymore="<table border=1 width=100% style='border-color: #536376;'>"
                for ll in listmore:
                    if ll['content']:
                        propertymore+="<tr><td style='width:30%;padding:5px;border:1px solid #ddd;'>"+str(ll['property'])+":</td><td style='color:#006600;padding:5px;border:1px solid #ddd;'>"+str(ll['content'])+"<font color=#fff>。</font></td></tr>"
                propertymore+="</table>"
                list={'pdtid':id,'company_id':company_id,'title':title,'productscategory':productscategory,'procatetext':procatetext,'refresh_time':str(refresh_time),'expire_time':str(expire_time),'details':propertymore+details,'location':location,'provide_status':provide_status,'total_quantity':total_quantity,'price':price,'price_unit':price_unit,'quantity_unit':quantity_unit,'quantity':quantity,'source':source,'specification':specification,'origin':origin,'impurity':impurity,'color':color,'useful':useful,'appearance':appearance,'manufacture':manufacture,'min_price':min_price,'max_price':max_price,'tags':tags,'compname':compname,'business':business,'regtime':str(regtime),'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'mobilelist':mobilelist,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'piclist':piclist,'viptype':arrviptype,'products_type_code':products_type_code,'lenpiclist':lenpiclist}
                cache.set("app_productdetail"+str(id),list,60*60)
                return list
            else:
                return None
    def getmoreproperty(self,listmore,text,value):
        if (value!="" and value!=None):
            value=value.strip()
            if value:
                if value[0:4]=="1011":
                    value=self.getcategorylabel_fromcode(value)
                listmore.append({'property':text,'content':value})
        return listmore
    def getcategorylabel_fromcode(self,code):
        sql="select label from category where code=%s"
        results = self.dbc.fetchonedb(sql,[code])
        if results:
            return results[0]
    def getcompinfo(self,pdtid,keywords,company_id=''):
        isbuycontact=None
        if company_id:
            isbuycontact=self.getbuycontact(company_id,pdtid)
        productsinfo=cache.get("app_productsinfo"+str(pdtid))
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
                list1['pdt_detail']=subString(pdt_detail,90)+'...'
                
                pdt_name=list1['pdt_name']
                docs=[pdt_name]
                list1['pdt_name']=pdt_name
            productsinfo=list1
            
        productsinfo['isbuycontact']=isbuycontact
        cache.set("app_productsinfo"+str(pdtid),productsinfo,60*60)
        return productsinfo
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
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], spconfig['port'] )
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
            res = cl.Query (querysty,'price')
        else:
            res = cl.Query ('','price')
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
    def getpricelist_company(self,kname='',frompageCount='',limitNum='',maxcount=100000,company_id=''):
        cl = SphinxClient()
        price=spconfig['name']['company_price']['name']
        serverid=spconfig['name']['company_price']['serverid']
        port=spconfig['name']['company_price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
        cl.SetLimits (frompageCount,limitNum,maxcount)
        cl.SetFilter('minPrice',[0],exclude=1)
        cl.SetFilter('is_checked',[1])
        if not company_id:
            a=1
            #cl.SetGroupBy( 'company_id',SPH_GROUPBY_ATTR )
        else:
            cl.SetFilter('company_id',[company_id])
        if kname:
            res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'','company_price')
        else:
            res = cl.Query ('','company_price')
        listall_baojia=[]
        listcount_baojia=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    td_id=match['id']
                    attrs=match['attrs']
                    fulltitle=attrs['ptitle']
                    company_id=attrs['company_id']
                    companyname=self.getcompanynamecomid(company_id)
                    province=attrs['province']
                    city=attrs['city']
                    title=fulltitle
#                    title=getlightkeywords(cl,[title],kname,"company_price")
                    gmt_time=attrs['ppost_time']
                    price_unit=attrs['price_unit']
                    min_price=attrs['min_price']
                    max_price=attrs['max_price']
                    price=min_price
                    if max_price:
                        price+="-"+max_price
                    if price_unit:
                        price+=price_unit
                    #details=self.getcompany_pricedetail(td_id)
                    #if details:
                    #    details=subString(details,150)
                    list1={'id':td_id,'td_title':title,'province':province,'city':city,'companyname':companyname,'company_id':company_id,'td_time':gmt_time,'price':price}
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
        return {'list':listall_baojia,'count':listcount_baojia}
    #企业报价，详情
    def getcompany_pricedetail(self,id):
        sql="select details from company_price where id=%s"
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return filter_tags(result[0])
    def getdomain_zz91(self,id):
        sql='select domain_zz91 from company where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    #----类别列表
    def getindexcategorylist(self,code,showflag):
        catelist=cache.get("app_cate1"+str(code))
        if (catelist==None):
            if (showflag==2):
                sql="select label,code from category_products where code like %s order by sort asc"
            else:
                sql="select label,code from category_products where code like %s"'"____"'" order by sort asc"
            listall_cate=[]
            catelist=self.dbc.fetchalldb(sql,[str(code)])
            numb=0
            for a in catelist:
                numb=numb+1
                if (showflag==1):
                    sql1="select label,code from category_products where code like '"+str(a[1])+"____' order by sort asc"
                    listall_cate1=[]
                    catelist1=self.dbc.fetchalldb(sql1)
                    for b in catelist1:
                        list1={'label':b[0],'label_hex':getjiami(b[0]),'code':b[1]}
                        listall_cate1.append(list1)
                else:
                    listall_cate1=None
                list={'label':a[0],'label_hex':getjiami(a[0]),'code':a[1],'catelist':listall_cate1,'numb':numb}
                listall_cate.append(list)
            cache.set("app_cate1"+str(code),listall_cate,60*60000)
        else:
            listall_cate=catelist
        return listall_cate
    def getcategoryname(self,code):
        #获得缓存
        zz91app_getcategoryname=cache.get("zz91app_getcategoryname"+str(code))
        if zz91app_getcategoryname:
            return zz91app_getcategoryname
        sql="select label from category_products where code=%s"
        catevalue=self.dbc.fetchonedb(sql,[code])
        if catevalue:
            #设置缓存
            cache.set("zz91app_getcategoryname"+str(code),catevalue[0],60*10)
            return catevalue[0]
    def getbuycontact(self,company_id,pdtid):
        sql2='select company_id from products where id=%s'
        result=self.dbc.fetchonedb(sql2,[pdtid])
        if result:
            forcompany_id=result[0]
            sql='select id from pay_mobileWallet where company_id=%s and forcompany_id=%s'
            buycontact=self.dbc.fetchonedb(sql,[company_id,forcompany_id])
            if buycontact:
                return 1
    #---获得来电宝电话
    def getldbphone(self,company_id):
        if company_id:
            sqlg="select front_tel,tel from phone where company_id=%s and expire_flag=0 and exists(select company_id from crm_company_service where crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and company_id=phone.company_id)"
            phoneresult=self.dbc.fetchonedb(sqlg,[company_id])
            if phoneresult:
                tel=phoneresult[1]
                tel=tel.replace("-",",,,")
                return {'front_tel':phoneresult[0],'tel':tel}
            else:
                return None
        else:
            return None
        
    #获得客户pv
    def getcompanypv(self,company_id):
        #公司pv
        pv=0
        sql="select sum(0) from analysis_products_pv where company_id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            pv=result[0]
            if not pv:
                pv=0
        vippv=0
        sql="select sum(0) from analysis_vip_pv where cid=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            vippv=result[0]
            if not vippv:
                vippv=0
        ppcpv=0
        sql="select sum(0) from analysis_ppc_log where cid=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            ppcpv=result[0]
            if not ppcpv:
                ppcpv=0
        
        pv=vippv+pv+ppcpv
        
        #询盘量
        qcount=0
        sql="select qcount from inquiry_count where company_id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            qcount=result[0]
        phonecount=0
        sql="select count(0) from phone_telclick_log where forcompany_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            phonecount=result[0]
            if not phonecount:
                phonecount=0
        return {'pv':pv,'qcount':qcount,'phonecount':phonecount}
    #公司供求信息 翻页
    def getcompanyproductslist(self,kname="",frompageCount="",limitNum="",company_id="",pdt_type="",status="",realdata=""):
        if realdata:
            listcount=1
            sql="select count(0) from products where company_id=%s and check_status in (0,1) and is_del=0 "
            result=self.dbc.fetchonedb(sql,[company_id])
            if result:
                listcount=result[0]
            sql="select id from products where company_id=%s and check_status in (0,1) and is_del=0 limit %s,%s"
            result=self.dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
            listall=[]
            
            if result:
                for list in result:
                    id=list[0]
                    list=self.getcompinfo(id,'',company_id)
                    type='10431004'
                    sql2='select id from products_keywords_rank where product_id=%s and type=%s and is_checked=0 and DATEDIFF(CURDATE(),`end_time`)<=0'
                    result2=self.dbc.fetchonedb(sql2,[id,type])
                    if result2:
                        list['havetop']=1
                    else:
                        list['havetop']=0
                    listall.append(list)
                
            return {'list':listall,'count':listcount}
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if (company_id) and company_id!="null":
            cl.SetFilter('company_id',[int(company_id)])
        if (pdt_type !='' and pdt_type!=None):
            cl.SetFilter('pdt_kind',[int(pdt_type)])
        if status:
            cl.SetFilter('check_status',[0,1])
        else:
            cl.SetFilter('check_status',[1])
        cl.SetFilter('is_del',[0])
        cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
        cl.SetLimits (frompageCount,limitNum,20000)
        if (kname):
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        else:
            res = cl.Query ('','offersearch_new,offersearch_new_vip')
        listcount=0
        listcount=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                for match in tagslist:
                    id=match['id']
                    
                    list=self.getcompinfo(id,kname,company_id)
                    
                    type='10431004'
                    sql2='select id from products_keywords_rank where product_id=%s and type=%s and is_checked=0 and DATEDIFF(CURDATE(),`end_time`)<=0'
                    result2=self.dbc.fetchonedb(sql2,[id,type])
                    if result2:
                        list['havetop']=1
                    else:
                        list['havetop']=0
                    listall.append(list)
                listcount=res['total_found']
        return {'list':listall,'count':listcount}