import MySQLdb

def database():
    #conn = MySQLdb.connect(host='192.168.2.40', user='root', passwd='10534jun',db='seocompany',charset='utf8')
    #return conn
    conn = MySQLdb.connect(host='192.168.2.10', user='seocompany', passwd='Gs8FXT6szWNqDhG8',db='seocompany',charset='utf8')
    return conn
    

