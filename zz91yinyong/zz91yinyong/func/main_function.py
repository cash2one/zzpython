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
                    bbscontent=cache.get("bbscontent"+str(id))
                    bbscontent=None
                    if (bbscontent==None):
                        sql="select content,account,company_id,reply_time from bbs_post where id=%s"
                        alist = self.dbc.fetchonedb(sql,id)
                        if alist:
                            havepic=havepicflag(alist[0])
                            content=subString(filter_tags(alist[0]),20)
                        else:
                            content=""
                            havepic=0
                        attrs=match['attrs']
                        title=attrs['ptitle']
                        if (content!=""):
                            title=content
                        gmt_time=attrs['ppost_time']
                        bbscontent={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'havepic':havepic,'mobileurl':mobileurl}
                        cache.set("bbscontent"+str(id),bbscontent,60)
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
                    title10=title.decode('utf-8')[:13]
                    pubdate=attrs['pubdate']
                    pubdate2=int_to_str(pubdate)
                    list1={'title':title,'title10':title10,'id':id,'pubdate':pubdate2,'newsurl':newsurl,'weburl':weburl,'mobileweburl':mobileweburl}
                    listall_news.append(list1)
                    if limitNum==1:
                        return list1
        return listall_news
    #类别列表
    def getindexcategorylist(self,code,showflag):
        catelist=cache.get("cate1"+str(code))
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
                    sql1="select label from category_products where code like '"+str(a[1])+"____' order by sort asc"
                    listall_cate1=[]
                    catelist1=self.dbc.fetchalldb(sql1)
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
    def getadlist(self,pkind):
        adcach=cache.get("m_indexad"+str(pkind))
        if adcach:
            return adcach
        sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and DATEDIFF(gmt_plan_end,CURDATE())>=0 and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
        list=self.dbads.fetchonedb(sql,[pkind])
        if list:
            list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}
            cache.set("m_indexad"+str(pkind),list1,60*60*2)
            return list1
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
