dbhost="rdsuo5342fhte95enp5i.mysql.rds.aliyuncs.com"
dbport=3306
def database():
    __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=5 ,maxconnections=5,maxshared=10,
                              host=dbhost , port=dbport , user='bsteelmanagement' , passwd='b7TqMWqfr9nxQbEZ',
                              db='bsteelmanagement',use_unicode=False,charset='utf8')
    return __pool.connection()
    #conn = MySQLdb.connect(host='10.171.223.228', user='bsteelmanagement', passwd='b7TqMWqfr9nxQbEZ',db='bsteelmanagement',charset='utf8')
    #return conn
    #conn = MySQLdb.connect(host='192.168.2.10', user='seocompany', passwd='Gs8FXT6szWNqDhG8',db='seocompany',charset='utf8')
    #cursor = conn.cursor()
    #return cursor
    

