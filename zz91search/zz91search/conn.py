from zz91conn import *
conn = database_comp()   
cursor = conn.cursor()
conn_ads = database_ads()
cursor_ads = conn_ads.cursor()
conn_news = database_news()