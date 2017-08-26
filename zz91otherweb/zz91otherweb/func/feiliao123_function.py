#-*- coding:utf-8 -*-
class zz91feiliao:
    def __init__(self):
        self.dbc=dbc
        self.dbn=dbn
    #报价列表
    def getprlist(self,frompageCount="",limitNum="",maxcount=1000,kname='',category_id='',assist_id='',categoryname='',arg='',gmt_begin='',gmt_end=''):
        price=SPHINXCONFIG['name']['price']['name']
        serverid=SPHINXCONFIG['name']['price']['serverid']
        port=SPHINXCONFIG['name']['price']['port']
        
        cl = SphinxClient()
        cl.SetServer ( serverid,port )
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
        elif arg=='3':
            cl.SetFilterRange('gmt_order',gmt_begin,gmt_end)
        cl.SetLimits (frompageCount,limitNum,maxcount)
        listall_baojia=[]
        listcount_baojia=0
        js=0
        if kname:
            kname=kname.replace('|',' ')
            res = cl.Query ('@(title,tags,search_label) '+kname,price)
        else:
            res = cl.Query ('',price)
        if res:
#            return res
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    td_id=match['id']
                    url='/detail/'+str(td_id)+'.html'
                    attrs=match['attrs']
                    type_id=attrs['type_id']
                    pricetable=self.getpricetable(td_id)
                    pricecategorydetail=self.getpricecategorydetail(type_id)
                    pricecategory=pricecategorydetail['name']
                    pinyin=pricecategorydetail['pinyin']
                    title=attrs['ptitle']
                    ptitle=re.sub('[\d]+月[\d]+日','',title)
                    ptitle=re.sub('价格','',ptitle)
                    ptitle=re.sub('地区','',ptitle)
                    hexptitle=getjiami(ptitle)
                    area=''
                    if kname:
                        area=re.sub(kname.encode('utf-8'),'',ptitle)
                    assist_type_id=attrs['assist_type_id']
                    assist_type=self.getpricecategory(assist_type_id)
                    pinyin2=self.getpriceattrpinyin(assist_type)
                    pcontent=self.getpricecontent(td_id,98)
                    company_numb=0
                    if categoryname:
                        company_numb=self.getpricelist_company_count(ptitle)
