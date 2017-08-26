from settings import spconfig,appurl
from sphinxapi import *
from operator import itemgetter, attrgetter


reload(sys)
sys.setdefaultencoding('UTF-8')

def tradeorderby(listall):
    listall = sorted(listall, key=itemgetter(1))
    changeflag="0"
    listallvip1=[]
    listallvip2=[]
    m=0
    for i in listall:
        m+=1
        if (changeflag==str(i[1])):
            list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
            listallvip2.append(list1)
            if (len(listall)==m):
                listallvip1+=listallvip2
        else:
            print listallvip2
            listallvip2=sorted(listallvip2, key=itemgetter(4,2,3),reverse=True)
            listallvip1+=listallvip2
            listallvip2=[]
            list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
            listallvip2.append(list1)
            if (len(listall)==m):
                listallvip1+=listallvip2
        changeflag=str(i[1])
    return listallvip1

cl = SphinxClient()
port = spconfig['port']
cl.SetServer ( spconfig['serverid'], port )
cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
cl.SetLimits (0,100,100)
rescount = cl.Query ( '','offersearch_new_vip')
pcount=0
listall=[]
if rescount:
    if rescount.has_key('matches'):
        tagslist=rescount['matches']
        testcom_id=0
        pcount=0
        for match in tagslist:
            id=match['id']
            com_id=match['attrs']['company_id']
            viptype=match['attrs']['viptype_ldb']
            phone_rate=int(match['attrs']['phone_rate'])
            refresh_time=float(match['attrs']['refresh_time'])
            pdt_date=float(match['attrs']['pdt_date'])
            if (testcom_id==com_id):
                pcount+=1
            else:
                pcount=0
            list1=(id,pcount,viptype,refresh_time,pdt_date,phone_rate)
            listall.append(list1)
            testcom_id=com_id
print tradeorderby(listall)