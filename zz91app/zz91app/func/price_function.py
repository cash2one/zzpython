#-*- coding:utf-8 -*-

class zprice:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getprice_clist(self,parent_id):
        #获得缓存
        zz91app_getprice_clist=cache.get("zz91app_getprice_clist"+str(parent_id))
        if zz91app_getprice_clist:
            return zz91app_getprice_clist
        sql='select name,id from price_category where parent_id=%s and showflag=1'
        resultlist=self.dbc.fetchalldb(sql,[parent_id])
        listall=[]
        for result in resultlist:
            list={'name':result[0],'id':result[1]}
            listall.append(list)
        #设置缓存
        cache.set("zz91app_getprice_clist"+str(parent_id),listall,60*5)
        return listall
    def getcategory_label(self,category_id):
        #获得缓存
        zz91app_getcategory_label=cache.get("zz91app_getcategory_label"+str(category_id))
        if zz91app_getcategory_label:
            return zz91app_getcategory_label
        sql='select name from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[category_id])
        if result:
            #设置缓存
            cache.set("zz91app_getcategory_label"+str(category_id),result[0],60*5)
            return result[0]
    def parent_id(self,id):
        #获得缓存
        zz91app_parent_id=cache.get("zz91app_parent_id"+str(id))
        if zz91app_parent_id:
            return zz91app_parent_id
        sql='select parent_id from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            #设置缓存
            cache.set("zz91app_parent_id"+str(id),result[0],60*5)
            return result[0]
    #----报价列表 页
    def getpricelist(self,keywords="",frompageCount="",limitNum="",category_id="",allnum="",assist_type_id="",arg=""):
        price=spconfig['name']['price']['name']
        serverid=spconfig['name']['price']['serverid']
        port=spconfig['name']['price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if arg==1:
            if category_id and category_id!="undefined":
                cl.SetFilter('type_id',category_id,False)
            if assist_type_id:
                cl.SetFilter('assist_type_id',assist_type_id,True)
        elif arg==2:
            if category_id and category_id!="undefined" and category_id!="[]":
                cl.SetFilter('type_id',category_id,True)
            if assist_type_id:
                cl.SetFilter('assist_type_id',assist_type_id,False)
        else:
            if category_id and str(category_id)!="undefined":
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
    def getpricefield(self,priceid):
        catelist=cache.get("price_fieldid"+str(priceid))
        if catelist:
            return catelist
        sql='select DISTINCT filed,name from price_titlefild where priceid=%s order by id asc'
        resultlist=self.dbc.fetchalldb(sql,[priceid])
        listname=[]
        listfield=[]
        for result in resultlist:
            name=result[1]
            #if name:
                #name=name.upper()
            filed=result[0]
            listname.append(name)
            listfield.append(filed)
#            list={'name':name,'filed':filed}
#            listall.append(list)
        listdir={'listname':listname,'listfield':listfield}
        if listname and listfield:
            cache.set("price_field"+str(priceid),listdir,60*20)
        return listdir
    def getpricefield2(self,categoryid="",assist_type_id="",priceid=""):
        catelist=cache.get("price_field"+str(categoryid)+str(assist_type_id))
        if catelist:
            return catelist
        sql='select DISTINCT field,name from price_category_field where price_category_id=%s and assist_type_id=%s order by id asc'
        resultlist=self.dbc.fetchalldb(sql,[categoryid,assist_type_id])
        if resultlist:
            listname=[]
            listfield=[]
            for result in resultlist:
                name=result[1]
                #if name:
                    #name=name.upper()
                field=result[0]
                listname.append(name)
                listfield.append(field)
            listdir={'listname':listname,'listfield':listfield}
            if listname and listfield:
                cache.set("price_field2"+str(categoryid)+str(assist_type_id),listdir,60*20)
                return listdir
        else:
            return self.getpricefield(priceid)
    #行情研究院
    def getpricedblist(self,frompageCount='',limitNum='',typeid='',assist_type_id=''):
        #获得缓存
        #zz91price_getpricedblist=cache.get("zz91price_getpricedblist"+str(typeid)+str(assist_type_id))+str(frompageCount)+str(limitNum)
        #if zz91price_getpricedblist:
            #return zz91price_getpricedblist 
        sqlarg=''
        argument=[]
        if typeid:
            sqlarg+=' and a.type_id in ('+str(typeid)+')'
            #argument.append(typeid)
        if assist_type_id:
            sqlarg+=' and a.assist_type_id=%s'
            argument.append(assist_type_id)
        sql1='select count(0) from price as a where id>0'+sqlarg
        sql='select a.id,a.title,a.content,a.type_id,b.pinyin,a.gmt_order from price as a left join price_category as b on a.type_id=b.id where a.id>0'+sqlarg
        sql+=' order by a.gmt_order desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            td_id=result[0]
            url='/detail/'+str(td_id)+'.html'
            ptitle=result[1]
            content=result[2]
            type_id=result[3]
            urlpath=result[4]
            gmt_order=formattime(result[5],1)
            content=filter_tags(content).replace(' ','')
            pcontent=subString(content,150)
            imgurl=get_img_url(result[2])
            pic=''
            if imgurl:
                pic=imgurl[0]
            if not pic:
                pic='http://img0.zz91.com/front/images/global/noimage.gif'
            list={'td_id':td_id,'url':url,'td_title':ptitle,'content':pcontent,'pic':pic,'urlpath':urlpath,'gmt_order':gmt_order}
            listall.append(list)
        #设置缓存
        #cache.set("zz91price_getpricedblist"+str(typeid)+str(assist_type_id)+str(frompageCount)+str(limitNum),{'list':listall,'count':count},60*10)
        return {'list':listall,'count':count}
    #行情研究院最终页
    def getpricedetail(self,id):
        sql='select title,content,gmt_order from price where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            content=result[1]
            gmt_order=formattime(result[2],1)
            return {'title':result[0],'content':result[1],'gmt_order':gmt_order}
    #----最终页price_list数据
    def getdetailpricelist(self,priceid,listfield,fromdata="",todate=""):
        #获得缓存
        #zz91price_getdetailpricelist=cache.get("zz91price_getdetailpricelist"+str(priceid)+str(listfield))
        #if zz91price_getdetailpricelist:
            #return zz91price_getdetailpricelist 
        listall=[]
        if len(listfield)>1:
            listfield2=','.join(listfield)
            sqlarg='id,postdate,label,label1,spec,type_id,assist_type_id,'+listfield2
            sql2='select '+sqlarg+' from price_list where priceid=%s'
            if fromdata:
                sql2+=' and postdate>=%s'
            if todate:
                sql2+=' and postdate<=%s'
            sql2+=' group by num'
            resultlist2=self.dbc.fetchalldb(sql2,[priceid])
            for result2 in resultlist2:
                id=result2[0]
                postdate=formattime(result2[1],1)
                label=result2[2]
                label1=result2[3]
                spec=result2[4]
                if spec:
                    spec=spec.replace("　","")
                type_id=result2[5]
                assist_type_id=result2[6]
                listvalue=[]
                list={}
                num=6
                curl='/chart/'+str(id)+'.html'
                for ltfied in listfield:
                    num+=1
                    
                    fidvalue=result2[num]
                    proname=label
                    #废铜
                    if type_id in [40]:
                        if ltfied=="label":
                            proname=fidvalue
                            if spec:
                                fidvalue=result2[num]+"("+str(spec)+")"
                                proname=fidvalue
                    if not fidvalue:
                        fidvalue=""
                    listvalue.append(fidvalue)
                company_numb=0
                if not label:
                    label=label1
                hexptitle=""
                if label:
                    #company_numb=self.getpricelist_company_count(label)
                    hexptitle=getjiami(label)
                list2={'id':id,'postdate':postdate,'curl':curl,'hexptitle':hexptitle,'listvalue':listvalue,'proname':proname}
                listall.append(list2)
        #设置缓存
        #cache.set("zz91price_getdetailpricelist"+str(priceid)+str(listfield),listall,60*10)
        return listall
    #----走势图数据
    def getchartpricelist(self,keywords='',frompageCount='',limitNum=30,timedate='',gmt_begin='',gmt_end='',area='',group='',attrbute='',maxcount=30,categoryid="",ctype=''):
       
    
        keywords=re.sub('\/.*',' ',keywords)
        keywords=re.sub('\(',' ',keywords)
        keywords=re.sub('\)',' ',keywords)
        keywords=re.sub(',',' ',keywords)
        keywords=re.sub('%',' ',keywords)
        keywords=re.sub('-',' ',keywords)
        pricelist=spconfig['name']['pricelist']['name']
        serverid=spconfig['name']['pricelist']['serverid']
        port=spconfig['name']['pricelist']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if group:
            cl.SetGroupBy(group,SPH_GROUPBY_ATTR )
        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'postdate' )
        if timedate:
            cl.SetFilter('postdate',[timedate])
        if categoryid:
            cl.SetFilter('type_id',[categoryid])
        if gmt_begin and gmt_end:
            if gmt_begin!="" and gmt_end!="":
                cl.SetFilterRange('postdate',gmt_begin,gmt_end)
                limitNum=maxcount=500
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if attrbute:
            res = cl.Query ('@(label,label1,spec,spec1,spec2) '+attrbute,pricelist)
        else:
            keyww=''
            if area:
                keyww+='@(title,typename,label,label1,label1,area,area1,area2,spec,spec1,spec2) '+area
            if keywords:
                #keyww+=' @(typename,title,label,label1,spec,spec1,spec2) '+keywords
                keyww+=' '+keywords
            if keyww:
                res = cl.Query (keyww,pricelist)
            else:       
                res = cl.Query ('',pricelist)
        listchart=[]
        count=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                js=0
                maxprice=0
                minprice=0
                sql='select label,label1,area,title,priceid,postdate,price,price1 from price_list where id=%s'
                for match in tagslist:
                    id=match['id']
                    if not area:
                        area=""
                    curl='/chart/'+str(id)+'.html?area='+area
                    
                    result=self.dbc.fetchonedb(sql,[id])
                    if result:
                        label=result[0]
                        label1=result[1]
                        parea=result[2]
                        title=result[3]
                        priceid=result[4]
                        postdate=result[5]
                        price=result[6]
                        if not price:
                            price=''
                        price1=result[7]
                        if not price1:
                            price1=''
                        if not price and not price1:
                            continue
                        postdate=formattime(postdate,1)
                    
    #                    attrs=match['attrs']
    #                    title=attrs['ptitle']
    #                    priceid=attrs['priceid']
                        purl='/detail/'+str(priceid)+'.html'
    #                    postdate=attrs['postdate']
    #                    label=attrs['plabel']
    #                    if not label:
    #                        label=attrs['plabel1']
                        if not label:
                            label=label1
                        if not label:
                            label=re.sub('.*?日','',title)
                        
    #                    price=attrs['pprice']
                        if '元' in price:
                            price11=re.findall('[\d]+',price)
                            if price11:
                                price=price11[0]
    #                    list['price']=price
    #                    price1=attrs['pprice1']
                        if '跌' in price1:
                            price1=price1.split('跌')[0]
                        elif '涨' in price1:
                            price1=price1.split('涨')[0]
                        elif '-' in price1:
                            price1=price1.split('-')[0]
                        lowprice=''
                        heiprice=''
                        splitarg=''
                        if '-' in price:
                            splitarg='-'
                        elif '/' in price:
                            splitarg='/'
                        if splitarg:
                            prilh=price.split(splitarg)
                            lowprice=prilh[0]
                            if lowprice.isdigit()==False:
                                lowprice=re.findall('[\d]+',lowprice)
                                if lowprice:
                                    lowprice=int(lowprice[0])
                                else:
                                    lowprice=0
                            else:
                                lowprice=int(lowprice)
    #                        list['lowprice']=lowprice
                            heiprice=prilh[1]
                            if heiprice.isdigit()==False:
                                heiprice=re.findall('[\d]+',heiprice)
                                if heiprice:
                                    heiprice=int(heiprice[0])
                                else:
                                    heiprice=0
                            else:
                                heiprice=int(heiprice)
    #                        list['heiprice']=heiprice
                        aveprice=0
                        if lowprice and heiprice:
                            aveprice=(lowprice+heiprice)/2
    #                        list['aveprice']=aveprice
