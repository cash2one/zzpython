from zz91conn import database_astoweb
conn=database_astoweb()
cursor = conn.cursor()
#----更新到数据库
def updateintodb(sql,argument):
    cursor.execute(sql,argument)
    conn.commit()
#----查询所有数据
def fetchalldb(sql,argument=''):
    if argument:
        cursor.execute(sql,argument)
    else:
        cursor.execute(sql)
    resultlist=cursor.fetchall()
    if resultlist:
        return resultlist
    else:
        return []
#----查询一条数据
def fetchonedb(sql,argument=""):
    if argument:
        cursor.execute(sql,argument)
    else:
        cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result
#----查询一条总数
def fetchnumberdb(sql,argument=''):
    if argument:
        cursor.execute(sql,argument)
    else:
        cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0
