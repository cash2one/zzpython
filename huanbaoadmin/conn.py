conn_ep = MySQLdb.connect(host='192.168.110.2', user='ep', passwd='4DjeuWecb3CuQWLc',db='ep',charset='utf8')
cursor_ep = conn_ep.cursor()
def closeconn():
	cursor_ep.close();