from zz91conn import *
conn = database_comp()
conn_work = database_work()
conn_ad = database_ads()

cursor = conn.cursor()
cursor_work = conn_work.cursor()
cursor_ad = conn_ad.cursor()
conn_other = database_other()
cursor_other = conn_other.cursor()
conn_news = database_news()
cursor_news = conn.cursor()


def closeconn():
	cursor.close();
	#cursor_work.close();
	#cursor_ads.close();