#!/usr/bin/env python   
#coding=utf-8   
import sys
import time,datetime
import os

reload(sys)
sys.setdefaultencoding('utf-8')
from company import drop_30daynocontact,drop_newcomp

#3天未联系掉公海
drop_newcomp()
#30天未联系掉公海
drop_30daynocontact()
