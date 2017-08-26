from zz91conn import database_help
try:
    conn = database_help()  
    cursor = conn.cursor()
except Exception:
    pass
def closeconn():
    #conn.close()
    #cursor.close()
    return False
    
    
