#import MySQLdb
from zz91conn import database_aqsiq
def database():
    conn = database_aqsiq()
    cursor = conn.cursor()
    return cursor
def closedatabase(cursor):
    cursor.close()
    conn.close()