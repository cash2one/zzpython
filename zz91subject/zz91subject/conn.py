﻿from zz91conn import *
conn = database_comp() 
cursor = conn.cursor()
conn_ad = database_ads()  
cursor_ad = conn_ad.cursor()
conn_sms = database_sms()
cursor_sms = conn_sms.cursor()
conn_tags = database_tags()
cursor_tags=conn_tags.cursor()
conn_other = database_other()
cursor_other=conn_other.cursor()
conn_news = database_news()
cursor_news=conn_news.cursor()
def closeconn():
	cursor.close()
	cursor_ad.close()
	cursor_sms.close()
	cursor_tags.close()