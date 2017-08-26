from zz91conn import database_huanbao
conn = database_huanbao() 
cursor = conn.cursor()
def closeconn():
	cursor.close()
