#!/usr/bin/env python   
#coding=utf-8   
import sys
import time,datetime
import os

reload(sys)
sys.setdefaultencoding('utf-8')
from company import *

#old_huangye()
#old_renshi_assign()
#old_renshi_history()


getcompany("company")
getcompany("company_account")
getcompany("analysis_esite_visit")
#getcompany("auth_user")
getcompany("crm_company_service")
getcompany("crm_service_apply")
getcompany("phone")
getcompany("pay_mobilewallet")
getcompany("oauth_access")
getcompany("pay_order")

qianbaocompany()
updateservice_endtime()
update_salesincome()
update_othercontact()
assigncompanynow()
assigncompany_vap_now()
os.system("/usr/local/coreseek/bin/indexer --config /mnt/pythoncode/zz91crm/coreseek/etc/company.conf company --rotate")