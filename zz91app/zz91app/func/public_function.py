#-*- coding:utf-8 -*-
import top.api
def tradeorderby(listall):
    listall = sorted(listall, key=itemgetter(1))
    changeflag="0"
    listallvip1=[]
    listallvip2=[]
    m=0
    for i in listall:
        m+=1
        if (changeflag==str(i[1])):
            list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
            listallvip2.append(list1)
            if (len(listall)==m):
                listallvip1+=listallvip2
        else:
            listallvip2=sorted(listallvip2, key=itemgetter(4,2,5,3),reverse=True)
            listallvip1+=listallvip2
            listallvip2=[]
            list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
            listallvip2.append(list1)
            if (len(listall)==m):
                listallvip1+=listallvip2
        changeflag=str(i[1])
    return listallvip1

def getnowurl(request):
    host=request.path_info
    qstring=request.META.get('QUERY_STRING','/')
    qstring=qstring.replace("&","^and^")
    return host+"?"+qstring
def formattime(value,flag):
    if value:
        if (flag==1):
            return value.strftime( '%-Y-%-m-%-d')
        if (flag==2):
            return value.strftime( '%-m-%-d %-H:%-M')
        if (flag==3):
            return value.strftime( '%Y-%-m-%d &nbsp;%-H:%M')
        else:
            return value.strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
    else:
        return ''
#
def remove_content_value(html):#移除a链接
    html=re.sub('<A.*?>','',html)
    html=re.sub('</A>','',html)
    html=re.sub('<a.*?>','',html)
    html=re.sub('</a>','',html)
    html=re.sub('</div>','',html)
    #html=re.sub('STYLE=".*?"','',html)
    html=re.sub('ALIGN=".*?"','',html)
    
    return html
#图片替换
def replacepic(htmlstr):
    nowhtml=htmlstr
    for n in range(1,20):
        head = nowhtml.find('<img')
        tail=len(nowhtml)
        if head != -1:
            cut = nowhtml[head:tail]
            src = cut.find('http')
            cut2 = cut[src:tail]
            quo = cut2.find('"')
            url = cut2[0:quo]
            
            cc = nowhtml[head-4:tail]
            dd = cc.find('>')
            ee = cc[0:dd+1]
            
            if (url.find("13327300632836987")!=-1):
                htmlstr=htmlstr.replace(ee,"")
            nowhtml=cut2
            if (url!=''):
                #url=url.replace("http://img1.zz91.com/","")
                #url=url.replace("http://","")
                newpicurl="http://img3.zz91.com/300x15000/"+url+""
                newpicurl=newpicurl.replace("http://img1.zz91.com/","")
                #newpicurl=url
                #htmlstr=htmlstr
                htmlstr=htmlstr.replace(url,newpicurl)
                #htmlstr=htmlstr.replace(ee,"")
                #htmlstr=htmlstr.replace("http://img1.zz91.com/bbsPost/2012/3/26/13327300632836987.jpg","")
            #htmlstr=htmlstr.replace("style='margin: 0px; padding: 0px; width: 482px; height: 115px;'","")
    return htmlstr
#图片替换
def replacepic1(htmlstr):
    nowhtml=htmlstr
    reg = r'src="(.+?)"' 
    imgre = re.compile(reg)  
    imglist = imgre.findall(htmlstr)  
    x = 0  
    for imgurl in imglist: 
        if "http://" in imgurl:
            imgurl=imgurl
        else:
            imgurl="http://app.zz91.com"+imgurl
        newpicurl="http://pyapp.zz91.com/app/changepic.html?url="+imgurl+"&width=300&height=1500"
        htmlstr=htmlstr.replace(imgurl,newpicurl)
        x = x + 1
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    #re_a=re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>',re.I)#a
    re_style1=re.compile(r'style="(.+?)"')
    #re_h=re.compile('</?\w+[^>]*>')#HTML标签
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_style1.sub('',s)#去掉style
    #s=re_h.sub('',s) #去掉HTML 标签
    #s=re_a.sub('',s) #去掉a 标签
    #s=replaceCharEntity(s)#替换实体
    htmlstr=s
    """
    for n in range(1,20):
        head = nowhtml.find('<img')
        tail=len(nowhtml)
        if head != -1:
            cut = nowhtml[head:tail]
            src = cut.find('src="')
            
            
            cut2 = cut[src+5:tail]
            quo = cut2.find('"')
            
            url = cut2[0:quo]
            url=url.replace("http://","")
            
            
            
            cc = nowhtml[head-4:tail]
            dd = cc.find('>')
            ee = cc[0:dd+1]
            
            s=cc.find('style=')
            if s>0:
                s2=cc.find('"')
                s1=cc[s:s2]
                #htmlstr=htmlstr.replace(s1,"")
            #htmlstr=htmlstr.replace(ee,"")
            
            
            if (url.find("13327300632836987")!=-1):
                htmlstr=htmlstr.replace(ee,"")
            if (url!=''):
                
                #url=url.replace("http://img1.zz91.com/","")
                #url=url.replace("http://","")
                #htmlstr=htmlstr.replace(ee,"<img src='"+url+"'>")
                
                newpicurl="http://app.zz91.com"+url
                #newpicurl=newpicurl.replace("http://img1.zz91.com/","")
                #newpicurl=url
                #htmlstr=htmlstr
                
                htmlstr=htmlstr.replace(url,newpicurl)
                #htmlstr=htmlstr.replace(ee,"")
                #htmlstr=htmlstr.replace("http://img1.zz91.com/bbsPost/2012/3/26/13327300632836987.jpg","")
            #htmlstr=htmlstr.replace("style='margin: 0px; padding: 0px; width: 482px; height: 115px;'","")
    """
    return htmlstr
