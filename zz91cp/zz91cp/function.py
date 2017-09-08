INDUSTRY_LABEL={
'10001000':'废塑料',
'10001001':'废金属',
'10001002':'废纸',
'10001003':'废旧轮胎与废橡胶',
'10001004':'废纺织品与废皮革',
'10001005':'废电子电器',
'10001006':'废玻璃',
'10001007':'废旧二手设备',
'10001008':'其他废料',
'10001009':'服务',
'10001010':'塑料原料',
}
#类别列表
def getindexcategorylist(code,showflag):
    #获得缓存
    zz91cp_getindexcategorylist=cache.get("zz91cp_getindexcategorylist"+str(code)+str(showflag))
    if zz91cp_getindexcategorylist:
        return zz91cp_getindexcategorylist
    catelist=getstaticValue('cate',code)
    if (catelist==None):
        sql="select label,code from category_products where code like %s order by sort asc"
        #cursor.execute(sql,str(code))
        listall_cate=[]
        #catelist=cursor.fetchall()
        catelist=dbc.fetchalldb(sql,str(code))
        for a in catelist:
            if (showflag==1):
                sql1="select label from category_products where code like '%s____' order by sort asc"
                #cursor.execute(sql1,str(a[1]))
                listall_cate1=[]
                #catelist1=cursor.fetchall()
                catelist1=dbc.fetchalldb(sql1,str(a[1]))
                for b in catelist1:
                    list1={'label':b[0]}
                    listall_cate1.append(list1)
            else:
                listall_cate1=None
            list={'label':a[0],'code':a[1],'catelist':listall_cate1}
            listall_cate.append(list)
        updatetaticValue('cate',code,listall_cate)
    else:
        listall_cate=catelist
    #设置缓存
    cache.set("zz91cp_getindexcategorylist"+str(code)+str(showflag),listall_cate,60*30)
    return listall_cate
#获得所有地区
def getarealist(code):
    #获得缓存
    zz91cp_getarealist=cache.get("zz91cp_getarealist"+str(code))
    if zz91cp_getarealist:
        return zz91cp_getarealist
    sql="select label,code from category where code like '"+str(code)+"____'"
    catelist=dbc.fetchalldb(sql)
    listall=[]
    for b in catelist:
        list={'code':b[1],'label':b[0],'label_hex':b[0].encode("hex")}
        listall.append(list)
    #设置缓存
    cache.set("zz91cp_getarealist"+str(code),listall,60*30)
    return listall

def getproducstcategorylist(code):
    #获得缓存
    zz91cp_getproducstcategorylist=cache.get("zz91cp_getproducstcategorylist"+str(code))
    if zz91cp_getproducstcategorylist:
        return zz91cp_getproducstcategorylist
    codelen=len(code)
    sql="select label,code from category_products where left(code,"+str(codelen)+")=%s and length(code)="+str(codelen+4)+" order by sort asc"
    catelist=dbc.fetchalldb(sql,code)
    listall=[]
    for b in catelist:
        list={'code':b[1],'label':b[0],'sql':sql}
        listall.append(list)
    #设置缓存
    cache.set("zz91cp_getproducstcategorylist"+str(code),listall,60*30)
    return listall
#记录点击次数
def cpchickNum(pingyin):
    if pingyin:
        sql="update daohang set showcount=showcount+1 where pingyin=%s"
        #cursor.execute(sql,[pingyin])
        #conn.commit()
        dbc.updatetodb(sql,[pingyin])
#相关供求类别
def getcategorylist(kname='',frompageCount='',limitcount=''):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    #cl.SetSortMode( SPH_SORT_EXTENDED,"sort desc" )
    if (frompageCount!=''):
        cl.SetLimits (frompageCount,limitcount,limitcount)
    else:
        cl.SetLimits (0,limitcount,limitcount)
    if (kname!=""):
        res = cl.Query (''+kname,'category_products')
    else:
        res = cl.Query ('','category_products')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            n=1
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                label=attrs['plabel']
                code=attrs['pcode']
                list1={'id':id,'code':code,'label':label,'label_hex':label.encode("hex"),'n':n}
                listall.append(list1)
                n=n+1
    return listall