#                    title=getlightkeywords(cl,[title],kname,"company_price")
                    gmt_time=attrs['gmt_time']
                    str_time=gmt_time[-5:].replace('-','月')+'日'
                    list1={'td_title':title,'ptitle':ptitle,'hexptitle':hexptitle,'area':area,'fulltitle':title,'td_id':td_id,'td_time':gmt_time,'str_time':str_time,'url':url,'pcontent':pcontent,'pricecategory':pricecategory,'categoryid':type_id,'assist_type_id':assist_type_id,'pinyin':pinyin,'pinyin2':pinyin2,'evennumber':'','assist_type':assist_type,'company_numb':company_numb,'pricetable':pricetable}
                    js=js+1
                    if js%2==0:
                        evennumber=1
                    else:
                        evennumber=0
                    list1['evennumber']=evennumber
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
        return {'list':listall_baojia,'count':listcount_baojia}
    
    def getpricetable(self,priceid):
        #获得缓存
        zz91price_getpricetable=cache.get("zz91price_getpricetable"+str(priceid))
        if zz91price_getpricetable:
            return zz91price_getpricetable 
        sql='select DISTINCT filed from price_titlefild where priceid=%s'
        resultlist=self.dbc.fetchalldb(sql,[priceid])
        return resultlist
        selectarg=u'id,'
        area=''
        price=''
        price1=''
        qushi=''
        area_numb=None
        price_numb=None
        price1_numb=None
        qushi_numb=None
        numb=0
        for result in resultlist:
            numb+=1
            filed=result[0]
            if filed=='area':
                selectarg+=u'area,'
                area_numb=numb
            elif filed=='price':
                selectarg+=u'price,'
                price_numb=numb
            elif filed=='price1':
                selectarg+=u'price1,'
                price1_numb=numb
            elif filed=='qushi':
                selectarg+=u'qushi,'
                qushi_numb=numb
        selectarg=selectarg[:-1]
        sql2='select '+selectarg+' from price_list where priceid=%s'
        resultlist2=self.dbc.fetchalldb(sql2,[priceid])
        for list2 in resultlist2:
            if area_numb:
                area=list2[area_numb]
            if price_numb:
                price=list2[price_numb]
            if price1_numb:
                price1=list2[price1_numb]
            if qushi_numb:
                qushi=list2[qushi_numb]
            list={'area':area,'price':price,'price1':price1,'qushi':qushi}
            #设置缓存
            cache.set("zz91price_getpricetable"+str(priceid),list,60*10)
            return list
    def getpricecategorydetail(self,id):
        sql='select name,pinyin from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        list={'name':'','pinyin':''}
        if result:
            list={'name':result[0],'pinyin':result[1]}
        return list
    def getpricecategory(self,id):
        sql1='select name from price_category where id=%s'
        result1=self.dbc.fetchonedb(sql1,[id])
        if result1:
            return result1[0]
        return ''
    def getpriceattrpinyin(self,label):
        sql='select pinyin from price_category_attr where label=%s'
        result=self.dbc.fetchonedb(sql,[label])
        if result:
            return result[0]
        return ''
    def getpriceattrpinyin(self,label):
        sql='select pinyin from price_category_attr where label=%s'
        result=self.dbc.fetchonedb(sql,[label])
        if result:
            return result[0]
        return ''
    def getpricecontent(self,id,len):
        sql='select content from price where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            content=result[0]
            if content:
                return filter_tags(content).replace(' ','')[:len]+'......'
            else:
                return content
    
    def getpricedblist(self,frompageCount='',limitNum='',typeid='',assist_type_id=''):
        sqlarg=''
        argument=[]
        if typeid:
            sqlarg+=' and type_id=%s'
            argument.append(typeid)
        sql1='select count(0) from price where id>0'+sqlarg
        sql='select id,title from price where id>0'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            td_id=result[0]
            url='/detail/'+str(td_id)+'.html'
            ptitle=result[1]
            list={'td_id':td_id,'url':url,'td_title':ptitle}
            listall.append(list)
        return {'list':listall,'count':count}
    
    #----资讯
    def getnewslist(self,keywords="",frompageCount=0,limitNum=6,typeid="",allnum="",typeid2="",contentflag=""):
        cl = SphinxClient()
        news=SPHINXCONFIG['name']['news']['name']
        serverid=SPHINXCONFIG['name']['news']['serverid']
        port=SPHINXCONFIG['name']['news']['port']
        cl.SetServer ( serverid, port)
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if (typeid):
            cl.SetFilter('typeid',typeid)
        if (typeid2):
            cl.SetFilter('typeid2',[typeid2])
        cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
        if (allnum):
            cl.SetLimits (frompageCount,limitNum,allnum)
        else:
            cl.SetLimits (frompageCount,limitNum)
        if (keywords):
            if "p" == keywords:
                res = cl.Query ('@(flag) '+keywords,news)
            else:
                res = cl.Query ('@(title,keywords) '+keywords,news)
        else:
            res = cl.Query ('',news)
        listall_news=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    weburl="http://news.zz91.com"
                    newsurl=self.dbn.get_newstype(id)
                    if newsurl and newsurl["url2"]:
                        weburl+="/"+newsurl["url2"]
                        weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                    mobileweburl="http://www.zz91.com/news/newsdetail"+str(id)+".htm?type=news"
                    title=filter_tags(attrs['ptitle'])
                    title10=subString(title.decode('utf-8'),80)
                    pubdate=attrs['pubdate']
                    pubdate2=int_to_str(pubdate)
                    list1={'title':title,'title10':title10,'id':id,'pubdate':pubdate2,'newsurl':newsurl,'weburl':weburl,'mobileweburl':mobileweburl}
                    listall_news.append(list1)
                    if limitNum==1:
                        return list1
        return listall_news
    #公司信息列表 翻页
    def getcompanylist(self,kname,frompageCount,limitNum,allnum):
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
                    if vipflag==1:
                        company_url="http://"+domain_zz91+".zz91.com"
                    else:
                        company_url="http://company.zz91.com/compinfo"+str(id)+".htm"
                    pbusiness=attrs['pbusiness']
                    if pbusiness:
                        pbusiness=subString(filter_tags(pbusiness),100)
                    parea_province=attrs['parea_province']
                    list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'address':address,'membership':membership,'viptype':viptype,'vipflag':vipflag,'domain_zz91':domain_zz91,'company_url':company_url}
                    listall_comp.append(list1)
                listcount_comp=res['total_found']
    
                return {'list':listall_comp,'count':listcount_comp}
    #获得新公司
    def getcompanylist1(self,code=""):
        argument=[]
        if code:
            sql='select id,name,membership_code,domain_zz91 from company where industry_code=%s order by gmt_created desc limit 0,7'
            argument.append(code)
        else:
            sql="select id,name,membership_code,domain_zz91 from company where industry_code!='10001000' and industry_code!='10001000' order by gmt_created desc limit 0,7"
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                name=result[1]
                membership_code=result[2]
                domain_zz91=result[3]
                #判断会员类型
                company_url="http://www.zz91.com"
                if int(membership_code)==10051003 or int(membership_code)==10051000:
                    company_url="http://company.zz91.com/compinfo"+str(id)+".htm"
                else:
                    company_url="http://"+domain_zz91+".zz91.com"
                list={'company_id':id,'company_name':name,"company_url":company_url}
                listall.append(list)
        return listall
    
    #trade交易页面
    #---最新供求
    #---下面企业报价
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
    #资讯页面
    def getfuzhuindexlist(self):
        sql='select id,typename,keywords from dede_arctype where reid=183 and (id=153 or id=155 or id=156)'
        resultlist=self.dbn.fetchalldb(sql)
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
            roll_img=self.get_news_all(0,4,flag='s',typeid2=typeid)['list']
            kinds_6=self.get_news_all(0,6,typeid2=typeid)['list']
            keywords10=self.gettypelist(0,10,keywords=kind_name)
            list={'roll_img':roll_img,'keywords10':keywords10,'kinds_6':kinds_6,'kind_name':kind_name,'kind_url':kind_url,'kind_url2':kind_url2,'idj':idj,'m2_sitem':m2_sitem,'m2_sitem_button':m2_sitem_button,'m2_sitem_text':m2_sitem_text}
            listall.append(list)
        return listall
    #----资讯列表(数据库)
    def get_news_all(self,frompageCount,limitNum,pubdate='',pubdate2='',flag='',title='',typeid='',typeid2='',has_txt='',kwd=''):
        
        argument=[]
        sql1='select count(0) from dede_archives where id>0'
        sql='select id,title,sortrank,click,writer,shorttitle,keywords,litpic,filename,description from dede_archives where id>0'
        if pubdate:
            argument.append(pubdate)
            sql1=sql1+' and senddate>=%s'
            sql=sql+' and senddate>=%s'
        if pubdate2:
            argument.append(pubdate2)
            sql1=sql1+' and senddate<=%s'
            sql=sql+' and senddate<=%s'
        if flag:
            if ',' in flag:
                sql1=sql1+' and flag=%s'
                sql=sql+' and flag=%s'
            else:
                sql1=sql1+' and find_in_set(%s,flag)'
                sql=sql+' and find_in_set(%s,flag)'
            argument.append(flag)
        if typeid:
            argument.append(typeid)
            sql1=sql1+' and typeid=%s'
            sql=sql+' and typeid=%s'
        if typeid2:
            argument.append(typeid2)
            sql1=sql1+' and typeid2=%s'
            sql=sql+' and typeid2=%s'
        if title:
#            argument.append(title)
            sql1=sql1+' and title like "%'+title+'%"'
            sql=sql+' and title like "%'+title+'%"'
        sql=sql+' order by id desc'
        if limitNum:
            sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbn.fetchnumberdb(sql1,argument)
        resultlist=self.dbn.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            js=0
            for result in resultlist:
                id=result[0]
                title=result[1]
                title12=title[:12]
                title15=title[:15]
                title16=title[:16]
                title20=title[:20]
                intdate=result[2]
                click=result[3]
                writer=result[4]
                shorttitle=result[5]
                keywords=result[6]
                litpic=result[7]
                filename=result[8]
                description=result[9]
                kwds=''
                kwds_hex=''
                if kwd and keywords:
                    kwdslist=keywords.split(',')[:kwd]
                    if kwd>1:
                        kwds=','.join(kwdslist)
                    else:
                        kwds=kwdslist[0]
                        kwds_hex=getjiami(kwds)
                pubdate=intdate
#                pubdate=int_to_str(intdate)
                pubdate1=time.strftime('%m-%d', time.localtime(pubdate))
                pubdate2=time.strftime('%Y-%m-%d', time.localtime(pubdate))
                newsurl=self.get_newstype(id)
                weburl=""
                weburl="http://news.zz91.com"
                typeid=''
                typeid2=''
                typename=''
                typename2=''
                if newsurl:
                    typeid=newsurl['typeid']
                    typename=newsurl['typename']
                    typeid2=newsurl['typeid2']
                    if newsurl["url2"]:
                        typename2=newsurl['typename2']
                        weburl+="/"+newsurl["url2"]
                    weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                content=''
                if has_txt:
                    if description:
                        content=filter_tags(description)
                        content=subString(str(content),has_txt)
                    #content=self.getnewsbody(id,has_txt)
                list={'id':id,'intdate':intdate,'pubdate':pubdate,'pubdate1':pubdate1,'pubdate2':pubdate2,'title':title,'title12':title12,'title15':title15,'title16':title16,'title20':title20,'weburl':weburl,'click':click,'writer':writer,'flaglist':'','flagnamestr':'','js':js,'typeid':typeid,'typeid2':typeid2,'typename':typename,'typename2':typename2,'shorttitle':shorttitle,'keywords':keywords,'litpic':litpic,'content':content,'kwds':kwds,'kwds_hex':kwds_hex,'filename':filename}
                #if flag:
                    #list['flaglist']=flaglist
                    #list['flagnamestr']=flagnamestr
                if limitNum==1:
                    return list
                listall.append(list)
                js=js+1
        return {'list':listall,'count':count}
    
    def gettypelist(self,frompageCount,limitNum,reid='',keywords='',has_news='',fromnews='',has_txt='',typeid='',typeid2=''):
        listall=[]
        argument=[]
        sqlarg=' from dede_arctype '
        if reid:
            if 'where' in sqlarg:
                sqlarg+=' and reid=%s'
            else:
                sqlarg+=' where reid=%s'
            argument.append(reid)
        if keywords:
            if 'where' in sqlarg:
                sqlarg+=' and keywords=%s'
            else:
                sqlarg+=' where keywords=%s'
            argument.append(keywords)
        sql='select id,typename,sortrank,keywords'+sqlarg
        sql+=' order by sortrank,id limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbn.fetchalldb(sql,argument)
        for result in resultlist:
            id=result[0]
            #nexttype=self.getnexttype(id)
            typename=result[1]
            typename_hex=''
            if typename:
                typename_hex=getjiami(typename)
            sortrank=result[2]
            keywords=result[3]
            newslist=[]
            if has_news:
                if reid==183:
                    typeid=typeid
                    typeid2=id