def get_img_url(html):#获得图片url
    #html=html.lower()
    if html:
        html=html.replace("data-original=","src=").replace("IMG",'img').replace("SRC",'src').replace("data-src","src")
        re_py3=r'<img.*?src="(.*?)".*?>'
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
        re_py3=r"<img.*?src='(.*?)'.*?>"
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
        re_py3=r'<img.*?src=(.*?) .*?>'
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
#关键字排名
def keywordsTop(keywords):
    #获得缓存
    #zz91app_keywordsTop=cache.get("zz91app_keywordsTop"+str(keywords))
    #if zz91app_keywordsTop:
        #return zz91app_keywordsTop
    if keywords:
        sql="select product_id from products_keywords_rank where name=%s and start_time<'"+str(date.today()+timedelta(days=1))+"' and end_time>'"+str(date.today())+"' and is_checked=1 and type in ('10431004','手机站关键字排名') and not exists(select id from products where id=products_keywords_rank.product_id and is_pause=1) order by start_time asc"
        results = dbc.fetchalldb(sql,keywords)
        #设置缓存
        #cache.set("zz91app_keywordsTop"+str(keywords),results,60*10)
        return results
    else:
        return None
def keywordstopcompany(product_id):
    #获得缓存
    #zz91app_keywordstopcompany=cache.get("zz91app_keywordstopcompany"+str(product_id))
    #if zz91app_keywordstopcompany:
        #return zz91app_keywordstopcompany
    sql="select id from products_keywords_rank where product_id=%s and start_time<'"+str(date.today()+timedelta(days=1))+"' and end_time>'"+str(date.today())+"' and is_checked=1 and type in ('10431004','手机站关键字排名') and not exists(select id from products where id=products_keywords_rank.product_id and is_pause=1) order by start_time asc"
    results = dbc.fetchonedb(sql,[product_id])
    #设置缓存
    #cache.set("zz91app_keywordstopcompany"+str(product_id),results,60*10)
    return results
#获取竞价排名客户信息
def getjingjialist(keywords='',limitcount='',mycompany_id=''):
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    #cl.SetSortMode( SPH_SORT_EXTENDED,"sort desc" )
    cl.SetGroupBy( 'product_id',SPH_GROUPBY_ATTR )
    cl.SetFilter('checked',[1])
    if (limitcount):
        cl.SetLimits (0,limitcount,limitcount)
    res=''
    if (keywords):
        res = cl.Query ('@(keywords,title,tags) '+keywords,'jingjiakeywords')
    if res:
        if res.has_key('matches'):
            keylist=res['matches']
            listall=[]
            for match in keylist:
                id=match['id']
                attrs=match['attrs']
                company_id=attrs['company_id']
                product_id=attrs['product_id']
                price=attrs['price']
                if not price:
                    price=0
                prolist=None
                #判断再生钱包余额,<0 下线
                onlineflag=1
                sql4='select sum(fee) from pay_mobileWallet where company_id=%s'
                blance=dbc.fetchonedb(sql4,[company_id])[0]
                if blance<int(price):
                    onlineflag=None
                    #sql="update app_jingjia_keywords set checked=0 where id=%s"
                    #dbc.updatetodb(sql,[id])
                if product_id and onlineflag:
                    prolist=getcompinfo(product_id,keywords,'')
                    if prolist:
                        sqlp="select check_status from products where id=%s"
                        resultp=dbc.fetchonedb(sqlp,[product_id])
                        if resultp:
                            check_status=resultp[0]
                        if str(check_status)!="2":
                            prolist['key_id']=id
                            #保存展示数据
                            gmt_modified=gmt_created=datetime.datetime.now()
                            sourcetype=1
                            userid=''
                            user_company_id=mycompany_id
                            key_id=id
                            showcount=1
                            sql="insert into app_jingjia_search(keywords,company_id,sourcetype,userid,user_company_id,key_id,showcount,gmt_modified,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            result=dbc.updatetodb(sql,[keywords,company_id,sourcetype,userid,user_company_id,key_id,showcount,gmt_modified,gmt_created])
                            if result:
                                prolist['search_id']=result[0]
                            price=attrs['price']
                            listall.append(prolist)
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
#城市联动js
def provincejs():
    sql="select code,label from category where left(code,4)=1001"
    result=dbc.fetchalldb(sql)
    listall={}
    if result:
        for list in result:
            list={'"'+list[0]+'"':'"'+list[1]+'"'}
            #list={'code':list[0],'label':list[1],'child':''}
            dictMerged3 = list.copy()
            dictMerged3.update( listall )
            listall=dictMerged3
        return listall
        for a in listall:
            sql="select code,label from category where code like '"+a['code']+"____'"
            result=dbc.fetchalldb(sql)
            if result:
                listall1=[]
                for list1 in result:
                    list2={'code':list1[0],'label':list1[1],'child':''}
                    listall1.append(list2)
                a['child']=listall1

                for b in listall1:
                    sql="select code,label from category where code like '"+b['code']+"____'"
                    result=dbc.fetchalldb(sql)
                    if result:
                        listall2=[]
                        for list3 in result:
                            list4={'code':list3[0],'label':list3[1],'child':''}
                            listall2.append(list4)
                        b['child']=listall2

                        for c in listall2:
                            sql="select code,label from category where code like '"+c['code']+"____'"
                            result=dbc.fetchalldb(sql)
                            if result:
                                listall3=[]
                                for list5 in result:
                                    list6={'code':list5[0],'label':list5[1]}
                                    listall3.append(list6)
                                c['child']=listall3
    return listall