#------最新报价信息
def getindexpricelist(kname="",assist_type_id="",limitcount="",searchname="",titlelen="",searchmode=1):
    if (titlelen=="" or titlelen==None):
        titlelen=100
    price=SPHINXCONFIG['name']['price']['name']
    serverid=SPHINXCONFIG['name']['price']['serverid']
    port=SPHINXCONFIG['name']['price']['port']
    cl = SphinxClient()
    cl.SetServer ( serverid,port )

    if searchmode==1:
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    else:
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,gmt_order desc" )
    
    cl.SetLimits (0,limitcount,limitcount)
    if(assist_type_id!=None and assist_type_id!=""):
        cl.SetFilter('assist_type_id',[assist_type_id])
    if (kname):
        res = cl.Query ('@(title,tags) '+kname,price)
    else:
        res = cl.Query ('',price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_baojia=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=subString(attrs['ptitle'],titlelen)
                gmt_time=attrs['gmt_time']
                #td_time=gmt_time.strftime('%Y-%m-%d')
                list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle'],'url':'http://jiage.zz91.com/detail/'+str(id)+'.html'}
                listall_baojia.append(list1)
            listcount_baojia=res['total_found']

            return listall_baojia
#------最新企业报价信息
def getcompanypricelist(kname="",limitcount="",titlelen="",company="",searchmode=1):
    if (titlelen=="" or titlelen==None):
        titlelen=100
    company_price=SPHINXCONFIG['name']['company_price']['name']
    serverid=SPHINXCONFIG['name']['company_price']['serverid']
    port=SPHINXCONFIG['name']['company_price']['port']
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    if searchmode==1:
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    else:
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,post_time desc" )
    cl.SetLimits (0,limitcount,limitcount)
    if (kname):
        try:
            res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname,company_price)
        except:
            res = None
    else:
        res = cl.Query ('',company_price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_baojia=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=subString(attrs['ptitle'],titlelen)
                title=title.replace("\\","-")
                company_id=attrs['company_id']
                gmt_time=attrs['ppost_time']
                min_price=attrs['min_price']
                max_price=attrs['max_price']
                price_unit=attrs['price_unit']
                price=''
                if min_price:
                    if isinstance(min_price,int):
                        min_price=float(min_price)
                if max_price:
                    if isinstance(max_price,int):
                        max_price=float(max_price)
                price=''
                if min_price>0 and min_price:
                    price+=str(min_price)
                if max_price and max_price>0 and min_price>0 and min_price:
                    price+="-"+str(min_price)
                if max_price and max_price>0 and min_price<=0:
                    price+=str(min_price)
                if price:
                    if price_unit:
                        price+=str(price_unit)
                country=attrs['country']
                province=attrs['province']
                city=attrs['city']
                companyname=None
                if company:
                    sqlc="select name from company where id=%s"
                    #cursor.execute(sqlc,[company_id])
                    #alist = cursor.fetchone()
                    alist=dbc.fetchonedb(sqlc,[company_id])
                    if alist:
                        companyname=alist[0]
                product_id=None
                sqlp="select product_id from company_price where id=%s"
                #cursor.execute(sqlp,[id])
                #alist = cursor.fetchone()
                alist=dbc.fetchonedb(sqlp,[id])
                if alist:
                    product_id=alist[0]
                if product_id:
                    list1={'title':title,'id':id,'product_id':product_id,'gmt_time':gmt_time,'min_price':min_price,'max_price':max_price,'price_unit':price_unit,'price':price,'area':province+city,'company_id':company_id,'companyname':companyname,'fulltitle':attrs['ptitle'],'url':'http://jiage.zz91.com/cdetail/'+str(id)+'.html'}
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
            return listall_baojia
#------企业报价 翻页
def getcompanypricelistmore(kname="",frompageCount="",limitNum="",titlelen="",company="",province="",searchmode=1):
    if (titlelen=="" or titlelen==None):
        titlelen=100
    company_price=SPHINXCONFIG['name']['company_price']['name']
    serverid=SPHINXCONFIG['name']['company_price']['serverid']
    port=SPHINXCONFIG['name']['company_price']['port']
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    if searchmode==1:
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    else:
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,post_time desc" )
    cl.SetLimits (frompageCount,limitNum,20000)
    if (kname):
        if (province and province!=""):
            k=kname+" "+province
        else:
            k=kname
        res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+k,company_price)
    else:
        res = cl.Query ('',company_price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_baojia=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=subString(attrs['ptitle'],titlelen)
                title=title.replace("\\","-")
                company_id=attrs['company_id']
                gmt_time=attrs['ppost_time']
                min_price=attrs['min_price']
                max_price=attrs['max_price']
                price_unit=attrs['price_unit']
                
                if min_price:
                    min_price=float(min_price)
                if max_price:
                    max_price=float(max_price)
                price=''
                if min_price>0 and min_price:
                    price+=str(min_price)
                if max_price and max_price>0 and min_price>0 and min_price:
                    price+="-"+str(min_price)
                if max_price and max_price>0 and min_price<=0:
                    price+=str(min_price)
                if price:
                    if price_unit:
                        price+=str(price_unit)
                #price=str(min_price)+"-"+str(max_price)+str(price_unit)
                
                if price_unit=="" or str(price_unit)=='None':
                    price_unit=None
                country=attrs['country']
                province=attrs['province']
                city=attrs['city']
                companyname=None
                sqlc="select name from company where id=%s"
                #cursor.execute(sqlc,[company_id])
                #alist = cursor.fetchone()
                alist=dbc.fetchonedb(sqlc,[company_id])
                sql='select b.domain_zz91 from company_price as a left join company as b on a.company_id=b.id where a.company_id=%s'
                result=dbc.fetchonedb(sql,[company_id])
                if result:
                    domain_zz91=result[0]
                if alist:
                    companyname=alist[0]
                product_id=None
                sqlp="select product_id from company_price where id=%s"
                alist=dbc.fetchonedb(sqlp,[id])
                if alist:
                    product_id=alist[0]
                if product_id:
                    sql='select pic_address from products_pic where product_id=%s'
                    result=dbc.fetchonedb(sql,[product_id])
                    if result:
                        pic_address=result[0]
                    else:
                        pic_address=''
                    list1={'title':title,'id':id,'product_id':product_id,'gmt_time':gmt_time,'min_price':min_price,'max_price':max_price,'price_unit':price_unit,'price':price,'area':province+city,'company_id':company_id,'companyname':companyname,'fulltitle':attrs['ptitle'],'url':'http://jiage.zz91.com/cdetail/'+str(id)+'.html','k':k,'pic_address':pic_address,'domain_zz91':domain_zz91}
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
            return {'list':listall_baojia,'count':listcount_baojia}
#最新互助信息
def getindexbbslist(kname='',limitcount='',bbs_post_category_id='',searchmode=1):
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], settings.SPHINXCONFIG['port'] )
    if searchmode==1:
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    else:
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,post_time desc" )
    cl.SetLimits (0,limitcount,limitcount)
    if(bbs_post_category_id!=None and bbs_post_category_id!=""):
        cl.SetFilter('bbs_post_category_id',[bbs_post_category_id])
    if (kname):
        res = cl.Query ('@(title,tags) '+kname,'huzhu')
    else:
        res = cl.Query ('','huzhu')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_news=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                sql="select content,reply_time,account,reply_count from bbs_post where id=%s"
                alist=dbc.fetchonedb(sql,id)
                if alist:
                    content=subString(filter_tags(alist[0]),300)
                    if alist[1]:
                        reply_time=formattime(alist[1],0)
                    else:
                        reply_time=""
                    if alist[3]:
                        reply_count=alist[3]
                    else:
                        reply_count=0
                    account=alist[2]
                    postname=getpostbbsusername(account)
                    if postname is None:
                        postname=""
                else:
                    content=""
                    havepic=0
                    username=""
                    reply_time=""
                gmt_time=attrs['ppost_time']
                if not reply_time:
                    reply_time=gmt_time
                if not title:
                    title=content
                list1={'title':title,'id':id,'gmt_time':reply_time,'content':content,'postname':postname,'reply_count':reply_count}
                listall_news.append(list1)

            return listall_news
#最新互助信息 翻页
def getbbslist(kname,frompageCount,limitNum,category_id,searchmode=1):

    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    if searchmode==1:
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    else:
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,post_time desc" )
    if (category_id):
        cl.SetFilter('bbs_post_category_id',[int(category_id)])
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    cl.SetLimits (frompageCount,limitNum,20000)
    if (kname):
        res = cl.Query ('@(title,tags) '+kname,'huzhu')
    else:
        res = cl.Query ('','huzhu')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_news=[]
            i=1
            for match in tagslist:
                id=match['id']
                yy=i % 6
                if yy==1:
                    yyhtml=1
                else:
                    yyhtml=None
                if (i % 6==0):
                    yyhtml_end=1
                else:
                    yyhtml_end=None
                sql="select content,reply_time,account,reply_count from bbs_post where id=%s"
                alist=dbc.fetchonedb(sql,id)
                if alist:
                    havepic=havepicflag(alist[0])
                    content=subString(filter_tags(alist[0]),300)
                    if alist[1]:
                        reply_time=formattime(alist[1],0)
                    else:
                        reply_time=""
                    if alist[3]:
                        reply_count=alist[3]
                    else:
                        reply_count=0
                    account=alist[2]
                    postname=getpostbbsusername(account)
                    if postname is None:
                        postname=""
                    
                attrs=match['attrs']
                title=attrs['ptitle']
                if not title:
                    title=content
                gmt_time=attrs['ppost_time']
                list1={'title':title,'id':id,'gmt_time':gmt_time,'yyhtml':yyhtml,'yyhtml_end':yyhtml_end,'havepic':havepic,'content':content,'postname':postname,'reply_count':reply_count}
                listall_news.append(list1)
                if i>=6:
                    i=1
                else:
                    i=i+1
            listcount_news=res['total_found']

            return {'list':listall_news,'count':listcount_news}
