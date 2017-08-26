from zz91conn import *
conn = database_comp()
conn_work = database_work()
conn_ads = database_ads()
conn_tags = database_tags()
conn_sms = database_sms()

cursor = conn.cursor()
cursor_work = conn_work.cursor()
cursor_ads = conn_ads.cursor()
cursor_tags = conn_tags.cursor()
cursor_sms = conn_sms.cursor()

def getlocalIP():
	return "192.168.2.2"
def closeconn():
	cursor.close();
	cursor_work.close();
	cursor_ads.close();