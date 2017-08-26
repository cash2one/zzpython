#-*- coding:utf-8 -*-

class zapps:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
        self.dbsms=dbsms
        self.dbn=dbn
        self.dbads=dbads
    def getadshowtype(self,id):
        js_function=None
        sqlp="select js_function from delivery_style where id=%s"
        alist=self.dbads.fetchonedb(sqlp,[id])
        if alist:
            js_function=alist[0]
        return js_function
    def getadlist(self,pkind,p):
        width=None
        height=None
        max_ad=None
        sqlp="select width,height,max_ad,delivery_style_id from ad_position where id=%s"
        alist=self.dbads.fetchonedb(sqlp,[pkind])
        if alist:
            width=alist[0]
            height=alist[1]
            max_ad=alist[2]
            delivery_style_id=alist[3]
            js_function=self.getadshowtype(delivery_style_id)
            
        sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and review_status='Y' and sequence=%s and online_status='Y' order by gmt_start asc,sequence asc"
        alist=self.dbads.fetchonedb(sql,[pkind,p])
        list=[]
        if alist:
            if (width=="0"):
                width=""
            if (height=="0"):
                height=""
            js_function=js_function.replace("{1}",alist[0])
            js_function=js_function.replace("|","")
            js_function=js_function.replace("\"","'")
            js_function=js_function.replace("{2}",alist[3])
            js_function=js_function.replace("{3}",'http://gg.zz91.com/hit?a='+str(alist[2]))
            js_function=js_function.replace("{4}",'width='+str(width))
            js_function=js_function.replace("{5}",'height='+str(height))
            list={'url':'http://gg.zz91.com/hit?a='+str(alist[2]),'picaddress':alist[0],'height':height,'width':width,'max_ad':max_ad,'js_function':js_function,'ad_title':alist[3]}
        return list
        #广告脚本
    def getadnum(self,code):
        max_ad=None
        sqlp="select max_ad from ad_position where id=%s"
        alist=self.dbads.fetchonedb(sqlp,[code])
        if alist:
            max_ad=alist[0]
        return max_ad
    def getadlistnew(self,pkind):
        width=None
        height=None
        max_ad=None
        sqlp="select width,height,max_ad,delivery_style_id from ad_position where id=%s"
        alist=self.dbads.fetchonedb(sqlp,[pkind])
        if alist:
            width=alist[0]
            height=alist[1]
            max_ad=alist[2]
            delivery_style_id=alist[3]
            js_function=self.getadshowtype(delivery_style_id)
            
        sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
        alist=self.dbads.fetchalldb(sql,[pkind])
        listvalue=[]
        if alist:
            for list in alist:
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
                list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'height':height,'width':width,'max_ad':max_ad,'js_function':js_function1,'ad_title':list[3]}
                listvalue.append(list1)
        return listvalue
    #来电宝客户全网推广
    def getppccomplist(self,m,keywords,page,adposition=''):
        if page==None:
            page=1
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetLimits ((page-1)*m,m,200)
        if (keywords):
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
            cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR,"ordt desc, refresh_time desc")
            cl.SetSelect("*,max(sort) AS ordt")
            cl.SetSortMode( SPH_SORT_EXTENDED,"ordt desc, refresh_time desc" )
            
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
        else:
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
            cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR,"ordt desc, refresh_time desc")
            cl.SetSelect("*,max(sort) AS ordt")
            cl.SetSortMode( SPH_SORT_EXTENDED,"ordt desc, refresh_time desc" )
            res = cl.Query ('','offersearch_ppc')
        listall=[]
        listcount=res['total_found']
        lastpage=int(ceil(float(listcount) / int(m)))
        if (listcount==0):
            cl.SetMatchMode ( SPH_MATCH_ANY )
            cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
            cl.SetLimits ((page-1)*m,m,200)
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    company_id=attrs['company_id']
                    ptitle=attrs['ptitle']
                    ppckeywords1=attrs['ppckeywords']
                    ppckeywords=subString(ppckeywords1,50)
                    companyname=attrs['companyname']
                    front_tel=attrs['front_tel']
                    front_tel=front_tel.replace("转分机","转")
                    pdt_kind=attrs['pdt_kind']
                    pdttxt=""
                    if (str(pdt_kind)=="0"):
                        pdttxt="供应"
                    if (str(pdt_kind)=="1"):
                        pdttxt="求购"
                    #----联系人信息
                    saveshowppc(company_id,adposition)
                    contact=None
                    sqlp="select contact,sex from company_account where company_id=%s"
                    companyaccount=self.dbc.fetchonedb(sqlp,[company_id])
                    if companyaccount:
                        contact=companyaccount[0]
                        
                        sex=companyaccount[1]
                        sex=""
                        if str(sex)=="0":
                            sex="先生"
                        if str(sex)=="1":
                            sex="女士"
                        if "先生" in contact or "女士" in contact:
                            contact=contact
                        else:
                            contact=contact+sex
                    sql1="select pic_address from products_pic where product_id=%s order by is_default desc,id desc"
                    productspic=self.dbc.fetchonedb(sql1,id)
                    if productspic:
                        pdt_images=productspic[0]
                        pdt_images='http://img3.zz91.com/100x100/'+pdt_images+''
                    else:
                        pdt_images='http://img3.zz91.com/100x100/'
                    purl="http://pyapp.zz91.com/app/ppchit.html?company_id="+str(company_id)+"&rd="+getjiami("http://www.zz91.com/ppc/productdetail"+str(id)+".htm")
                    curl="http://pyapp.zz91.com/app/ppchit.html?company_id="+str(company_id)+"&rd="+getjiami("http://www.zz91.com/ppc/index"+str(company_id)+".htm")
                    lis={'id':id,'ptitle':ptitle,'pdttxt':pdttxt,'pdt_images':pdt_images,'company_id':company_id,'ppckeywords':ppckeywords,'ppctel':front_tel,'companyname':companyname,'contact':contact,'curl':curl,'purl':purl}
                    listall.append(lis)
        return {'listall':listall,'lastpage':lastpage}