#最新互助信息 翻页
def getbbsreplylist(kname,frompageCount,limitNum,bbs_post_id):

    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    if (bbs_post_id):
        cl.SetFilter('bbs_post_id',[int(bbs_post_id)])
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    cl.SetLimits (frompageCount,limitNum,20000)
    if (kname):
        res = cl.Query ('@(title,tags) '+kname,'huzhureply')
    else:
        res = cl.Query ('','huzhureply')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_news=[]
            lou=1
            for match in tagslist:
                id=match['id']
                sql="select content,account,gmt_created from bbs_post_reply where id=%s"
                #cursor.execute(sql,id)
                #alist = cursor.fetchone()
                alist=dbc.fetchonedb(sql,id)
                if alist:
                    content=subString(filter_tags(alist[0]),50)
                    username=getusername(alist[1])
                    gmt_time=alist[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
                attrs=match['attrs']
                title=attrs['ptitle']
                list1={'lou':lou,'title':title,'id':id,'gmt_time':gmt_time,'content':content,'nickname':username}
                lou=lou+1
                listall_news.append(list1)
            listcount_news=res['total_found']

            return {'list':listall_news,'count':listcount_news}
#报价列表 翻页
def getpricelist(kname,frompageCount,limitNum,category_id):

    price=SPHINXCONFIG['name']['price']['name']
    serverid=SPHINXCONFIG['name']['price']['serverid']
    port=SPHINXCONFIG['name']['price']['port']
    cl = SphinxClient()
    cl.SetServer ( serverid,port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    if (category_id):
        cl.SetFilter('type_id',[int(category_id)])
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_time desc" )
    cl.SetLimits (frompageCount,limitNum,20000)
    if (kname):
        res = cl.Query ('@(title,tags) '+kname,price)
    else:
        res = cl.Query ('',price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_news=[]
            for match in tagslist:
                id=match['id']
                sql="select content,tags from price where id=%s and is_checked=1"
                #cursor.execute(sql,id)
                #alist = cursor.fetchone()
                alist=dbc.fetchonedb(sql,id)
                if alist:
                    content=subString(filter_tags(alist[0]),50)
                    tags=alist[1]
                attrs=match['attrs']
                title=attrs['ptitle']
                gmt_time=attrs['gmt_time']
                list1={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'tags':tags}
                listall_news.append(list1)
            listcount_news=res['total_found']

            return {'list':listall_news,'count':listcount_news}
#公司信息列表 翻页
def getcompanylist(kname,frompageCount,limitNum,allnum):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
    cl.SetLimits (frompageCount,limitNum,allnum)
    if (kname):
        res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
    else:
        res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_comp=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                compname=attrs['compname']
                viptype=str(attrs['membership_code'])
                domain_zz91=attrs['domain_zz91']
                address=attrs['paddress']
                membership="普通会员"
                vipflag=None
                if (viptype == '10051000'):
                    membership='普通会员'
                    vipflag=None
                if (viptype == '10051001'):
                    membership='再生通'
                    vipflag=1
                if (viptype == '1725773192'):
                    membership='银牌品牌通'
                    vipflag=1
                if (viptype == '1725773193'):
                    membership='金牌品牌通'
                    vipflag=1
                if (viptype == '1725773194'):
                    membership='钻石品牌通'
                    vipflag=1
                pbusiness=attrs['pbusiness']
                if pbusiness:
                    pbusiness=subString(filter_tags(pbusiness),500)
                parea_province=attrs['parea_province']
                productlist=getcompanyproductslist('',1,2,id,'')
                list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'address':address,'membership':membership,'viptype':viptype,'vipflag':vipflag,'domain_zz91':domain_zz91,'productlist':productlist}
                listall_comp.append(list1)
            listcount_comp=res['total_found']

            return {'list':listall_comp,'count':listcount_comp}
#关键词搜索公司
def getcompanylist_firm(kname,frompageCount,limitNum,allnum):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
    cl.SetLimits (frompageCount,limitNum,allnum)
    if (kname):
        res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
    else:
        res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_comp=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                compname=attrs['compname']
                viptype=str(attrs['membership_code'])
                domain_zz91=attrs['domain_zz91']
                address=attrs['paddress']
                service_code=attrs['service_code']
                sql1='select contact from company_account where company_id=%s'
                result1=dbc.fetchonedb(sql1,[id])
                sql2='select zst_year from company where id=%s'
                result2=dbc.fetchonedb(sql2,[id])
                sql3='select label from category where code=%s'
                result3=dbc.fetchonedb(sql3,[service_code])
                if result1:
                    contact=result1[0]
                else:
                    contact=''
                if result2:
                    zst_year=result2[0]
                if result3:
                    service=result3[0]
                membership="普通会员"
                vipflag=None
                if (viptype == '10051000'):
                    membership='普通会员'
                    vipflag=None
                if (viptype == '10051001'):
                    membership='再生通'
                    vipflag=1
                if (viptype == '1725773192'):
                    membership='银牌品牌通'
                    vipflag=1
                if (viptype == '1725773193'):
                    membership='金牌品牌通'
                    vipflag=1
                if (viptype == '1725773194'):
                    membership='钻石品牌通'
                    vipflag=1
                pbusiness=attrs['pbusiness']
                if pbusiness:
                    pbusiness=subString(filter_tags(pbusiness),500)
                parea_province=attrs['parea_province']
                productlist=getcompanyproductslist('',1,2,id,'')
                list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'address':address,'membership':membership,'viptype':viptype,'vipflag':vipflag,'domain_zz91':domain_zz91,'productlist':productlist,'contact':contact,'zst_year':zst_year,'service':service}
                listall_comp.append(list1)
            listcount_comp=res['total_found']

            return {'list':listall_comp,'count':listcount_comp}
#关键词搜索价格
def getindexcompanylist_price(kname,frompageCount,limitNum,allnum):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
    cl.SetLimits (frompageCount,limitNum,allnum)
    if (kname):
        res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
    else:
        res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_comp=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                compname=attrs['compname']
                viptype=str(attrs['membership_code'])
                domain_zz91=attrs['domain_zz91']
                address=attrs['paddress']
                sql1='select contact from company_account where company_id=%s'
                result1=dbc.fetchonedb(sql1,[id])
                sql2='select zst_year from company where id=%s'
                result2=dbc.fetchonedb(sql2,[id])
                if result1:
                    contact=result1[0]
                else:
                    contact=''
                if result2:
                    zst_year=result2[0]
                membership="普通会员"
                vipflag=None
                if (viptype == '10051000'):
                    membership='普通会员'
                    vipflag=None
                if (viptype == '10051001'):
                    membership='再生通'
                    vipflag=1
                if (viptype == '1725773192'):
                    membership='银牌品牌通'
                    vipflag=1
                if (viptype == '1725773193'):
                    membership='金牌品牌通'
                    vipflag=1
                if (viptype == '1725773194'):
                    membership='钻石品牌通'
                    vipflag=1
                pbusiness=attrs['pbusiness']
                if pbusiness:
                    pbusiness=subString(filter_tags(pbusiness),500)
                parea_province=attrs['parea_province']
                productlist=getcompanyproductslist('',1,2,id,'')
                list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'address':address,'membership':membership,'viptype':viptype,'vipflag':vipflag,'domain_zz91':domain_zz91,'productlist':productlist,'contact':contact,'zst_year':zst_year}
                listall_comp.append(list1)
            listcount_comp=res['total_found']

            return {'list':listall_comp,'count':listcount_comp}
#获得帐号
def getcompanyaccount(company_id):
    #获得缓存
    zz91cp_getcompanyaccount=cache.get("zz91cp_getcompanyaccount"+str(company_id))
    if zz91cp_getcompanyaccount:
        return zz91cp_getcompanyaccount
    sql="select account from  company_account where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if (result):
        #设置缓存
        cache.set("zz91cp_getcompanyaccount"+str(company_id),result[0],60*10)
        return result[0]
#获得互助发布者
def getpostbbsusername(account):
    sql="select contact from  company_account where account=%s"
    result=dbc.fetchonedb(sql,[account])
    if result:
        return result[0]
#获得公司ID
def getcompany_id(cname,regtime):
    #获得缓存
    zz91cp_getcompany_id=cache.get("zz91cp_getcompany_id"+str(cname))
    if zz91cp_getcompany_id:
        return zz91cp_getcompany_id
    sql="select id from company where name=%s and gmt_created=%s"
    newcode=dbc.fetchonedb(sql,[str(cname),str(regtime)])
    if (newcode == None):
        return '0'
    else:
        #设置缓存
        cache.set("zz91cp_getcompany_id"+str(cname),newcode[0],60*10)
        return newcode[0]
#获得公司名称
def getcompanyname(uname):
    #获得缓存
    zz91cp_getcompanyname=cache.get("zz91cp_getcompanyname"+str(uname))
    if zz91cp_getcompanyname:
        return zz91cp_getcompanyname
    sql="select company_id from company_account where account=%s"
    newcode=dbc.fetchonedb(sql,[uname])
    if (newcode):
        company_id=newcode[0]
        sqlc="select name from company where id=%s"
        #cursor.execute(sqlc,[company_id])
        #clist=cursor.fetchone()
        clist=dbc.fetchonedb(sqlc,[company_id])
        if clist:
            #设置缓存
            cache.set("zz91cp_getcompanyname"+str(uname),{'company_id':company_id,'companyname':clist[0]},60*10)
            return {'company_id':company_id,'companyname':clist[0]}

