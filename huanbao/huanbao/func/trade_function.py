# -*- coding: utf-8 -*-  
class zztrade:
    def __init__(self):
        self.db=db
        
    def gettradesupplylist(self,frompageCount="",limitNum=""):
        argument=[]
        sqlcount="select count(0) as count from trade_supply where id>0"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select id,uid,cid,title,details,category_code,group_id,photo_cover,province_code,area_code,total_num,total_units,price_num,price_units,price_from,price_to,use_to,used_product,tags,tags_sys,details_query,property_query,message_count,view_count,favorite_count,html_path,integrity,gmt_publish,gmt_refresh,valid_days,gmt_expired,del_status,pause_status,check_status,check_admin,check_refuse,gmt_check,gmt_created,gmt_modified,info_come_from from trade_supply where id>0 limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}
    
    def gettradebuylist(self,frompageCount="",limitNum=""):
        argument=[]
        sqlcount="select count(0) as count from trade_buy where id>0"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select id,uid,cid,title,details,category_code,photo_cover,province_code,area_code,buy_type,quantity_year,quantity_untis,supply_area_code,use_to,gmt_confirm,gmt_receive,gmt_publish,gmt_refresh,valid_days,gmt_expired,tags_sys,details_query,message_count,view_count,favorite_count,plus_count,html_path,del_status,pause_status,check_admin,check_refuse,gmt_check,gmt_modified,info_come_from from trade_buy where id>0 limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}