def getcompinfo(pdtid,keywords,company_id=''):
    isbuycontact=None
    if company_id:
        isbuycontact=getbuycontact(company_id,pdtid)
    productsinfo=cache.get("app_productsinfoa"+str(pdtid))
    #productsinfo=None
    if (productsinfo==None):
        sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%%Y/%%m/%%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit,p.check_status FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code where p.id=%s;"
        productlist = dbc.fetchonedb(sql,pdtid)
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
            if (viptype == '10051003'):
                arrviptype['vippic']="http://img0.zz91.com/zz91/ppc/images/ldblogo.jpg"
                arrviptype['vipname']='来电宝'
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
            check_status=productlist[14]
            if (price_unit==None):
                price_unit=''
            else:
                if (allprice!=''):
                    allprice=allprice+price_unit
            #---接听率
            sql1="select phone_rate,level from ldb_level where company_id=%s and is_date=0 and exists(select company_id from crm_company_service where crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and company_id=ldb_level.company_id)"
            ldbrate = dbc.fetchonedb(sql1,[productlist[0]])
            if ldbrate:
                phone_rate=ldbrate[0]
                phone_level=ldbrate[1]
            else:
                phone_rate=None
                phone_level=None
            #----
            sql1="select pic_address from products_pic where product_id=%s and check_status=1"
            productspic = dbc.fetchonedb(sql1,productlist[2])
            if productspic:
                pdt_images=productspic[0]
            else:
                pdt_images=""
            if (pdt_images == '' or pdt_images == '0'):
                pdt_images='../cn/img/noimage.gif'
            else:
                pdt_images='http://img3.zz91.com/135x135/'+pdt_images+''
            
            ldbtel=getldbphone(productlist[0])
            isshowcontact=getisbuyshowphone(productlist[0])
            list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
            ,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5],'check_status':check_status
            ,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype
            ,'pdt_images':pdt_images,'pdt_price':allprice
            ,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'ldbtel':ldbtel,'phone_rate':phone_rate,'phone_level':phone_level,'isshowcontact':isshowcontact}
        else:
            list1=None
            
        #list1=getproid(pdtid)
        if (list1 == None):
            return None
        else:
            pdt_images=list1['pdt_images']
            
            vodiotypelist=["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]
            if pdt_images:
                kzmlist=pdt_images.split(".")
                if kzmlist:
                    pictype=kzmlist[len(kzmlist)-1].lower()
                    if pictype in vodiotypelist:
                        pdt_images="../../image/video.png"
                        list1['pdt_images']=pdt_images
            if (pdt_images=='../cn/img/noimage.gif'):
                list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
            pdt_detail=filter_tags(list1['pdt_detail'])
            pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
            list1['pdt_detail']=subString(pdt_detail,100)+'...'
        productsinfo=list1
        cache.set("app_productsinfoa"+str(pdtid),list1,60*60)
    productsinfo['isbuycontact']=isbuycontact
    return productsinfo
def getisbuyshowphone(company_id):
    gmt_created=datetime.datetime.now()
    sql='select id from shop_showphone where company_id=%s and gmt_end>=%s order by id desc'
    result=dbc.fetchonedb(sql,[company_id,gmt_created])
    if result:
        return 3
def getbuycontact(company_id,pdtid):
    sql2='select company_id from products where id=%s'
    result=dbc.fetchonedb(sql2,[pdtid])
    if result:
        forcompany_id=result[0]
        sql='select id from pay_mobileWallet where company_id=%s and forcompany_id=%s'
        buycontact=dbc.fetchonedb(sql,[company_id,forcompany_id])
        if buycontact:
            return 1
#---获得来电宝电话
def getldbphone(company_id):
    if company_id:
        sqlg="select front_tel,tel from phone where company_id=%s and expire_flag=0 and exists(select company_id from crm_company_service where crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and company_id=phone.company_id)"
        phoneresult=dbc.fetchonedb(sqlg,[company_id])
        if phoneresult:
            tel=phoneresult[1]
            tel=tel.replace("-",",,,")
            return {'front_tel':phoneresult[0],'tel':tel}
        else:
            return None
    else:
        return None
#获得公司ID
def getcompany_id(cname,regtime):
    sql="select max(id) from company"
    newcode=dbc.fetchonedbmain(sql)
    if (newcode == None):
        return '0'
    else:
        return newcode[0]
#--我的账号
def getaccount(company_id):
    sqlr="select account from company_account where company_id=%s"
    rlist = dbc.fetchonedb(sqlr,[str(company_id)])
    if rlist:
        return rlist[0]
def getcompanyid(account):
    sql="select company_id from  company_account where account=%s"
    result=dbc.fetchonedb(sql,[account])
    if result:
        return result[0]
#记录浏览关键字
def updatesearchKeywords(appid,company_id,keywords,ktype=""):
    gmt_created=datetime.datetime.now()
    if keywords and appid:
        sqlc="select count(0) from app_user_keywords where appid=%s"
        resultc=dbc.fetchonedb(sqlc,[appid])
        if resultc[0]<=20:
            sql="select id from app_user_keywords where appid=%s and keywords=%s"
            result=dbc.fetchonedb(sql,[appid,keywords])
            if not result:
                sqla="insert into app_user_keywords(appid,ktype,company_id,keywords,gmt_created) values(%s,%s,%s,%s,%s)"
                dbc.updatetodb(sqla,[appid,ktype,company_id,keywords,gmt_created])
        else:
            sql="select id from app_user_keywords where appid=%s and keywords=%s"
            result=dbc.fetchonedb(sql,[appid,keywords])
            if not result:
                sqlm="select min(id) from app_user_keywords where appid=%s"
                res=dbc.fetchonedb(sqlm,[appid])
                if res:
                    minid=res[0]
                    sql="delete from app_user_keywords where id=%s"
                    dbc.updatetodb(sql,[minid])
                sqla="insert into app_user_keywords(appid,ktype,company_id,keywords,gmt_created) values(%s,%s,%s,%s,%s)"
                dbc.updatetodb(sqla,[appid,ktype,company_id,keywords,gmt_created]);
#更新登录数据
def updatelogin(request,company_id):
    gmt_modified=datetime.datetime.now()
    sqll="update company_account set gmt_last_login=%s,gmt_modified=%s where company_id=%s"
    dbc.updatetodb(sqll,[gmt_modified,gmt_modified,company_id]);
    ip=getIPFromDJangoRequest(request)
    gmt_modifiedto=str(int(time.mktime(gmt_modified.timetuple())))+"000"
    try:
        payload={'appCode':'zz91','operator':company_id,'operation':'login','ip':ip,'time':gmt_modifiedto,'data':''}
        r= requests.post("http://apps1.zz91.com/zz91-log/log",data=payload)
        return r.content
    except:
        return None
def getIPFromDJangoRequest(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        return request.META.get('REMOTE_ADDR')
#阿里大于短信系统
def postsms_dayu(mobile,sms_template_code,sms_free_sign_name,sms_param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo("23410861", "72b4d7f51b757714b946d82ff9376a55"))
    req.sms_type = "normal"
    req.rec_num = mobile
    req.sms_template_code=sms_template_code
    req.sms_free_sign_name=sms_free_sign_name
    req.sms_param = json.dumps(sms_param,ensure_ascii=False,indent=2)
    try:
        resp= req.getResponse()
        if resp.get('alibaba_aliqin_fc_sms_num_send_response').get('result').get('success')==True:
            return True
        else:
            return False
    except Exception,e:
        return False
#----发手机短信
def postsms(mobile,username,userid):
    sqlp="select TIMESTAMPDIFF(SECOND,gmt_created,now()) as ltime from auth_forgot_password_log where company_id=%s and DATEDIFF(CURDATE(),gmt_created)<1 order by gmt_created desc"
    plist=dbc.fetchalldb(sqlp,[userid])
    pcount=len(plist)
    if (pcount<10):
        if plist:
            ltime=plist[0][0]
            if ltime<=60:
                return '验证码已经发送，一分钟内请不要重复提交！'
        tmp = random.randint(10000, 99999)
        #content="欢迎使用ZZ91再生网服务。验证码是："+str(tmp)+",输入验证码继续完成操作，该验证码10分钟内输入有效。"
        #url="http://mt.10690404.com/send.do?Account=astokf&Password=C@4k@33lsbe2lw^6&Mobile="+str(mobile)+"&Content="+content+"&Exno=0"
        #f = urllib.urlopen(url)
        #html = f.read()
        #o = json.loads(html)
        
        sms_template_code="SMS_12520535"
        sms_free_sign_name="ZZ91再生网"
        smscontent=r'验证是：(.*?)，请勿泄露'
        code=tmp
        sms_param={"code": str(code), "product": "ZZ91再生网"}
        returnsms=postsms_dayu(mobile[0:11],sms_template_code,sms_free_sign_name,sms_param)
        
        gmt_created=datetime.datetime.now()
        sql="insert into auth_forgot_password_log(company_id,type,gmt_created,gmt_modified) values(%s,%s,%s,%s)"
        dbc.updatetodb(sql,[userid,1,gmt_created,gmt_created]);
        sqlp="select id from auth_forgot_password where username=%s and userid=%s order by id desc"
        plist=dbc.fetchonedb(sqlp,[username,userid]);
        if not plist:
            sql="insert into auth_forgot_password(username,userid,auth_key,gmt_created) values(%s,%s,%s,%s)"
            dbc.updatetodb(sql,[username,userid,tmp,gmt_created]);
        else:
            sql="update auth_forgot_password set auth_key=%s,gmt_created=%s where id=%s"
            dbc.updatetodb(sql,[tmp,gmt_created,plist[0]]);
        return True
    else:
        return "您已经超过了每天发生10条短信的限制！"
#验证APP是否绑定
def appbinding(appid):
    sql="select target_account from oauth_access where open_id=%s and target_account<>'0'"
    list=dbc.fetchonedb(sql,[appid]);
    if list:
        return list[0]
    else:
        return None
    
def getallpricecategroy(categoryid):
    if not categoryid:
        return None
    list=categoryid
    sql="select id from price_category where parent_id in %s and showflag=1"
    alist=dbc.fetchalldb(sql,[categoryid])
    if alist:
        for ll in alist:
            list.append(int(ll[0]))
            sql1="select id from price_category where parent_id=%s and showflag=1"
            aalist=dbc.fetchalldb(sql1,[ll[0]])
            if aalist:
                for lll in aalist:
                    list.append(int(lll[0]))
                    sql11="select id from price_category where parent_id=%s and showflag=1"
                    aaalist=dbc.fetchalldb(sql11,[lll[0]])
                    if aaalist:
                        for llll in aaalist:
                            list.append(int(llll[0]))
    return list

def getcategory_company_price(code):
    if not code:
        code='____'
    sql="select id,label,code from category_company_price where code like %s and is_del=0"
    alist=dbc.fetchalldb(sql,[code])
    listall=[]
    if alist:
        for ll in alist:
            list1={'id':ll[0],'label':ll[1],'code':ll[2],'child':''}
            sql1="select id,label,code from category_company_price where code like %s and is_del=0"
            aalist=dbc.fetchalldb(sql1,[ll[2]+"____"])
            child1=[]
            if aalist:
                for lll in aalist:
                    list2={'id':lll[0],'label':lll[1],'code':lll[2],'child':''}
                    sql11="select id,label,code from category_company_price where code like %s and is_del=0"
                    aaalist=dbc.fetchalldb(sql11,[lll[2]+"____"])
                    child2=[]
                    if aaalist:
                        for llll in aaalist:
                            list3={'id':llll[0],'label':llll[1],'code':llll[2],'child':''}
                            child2.append(list3)
                    list2['child']=child2
                    child1.append(list2)
            list1['child']=child1
            listall.append(list1)
    return listall

#昨天
def getYesterday():   
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)   
    yesterday=today-oneday    
    return yesterday  

#今天     
def getToday():   
    return datetime.date.today()     
 
#获取给定参数的前几天的日期，返回一个list   
def getDaysByNum(num):   
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)       
    li=[]        
    for i in range(0,num):   
        #今天减一天，一天一天减   
        today=today-oneday   
        #把日期转换成字符串   
        #result=datetostr(today)   
        li.append(datetostr(today))   
    return li   

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt
def datetime_timestamp(dt):
     #dt为字符串
     #中间过程，一般都需要将字符串转化为时间数组
     #time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     #将"2012-03-28 06:53:40"转化为时间戳
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return int(s)
#将字符串转换成datetime类型  
def strtodatetime(datestr,format):       
    return datetime.datetime.strptime(datestr,format)   
 
