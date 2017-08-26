#-*- coding:utf-8 -*-
class zz91log:
    def __init__ (self):
        from zz91conn import database_log
        self.conn_log=database_log()
        self.cursor_log=self.conn_log.cursor()
    def getloglist(self,frompageCount,limitNum,status="",ip="",website="",gmt_begin="",gmt_end=""):
        sqlcount="select count(0) from nginx_log where id>0 "
        sql="select id,ipP,timeP,requestP,statusP,bodyBytesSentP,referP,userAgentP,uesreP,syeP,province,website from nginx_log where id>0 "
        
        argument=[]
        if status:
            sql+=" and statusP=%s"
            sqlcount+=" and statusP=%s"
            argument.append(status)
        if ip:
            sql+=" and ipP=%s"
            sqlcount+=" and ipP=%s"
            argument.append(ip)
        if website:
            sql+=" and website=%s"
            sqlcount+=" and website=%s"
            argument.append(website)
        if gmt_begin:
            sql+=" and timeP>=%s"
            sqlcount+=" and timeP>=%s"
            argument.append(gmt_begin)
        if gmt_end:
            sql+=" and timeP<=%s"
            sqlcount+=" and timeP<=%s"
            argument.append(gmt_end)
        sql+=" order by id desc limit "+str(frompageCount)+","+str(limitNum)+" "
        if argument:
            self.cursor_log.execute(sqlcount,argument)
        else:
            self.cursor_log.execute(sqlcount)
        result=self.cursor_log.fetchone()
        if result:
            count=result[0]
        else:
            count=0
        if argument:
            self.cursor_log.execute(sql,argument)
        else:
            self.cursor_log.execute(sql)
        resultlist=self.cursor_log.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                ipP=result[1]
                province=result[10]
                timeP=formattime(result[2])
                requestP=result[3]
                statusP=result[4]
                bodyBytesSentP=result[5]
                referP=result[6]
                referP=referP[1:-1]
                requestParr=requestP.split(" ")
                website=result[11]
                if len(requestParr)>1:
                    requestP=requestParr[1]
                    requestPurl="http://"+website+requestParr[1]
                userAgentP=result[7]
                uesreP=result[8]
                syeP=result[9]
                list={'id':id,'ipP':ipP,'timeP':timeP,'requestP':requestP,'requestPurl':requestPurl,'statusP':statusP,'bodyBytesSentP':bodyBytesSentP,'referP':referP,'userAgentP':userAgentP,'uesreP':uesreP,'syeP':syeP,'province':province,'website':website}
                listall.append(list)
        return {'list':listall,'count':count}
    
        