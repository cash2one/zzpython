﻿conn = MySQLdb.connect(host='192.168.110.118', user='ast', passwd='astozz91jiubao',db='ast',charset='utf8')   
cursor = conn.cursor()
conn_my = MySQLdb.connect(host='192.168.110.118', user='kang', passwd='astozz91jiubao',db='ast',charset='utf8')
cursor_my=conn_my.cursor()
conn_tags = MySQLdb.connect(host='192.168.110.118', user='zztags', passwd='FJfAFLFcb95xTZ9m',db='zztags',charset='utf8')
cursor_tags=conn_tags.cursor()
conn_ads = MySQLdb.connect(host='192.168.110.118', user='zzads', passwd='aJuUVbChYJ57t2SX',db='zzads',charset='utf8')
cursor_ads = conn_ads.cursor()
conn_news = MySQLdb.connect(host='192.168.110.2', user='zz91news', passwd='4ReLhW3QLyaaECzU',db='zz91news',charset='utf8')
cursor_news = conn.cursor()

def closeconn():
	cursor.close()
	cursor_my.close()
	cursor_tags.close()
	cursor_ads.close()
	cursor_news.close()