#时间转换成字符串,格式为2008-08-02   
def datetostr(date):     
    return   str(date)[0:10]   
 
#两个日期相隔多少天，例：2008-10-03和2008-10-01是相隔两天  
def datediff(beginDate,endDate):   
    format="%Y-%m-%d";
    bd=strtodatetime(beginDate,format)   
    ed=strtodatetime(endDate,format)       
    oneday=datetime.timedelta(days=1)   
    count=0
    if ed>bd:
        while bd!=ed:   
            ed=ed-oneday   
            count+=1 
        return count   

 
 
#获取两个时间段的所有时间,返回list  
def getDays(beginDate,endDate):   
    format="%Y-%m-%d";   
    bd=strtodatetime(beginDate,format)   
    ed=strtodatetime(endDate,format)   
    oneday=datetime.timedelta(days=1)    
    num=datediff(beginDate,endDate)+1    
    li=[]   
    for i in range(0,num):    
        li.append(datetostr(ed))   
        ed=ed-oneday   
    return li   


#获取当前年份 是一个字符串  
def getYear(datestr=""):
    if not datestr: 
        return str(datetime.date.today())[0:4]
    else:
        return str(datestr)[0:4]
 
#获取当前月份 是一个字符串  
def getMonth(datestr=""):
    if not datestr:  
        return str(datetime.date.today())[5:7]
    else:
        return str(datestr)[5:7]  
 
