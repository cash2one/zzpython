import MySQLdb,re
from conn import database
def getnewslist(ntype,num):
    cursor=database()
    sql="select id,ntitle,ndate from aqsiq_news where ntype=%s limit 0,%s"
    cursor.execute(sql,[ntype,num])
    resultlist=cursor.fetchall()
    listall=[]
    for list in resultlist:
        list={'id':list[0],'ntitle':list[1],'ndate':list[2]}
        listall.append(list)
    return listall

def hand_content(re_py,content):
    urls_pat=re.compile(re_py,re.DOTALL)
    e_content=re.findall(urls_pat,content)
    for e_content in e_content:
        content=content.replace(e_content,'')
    return content