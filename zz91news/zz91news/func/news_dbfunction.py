#-*- coding:utf-8 -*-
def getfuzhuindexlist():
    listall=cache.get("news_fuzhuindexlist")
    if not listall:
        sql='select id,typename,keywords from dede_arctype where reid=183 order by id limit 0,4'
        resultlist=dbn.fetchalldb(sql)
        js=0
        listall=[]
        for result in resultlist:
            typeid=result[0]
            kind_name=result[1]
            kind_url=result[2]
            kind_url2=kind_url+'/list/'
            if typeid==156:
                kind_url=kind_url+'/list'
            js+=1
            idj=str(js)+'F'
            m2_sitem='m2_sitem'+str(js)
            m2_sitem_text='m2_sitem_text'+str(js)
            m2_sitem_button='m2_sitem_button'+str(js)
            roll_img=zzn.get_news_all(0,4,flag='s',typeid2=typeid)['list']
            kinds_6=zzn.get_news_all(0,6,typeid2=typeid)['list']
            keywords10=zzn.gettypelist(0,10,keywords=kind_name)
            list={'roll_img':roll_img,'keywords10':keywords10,'kinds_6':kinds_6,'kind_name':kind_name,'kind_url':kind_url,'kind_url2':kind_url2,'idj':idj,'m2_sitem':m2_sitem,'m2_sitem_button':m2_sitem_button,'m2_sitem_text':m2_sitem_text}
            listall.append(list)
        if listall:
            cache.set("news_fuzhuindexlist",listall,60*20)
    return listall
def getmaowenbanlist():
    listall=cache.get("news_maowenbanlist")
    if not listall:
        sql='select typename from dede_arctype where reid in (191,192,193,194) order by sortrank'
        resultlist=dbn.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            typename=result[0]
            typename_hex=getjiami(typename)
            list={'typename':typename,'typename_hex':typename_hex}
            listall.append(list)
        if listall:
            cache.set("news_maowenbanlist",listall,60*20)
    return listall
#专题列表
def get_special_list():
    listall=cache.get("news_maowenbanlist")
    if not listall:
        sql='select id,typeid,title,filename,litpic,description from dede_archives where exists(select aid from dede_addonspec where dede_archives.id=aid) order by pubdate desc limit 0,6'
        resultlist=dbn.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            typeid=result[1]
            title=result[2]
            filename=result[3]
            litpic=result[4]
            description=result[5]
            listdir={'id':id,'typeid':typeid,'title':title,'filename':filename,'litpic':litpic,'description':description}
            listall.append(listdir)
        if listall:
            cache.set("news_maowenbanlist",listall,60*20)
    return listall
        
#----读取友情链接
def getnewslinks1(fromNom,LimitNum):
    listall=cache.get("news_newslinks1"+str(fromNom)+str(LimitNum))
    if not listall:
        sql='select id,title,link from data_index where category_code=10201000 order by id desc limit %s,%s'
        resultlist=dbc.fetchalldb(sql,[fromNom,LimitNum])
        listall=[]
        for result in resultlist:
            id=result[0]
            title=result[1]
            link=result[2]
            list={'id':id,'title':title,'link':link}
            listall.append(list)
        if listall:
            cache.set("news_newslinks1"+str(fromNom)+str(LimitNum),listall,60*20)
    return listall
#广告样式
def getadshowtype(id):
    js_function=cache.get("news_adshowtype"+str(id))
    if not js_function:
        js_function=None
        sqlp="select js_function from delivery_style where id=%s"
        alist = dba.fetchonedb(sqlp,[id])
        if alist:
            js_function=alist[0]
            cache.set("news_adshowtype"+str(id),js_function,60*60)
    return js_function
#----获得广告
def getadlist(pkind):
    listvalue=cache.get("news_adlist"+str(pkind))
    if not listvalue:
        width=None
        height=None
        max_ad=None
        sqlp="select width,height,max_ad,delivery_style_id from ad_position where id=%s"
        alist = dba.fetchonedb(sqlp,[pkind])
        if alist:
            width=alist[0]
            height=alist[1]
            max_ad=alist[2]
            delivery_style_id=alist[3]
            js_function=getadshowtype(delivery_style_id)
        sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
        alist = dba.fetchalldb(sql,[pkind])
        listvalue=[]
        i=0
        for list in alist:
            i=i+1
            if (width=="0"):
                width=""
            if (height=="0"):
                height=""
            js_function1=js_function.replace("{1}",list[0])
            js_function1=js_function1.replace("|","")
            js_function1=js_function1.replace("\"","'")
            js_function1=js_function1.replace("{2}",list[3])
            js_function1=js_function1.replace("{3}",'http://gg.zz91.com/hit?a='+str(list[2]))
            js_function1=js_function1.replace("{4}",'width='+str(width))
            js_function1=js_function1.replace("{5}",'height='+str(height))
            list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3],'i':i}
            #list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'height':height,'width':width,'max_ad':max_ad,'js_function':js_function1,'ad_title':alist[3]}
            listvalue.append(list1)
        if listvalue:
            cache.set("news_adlist"+str(pkind),listvalue,60*60)
    return listvalue
