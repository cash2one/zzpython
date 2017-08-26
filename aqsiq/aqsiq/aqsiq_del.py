#-*- coding:utf-8 -*- 
from conn import database
import re

def hand_content(re_py,content):
    urls_pat=re.compile(re_py,re.DOTALL)
    e_content=re.findall(urls_pat,content)
    for e_content in e_content:
        content=content.replace(e_content,'')
    return content

cursor=database()
sql='select id,ntitle,ncontent from aqsiq_news order by id desc limit 20,1'
cursor.execute(sql)
resultlist=cursor.fetchall()
if resultlist:
    for result in resultlist:
        ncontent=result[2]
        ncontent=hand_content(u'具体请咨询.*',ncontent)
        ncontent=hand_content(u'<DIV>乔洪飞先生.*?</DIV>',ncontent)
        ncontent=hand_content(u'<P>高小姐.*',ncontent)
        pcontent=re.findall(u'<P>.*?</P>',ncontent)
        if pcontent:
            ptag=pcontent[-1]
#            print ptag
#            print len(ptag)
            if len(pcontent)>1:
                ncontent=ncontent.replace(ptag,'')
        print ncontent