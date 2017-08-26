#-*- coding:utf-8 -*-
import settings
from zz91db_ast import companydb
from zz91settings import SPHINXCONFIG
from sphinxapi import *

dbc=companydb()

def getpriceattrpinyin(label):
    sql='select pinyin from price_category_attr where label=%s'
    result=dbc.fetchonedb(sql,[label])
    if result:
        return result[0]
    return ''

def getpricecategorydetail(id):
    sql='select name,pinyin from price_category where id=%s'
    result=dbc.fetchonedb(sql,[id])
    list={'name':'','pinyin':''}
    if result:
        list={'name':result[0],'pinyin':result[1]}
    return list

#----报价列表
def getprlist(frompageCount,limitNum,maxcount=100000,kname='',category_id='',assist_id='',categoryname='',arg=''):
    price=SPHINXCONFIG['name']['price']['name']
    serverid=SPHINXCONFIG['name']['price']['serverid']
    port=SPHINXCONFIG['name']['price']['port']
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    if category_id:
        cl.SetFilter('type_id',category_id)
    if assist_id:
        cl.SetFilter('assist_type_id',assist_id)
    cl.SetGroupBy( 'type_id',SPH_GROUPBY_ATTR )
#    cl.SetGroupBy( 'assist_type_id',SPH_GROUPBY_ATTR )
    cl.SetLimits (frompageCount,limitNum,maxcount)
    if kname:
        if '|' in kname:
            querysty=''
            knamelist=kname.split('|')
            for knm in knamelist:
                querysty+='|@(title,tags,content_query) "'+knm+'"'
            querysty=querysty[1:]
            res = cl.Query (querysty,price)
        else:
            res = cl.Query ('@(title,tags,content_query) '+kname,price)
    else:
        res = cl.Query ('',price)
    listall_baojia=[]
    listcount_baojia=0
    js=0
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            for match in tagslist:
                td_id=match['id']
                attrs=match['attrs']
                type_id=attrs['type_id']
                title=attrs['ptitle']
                assist_type_id=attrs['assist_type_id']
#                assist_typedetail=getpricecategorydetail(assist_type_id)
#                assist_type=assist_typedetail['name']
                type_pinyin=getpriceattrpinyin(type_id)
                pricecategorydetail=getpricecategorydetail(type_id)
                pricecategory=pricecategorydetail['name']
                pinyin=pricecategorydetail['pinyin']
#                print type_id
#                print assist_type
#                print title
                if pricecategory and pinyin:
                    print assist_type_id
                    print pricecategory
                    print pinyin
                    
                    parent_id=1
                    price_category_id=assist_type_id
                    label=pricecategory
                    sortrank=50
                    
#                    sql='insert into price_category_attr(parent_id,price_category_id,label,pinyin,sortrank) values(%s,%s,%s,%s,%s)'
#                    dbc.updatetodb(sql,[parent_id,price_category_id,label,pinyin,sortrank])
#                    break

def getsonclist(id):
    sql='select id from price_category where parent_id=%s'
    resultlist=dbc.fetchalldb(sql,[id])
    listall=[]
    for result in resultlist:
        try:
            listall.append(result[0])
        except:
            pass
    return listall

def getpriceareapro():
    '''
    listall=getsonclist(17)
    for list in listall:
        getprlist(0,200,200,'',[list],'','')
    '''
    getprlist(0,200,200,'','',[298])

if __name__=="__main__":
    getpriceareapro()