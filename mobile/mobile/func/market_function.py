#-*- coding:utf-8 -*-
import datetime
from _mysql import result
#from maps_zz91.commfunction import sql1
class zmarket:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #获得用户所在市的label
    def get_city_maybe(self,area_code=''):
        #取得所在城市对应的label
        sql='select label from category where code=%s'
        result=self.dbc.fetchonedb(sql,area_code)
        if result:
            label=result[0]
        return label
    #获得用户所在的城市市场（首页推荐）
    def get_city_market(self,city_label):
        sqlarg=''
        sqlarg+=" and area like '%%"+city_label+"%%'"
        sql="select id,name,area,industry,category,business,introduction,address,company_num,product_num,words from market where is_del=0"+sqlarg
        sql1='select count(0) from market where  is_del=0'+sqlarg
        resultlist=self.dbc.fetchalldb(sql)
        count=self.dbc.fetchnumberdb(sql1)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                #根据id获得pic
                pic_address=self.getonepicture(id)
                name=result[1]
                area=result[2]
                industry=result[3]
                category=result[4]
                business=result[5]
                introduction=result[6]
                address=result[7]
                company_num=result[8]
                product_num=result[9]
                words=result[10]
                list={'id':id,'pic_address':pic_address,'name':name,'area':area,'industry':industry,'category':category,'business':business,'introduction':introduction,'address':address,'company_num':company_num,'product_num':product_num,'words':words}
                listall.append(list)
            return {'list':listall,'count':count}
    #获得市场列表
    def getmarketlist(self,frompageCount='',limitNum='',industry='',category='',province=''):
        argument=[]
        sqlarg=''
        if industry and category:
            sqlarg+=' and industry=%s and category=%s'
            argument.extend([industry,category])
        if province:
            sqlarg+=" and area like '%%"+province+"%%'"
        sql1='select count(0) from market where id>0 and is_del=0 '+sqlarg
        sql="select id,name,area,industry,category,business,introduction,address,company_num,product_num,words from market where is_del=0"+sqlarg
        sql=sql+' order by company_num desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        count=self.dbc.fetchnumberdb(sql1,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                #根据id获得pic
                pic_address=self.getonepicture(id)
                name=result[1]
                area=result[2]
                industry=result[3]
                category=result[4]
                business=result[5]
                introduction=result[6]
                address=result[7]
                company_num=result[8]
                product_num=result[9]
                words=result[10]
                list={'id':id,'pic_address':pic_address,'name':name,'area':area,'industry':industry,'category':category,'business':business,'introduction':introduction,'address':address,'company_num':company_num,'product_num':product_num,'words':words}
                listall.append(list)
            return {'list':listall,'count':count}
    #获得其他市场列表
    def getothermarketlist(self,frompageCount='',limitNum='',industry=''):
        sql1='select count(0) from market where id>0 and is_del=0 and industry=%s '
        sql="select id,name,area,industry,category,business,introduction,address,company_num,product_num,words from market where industry=%s  and is_del=0"
        sql=sql+' order by company_num desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,[industry])
        count=self.dbc.fetchnumberdb(sql1,[industry])
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                #根据id获得pic
                pic_address=self.getonepicture(id)
                name=result[1]
                area=result[2]
                industry=result[3]
                category=result[4]
                business=result[5]
                introduction=result[6]
                address=result[7]
                company_num=result[8]
                product_num=result[9]
                words=result[10]
                list={'id':id,'pic_address':pic_address,'name':name,'area':area,'industry':industry,'category':category,'business':business,'introduction':introduction,'address':address,'company_num':company_num,'product_num':product_num,'words':words}
                listall.append(list)
            return {'list':listall,'count':count}
    #获得一张图片   
    def getonepicture(self,id):
        #若已设置默认图片
        sql='select pic_address from market_pic where market_id=%s and is_default=1 and check_status=1'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            pic_address=result[0]
            return pic_address
        else:
            #未设置默认则依据更新时间选择一张
            sql1='select pic_address from market_pic where market_id=%s and check_status=1 order by gmt_created desc limit 0,1'
            result=self.dbc.fetchonedb(sql1,[id])
            if result:
                pic_address=result[0]
                return pic_address
    #获取多张图片
    def getmanypicture(self,id):
        sql='select pic_address from market_pic where market_id=%s and check_status=1'
        resultlist=self.dbc.fetchalldb(sql,[id])
        listall=[]
        if resultlist:
            for result in resultlist:
                pic_address=result[0]
                list={'pic_address':pic_address}
                listall.append(list)
            return {'list':listall}
    #获得市场详细
    def getmarketdetail(self,market_pinyin=''):
        #获得缓存
        mobile_marketdetail=cache.get("mobile_marketdetail"+str(market_pinyin))
        if mobile_marketdetail:
            return mobile_marketdetail
        sql='select id,name,area,industry,category,business,introduction,address,company_num,product_num from market where words=%s and is_del=0'
        result=self.dbc.fetchonedb(sql,[market_pinyin])
        if result:
            id=result[0]
            pic_address=self.getmanypicture(id)
            name=result[1]
            area=result[2]
            industry=result[3]
            category=result[4]
            business=result[5]
            introduction=result[6]
            address=result[7]
            company_num=result[8]
            product_num=result[9]
            list={"id":id,"pic_address":pic_address,"name":name,"area":area,"industry":industry,"category":category,"business":business,"introduction":introduction,"address":address,"company_num":company_num,"product_num":product_num}
            #设置缓存
            cache.set("mobile_marketdetail"+str(market_pinyin),list,60*30)
            return list
    #获取当前登录用户的主营行业和公司地址（用来判断是否符合入住条件）
    def get_user_info(self,id):
        sql='select industry_code,area_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            industry_code=result[0]
            area_code=result[1]
            return {'industry_code':industry_code,'area_code':area_code}
    #判断地区是否相同(area_code为用户地址信息，areatxt为当前产业带地址信息)
    def isequal_area(self,area_code,areatxt):
        sql='select label from category where code=%s'
        result=self.dbc.fetchonedb(sql,[area_code])
        if result:
            label=result[0]
            if label in areatxt:
                return 1
            else:
                return 0
        else:
            return 0
    #加入市场
    def join_market(self,company_id,market_id):
        gmt_created=datetime.datetime.now()  
        gmt_modified=datetime.datetime.now()
        sql='insert into market_company (market_id,company_id,gmt_created,gmt_modified) values (%s,%s,%s,%s)'
        self.dbc.updatetodb(sql,[market_id,company_id,gmt_created,gmt_modified])
        #market表中company_num加一
        sql1='select company_num from market where id=%s'
        result=self.dbc.fetchonedb(sql1,[market_id])
        if result:
            company_num=result[0]
            company_num=company_num+1
            sql2='insert into market (company_num) values (%s)'
            self.dbc.updatetodb(sql2,[company_num])
            
    #获得该市场的商户信息
    def getcompanylist(self,kname,frompageCount,limitNum,market_id,ldb=''):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if ldb!='' and ldb:
            cl.SetFilter('apply_status',[1])
        cl.SetSortMode( SPH_SORT_EXTENDED,"mobile_order desc,gmt_start desc" )
        cl.SetLimits (frompageCount,limitNum,200000)
        if (kname):
            res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
        else:
            res = cl.Query ('','company')
        listcount_comp=0
        listall_comp=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    compname=attrs['compname']
                    viptype=str(attrs['membership_code'])
                    membership="普通会员"
                    if (viptype == '10051000'):
                        membership='普通会员'
                    if (viptype == '10051001'):
                        membership='再生通'
                    if (viptype == '1725773192'):
                        membership='银牌品牌通'
                    if (viptype == '1725773193'):
                        membership='金牌品牌通'
                    if (viptype == '1725773194'):
                        membership='钻石品牌通'
                    pbusiness=subString(filter_tags(attrs['pbusiness']),150)
                    parea_province=attrs['parea_province']
                    ldbphone=getldbphone(id)
                    list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'membership':membership,'viptype':viptype,'ldbphone':ldbphone}
                    listall_comp.append(list1)
                listcount_comp=res['total_found']
        return {'list':listall_comp,'count':listcount_comp}
                
    #获得该市场供求
    
            
            