#                    typeid=[]
                else:
                    typeid=id
                    typeid2=typeid2
                if fromnews:
                    newslist=self.get_news_all(frompageCount=fromnews,limitNum=has_news,typeid=typeid,typeid2=typeid2,has_txt=has_txt)['list']
                else:
                    newslist=self.get_news_all(frompageCount=0,limitNum=has_news,typeid=typeid,typeid2=typeid2,has_txt=has_txt)
            list={'id':result[0],'typename':typename,'typename_hex':typename_hex,'sortrank':sortrank,'keywords':keywords,'newslist':newslist}
            listall.append(list)
        return listall
    
    #获得新闻栏目id列表
    def getcolumnid(self):
        sql='select id,typename,keywords from dede_arctype where reid=184 order by sortrank limit 0,20'
        resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            listall.append(result[0])
        return listall
    #----资讯列表(搜索引擎)
    def getnewslistlatest(self,keywords="",frompageCount="",limitNum=3,typeid="",typeid2="",allnum="",arg='',flag='',type='',MATCH="",num="",has_txt=""):
#        if keywords:
#            keywords=keywords.upper()
#        if '%' in keywords:
#            keywords=keywords.replace('%','%%')
        news=SPHINXCONFIG['name']['news']['name']
        serverid=SPHINXCONFIG['name']['news']['serverid']
        port=SPHINXCONFIG['name']['news']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        if MATCH!="":
            cl.SetMatchMode ( SPH_MATCH_ANY )
        else:
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if typeid:
            cl.SetFilter('typeid',typeid)
        if typeid2 and typeid2!="":
            cl.SetFilter('typeid2',typeid2)
        if MATCH!="":
            cl.SetSortMode( SPH_SORT_EXTENDED ,'@weight DESC,pubdate desc' )
        else:
            cl.SetSortMode( SPH_SORT_ATTR_DESC ,'pubdate' )
        if num:
            cl.SetLimits (0,num,num)
        else:
            if (allnum):
                cl.SetLimits (frompageCount,limitNum,allnum)
            else:
                cl.SetLimits (frompageCount,limitNum)
        if (keywords):
            if flag:
                res = cl.Query ('@(title,description) '+keywords+'&@(flag) "p"',news)
            else:
                if arg==1:
                    res = cl.Query ('@(title,description) '+keywords,news)
                else:
                    res = cl.Query ('@(title) '+keywords,news)
        else:
            if flag:
                res = cl.Query ('@(flag) "p"',news)
            else:
                res = cl.Query ('',news)
        listall_news=[]
        listcount_news=0
        numb=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    content=''
                    if has_txt:
                        content=self.getnewsbody(id,has_txt)
                    newsurl=self.get_newstype(id)
                    weburl="http://news.zz91.com"
                    if newsurl:
                        if newsurl["url2"]:
                            weburl+="/"+newsurl["url2"]
                        weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                    attrs=match['attrs']
                    title=attrs['ptitle']