#公司供求信息 翻页
def getcompanyproductslist(kname,frompageCount,limitNum,company_id,pdt_type):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    if (company_id):
        cl.SetFilter('company_id',[int(company_id)])
    if (pdt_type !='' and pdt_type!=None):
        cl.SetFilter('pdt_kind',[int(pdt_type)])
    cl.SetSortMode( SPH_SORT_EXTENDED,"viptype_ldb desc,refresh_time desc" )
    cl.SetLimits (frompageCount,limitNum,200000)
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
                #list=getproductsinfo(id,cursor,kname)
                list=getproductsinfo(id,kname)
                listall.append(list)
            listcount=res['total_found']
            return {'list':listall,'count':listcount}
#供求列表页
def getsyproductslist(kname,frompageCount,limitNum,pinyin):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
    cl.SetLimits (frompageCount,limitNum,1000000)
    if (kname and kname!=""):
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
    else:
        if (pinyin):
            res = cl.Query ('@pinyin '+str(pinyin),'offersearch_new,offersearch_new_vip')
        else:
            res = cl.Query ('','offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                pdt_name=attrs['ptitle']
                list={'id':id,'pdt_name':pdt_name}
                listall.append(list)
            listcount=res['total_found']

            return {'list':listall,'count':listcount}
#供求列表页 翻页
def getproductslist(kname="",frompageCount="",limitNum="",ptype="",havepic=""):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"viptype_ldb desc,refresh_time desc" )
    cl.SetLimits (frompageCount,limitNum,1000000)
    if (ptype=='None'):
        ptype=""
    if (ptype and ptype!=""):
        cl.SetFilter('pdt_kind',[int(ptype)])
    if (havepic and havepic!=""):
        cl.SetFilterRange('havepic',1,100)
    if (kname and kname!=""):
        try:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        except:
            res = None
    else:
        res = cl.Query ('','offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                pdt_name=attrs['ptitle']
                #list=getproductsinfo(id,cursor,kname)
                list=getproductsinfo(id,kname)
                listall.append(list)
            listcount=res['total_found']
            return {'list':listall,'count':listcount}
#索引公司列表页
def getsycompanylist(kname,frompageCount,limitNum,pinyin,maxcount):
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
    cl.SetLimits (frompageCount,limitNum,maxcount)
    if (kname and kname!=""):
        res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
    else:
        if (pinyin):
            res = cl.Query ('@pinyin '+str(pinyin),'company')
        else:
            res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            i=0
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                compname=attrs['compname']
                pbusiness=filter_tags(attrs['pbusiness'][0:1000])[0:150]+'...'
                list={'id':id,'compname':compname,'business':pbusiness}
                listall.append(list)
                i+=1
            listcount=res['total_found']
            return {'list':listall,'count':listcount}
#-------------最新标签
def newtagslist(kname,num):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"search_count desc" )
    cl.SetLimits (0,num,num)
    if (kname):
        res = cl.Query ('@tname '+kname,'tagslist')
    else:
        res = cl.Query ('','tagslist')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_tags=[]
            ii=1
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                tags=attrs['tags']
                tags=tags.replace("/","")
                list1={'kname':tags,'id':id,'classid':ii,'kname_hex':tags.encode("hex")}
                listall_tags.append(list1)
                ii+=1
                if (ii>2):
                    ii=1
            return listall_tags
#索引标签库列表
def gettagslist(frompageCount,limitNum,pinyin,maxcount):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
    cl.SetLimits (frompageCount,limitNum,maxcount)
    if (pinyin):
        res = cl.Query ('@pinyin '+str(pinyin),'tagslist')
    else:
        res = cl.Query ('','tagslist')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                tags=attrs['tags']
                list={'id':id,'tags':tags,'tags_hex':tags.encode("hex")}
                listall.append(list)
            listcount=res['total_found']
            return {'list':listall,'count':listcount}
        
def getpic_address(product_id):
    #获得缓存
    zz91cp_getpic_address=cache.get("zz91cp_getpic_address"+str(product_id))
    if zz91cp_getpic_address:
        return zz91cp_getpic_address
    sql='select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc'
    #cursor.execute(sql,[product_id])
    #ldbresult=cursor.fetchone()
    ldbresult=dbc.fetchonedb(sql,[product_id])
    if ldbresult:
        #设置缓存
        cache.set("zz91cp_getpic_address"+str(product_id),ldbresult[0],60*10)
        return ldbresult[0]
#---供求列表
def getindexofferlist(kname,pdt_type,limitcount):
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED," viptype_ldb desc,refresh_time desc" )
    cl.SetLimits (0,limitcount,limitcount)
    if (pdt_type!=None):
        cl.SetFilter('pdt_kind',[int(pdt_type)])
    if (kname==None):
        res = cl.Query ('','offersearch_new,offersearch_new_vip')
    else:
        try:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new_vip,offersearch_new')
        except KeyError:
            res = cl.Query ('','offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            listall_offerlist=[]
            n=0
            for match in itemlist:
                pid=match['id']
                attrs=match['attrs']
                pdt_date=attrs['pdt_date']
                sql="select refresh_time,min_price,max_price,price_unit,price,total_quantity,quantity_unit,quantity,city,area_code from v_productsmindetail where id="+str(pid)+""
                productlist=dbc.fetchonedb(sql)
                if productlist:
                    pdt_date=productlist[0].strftime( '%-Y-%-m-%-d')
                    pdt_datem=productlist[0].strftime( '%-m/%-d')
                title=subString(attrs['ptitle'],40)
                #价格范围判断
                #价格
                allprice=""
                min_price=productlist[1]
                if (min_price==None):
                    min_price=''
                else:
                    min_price=str(min_price)
                    if (min_price!='0.0'):
                        allprice=allprice+min_price
                max_price=productlist[2]
                if (max_price==None):
                    max_price=''
                else:
                    max_price=str(max_price)
                    if (max_price!='0.0' and max_price!=min_price):
                        allprice=allprice+'-'+max_price
                price_unit=productlist[3]
                #
                if (price_unit==None):
                    price_unit=''
                else:
                    if (allprice!=''):
                        allprice=allprice+price_unit
                    else:
                        price=productlist[4]
                        if price:
                            allprice=price+price_unit
                if not allprice or str(allprice)=="0":
                    allprice="面议/电议"
                #供求数量
                total_quantity=productlist[5]
                quantity_unit=productlist[6]
                if (quantity_unit==None):
                    quantity_unit=''
                if (total_quantity=='' or total_quantity==' ' or total_quantity==None):
                    quantity=productlist[7]
                    if not quantity:
                        total_quantity=None
                    else:
                        total_quantity=quantity+quantity_unit
                else:
                    total_quantity=total_quantity+quantity_unit
                #地区
                com_province=productlist[8]
                if (com_province==None):
                    com_province=''
                area_code=productlist[9]
                #地区信息
                if (area_code):
                    sqld="select label from category where code=%s"
                    arealabel=dbc.fetchonedb(sqld,[str(area_code[:-4])])
                    if arealabel:
                        if arealabel[0]:
                            com_province=arealabel[0]+' '+com_province
                
                productspic=getpic_address(pid)
                if productspic:
                    pdt_images=productspic
                else:
                    pdt_images=""
                if (pdt_images == '' or pdt_images == '0'):
                    pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                else:
                    pdt_images='http://img3.zz91.com/250x250/'+pdt_images+''
                n=n+1
                list={'id':pid,'title':title,'gmt_time':pdt_date,'gmt_time_m':pdt_datem,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images,'num':n,'price':allprice,'total_quantity':total_quantity,'com_province':com_province}
                listall_offerlist.append(list)
            return listall_offerlist

#获得中文首拼音
def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:        
        ord(str1)
        return str1
    except:
        asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''
def getofferprice(id):
    #获得缓存
    zz91cp_getofferprice=cache.get("zz91cp_getofferprice"+str(id))
    if zz91cp_getofferprice:
        return zz91cp_getofferprice
    sql="select p.min_price,p.max_price,p.price_unit from products as p where p.id=%s"
    #cursor.execute(sql,[id])
    #plist = cursor.fetchone()
    plist=dbc.fetchonedb(sql,[id])
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
        #设置缓存
        cache.set("zz91cp_getofferprice"+str(id),allprice,60*10)
        return allprice
    
#---公司库首页有图片的最新供求列表
def getindexofferlist_pic(kname="",pdt_type="",limitcount="",membertype=""):
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,limitcount,limitcount)
    if (pdt_type):
        cl.SetFilter('pdt_kind',[int(pdt_type)])
    cl.SetFilterRange('havepic',1,100)
    #cl.SetFilterRange('haveprice',2,1000)
    if membertype:
        searchindex="offersearch_new_vip"
        cl.SetFilterRange('length_price',1,100000)
    else:
        searchindex="offersearch_new,offersearch_new_vip"
    cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
    if not kname:
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
                company_id=attrs['company_id']
                companyname=''
                sql="select name from company where id=%s"
                result=dbc.fetchonedb(sql,[company_id])
                if result:
                    companyname=result[0]
                #获取产品标签列表
                tags=''
                sql="select tags from products where id=%s"
                result=dbc.fetchonedb(sql,[pid])
                if result:
                    tags=result[0]
                alltags=''
                if tags:
                    tagslist=tags.split(",")
                    alltags=[]
                    for ts in tagslist:
                        if len(ts)<=16:
                            tlist={'tags':ts,'tags_hex':getjiami(ts)}
                            alltags.append(tlist)
                kindtxt=''
                if (pdt_kind==1):
                    kindtxt="求购"
                else:
                    kindtxt="供应"
                title=subString(attrs['ptitle'],100)
                sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc"
                productspic=dbc.fetchonedb(sql1,[pid])
                if productspic:
                    pdt_images=productspic[0]
                else:
                    pdt_images=""
                if (pdt_images == '' or pdt_images == '0'):
                    pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                else:
                    pdt_images='http://img3.zz91.com/220x165/'+pdt_images+''
                list={'id':pid,'title':title,'gmt_time':pdt_date,'kindtxt':kindtxt,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images,'price':price,'companyname':companyname,'alltags':alltags,'company_id':company_id}
                listall_offerlist.append(list)
            return listall_offerlist

