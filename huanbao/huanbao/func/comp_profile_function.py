# -*- coding: utf-8 -*-  
class zzprofile:
    def __init__(self):
        self.db=db

    def getcompprofilelist(self,frompageCount="",limitNum=""):
        argument=[]
        sqlcount="select count(0) as count from comp_profile where id>0"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select id,name,details,industry_code,main_buy,main_product_buy,main_supply,main_product_supply,member_code,business_code,area_code,province_code,legal,funds,main_brand,address,address_zip,domain,domain_two,message_count,view_count,tags,details_query,gmt_created,gmt_modified,del_status,process_method,process,employee_num,developer_num,plant_area,main_market,main_customer,month_output,year_turnover,year_exports,quality_control,register_area,enterprise_type,send_time,receive_time,oper_name from comp_profile where id>0 limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}
