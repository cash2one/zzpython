#-*- coding:utf-8 -*-
import datetime
from _mysql import result
#from maps_zz91.commfunction import sql1
class zye:
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
        sql="select id,name,area,industry,category,business,introduction,address,company_num,product_num,words from market where is_del=0"+sqlarg+' order by company_num desc '
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
        if industry:
            sqlarg+=' and industry=%s'
            argument.extend([industry])
        if category:
            sqlarg+=' and category=%s'
            argument.extend([category])
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
    #获得一张图片   
    def getonepicture(self,id):
        #若已设置默认图片
        pic_address=None
        sql='select pic_address from market_pic where market_id=%s and is_default=1 and check_status=1'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            pic_address=result[0]
        else:
            #未设置默认则依据更新时间选择一张
            sql1='select pic_address from market_pic where market_id=%s and check_status=1 order by gmt_created desc limit 0,1'
            result=self.dbc.fetchonedb(sql1,[id])
            if result:
                pic_address=result[0]
        if pic_address:
            return "http://img3.zz91.com/300x15000/"+pic_address
        else:
            return "http://img0.zz91.com/front/images/global/noimage.gif"
    #获取多张图片
    def getmanypicture(self,id):
        sql='select pic_address from market_pic where market_id=%s and check_status=1'
        resultlist=self.dbc.fetchalldb(sql,[id])
        listall=[]
        if resultlist:
            for result in resultlist:
                pic_address=result[0]
                if pic_address:
                    pic_address= "http://img3.zz91.com/300x15000/"+pic_address
                else:
                    pic_address= "http://img0.zz91.com/front/images/global/noimage.gif"
                list={'pic_address':pic_address}
                listall.append(list)
            return listall
    #获得市场详细
    def getmarketdetail(self,ye_pinyin='',id=''):
        if id:
            sql='select id,name,area,industry,category,business,introduction,address,company_num,product_num from market where id=%s and is_del=0'
            result=self.dbc.fetchonedb(sql,[id])
        else:
            sql='select id,name,area,industry,category,business,introduction,address,company_num,product_num from market where words=%s and is_del=0'
            result=self.dbc.fetchonedb(sql,[ye_pinyin])
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
            pic_img={'pic_address':pic_address}
            industry_code=None
            if industry=="废金属":
                industry_code="1000"
            if industry=="废塑料":
                industry_code="1001"
            if industry=="二手设备":
                industry_code="1002"
            list={"id":id,"name":name,"area":area,"industry":industry,'industry_code':industry_code,"category":category,"business":business,"introduction":introduction,"address":address,"company_num":company_num,"product_num":product_num}
            return {'list':list,'pic_img':pic_img}
    #判断当前用户是否已加入当前的产业带
    def is_in_market(self,market_id,company_id):
        sql='select company_id,is_quit from market_company where market_id=%s'
        resultlist=self.dbc.fetchalldb(sql,[market_id])
        i=0
        is_quit=0
        if resultlist:
            for result in resultlist:
                id=result[0]
                is_quit=result[1]
                #如果存在
                if company_id==id:
                    i=1
                    
                break
            return (i,is_quit)
        return (i,is_quit)    
        
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
        #判断是否是以前加入过但退出的用户
        sql0='select is_quit from market_company where market_id=%s and company_id=%s'
        resultlist=self.dbc.fetchonedb(sql0,[market_id,company_id])
        ex=0
        if resultlist:
            is_quit=result[1]
            #若以前加入过则update
            gmt_modified=datetime.datetime.now()
            sql='update market_company set is_quit=0,gmt_modified=%s where  market_id=%s and company_id=%s'
            self.dbc.updatetodb(sql,[gmt_modified,market_id,company_id])
        #否则insert
        else:
            gmt_created=datetime.datetime.now()  
            gmt_modified=datetime.datetime.now()
            sql='insert into market_company (market_id,company_id,gmt_created,gmt_modified) values (%s,%s,%s,%s)'
            self.dbc.updatetodb(sql,[market_id,company_id,gmt_created,gmt_modified])
            #market表中company_num加一
            sql2='update market set company_num=company_num+1 where id=%s '
            self.dbc.updatetodb(sql2,[market_id])

    #退出市场
    def quit_market(self,company_id,market_id):
        gmt_modified=datetime.datetime.now()
        sql='update market_company set is_quit=1,gmt_modified=%s where company_id=%s and market_id=%s'
        self.dbc.updatetodb(sql,[gmt_modified,company_id,market_id])
        #market表中company_num减一
        sql1='select company_num from market where id=%s'
        result=self.dbc.fetchonedb(sql1,[market_id])
        if result:
            company_num=result[0]
            company_num=company_num-1
            sql2='update market set company_num=%s where id=%s'
            self.dbc.updatetodb(sql2,[company_num,market_id])
    #市场供求
    def getyeproductslist(self,frompageCount,limitNum,market_id=''):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetFilter('is_del',[0])
        cl.SetFilter('is_pause',[0])
        cl.SetFilter('check_status',[1])
        cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
        cl.SetLimits (frompageCount,limitNum,20000)
        if market_id:
            res = cl.Query ('@(market_list) ,'+str(market_id)+',','product_market')
        else:
            res = cl.Query ('','product_market')
        listcount_comp=0
        listall_comp=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    product_id=attrs['product_id']
                    list=getcompinfo(product_id,'','')
                    listall_comp.append(list)
                listcount_comp=res['total_found']
        return {'list':listall_comp,'count':listcount_comp}
    #获得该市场的商户信息
    def getcompanylist(self,frompageCount,limitNum,market_id=''):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if market_id:
            cl.SetFilter('market_id',[int(market_id)])
        cl.SetFilter('is_block',[0])
        cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
        cl.SetLimits (frompageCount,limitNum,20000)
        res = cl.Query ('','company_market')
        listcount_comp=0
        listall_comp=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    company_id=attrs['company_id']
                    list=getcompanydetail(company_id)
                    listall_comp.append(list)
                listcount_comp=res['total_found']
        return {'list':listall_comp,'count':listcount_comp}
    