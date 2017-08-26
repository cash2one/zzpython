#!/usr/bin/env python   
#coding=utf-8   
import sys
import time,datetime
import os

reload(sys)
sys.setdefaultencoding('utf-8')
from company import *
getcompany("company")
getcompany("company_account")
getcompany("analysis_esite_visit")
getcompany("crm_company_service")
getcompany("crm_service_apply")
getcompany("phone")
getcompany("pay_mobilewallet")
getcompany("oauth_access")
getcompany("pay_order")

updateservice_endtime(day=1)
update_othercontact()
assigncompanynow()
#多余分配给新签
assigncompanynow(user_category_code='1306')
assigncompany_vap_now()
qianbaocompany()

os.system("/usr/local/coreseek/bin/indexer --config /mnt/pythoncode/zz91crm/coreseek/etc/company.conf delta_company --rotate")