#最新加入高会            
def getcompanyindexcomplist(kname,num):
    #-------------供求列表
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
    cl.SetLimits (0,num,num)
    #cl.SetFilter('apply_status',[1])

    #nowdate=date.today()-timedelta(days=900)
    #nextday=date.today()+timedelta(days=1)
    #formatnowdate=time.mktime(nowdate.timetuple())
    #formatnextday=time.mktime(nextday.timetuple())
    #cl.SetFilterRange('gmt_start',int(formatnowdate),int(formatnextday))
    listall_company=[]
    if (kname):
        res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
    else:
        res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            i=0
            for match in itemlist:
                id=match['id']
                attrs=match['attrs']
                comname=attrs['compname']
                industry_code=attrs['industry_code']
                industry=''
                if industry_code and str(industry_code)!="0":
                    if INDUSTRY_LABEL.has_key(str(industry_code)):
                        industry=INDUSTRY_LABEL[str(industry_code)]
                
                business=filter_tags(attrs['pbusiness'])
                business100=subString(business,150)
                area_province=attrs['parea_province']
                domain_zz91=attrs['domain_zz91']
                num=i % 2
                i=i+1
                
                if num==0:
                    n=1
                if num==1:
                    n=2
                #来电宝客户
                company_id=id
                if company_id:
                    sqll="select id from crm_company_service where company_id=%s and crm_service_code in(1007,1008,1009,1010,1011) and apply_status=1"
                    ldbresult=dbc.fetchonedb(sqll,[company_id])
                    if ldbresult:
                        ldbflag=1
                    else:
                        ldbflag=None
                    contact=''
                    sqlc="select contact,sex from company_account where company_id=%s"
                    resultc=dbc.fetchonedb(sqlc,[company_id])
                    if resultc:
                        contact=resultc[0]
                if domain_zz91:
                    domain_zz91=domain_zz91.strip()
                if domain_zz91=="":
                    url="http://company.zz91.com/compinfo"+str(id)+".htm"
                    url_contact="http://company.zz91.com/compinfo"+str(id)+".htm"
                    url_quesion="http://company.zz91.com/compinfo"+str(id)+".htm"
                else:
                    url="http://"+domain_zz91+".zz91.com"
                    url_contact="http://"+str(domain_zz91)+".zz91.com/lxfs.htm"
                    url_quesion="http://"+str(domain_zz91)+".zz91.com/zxly.htm"
                if ldbflag==1:
                    url="http://www.zz91.com/ppc/index"+str(id)+".htm"
                    url_contact="http://www.zz91.com/ppc/contact"+str(id)+".htm"
                    url_quesion="http://www.zz91.com/ppc/contact"+str(id)+".htm"
                
                list={'id':id,'comname':comname,'business':business,'industry':industry,'area_province':area_province,'domain_zz91':domain_zz91,'business100':business100,'url':url,'url_contact':url_contact,'url_quesion':url_quesion,'num':n,'contact':contact}
                listall_company.append(list)
    return listall_company
def getvipcompanycount():
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
    cl.SetLimits (0,1,1)
    cl.SetFilter('apply_status',[1])
    res = cl.Query ('','company')
    if res:
        listcount=res['total_found']
    return listcount
    
#获得公司的一张供求图片信息
def getoneproductscompany(company_id):  
    #获得缓存
    zz91cp_getoneproductscompany=cache.get("zz91cp_getoneproductscompany"+str(company_id))
    if zz91cp_getoneproductscompany:
        return zz91cp_getoneproductscompany  
    sql="select a.pic_address,b.title from products_pic as a left join products as b on a.product_id=b.id where b.company_id=%s and a.check_status=1 order by a.is_default desc limit 0,1"
    #cursor.execute(sql,[company_id])
    #productspic = cursor.fetchone()
    productspic=dbc.fetchonedb(sql,[company_id])
    pdt_title=""
    if productspic:
        pdt_images=productspic[0]
        pdt_title=productspic[1]
    else:
        pdt_images=""
    if (pdt_images == '' or pdt_images == '0'):
        pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
    else:
        pdt_images='http://img3.zz91.com/220x165/'+pdt_images+''
        #设置缓存
    cache.set("zz91cp_getoneproductscompany"+str(company_id),{'pdt_images':pdt_images,'pdt_title':pdt_title},60*10)
    return {'pdt_images':pdt_images,'pdt_title':pdt_title}
#获得公司主营业务
def getcompanybusiness(company_id):
    #获得缓存
    zz91cp_getcompanybusiness=cache.get("zz91cp_getcompanybusiness"+str(company_id))
    if zz91cp_getcompanybusiness:
        return zz91cp_getcompanybusiness  
    sql="select business from company where id=%s"
    #cursor.execute(sql,[company_id])
    #comp = cursor.fetchone()
    comp=dbc.fetchonedb(sql,[company_id])
    if comp:
        #设置缓存
        cache.set("zz91cp_getcompanybusiness"+str(company_id),comp[0],60*10)
        return comp[0]
