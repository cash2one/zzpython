from zz91conn import database_astoweb
conn=database_astoweb()
cursor = conn.cursor()
def closeconn():
	cursor.close()