#                    if re.findall('^[A-Z]+',keywords):
#                    else:
#                        title=re.sub(keywords,'<font color="red">'+keywords+'</font>',title)
                    click=attrs['click']
                    pubdate=attrs['pubdate']
                    pic=attrs['litpic']
                    if pic!="" and pic:
                        litpic=pic
                        has_pic=1
                    else: 
                        litpic="http://img0.zz91.com/front/images/global/noimage.gif"
                        has_pic=''
                    #litpic=''
                    pubdate1=time.strftime('%m-%d', time.localtime(pubdate))
                    pubdate2=time.strftime('%Y-%m-%d', time.localtime(pubdate))
                    title=title.replace('&nbsp;','')
                    title10=title.decode('utf8')[:10]
                    title12=title.decode('utf8')[:12]
                    title15=title.decode('utf8')[:15]
                    title16=title.decode('utf8')[:16]
                    title20=title.decode('utf8')[:20]
                    numb+=1
                    list1={'numb':numb,'title':title,'title10':title10,'title12':title12,'title15':title15,'title16':title16,'title20':title20,'click':click,'id':id,'pubdate1':pubdate1,'pubdate':pubdate2,'weburl':weburl,'litpic':litpic,'has_pic':has_pic,'content':content}
#                    if type:
                    if keywords in title or arg==1 or arg==2:
                        listall_news.append(list1)
                        #title=search_strong(keywords,title)
                        list1['title']=title
                    else:
                        listall_news.append(list1)
                    if limitNum==1 or num==1:
                        return list1
                listcount_news=res['total_found']
        if num:
            return listall_news
        else:
            return {'list':listall_news,'count':listcount_news}
    
    def get_newstype(self,id):
        sql='select typeid,typeid2 from dede_archives where id=%s'
        result=self.dbn.fetchonedb(sql,[id])
        if result:
            typeid=result[0]
            typeid2=result[1]
            sql2='select typename,keywords from dede_arctype where id=%s'
            result2=self.dbn.fetchonedb(sql2,[typeid])
            if result2:
                list={'typename':result2[0],'url':result2[1],'typeid':typeid,'typeid2':typeid2,'url2':'','typename2':''}
                if typeid2!='0':
                    sql3='select keywords,typename from dede_arctype where id=%s'
                    result3=self.dbn.fetchonedb(sql3,[typeid2])
                    if result3:
                        list['url2']=result3[0]
                        list['typename2']=result3[1]
                return list
    def getnewsbody(self,id,has_txt):
        sql='select description from dede_archives where id=%s'
        resultlist=self.dbn.fetchonedb(sql,id)
        if resultlist:
            content=resultlist[0]
            if content:
                content=content[:has_txt]
                return content
            
    #---供求
    def getproductslist(self):
        sql="select id,company_id,products_type_code,title,source,total_quantity,quantity_unit,manufacture from products where is_del=0 and check_status=1 and is_pause=0 order by refresh_time desc limit 0,6"
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        t_url=""
        if resultlist:
            for result in resultlist:
                id=result[0]
                company_id=result[1]
                str_mem=self.getmembership(company_id)
                if str_mem=='0':
                    #普会供求页
                    t_url="http://trade.zz91.com/productdetails"+str(id)+".htm"
                elif str_mem=="1":
                    #来电宝供求页
                    t_url="http://www.zz91.com/ppc/productdetail"+str(id)+".htm"
                else:
                    #高会供求页,like:http://aqsiqcn.zz91.com/products1500837.htm
                    t_url="http://"+str_mem+".zz91.com/products"+str(id)+".htm"
                pic_url=self.getonepicture(id)
                products_type_code=result[2]
                title=result[3]
                source=result[4]
                total_quantity=result[5]
                quantity_unit=result[6]
                manufacture=result[7]
                list={'id':id,'company_id':company_id,'products_type_code':products_type_code,'title':title,'source':source,'total_quantity':total_quantity,'quantity_unit':quantity_unit,'manufacture':manufacture,'pic_url':pic_url,"t_url":t_url}
                listall.append(list)
        return listall
    #判断高会普会来电宝
    def getmembership(self,id):
        sql='select domain_zz91,membership_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            domain_zz91=result[0]
            membership_code=int(result[1])
            if membership_code==10051003:
                return '1'
            if membership_code==10051000:
                return '0'
            else:
                return domain_zz91
    #获得图片地址
    def getonepicture(self,id):
        pic_url=''
        sql='select id,product_id,pic_address from products_pic where check_status=1 and product_id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            pic_address=result[2]
            pic_url='http://img3.zz91.com/140x80/'+pic_address
        else:
            pic_url="/new/images/logo.jpg"
        return pic_url
    #---资讯
    def getlatestnews(self):
        sql="select id,title,litpic,description from dede_archives where id>0 order by id desc limit 0,10"
        resultlist=self.dbn.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                title=result[1]
                litpic=result[2]
                if litpic=='' or litpic==None:
                    litpic="http://img0.zz91.com/front/images/global/noimage.gif"
                description=result[3]
                description=description[:100]
                description+="..."
                newsurl=self.get_newstype(id)
                weburl=""
                weburl="http://news.zz91.com"
                typeid=''
                typeid2=''
                typename=''
                typename2=''
                if newsurl:
                    typeid=newsurl['typeid']
                    typename=newsurl['typename']
                    typeid2=newsurl['typeid2']
                    if newsurl["url2"]:
                        typename2=newsurl['typename2']
                        weburl+="/"+newsurl["url2"]
                    weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
                list={"id":id,"title":title,"litpic":litpic,"description":description,'weburl':weburl}
                listall.append(list)
        return listall
                