#是否来电宝客户
def isldb(company_id):
    sqlg="select front_tel from phone where company_id=%s and expire_flag=0"
    #cursor.execute(sqlg,company_id)
    #phoneresult=cursor.fetchone()
    phoneresult=dbc.fetchonedb(sqlg,company_id)
    if phoneresult:
        return 1
    else:
        return None
#最新加入高会(含供求图片)            
def getindexcompanylist_pic(keywords="",num="",frompageCount="",limitNum="",pdt_kind='',nopic=''):
    #-------------供求列表
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED," viptype desc, refresh_time desc" )
    cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
    cl.SetFilterRange('havepic',1,100)
    if not nopic:
        cl.SetFilterRange('viptype',1,100)
    if pdt_kind:
        cl.SetFilter('pdt_kind',[int(pdt_kind)])
    if (num):
        cl.SetLimits (0,num,num)
    else:
        cl.SetLimits (frompageCount,limitNum,20000)
        
    if (keywords):
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_new,offersearch_new_vip')
    else:
        res = cl.Query ('','offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            listall_company=[]
            for match in itemlist:
                id=match['id']
                attrs=match['attrs']
                company_id=attrs['company_id']
                business=getcompanybusiness(company_id)
                #list=getproductsinfo(id,cursor,keywords)
                list=getproductsinfo(id,keywords)
                list['business']=business
                pdt_images=list['pdt_images']
                pdt_images=pdt_images.replace('122x93','200x169')
                list['pdt_images']=pdt_images
                ldbflag=isldb(company_id)
                list['ldbflag']=ldbflag
                listall_company.append(list)
            listcount=res['total_found']
            return {'list':listall_company,'listcount':listcount}

#最新加入普会
def getcommoncompanylist(keywords="",num="",frompageCount="",limitNum="",pic="",companyflag=""):
    #-------------供求列表
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"viptype_ldb desc, refresh_time desc" )
    #判断是否公司分组
    if (companyflag):
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
    if pic:
        cl.SetFilterRange('havepic',1,100)
    cl.SetFilter('viptype',[0])
    if (num):
        cl.SetLimits (0,num,num)
    else:
        cl.SetLimits (frompageCount,limitNum,20000)
        
    if (keywords):
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_new')
    else:
        res = cl.Query ('','offersearch_new')
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            listall_company=[]
            for match in itemlist:
                id=match['id']
                attrs=match['attrs']
                company_id=attrs['company_id']
                business=getcompanybusiness(company_id)
                #list=getproductsinfo(id,cursor,keywords)
                list=getproductsinfo(id,keywords)
                list['business']=business
                #pdt_images=list['pdt_images']
                #pdt_images=pdt_images.replace('width=122&height=93','width=200&height=169')
                #list['pdt_images']=pdt_images
                ldbflag=isldb(company_id)
                list['ldbflag']=ldbflag
                listall_company.append(list)
            listcount=res['total_found']
            return {'list':listall_company,'listcount':listcount}
#微信绑定客户
def getweixincomplist(frompageCount="",limitNum=""):
    #获得缓存
    zz91cp_getweixincomplist=cache.get("zz91cp_getweixincomplist")
    if zz91cp_getweixincomplist:
        return zz91cp_getweixincomplist 
    sqlc="select count(0) from oauth_access as c where c.open_type='weixin.qq.com' and exists(select a.company_id from company_account as a left join products as b on a.company_id=b.company_id where b.check_status=1 and c.target_account=a.account)"
    #cursor.execute(sqlc)
    #listcount = cursor.fetchone()[0]
    listcount=dbc.fetchnumberdb(sqlc)
    #sql="select username from auth_user where exists(select target_account from oauth_access where target_account=auth_user.username) and exists(select account from products where account=auth_user.username) limit "+str(frompageCount)+","+str(frompageCount+limitNum)+""
    sql="select c.target_account from oauth_access as c where c.open_type='weixin.qq.com' and exists(select a.company_id from company_account as a left join products as b on a.company_id=b.company_id where b.check_status=1 and c.target_account=a.account) order by c.gmt_created desc limit "+str(frompageCount)+","+str(limitNum)+""
    #cursor.execute(sql)
    #alist=cursor.fetchall()
    alist=dbc.fetchalldb(sql)
    listall=[]
    if alist:
        for list in alist:
            sqlc="select company_id from company_account where account=%s"
            #cursor.execute(sqlc,[list[0]])
            #clist = cursor.fetchone()
            clist=dbc.fetchonedb(sqlc,[list[0]])
            if clist:
                company_id=clist[0]
                sqlp="select id,company_id from products where company_id=%s and check_status=1 order by refresh_time desc limit 0,1"
                #cursor.execute(sqlp,[company_id])
                #aalist = cursor.fetchone()
                aalist=dbc.fetchonedb(sqlp,[company_id])
                if aalist:
                    id=aalist[0]
                    company_id=aalist[1]
                    business=getcompanybusiness(company_id)
                    keywords=None
                    #list=getproductsinfo(id,cursor,keywords)
                    list=getproductsinfo(id,keywords)
                    list['business']=business
                    list['businessmini']=subString(business,10)
                    pdt_images=list['pdt_images']
                    pdt_images=pdt_images.replace('122x93','210x205')
                    list['pdt_images']=pdt_images
                    ldbflag=isldb(company_id)
                    list['ldbflag']=ldbflag
                    listall.append(list)
            
            
    #设置缓存
    cache.set("zz91cp_getweixincomplist",{'list':listall,'listcount':listcount},60*10)               
    return {'list':listall,'listcount':listcount}            
#根据拼音获得导航属性
def getpingyinattribute(pingyin):
    #获得缓存
    zz91cp_getpingyinattribute=cache.get("zz91cp_getpingyinattribute"+str(pingyin))
    zz91cp_getpingyinattribute=None
    if zz91cp_getpingyinattribute:
        return zz91cp_getpingyinattribute 
    sql="select label,templates,keywords,keywords1,num_str,keywords2,keywords3,sid,id from daohang where pingyin=%s"
    daohanglist=dbc.fetchonedb(sql,[pingyin])
    list=None
    if (daohanglist):
        label=daohanglist[0]
        keywords=daohanglist[2]
        keywords1=daohanglist[3]
        keywords2=daohanglist[5]
        keywords3=daohanglist[6]
        num_str=daohanglist[4]
        sid=daohanglist[7]
        id=daohanglist[8]
        label=label.replace("价格","")
        if (keywords=='' or keywords==None):
            keywords=label
        if (keywords1=='' or keywords1==None):
            keywords1=label
        if (keywords2=='' or keywords2==None):
            keywords2=label
        if (keywords3=='' or keywords3==None):
            keywords3=label
        keywords=keywords.replace("价格","")
        keywords=keywords.replace("行情","")
        keywords=keywords.replace("求购","")
        keywords=keywords.replace("采购","")
        keywords=keywords.replace("回收","")
        keywords=keywords.replace("供应","")
        keywords=keywords.replace("出售","")
        keywords1=keywords1.replace("价格","")
        keywords2=keywords2.replace("价格","")
        keywords3=keywords3.replace("价格","")
        adkeywords=urlquote(keywords)
        sqlp="update daohang set showcount=showcount+1 where id=%s"
        dbc.updatetodb(sqlp,[id])
        list={'id':id,'label':label,'keywords':keywords,'keywords1':keywords1,'keywords2':keywords2,'keywords3':keywords3}
    #设置缓存
    cache.set("zz91cp_getpingyinattribute"+str(pingyin),list,60*10)         
    return list
