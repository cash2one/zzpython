import MySQLdb,sys
from MySQLdb.cursors import DictCursor,BaseCursor
from DBUtils.PooledDB import PooledDB
reload(sys)
sys.setdefaultencoding('UTF-8')
def opendb():
    #db = MySQLdb.connect(user='zz91crm', db='zz91crm', passwd='zJ88friend', host='192.168.2.4', charset="utf8")
    __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=5 ,maxconnections=5,maxshared=10,
                              host='192.168.2.4' , port=3306 , user='zz91crm' , passwd='zJ88friend',
                              db='zz91crm',use_unicode=False,charset='utf8')
    return __pool.connection()

def opendb1():
    #db = MySQLdb.connect(user='zz91crm', db='zz91crm', passwd='zJ88friend', host='192.168.2.4', charset="utf8")
    __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=5 ,maxconnections=5,maxshared=10,
                              host='192.168.2.4' , port=3306 , user='zz91crm' , passwd='zJ88friend',
                              db='astoweb',use_unicode=False,charset='utf8')
    return __pool.connection()

def opendbserver():
    __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=5 ,maxconnections=5,maxshared=10,
                              host='rdsuo5342fhte95enp5ipublic.mysql.rds.aliyuncs.com' , port=3398 , user='ast' , passwd='astozz91jiubao',
                              db='ast',use_unicode=False,charset='utf8')
    return __pool.connection()
    #return db
def opendb_rt():
    #db = MySQLdb.connect(host="192.168.2.4", user="root", passwd="zj88friend", port=9306,charset="utf8")
    #return db
    __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=5 ,maxconnections=5,maxshared=10,
                              host='192.168.2.4' , user='root' , passwd="zj88friend", port=9306,charset="utf8")
    return __pool.connection()
class crmdb:
    #----初始化数据库连接
    def __init__(self,dbtype=""):
        if not dbtype:
            self.conn=opendb()
        if dbtype=="astoweb":
            self.conn=opendb1()
        if dbtype=="local":
            self.conn=opendb()
        if dbtype=="server":
            self.conn=opendbserver()
        self.cursor=self.conn.cursor(cursorclass = DictCursor)
    #----更新到数据库
    def updatetodb(self,sql,argument):
        self.cursor.execute(sql,argument)
        self.cursor.execute('SELECT last_insert_id() as id')
        result=self.cursor.fetchone()
        self.conn.commit()
        if result:
            return result
    #----查询所有数据
    def fetchalldb(self,sql,argument=''):
        if argument:
            self.cursor.execute(sql,argument)
        else:
            self.cursor.execute(sql)
        resultlist=self.cursor.fetchall()
        if resultlist:
            return resultlist
        else:
            return []
    #----查询一条数据
    def fetchonedb(self,sql,argument=''):
        if argument:
            self.cursor.execute(sql,argument)
        else:
            self.cursor.execute(sql)
        result=self.cursor.fetchone()
        if result:
            return result
    #----查询一条总数
    def fetchnumberdb(self,sql,argument=''):
        if argument:
            self.cursor.execute(sql,argument)
        else:
            self.cursor.execute(sql)
        result=self.cursor.fetchone()
        if result:
            return result['count(0)']
        else:
            return 0
    #----关闭连接
    def closedb(self):
        self.conn.close()
    #----数据事物回滚
    def rollbackdb(self):
        self.conn.rollback()