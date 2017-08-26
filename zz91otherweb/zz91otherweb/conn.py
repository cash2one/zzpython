import MySQLdb,sys
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from zz91conn import database_comp
reload(sys)
sys.setdefaultencoding('UTF-8')
class dictzz91astdb:
    #----初始化数据库连接
    def __init__(self):
        self.conn=database_comp()
        self.cursor=self.conn.cursor(cursorclass = DictCursor)
    #----更新到数据库
    def updatetodb(self,sql,argument):
        self.cursor.execute(sql,argument)
        self.cursor.execute('SELECT last_insert_id()')
        result=self.cursor.fetchone()
        self.conn.commit()
        if result:
            return result
        else:
            self.rollbackdb()
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