#获取当前天 是一个字符串  
def getDay(datestr=""):
    if not datestr:
        return str(datetime.date.today())[8:10]
    else:
        return str(datestr)[8:10]    

def getNow():   
    return datetime.datetime.now()

def getdatelist():
    nyear=getYear()
    nmonth=getMonth()
    yearlist=[]
    monthlist=[]
    for i in range(1,int(nmonth)+1):
        monthlist.append(i)
    for i in range(int(nyear),2004,-1):
        if (i!=int(nyear)):
            monthl=[1,2,3,4,5,6,7,8,9,10,11,12]
        else:
            monthl=monthlist
        list={'year':i,'month':monthl}
        yearlist.append(list)
    return yearlist

#获得远程图片宽和高
def getpicturewh(url):
    #url = 'http://img1.zz91.com/ads/1377964800000/f53cb9e8-8fc5-4bf1-ae3b-468f5f814da0.gif'
    file = urllib.urlopen(url)
    tmpIm = StringIO.StringIO(file.read())
    im = Image.open(tmpIm)
    isize={'width':im.size[0],'height':im.size[1]}
    return isize
#加密
def getjiami(strword):
    if strword:
        return strword.encode('utf8','ignore').encode("hex")
    else:
        return ''
def getjiemi(strword):
    if strword:
        return strword.decode("hex").decode('utf8','ignore')
    else:
        return ''