#----公司库首页有图片的最新供求列表
def getindexofferlist_pic(kname="",pdt_type="",limitcount="",membertype=""):
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
    cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
    
    cl.SetLimits (0,limitcount,limitcount)
    if (pdt_type!=None and pdt_type!=""):
        cl.SetFilter('pdt_kind',[int(pdt_type)])
    cl.SetFilterRange('havepic',1,100)
    cl.SetFilterRange('haveprice',2,1000)
    if membertype:
        searchindex="offersearch_new_vip"
        cl.SetFilterRange('length_price',1,100000)
    else:
        searchindex="offersearch_new,offersearch_new_vip"
    if (kname==None):
        res = cl.Query ('',searchindex)
    else:
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,searchindex)
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            listall_offerlist=[]
            for match in itemlist:
                pid=match['id']
                price=getofferprice(pid)
                attrs=match['attrs']
                pdt_date=attrs['pdt_date']
                pdt_kind=attrs['pdt_kind']
                kindtxt=''
                if (pdt_kind=='1'):
                    kindtxt="供应"
                else:
                    kindtxt="求购"
                title=subString(attrs['ptitle'],40)
                sql1="select pic_address from products_pic where product_id=%s order by is_default desc,id desc"
                productspic = dbc.fetchonedb(sql1,pid)
                if productspic:
                    pdt_images=productspic[0]
                else:
                    pdt_images=""
                if (pdt_images == '' or pdt_images == '0'):
                    pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                else:
                    pdt_images='http://images.zz91.com/images.php?picurl=http://img1.zz91.com/'+pdt_images+'&width=85&height=85'
                list={'id':pid,'title':title,'gmt_time':pdt_date,'kindtxt':kindtxt,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images,'price':price}
                listall_offerlist.append(list)
            return listall_offerlist
#获得价格
def getofferprice(id):
    allprice=cache.get("news_offerprice"+str(id))
    if not allprice:
        sql="select p.min_price,p.max_price,p.price_unit from products as p where p.id=%s"
        plist = dbc.fetchonedb(sql,id)
        if plist:
            #价格范围判断
            allprice=""
            min_price=plist[0]
            if (min_price==None):
                min_price=''
            else:
                min_price=str(min_price)
                if (min_price!='0.0'):
                    allprice=allprice+min_price
            max_price=plist[1]
            if (max_price==None):
                max_price=''
            else:
                max_price=str(max_price)
                if (max_price!='0.0' and max_price!=min_price):
                    allprice=allprice+'-'+max_price
            price_unit=plist[2]
            #
            if (price_unit==None):
                price_unit=''
            else:
                if (allprice!=''):
                    allprice=allprice+price_unit
            if (allprice==""):
                allprice="电议或面议"
            cache.set("news_offerprice"+str(id),allprice,60*20)
    return allprice
#----添加搜索词
def addsearch_keywords(webtype,keywords,ip,gmt_created,detailtime,numb):
    sql1='select id,ip,numb from search_keywords where keywords=%s and gmt_created=%s'
    result=dbo.fetchonedb(sql1,[keywords,gmt_created])
    if result:
        id=result[0]
        ip1=result[1]
        ip=ip1+','+ip
        numb1=result[2]
        numb=numb1+numb
        sql='update search_keywords set ip=%s,numb=%s where id=%s'
        dbo.updatetodb(sql,[ip,numb,id])
    else:
        sql='insert into search_keywords(webtype,keywords,ip,gmt_created,detailtime,numb) values(%s,%s,%s,%s,%s,%s)'
        dbo.updatetodb(sql,[webtype,keywords,ip,gmt_created,detailtime,numb])
#----读取早晚报
def getdownloadinfo():
    listall=cache.get("news_downloadinfo")
    if not listall:
        sql="select id,title,gmt_created from download_info where is_deleted=0 and code in (2005100010001000,2005100010011001) order by id desc limit 0,6"
        result=dbc.fetchalldb(sql)
        listall=[]
        for list in result:
            list={'id':list[0],'title':list[1],'putdate':getMonth(list[2])+"-"+getDay(list[2])}
            listall.append(list)
        if listall:
            cache.set("news_downloadinfo",listall,60*60)
    return listall
#----读取企业新闻
def getcompanynews(fromcount,limitcount,allcount=''):
    if allcount:
        sql1='select count(0) from esite_news'
        count=dbc.fetchnumberdb(sql1)
    sql="select a.id,a.company_id,a.title,a.post_time,b.domain_zz91,b.membership_code from esite_news as a left join company as b on a.company_id=b.id order by id desc limit "+str(fromcount)+","+str(limitcount)+""
    result=dbc.fetchalldb(sql)
    listall=[]
    if result:
        for list in result:
            id=list[0]
            company_id=list[1]
            title=list[2]
            short_title=getTitleLen(title,12)
            post_time=date_to_str(list[3])
            short_time=''
#            short_time=date_to_str(list[3])
            domain_zz91=list[4]
            if not domain_zz91:
                domain_zz91=''
            membership_code=list[5]
            if membership_code=='10051003':
                url='http://www.zz91.com/ppc/newsdetail'+str(id)+'.htm'
            else:
                url='http://'+domain_zz91+'.zz91.com/news'+str(id)+'.htm'
            list={'id':id,'weburl':url,'title':title,'company_id':company_id,'domain_zz91':domain_zz91,'pubdate':post_time,'post_time':post_time,'short_time':short_time,'short_title':short_title}
            listall.append(list)
    if allcount:
        return {'list':listall,'count':count}
    return listall
#--我的账号
def getaccount(company_id):
    sqlr="select account from company_account where company_id=%s"
    rlist = dbc.fetchonedb(sqlr,[str(company_id)])
    if rlist:
        return rlist[0]
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