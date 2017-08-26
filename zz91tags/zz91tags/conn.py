from zz91conn import *
conn = database_comp()   
cursor = conn.cursor()
conn_tags = database_tags()
cursor_tags=conn_tags.cursor()
conn_ads = database_ads()
cursor_ads = conn_ads.cursor()
conn_news = database_news()
cursor_news = conn_news.cursor()

def closeconn():
	cursor.close()
	cursor_tags.close()
	cursor_ads.close()
	cursor_news.close()