#判断是否为HEX码
def gethextype(keywords):
    zwtype=0
    zwflag=0
    strvalue="abcdef0123456789"
    if keywords:
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
    else:
        return False
#关键字加亮  搜索引擎
def getlightkeywords(cl,docs,words,index):
    opts = {'before_match':'<font color=red>', 'after_match':'</font>', 'chunk_separator':' ... ', 'limit':400, 'around':15}
    tagscrl = cl.BuildExcerpts(docs, index, words, opts)
    if tagscrl:
        return tagscrl[0]
    else:
        return docs
def validateEmail(email):
    if len(email) > 5:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
           return 1
    return 0

def getadlistkeywords(pkind,keywords):
    adid="0"
    adidlist="0"
    sqlp="select ad_id from ad_exact_type where ad_position_id=%s and anchor_point=%s"
    alist=dbs.fetchalldb(sqlp,[pkind,keywords])
    if alist:
        for aid in alist:
            ad_id=aid[0]
            adidlist+=","+str(ad_id)
            #adidlist.append(ad_id)
    #if adidlist:
        #adid=adidlist[0]
    #return adidlist    
    sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and id in ("+str(adidlist)+") and review_status='Y' and online_status='Y' order by sequence asc,gmt_start asc"
    alist=dbs.fetchalldb(sql,[pkind])
    listvalue=[]
    if alist:
        for list in alist:
            list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'url_hex':getjiami('http://gg.zz91.com/hit?a='+str(list[2])),'picaddress':list[0],'ad_title':list[3],'ad_target_url':list[1]}
            listvalue.append(list1)
    return listvalue
#获得城市信息
def getnavareavalue(code):
    if code:
        sql="select label,code from category where code=%s"
        result=dbc.fetchonedb(sql,[code])
        if result:
            area2=result[0]
            return result
    else:
        return None
#获得app token
def gettoken(company_id):
    sql="select token from app_token where company_id=%s and TIMESTAMPDIFF(HOUR,gmt_created,NOW())<=4"
    listd=dbc.fetchonedb(sql,[company_id])
    if listd:
        return listd[0]
