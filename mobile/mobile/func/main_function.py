#-*- coding:utf-8 -*-
class zmain:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
        self.dbn=dbn
        self.dbads=dbads
    #----互助
    def getbbslist(self,kname='',frompageCount=0,limitNum=1,allnum='',category_id='',fromtime='',endtime='',datetype=''):
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], spconfig['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetFilter('is_del',[0])
        cl.SetFilter('check_status',[1,2])
        if (category_id):
            cl.SetFilter('bbs_post_category_id',[11,18])
        if fromtime and endtime:
            cl.SetFilterRange('post_time',fromtime,endtime)
        if (datetype==1):
            cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc,reply_time desc" )
        if (datetype in (2,3)):
            cl.SetSortMode( SPH_SORT_EXTENDED,"reply_count desc" )
        if (allnum):
            cl.SetLimits (frompageCount,limitNum,allnum)
        else:
            cl.SetLimits (frompageCount,limitNum)
        if (kname):
            res = cl.Query ('@(title,tags) '+kname,'huzhu')
        else:
            res = cl.Query ('','huzhu')
        listall_news=[]
        if res:
    #        return res
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    mobileurl='http://m.zz91.com/huzhuview/'+str(id)+'.htm'
                    sql="select content,account,company_id,reply_time from bbs_post where id=%s"
                    alist = self.dbc.fetchonedb(sql,id)
                    if alist:
                        havepic=havepicflag(alist[0])
                        content=subString(filter_tags(alist[0]),80)
                    else:
                        content=""
                        havepic=0
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    if (content!=""):
                        title=content
                    gmt_time=attrs['ppost_time']
                    bbscontent={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'havepic':havepic,'mobileurl':mobileurl}
                    listall_news.append(bbscontent)
                    if limitNum==1:
                        return bbscontent
        return listall_news
    #----资讯
    def getnewslist(self,keywords="",frompageCount=0,limitNum=1,typeid="",allnum="",typeid2="",contentflag=""):
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
                    mobileweburl="http://m.zz91.com/news/newsdetail"+str(id)+".htm?type=news"
                    title=filter_tags(attrs['ptitle'])
                    if title:
                        title10=subString(title,80)
                    pubdate=attrs['pubdate']
                    pubdate2=int_to_str(pubdate)
                    list1={'title':title,'title10':title10,'id':id,'pubdate':pubdate2,'newsurl':newsurl,'weburl':weburl,'mobileweburl':mobileweburl}
                    listall_news.append(list1)
                    if limitNum==1:
                        return list1
        return listall_news
    #类别列表
    def getindexcategorylist(self,code,showflag):
        catelist=cache.get("mobile_cateb"+str(code))
        if (catelist==None):
            if (showflag==2):
                sql="select label,code,pinyin from category_products where code like %s order by sort asc"
            else:
                sql="select label,code,pinyin from category_products where code like %s"'"____"'" order by sort asc"
            listall_cate=[]
            catelist=self.dbc.fetchalldb(sql,[str(code)])
            numb=0
            for a in catelist:
                numb=numb+1
                if (showflag==1):
                    sql1="select label,pinyin from category_products where code like '"+str(a[1])+"____' order by sort asc"
                    listall_cate1=[]
                    catelist1=self.dbc.fetchalldb(sql1)
                    for b in catelist1:
                        list1={'label':b[0],'pinyin':b[1].lower()}
                        listall_cate1.append(list1)
                else:
                    listall_cate1=None
                list={'label':a[0],'code':a[1],'catelist':listall_cate1,'numb':numb,'pinyin':a[2].lower()}
                listall_cate.append(list)
            cache.set("mobile_cateb"+str(code),listall_cate,60*6)
        else:
            listall_cate=catelist
        
        return listall_cate
    def getadlist(self,pkind):
        adcach=cache.get("mobile_indexad"+str(pkind))
        #adcach=None
        if adcach:
            return adcach
        sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and DATEDIFF(gmt_plan_end,CURDATE())>=0 and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
        list=self.dbads.fetchonedb(sql,[pkind])
        if list:
            list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}
            cache.set("mobile_indexad"+str(pkind),list1,60*10)
            return list1
    def getadlistall(self,pkind):
        adcach=cache.get("mobile_indexadall"+str(pkind))
        nowdate=getDay()
        if adcach:
            return adcach
        sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and DATEDIFF(gmt_plan_end,CURDATE())>=0 and review_status='Y' and online_status='Y' order by sequence asc,gmt_start asc"
        adlist=self.dbads.fetchalldb(sql,[pkind])
        listall=[]
        if adlist:
            for list in adlist:
                list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}
                listall.append(list1)
            cache.set("mobile_indexad"+str(pkind),listall,60*10)
        return listall
    #----微门户关键词
    def getcplist(self,keywords,frompageCount=0,limitNum=1,allnum=2000):
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], spconfig['port'] )
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight desc" )
        cl.SetLimits (frompageCount,limitNum,allnum)
        if not keywords:
            res = cl.Query ('','daohangkeywords')
        else:
            res = cl.Query ('@label '+keywords,'daohangkeywords')
        listall=[]
        listcount=0
        if res:
            listcount=res['total_found']
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    label=attrs['plabel']
                    pingyin=attrs['ppinyin']
                    list={'label':label,'pingyin':pingyin,'label_hex':getjiami(label)}
                    listall.append(list)
        if not listall:
            cl.SetMatchMode ( SPH_MATCH_ALL )
            cl.SetSortMode( SPH_SORT_EXTENDED,"showcount desc" )
            res = cl.Query ('','daohangkeywords')
            if res:
                listcount=res['total_found']
                if res.has_key('matches'):
                    tagslist=res['matches']
                    listall_news=[]
                    for match in tagslist:
                        id=match['id']
                        attrs=match['attrs']
                        label=attrs['plabel']
                        pingyin=attrs['ppinyin']
                        list={'label':label,'pingyin':pingyin,'label_hex':getjiami(label)}
                        listall.append(list)
        if listcount>2000:
            listcount=2000
        return {'list':listall,'count':listcount}
    
    #客户关键字
    def getuserkeywords(self,company_id):
        sql="select keywords from app_user_keywords where company_id=%s limit 0,20"
        list=self.dbc.fetchalldb(sql,[company_id])
        k=""
        if list:
            for l in list:
                if l:
                    k+=str(l[0])+"|"
        else:
            k=""
            sql="select a.label from products as b left join category_products as a on a.code=b.products_type_code where b.company_id=%s limit 0,20"
            list=self.dbc.fetchalldb(sql,[company_id])
            if list:
                for l in list:
                    if l:
                        k+=str(l[0])+"|"
        return k
    #砍价产品列表
    def getkanjialist(self,proid="",company_id=""):
        argument=[]
        sql="select name,price,number,lastprice,cut_price,end_time,havenumber,id,DATEDIFF(end_time,CURDATE()) from subject_kanjia_pro where id>0"
        if proid:
            sql+=" and id=%s"
            argument.append(proid)
        sql+=" order by gmt_created desc"
        result=self.dbc.fetchalldb(sql,argument)
        listall=[]
        if result:
            for list in result:
                #0元剩余名额
                number=list[2]
                dprice=0
                sqlc="select count(0) from subject_kanjia_baoming where pro_id=%s and price_now<=0"
                resultc=self.dbc.fetchonedb(sqlc,[list[7]])
                bcount=resultc[0]
                bcount=int(number)-bcount
                if bcount<=0:
                    dprice=list[3]
                havebaoming=None
                if company_id:
                    sqlc="select id from subject_kanjia_baoming where company_id=%s and pro_id=%s"
                    resultc=self.dbc.fetchonedb(sqlc,[company_id,list[7]])
                    if resultc:
                        havebaoming=1
                l={'id':list[7],'name':list[0],'price':list[1],'number':list[2],'lastprice':list[3],'cut_price':list[4],'end_time':list[5],'havenumber':list[6],'bcount':bcount,'dprice':dprice,'havebaoming':havebaoming,'endtimeflag':list[8]}
                listall.append(l)
        return listall

    #帮帮砍价
    def kanjiacutsave(self,baoming_id,weixinid,pro_id,price_cut):
        gmt_created=gmt_modified=datetime.datetime.now()
        sql="select id from subject_kanjia_havecut where weixinid=%s and baoming_id=%s"
        result=self.dbc.fetchonedb(sql,[weixinid,baoming_id])
        if not result:
            sql1="insert into subject_kanjia_havecut(weixinid,pro_id,baoming_id,price_cut,gmt_created) values(%s,%s,%s,%s,%s)"
            resu=self.dbc.updatetodb(sql1,[weixinid,pro_id,baoming_id,price_cut,gmt_created])
            sql2="update subject_kanjia_baoming set price_now=price_now-%s where id=%s"
            self.dbc.updatetodb(sql2,[price_cut,baoming_id])
            return resu
        return None
    #--砍价列表
    def getkanjiacutlist(self,baoming_id=""):
        argument=[]
        sqlarg=''
        if baoming_id:
            sqlarg+=' and baoming_id=%s'
            argument.append(baoming_id)
        sql='select id,weixinid,pro_id,baoming_id,price_cut,gmt_created from subject_kanjia_havecut where id>0'+sqlarg
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            gmt_created=formattime(result[5],0)
            weixinid=result[1]
            pro_id=result[2]
            price_cut=result[4]
            list={'id':id,'pro_id':pro_id,'gmt_created':gmt_created,'price_cut':price_cut,'weixinid':weixinid}
            listall.append(list)
        return listall
