from zz91conn import database_shebei
def database():
    #conn = MySQLdb.connect(host='192.168.2.40', user='root', passwd='10534jun',db='feiliao123',charset='utf8')
    #return conn
    conn = database_shebei()
    return conn