def getcategoryname(code):
    #获得缓存
    zz91cp_getcategoryname=cache.get("zz91cp_getcategoryname"+str(code))
    if zz91cp_getcategoryname:
        return zz91cp_getcategoryname 
    sql="select label from category where code=%s"
    #cursor.execute(sql,[code])
    #resultlist=cursor.fetchone()
    resultlist=dbc.fetchonedb(sql,[code])
    if resultlist:
        #设置缓存
        cache.set("zz91cp_getcategoryname"+str(code),resultlist[0],60*10)         
        return resultlist[0]
#老站相关
def getoldnewslist(kname=""):
    #获得缓存
    zz91cp_getoldnewslist=cache.get("zz91cp_getoldnewslist"+str(kname))
    if zz91cp_getoldnewslist:
        return zz91cp_getoldnewslist 
    sql="select title,content,tags,post_time,visited_count,old_news_id from news_list order by post_time desc limit 0,10"
    #cursor.execute(sql)
    #oldlist = cursor.fetchall()
    oldlist=dbc.fetchalldb(sql)
    if oldlist:
        listall=[]
        for nlist in oldlist:
            list={'title':nlist[0],'content':nlist[1],'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4],'old_news_id':nlist[5]}
            listall.append(list)
        #设置缓存
        cache.set("zz91cp_getoldnewslist"+str(kname),listall,60*10)     
        return listall

#老站资讯详细内容
def getnewsdetail(newsid="",newszd=""):
    #获得缓存
    zz91cp_getnewsdetail=cache.get("zz91cp_getnewsdetail"+str(newsid)+str(newszd))
    if zz91cp_getnewsdetail:
        return zz91cp_getnewsdetail 
    tags=None
    list=None
    sql="select title,content,tags,post_time,visited_count from news_list where "+newszd+"=%s"
    #cursor.execute(sql,[newsid])
    #nlist = cursor.fetchone()
    nlist=dbc.fetchonedb(sql,[newsid])
    if nlist:
        tags=nlist[2]
        if (tags and tags!=""):
            tags=tags.replace(",","|")
        content=nlist[1]
        content=replacepic(content)
        list={'title':nlist[0],'content':content,'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4]}
        
    else:
        sql="select title,content,tags,post_time,visited_count,check_status from bbs_post where "+newszd+"=%s and check_status=1"
        #cursor.execute(sql,[newsid])
        #nlist = cursor.fetchone()
        nlist=dbc.fetchonedb(sql,[newsid])
        if nlist:
            tags=nlist[2]
            content=nlist[1]
            content=replacepic(content)
            checkStatus=nlist[5]
            if (checkStatus and checkStatus=='1'):
                checkStatus='1';
            else:
                checkStatus=None;
            if (tags and tags!=""):
                tags=tags.replace(",","|")
            list={'title':nlist[0],'content':content,'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4],'check_status':checkStatus}
        else:
            sql="select title,content,tags,post_time,visited_count,check_status from bbs_post where id=%s and check_status=1"
            #cursor.execute(sql,[newsid])
            #nlist = cursor.fetchone()
            nlist=dbc.fetchonedb(sql,[newsid])
            if nlist:
                content=nlist[1]
                content=replacepic(content)
                checkStatus=nlist[5]
                if (checkStatus and checkStatus=='1'):
                    checkStatus='1';
                else:
                    checkStatus=None;
                list={'title':nlist[0],'content':content,'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4],'check_status':checkStatus}
                tags=nlist[2]
                if (tags and tags!=""):
                    tags=tags.replace(",","|")
    #设置缓存
    cache.set("zz91cp_getnewsdetail"+str(newsid)+str(newszd),{'list':list,'tags':tags},60*10)                
    return {'list':list,'tags':tags}
#新闻栏目
def getlbhex():
    lb="国内资讯,国外资讯,市场动态,商务交流,焦点关注,行情综述,废料百科,热门评论,再生技术"
    lb_hex="国内,国外,市场动态,商务|交流,焦点关注,行情综述,百科,评论,再生技术"
    alllist=[]
    lbarr=lb.split(",")
    lbarr_hex=lb_hex.split(",")
    i=0
    for a in lbarr:
        list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
        alllist.append(list)
        i=i+1
    return alllist
#优质客户推荐栏目            
def gettjhex1():
    lb="钢铁,稀有金属,贵金属,有色金属,金属混合\复合料,废金属处理设备,金属助剂"
    lb_hex="钢铁,稀有金属,贵金属,有色金属,金属混合|复合料,废金属处理设备,金属助剂"
    alllist=[]
    lbarr=lb.split(",")
    lbarr_hex=lb_hex.split(",")
    i=0
    for a in lbarr:
        list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
        alllist.append(list)
        i=i+1
    return alllist
def gettjhex2():
    lb="通用废塑料,工程废塑料,塑料颗粒,特种废塑料,塑料混合/复合料,废塑料处理设备,塑料助剂"
    lb_hex="通用废塑料,工程废塑料,塑料颗粒,特种废塑料,塑料混合|复合料,废塑料处理设备,塑料助剂"
    alllist=[]
    lbarr=lb.split(",")
    lbarr_hex=lb_hex.split(",")
    i=0
    for a in lbarr:
        list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
        alllist.append(list)
        i=i+1
    return alllist
def gettjhex3():
    lb="废纺织品,废纸,二手设备,废电子电器,废橡胶,废轮胎,服务"
    lb_hex="纺织品,废纸,设备,电子电器,橡胶,轮胎,服务"
    alllist=[]
    lbarr=lb.split(",")
    lbarr_hex=lb_hex.split(",")
    i=0
    for a in lbarr:
        list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
        alllist.append(list)
        i=i+1
    return alllist
#微门户关键词
def getcplist(keywords,limitcount):
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"showcount desc" )
    cl.SetLimits (0,limitcount,limitcount)
    keywords=''
    if keywords=='':
        res = cl.Query ('','daohangkeywords')
    else:
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
                if pingyin!="":
                    list={'label':label,'pingyin':pingyin}
                    listall.append(list)
    if listall==[]:
        res = cl.Query ('','daohangkeywords')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    label=attrs['plabel']
                    pingyin=attrs['ppinyin']
                    if pingyin!="":
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
    return listall
#获取竞价排名客户信息
def getjingjialist(keywords='',limitcount='',mycompany_id=''):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetGroupBy( 'product_id',SPH_GROUPBY_ATTR )
    cl.SetFilter('checked',[1])
    if (limitcount):
        cl.SetLimits (0,limitcount,limitcount)
    res=''
    if not mycompany_id:
        mycompany_id=0
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
                    
                    prolist=getproductsinfo(product_id,keywords)
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
                            t=random.randrange(0,1000000)
                            hiturl=getjiami(str(t)+str(gmt_modified)+keywords)
                            sql="insert into app_jingjia_search(keywords,company_id,sourcetype,userid,user_company_id,key_id,showcount,gmt_modified,gmt_created,hiturl,pdt_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            result=dbc.updatetodb(sql,[keywords,company_id,sourcetype,userid,user_company_id,key_id,showcount,gmt_modified,gmt_created,hiturl,product_id])
                            if result:
                                prolist['search_id']=result[0]
                            prolist['hiturl']=hiturl
                            price=attrs['price']
                            listall.append(prolist)
            return listall
#资讯
#----新闻列表 翻页
def getnewslist(keywords="",frompageCount="",limitNum="",typeid="",allnum="",typeid2="",contentflag="",cursornews="",searchmode=1):
    port = spconfig['port']
    cl = SphinxClient()
    
    news=spconfig['name']['news']['name']
    serverid=spconfig['name']['news']['serverid']
    port=spconfig['name']['news']['port']
    cl.SetServer ( serverid, port )
    if searchmode==1:
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
    else:
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,id desc" )
    if (typeid and typeid!=[0]):
        cl.SetFilter('typeid',typeid)
    if (typeid2):
        cl.SetFilter('typeid2',[typeid2])
    if (allnum):
        cl.SetLimits (frompageCount,limitNum,allnum)
    else:
        cl.SetLimits (frompageCount,limitNum)
    if (keywords):
        if "p" == keywords:
            res = cl.Query ('@(flag) '+keywords,'news')
        else:
            res = cl.Query ('@(title,keywords) '+keywords,'news')
    else:
        res = cl.Query ('','news')
    listall_news=[]
    listcount_news=0
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            for match in tagslist:
                id=match['id']
                newsurl=get_newstype(id)
                attrs=match['attrs']
                weburl="http://news.zz91.com"
                if newsurl:
                    if newsurl["url2"]:
                        weburl+="/"+newsurl["url2"]
                    weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                mobileweburl="http://m.zz91.com/news/newsdetail"+str(id)+".htm?type=news"
                title=filter_tags(attrs['ptitle'])
                title10=subString(title.decode('utf-8'),80)
                pubdate=attrs['pubdate']
                timeArray = time.localtime(pubdate)  
                pubdate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                if not contentflag:
                    content=getnewscontent(id)['content']
                else:
                    content=""
                havepic=havepicflag(content)
                littlecontent=subString(filter_tags(content),300)
                littlecontent=littlecontent.replace('\n','').replace('\r','')
                littlecontent=littlecontent.replace('　','').rstrip()
                list1={'title':title,'title10':title10,'id':id,'pubdate':pubdate,'littlecontent':littlecontent,'content':content,'havepic':havepic,'newsurl':newsurl,'weburl':weburl,'mobileweburl':mobileweburl}
                listall_news.append(list1)
            listcount_news=res['total_found']
    return {'list':listall_news,'count':listcount_news}
#新闻内容
def getnewscontent(id):
    newscontent=cache.get("cp_newscontent"+str(id))
    newscontent=None
    if (newscontent==None):
        sqlt="select title,pubdate,click from dede_archives where id=%s"
        alist=dbn.fetchonedb(sqlt,[id])
        title=""
        pubdate=""
        click=""
        if alist:
            title=alist[0]
            pubdate=''
            if alist[1]:
                timeArray = time.localtime(alist[1])  
                pubdate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            click=alist[2]
        sql="select body from dede_addonarticle where aid=%s"
        alist=dbn.fetchonedb(sql,[id])
        content=""
        if alist:
            content=alist[0]
            content=replacepic(content)
        newscontent={'title':title,'pubdate':pubdate,'content':content,'click':click}
        cache.set("cp_newscontent"+str(id),newscontent,60*60)
    return newscontent
#----获取最终页当前新闻栏目(一期)
def get_newstype(id):
    sql='select typeid,typeid2 from dede_archives where id=%s'
    result=dbn.fetchonedb(sql,[id])
    if result:
        typeid=result[0]
        typeid2=result[1]
        sql2='select typename,keywords from dede_arctype where id=%s'
        result2=dbn.fetchonedb(sql2,[typeid])
        if result2:
            list={'typename':result2[0],'url':result2[1],'typeid':typeid,'typeid2':typeid2,'url2':''}
            if typeid2!='0':
                sql3='select keywords from dede_arctype where id=%s'
                result3=dbn.fetchonedb(sql3,[typeid2])
                if result3:
                    list['url2']=result3[0]
            return list
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
    if "乙醚" in s:
        return 2
    return None
#获得经营模式
def getbusiness_mod(code):
    sql='select label,code from category where parent_code=%s'
    result=dbc.fetchalldb(sql,[code])
    business_mod=[]
    for list in result:
        dict={'label':list[0],'code':list[1]}
        business_mod.append(dict)
    return business_mod
#获得行业类别
def getindustry_label(code):
    sql='select label,code from category where parent_code=%s'
    result=dbc.fetchalldb(sql,[code])
    industry_label=[]
    for list in result:
        dict={'label':list[0],'code':list[1]}
        industry_label.append(dict)
    return industry_label
#微门户首页类
class weimenhu:
    def __init__(self):
        self.dbc=dbc
    def getnewandhot(self):
        newest=[]
        hot=[]
        #获得最新微门户
        sql1='select id ,label,pingyin from daohang order by id desc limit 0,8'
        resultlist1=self.dbc.fetchalldb(sql1)
        for result in resultlist1:
            id1=result[0]
            label=result[1]
            pingyin=result[2]
            list={'id1':id1,'label':label,'pingyin':pingyin}
            newest.append(list)
        #获得热门搜索
        sql2='select id ,label,pingyin, showcount from daohang order by showcount desc limit 0,10'
        resultlist2=self.dbc.fetchalldb(sql2)
        for result in resultlist2:
            id2=result[0]
            label=result[1]
            pingyin=result[2]
            showcount=result[3]
            pdt_images="http://img0.zz91.com/front/images/global/noimage.gif"
            offerpic=getindexofferlist_pic(kname=label,limitcount=1)
            picaddress=''
            if offerpic:
                for plist in offerpic:
                    picaddress=plist['pdt_images']
            list={'id2':id2,'label':label,'pingyin':pingyin,'showcount':showcount,'picaddress':picaddress}
            hot.append(list)
        return {"newest":newest,"hot":hot}
    def getcomplist(self):
        #-------------供求列表
        port = settings.SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
        cl.SetLimits (0,300)
        cl.SetFilter('apply_status',[1])
        nowdate=date.today()-timedelta(days=90)
        nextday=date.today()+timedelta(days=1)
        formatnowdate=time.mktime(nowdate.timetuple())
        formatnextday=time.mktime(nextday.timetuple())
        cl.SetFilterRange('gmt_start',int(formatnowdate),int(formatnextday))
        
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
                    list={'id':id,'comname':comname,'business':business,'area_province':area_province,'domain_zz91':domain_zz91}
                    listall_company.append(list)
                return listall_company    
    def subString(self,string,length): 
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
            
    def getpricelist_daohang(self,kname="",assist_type_id="",limitcount="",searchname="",titlelen="",hangqing=""):
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
                    title=self.subString(attrs['ptitle'],titlelen)
    #                title=getlightkeywords(cl,[title],kname,"price")
                    gmt_time=attrs['gmt_time']
                    #td_time=gmt_time.strftime('%Y-%m-%d')
                    list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle']}
                    listall_baojia.append(list1)
                listcount_baojia=res['total_found']
                return listall_baojia 
    #左右分           
    def leftandright(self,all=''):  
        left=[]
        right=[]     
        count=0
        if all:
            for i in all:
                if count <4:
                    left.append(i)
                    count+=1
                if count>=4 and count<8:
                    right.append(i)
                    count+=1
        return {'left':left,'right':right}
    #获得最终类
    def getlastcategory(self,category_code=""):
        listall=[]
        sql="select id ,title ,pinyin from data_index where category_code=%s"
        resultlist=self.dbc.fetchalldb(sql,[category_code])
        if resultlist:
            for result in resultlist:
                id=result[0]
                title=result[1]
                pinyin=result[2]
                if pinyin:
                    pinyin=pinyin.lower()
                list={'id':id,'title':title,'pinyin':pinyin}
                listall.append(list)
        return listall
    def getdaohanglist(self,category_code):
        catelist=cache.get("price_daohanglist"+str(category_code))
        #catelist=None
        if catelist:
            return catelist
        sql='select title,link from data_index where category_code=%s order by sort asc,gmt_created asc'
        resultlist=self.dbc.fetchalldb(sql,[category_code])
        listall=[]
        numb=0
        for result in resultlist:
            numb+=1
            listall.append({'title':result[0],'link':result[1],'numb':numb})
        if listall:
            cache.set("price_daohanglist"+str(category_code),listall,60*20)
        return listall