#                            listchart.append(list)
                        else:
                            if not price1:
                                price1=price
                            if price.isdigit()==True and price1.isdigit()==True:
                                lowprice=int(price)
                                heiprice=int(price1)
                                aveprice=(lowprice+heiprice)/2
    #                            list['aveprice']=aveprice
                        if ctype=="app":
                            list={'xAxis':postdate,'yAxis':aveprice}
                        else:
                            list={'posttime':str_to_int(postdate),'postdate2':postdate,'aveprice':aveprice}
                        listchart.append(list)
                count=res['total_found']
        return listchart
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
        cl.SetLimits (0,limitnum)
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
                    
                    pdt_date=int_to_str(attrs['refresh_time'])
                    short_time=pdt_date[5:]
                    proimg=self.getproductimg(pid,"50x50")
                    province=self.getproductsprovince(company_id)
                    price=attrs['min_price']
                    title=subString(attrs['ptitle'],40)
                    
                    list={'id':pid,'title':title,'gmt_time':pdt_date,'short_time':short_time,'fulltitle':attrs['ptitle'],'proimg':proimg,'price':price,'province':province}
                    listall_offerlist.append(list)
        return listall_offerlist
    #---获取默认图片
    def getproductimg(self,id,size):
        #----
        sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc"
        productspic = self.dbc.fetchonedb(sql1,[id])
        if productspic:
            pdt_images=productspic[0]
        else:
            pdt_images=""
        if (pdt_images == '' or pdt_images == '0'):
            pdt_images='../cn/img/noimage.gif'
        else:
            pdt_images='http://img3.zz91.com/'+str(size)+'/'+pdt_images+''
        return pdt_images
    #获得供求地区
    def getproductsprovince(self,company_id):
        sql="select b.label from company as c left OUTER join category as b on left(c.area_code,12)=b.code where c.id=%s"
        province = self.dbc.fetchonedb(sql,[company_id])
        if province:
            provincename=province[0]
            return provincename
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
    def getpricecategorypinyin(self,id):
        sql='select pinyin from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    #新版app我的行情定制
    def getmyorderprice(self,company_id):
        sql='select id,label,company_id,category_id,assist_id,keywords from app_order_price where company_id=%s'
        alistall = self.dbc.fetchalldb(sql,[company_id])
        listall=[]
        if alistall:
            for alist in alistall:
                list={'id':alist[0],
                      'label':alist[1],
                      'company_id':alist[2],
                      'category_id':alist[3],
                      'assist_id':alist[4],
                      'keywords':alist[5]}
                listall.append(list)
            return listall
        else:
            return None
        
    #企业报价详细页
    def getcompanyprice_detail(self,id):
        sql="select a.product_id,a.title,a.price,a.price_unit,a.min_price,a.max_price,a.area_code,a.details,a.is_checked,a.refresh_time,b.label,a.company_id,c.label,a.category_company_price_code,d.name from company_price as a left join category as b on left(a.area_code,16)=b.code left join category as c on left(a.area_code,12)=c.code left join company as d on d.id=a.company_id where a.id=%s"
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            product_id=result[0]
            title=result[1]
            price=result[2]
            price_unit=result[3]
            min_price=result[4]
            max_price=result[5]
            area_code=result[6]
            rprice=''
            if price:
                rprice=price
            if min_price:
                rprice=min_price
            if max_price:
                rprice=rprice+"-"+max_price
            price=rprice
            details=result[7]
            refresh_time=formattime(result[9],1)
            city=result[10]
            province=result[12]
            company_id=result[11]
            category_company_price_code=result[13]
            companyname=result[14]
            clabel=''
            sql2='select label from category_company_price where code=%s'
            alist2 = self.dbc.fetchonedb(sql2,[category_company_price_code])
            if alist2:
                clabel=alist2[0]
            list={'product_id':product_id,'title':title,'price':price,'min_price':min_price,'max_price':max_price,'price_unit':price_unit,'area_code':area_code,'details':details,'refresh_time':refresh_time,'city':city,'company_id':company_id,'province':province,'category_company_price_code':category_company_price_code,'companyname':companyname,'clabel':clabel}
            return list
            
            
    