#记录客户pv uv
def getproductspv(products_id,company_id):
    sql="select id from analysis_products_pv where products_id=%s and company_id=%s"
    list=dbc.fetchonedb(sql,[products_id,company_id])
    if not list:
        gmt_modified=datetime.datetime.now()
        sqli="insert into analysis_products_pv(products_id,company_id,pv,uv,gmt_modified) values(%s,%s,%s,%s,%s)"
        dbc.updatetodb(sqli,[products_id,company_id,1,1,gmt_modified])
    else:
        sql="update analysis_products_pv set pv=pv+1 where id=%s"
        dbc.updatetodb(sql,[list[0]])
#
def getloginstatus(company_id,usertoken):
    if not company_id or str(company_id)=="0" or not usertoken:
        return None
    else:
        myusertoken=gettoken(company_id)
        if not myusertoken:
            return None
        if myusertoken!=usertoken:
            return None
    return 1
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
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_br.sub('\t',s)#将br转换为换行
    s=re_br.sub('\r',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    s=s.replace(" ","")
    s=s.replace('<br>','').replace('&nbsp;',' ')
    s=s.replace('　','')
    return s

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

def remove_script(html):#移除script
    if '<script' in html:
        re_py=r'<script.*?</script>'
        urls_pat=re.compile(re_py,re.DOTALL)
        img_url=re.findall(urls_pat,html)
        for img_url in img_url:
            html=html.replace(img_url,'')
    return html

def remove_content_a(html):#移除a链接
    html=re.sub('<A.*?>','',html)
    html=re.sub('</A>','',html)
    html=re.sub('<a.*?>','',html)
    html=re.sub('style=".*?"','',html)
    html=re.sub('</a>','',html)
    return html
def remove_content_valuemore(html):#移除a链接
    html=re.sub('<A.*?>','',html)
    html=re.sub('</A>','',html)
    html=re.sub('<a.*?>','',html)
    html=re.sub('</a>','',html)
    html=re.sub('</div>','',html)
    html=re.sub('<table.*?>','',html)
    html=re.sub('<tr.*?>','',html)
    html=re.sub('<td.*?>','',html)
    html=re.sub('</table>','',html)
    html=re.sub('</tr>','',html)
    html=re.sub('</td>','',html)
    html=re.sub('\r','',html)
    html=re.sub('\n','',html)
    html=re.sub('\t','',html)
    html=re.sub('<tbody.*?>','',html)
    html=re.sub('<tbody.*?>','',html)
    html=re.sub('<!--.*?-->','',html)
    html=re.sub('<span.*?>','',html)
    html=re.sub('</span>','',html)
    
    html=re.sub('<wb.*?>','',html)
    html=re.sub('</wb.*?>','',html)
    html=re.sub('<iframe.*?>','',html)
    html=re.sub('</iframe>','',html)
    
    html=re.sub('<h.*?>','',html)
    html=re.sub('</h.*?>','',html)
    html=re.sub('<li.*?>','',html)
    html=re.sub('</li>','<br />',html)
    html=re.sub('<ul.*?>','',html)
    html=re.sub('</ul>','',html)
    html=re.sub('<ol.*?>','',html)
    html=re.sub('</ol>','',html)
    
    html=re.sub('<div.*?>','',html)
    html=re.sub('</div>','<br />',html)
    
    html=re.sub('align=".*?"','',html)
    
    html=re.sub('STYLE=".*?"','',html)
    html=re.sub('style=".*?"','',html)
    html=re.sub('class=".*?"','',html)
    html=re.sub('ALIGN=".*?"','',html)
    html=re.sub('align=center','',html)
    html=re.sub('width=".*?"','',html)
    html=re.sub('height=".*?"','',html)
    html=re.sub('<input.*?>','',html)
    html=re.sub('<blockquote.*?>','',html)
    html=re.sub('</blockquote>','',html)
    
    
    return html
def subString(string,length):   
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

def getadlist(pkind):
    adcach=cache.get("app_indexad"+str(pkind))
    adcach=None
    if adcach:
        return adcach
    sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and DATEDIFF(gmt_plan_end,CURDATE())>=0 and review_status='Y' and online_status='Y' order by sequence asc,gmt_start asc"
    list=dbads.fetchonedb(sql,[pkind])
    if list:
        target_url=list[1]
        picaddress=list[0]
        if target_url and "choujiang" not in target_url:
            target_url=target_url.replace("http://m.zz91.com","")
        if picaddress:
            picaddress=picaddress.replace("http://img1.zz91.com/","http://img3.zz91.com/300x300/")
        list1={'target_url':target_url,'picaddress':picaddress,'ad_title':list[3]}
        cache.set("app_indexad"+str(pkind),list1,60*30)
        return list1
def getadlistall(pkind):
    adcach=cache.get("app_indexadall"+str(pkind))
    nowdate=getDay()
    if adcach:
        return adcach
    sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and DATEDIFF(gmt_plan_end,CURDATE())>=0  and review_status='Y' and online_status='Y' order by sequence asc,gmt_start asc"
    adlist=dbads.fetchalldb(sql,[pkind])
    listall=[]
    listfirst=""
    listlast=""
    if adlist:
        i=0
        for list in adlist:
            if i==0:
                listfirst={'target_url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}
            list1={'target_url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}
            listall.append(list1)
            listlast=[{'target_url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}]
            i=i+1
        #listall.append(listfirst)
        #listall=listlast+listall
        cache.set("app_indexadall"+str(pkind),listall,60*10)
    return listall
#微信绑定抽奖 2015-12-7  2016-1-7
#端午抽奖  2016-6-2 2016-6-7
def choujiang(account="",company_id="",appid=""):
    format="%Y-%m-%d"
    gmt_created=getNow()
    beginDate="2016-6-2"
    endDate="2016-6-7"
    bnum=3
    btype=3
    jiangpin=-1
    nowdate=date_to_int(getToday())
    endDate=date_to_int(strtodatetime(endDate,format))
    if nowdate>endDate:
        return None
    if nowdate<date_to_int(strtodatetime(beginDate,format)):
        return None
    
    if account:
        sql="select company_id from company_account where account=%s"
        result=dbc.fetchonedb(sql,[account])
        if result:
            company_id=result[0]
    if appid:
        sqlc="select id from oauth_access where open_id=%s and open_type='app.zz91.com' and gmt_created>'"+beginDate+"'"
        list=dbc.fetchonedb(sqlc,[str(appid)])
        if list:
            if company_id:
                sql="select id from subject_choujiang where company_id=%s and btype=3"
                result=dbc.fetchonedb(sql,[company_id])
                if not result:
                    sql="insert into subject_choujiang(btype,gmt_created,bnum,company_id,jiangpin) values(%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sql,[btype,gmt_created,bnum,company_id,jiangpin])
#是否收藏
def isfavorite(content_id,favorite_type_code,company_id):
    if content_id and favorite_type_code and company_id:
        sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
        clist=dbc.fetchonedb(sql,[favorite_type_code,content_id,company_id])
        if clist:
            return 1
        else:
            return 0
    else:
        return 0
def getprofilerid(account):
    sql="select id from bbs_user_profiler where account=%s"
    newcode=dbc.fetchonedb(sql,[account])
    if (newcode == None):
        return '0'
    else:
        return newcode[0]
#写入朋友圈 
def insert_appquan(company_id,title,content,pic,url,type,gmt_created):
    bbs_post_category_id=106
    recontent=content
    if recontent:
        rpl1=re.findall('[0-9\ ]+',recontent)
        for r1 in rpl1:
            if len(r1)>10:
                recontent=recontent.replace(r1,r1[:-3]+'***')
    gmt_modified=gmt_created
    username=getaccount(company_id)
    if not title:
        title=""
    
    if bbs_post_category_id==106:
        bbs_post_assist_id=107
    else:
        bbs_post_assist_id=24
    bbs_user_profiler_id=1
    if (recontent and recontent!=""):
        bbs_user_profiler_id=getprofilerid(username)
        if (bbs_user_profiler_id==None):
            bbs_user_profiler_id=1
        reply_count=0
        title=title.strip()
        if (pic=="http://img0.zz91.com/zz91/images/indexLogo.png"):
            pic=""
        if pic:
            littlepic=pic
        else:
            littlepic="http://img0.zz91.com/zz91/images/link.png"
        content="<div style='background-color: #ebebeb;padding: 10px;line-height: 22px;clear:both;min-height: 50px;position: relative;' class='quanlink' url='"+url+"'><img src='"+littlepic+"' style='max-width: 40px;max-height: 40px;vertical-align:middle;float:left;margin-right: 10px;position: absolute;' /><div style='float: left;padding-left: 50px;word-break:break-all;'>"+recontent+"</div><div style='clear:both'></div></div>"
        value=[company_id,bbs_user_profiler_id,username,bbs_post_category_id,title,content,0,1,gmt_created,gmt_modified,gmt_modified,gmt_modified,4,bbs_post_assist_id,reply_count]
        sql="insert into bbs_post(company_id,bbs_user_profiler_id,account,bbs_post_category_id,title,content,is_del,check_status,gmt_created,gmt_modified,post_time,reply_time,postsource,bbs_post_assist_id,reply_count) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=dbc.updatetodb(sql,value)
        if result:
            bbs_post_id=result[0]
            
    """
    sql="select id from app_quan where company_id=%s and url=%s"
    result=dbc.fetchonedb(sql,[company_id,url])
    if not result:
        value=[company_id,title,content,pic,url,type,gmt_created]
        sql="insert into app_quan(company_id,title,content,pic,url,type,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
    """

