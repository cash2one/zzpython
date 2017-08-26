from zz91conn import *
conn = database_comp()
conn_work = database_work()
conn_ads = database_ads()
conn_news = database_news()
cursor_news = conn_news.cursor()
cursor = conn.cursor()
conn_other = database_other()
cursor_other = conn_other.cursor()
conn_ep = database_huanbao()
def getlocalIP():
	return "192.168.2.2"
def closeconn():
	cursor.close()
	cursor_news.close()
	conn_other.close()
	cursor_other.close()
	cursor.close()
	conn.close()
	conn_work.close()
	conn_ads.close()
	conn_news.close()
	conn_ep.close()
	

#mc = memcache.Client([settings.memcacheconfig],debug=0)
#mc2 = memcache.Client(['192.168.110.114:11211'],debug=0)