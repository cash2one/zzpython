from zz91conn import *
conn = database_comp()
cursor = conn.cursor()
conn_tags=database_tags()
cursor_tags=conn_tags.cursor()

def closeconn():
	cursor.close()
	cursor_tags.close()