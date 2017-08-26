#-*- coding:utf-8 -*-
class zz91other:
    def __init__ (self):
        from zz91conn import database_other
        self.conn_other=database_other()
        self.cursor_other=self.conn_other.cursor()
    def addwebartical(self,title,litpic,weburl,typeid,content,gmt_created,updatetime,sortrank,wtype):
        sql='insert into website(name,pic,url,typeid,content,gmt_created,updatetime,sortrank,wtype) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor_other.execute(sql,[title,litpic,weburl,typeid,content,gmt_created,updatetime,sortrank,wtype])
        self.conn_other.commit()
    def updateartical(self,title,litpic,weburl,typeid,content,updatetime,sortrank,wtype,artid):
        sql='update website set name=%s,pic=%s,url=%s,typeid=%s,content=%s,updatetime=%s,sortrank=%s,wtype=%s where id=%s'
        self.cursor_other.execute(sql,[title,litpic,weburl,typeid,content,updatetime,sortrank,wtype,artid])
        self.conn_other.commit()
        
    def getsearch_keywords(self,frompageCount,limitNum,pagetype='',gmt_begin='',gmt_end=''):
        sql1='select count(0) from search_keywords where id>0'
        sql='select id,webtype,keywords,ip,gmt_created,numb from search_keywords where id>0'
        argument=[]
        if pagetype:
            sql=sql+' and webtype=%s'
            sql1=sql1+' and webtype=%s'
            argument.append(pagetype)
        if gmt_begin and gmt_end:
            sql=sql+' and gmt_created>=%s and gmt_created<=%s'
            sql1=sql1+' and gmt_created>=%s and gmt_created<=%s'
            argument.append(gmt_begin)
            argument.append(gmt_end)
            sql1=sql1.replace('count(0)', 'count(distinct keywords)')
            sql=sql.replace('numb', 'sum(numb)')
            sql=sql+' group by keywords'
        sql=sql+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            self.cursor_other.execute(sql1,argument)
        else:
            self.cursor_other.execute(sql1)
        result=self.cursor_other.fetchone()
        if result:
            count=result[0]
        else:
            count=0
        if argument:
            self.cursor_other.execute(sql,argument)
        else:
            self.cursor_other.execute(sql)
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                typeid=result[1]
                typename=self.gettypename(typeid)
                list={'id':result[0],'typeid':typeid,'typename':typename,'keywords':result[2],'ip':result[3],'gmt_created':formattime(result[4],1),'numb':result[5]}
                listall.append(list)
        return {'list':listall,'count':count}
    def addsearch_keywords(self,webtype,keywords,ip,gmt_created,detailtime,numb):
        sql1='select id,ip,numb from search_keywords where keywords=%s and gmt_created=%s'
        self.cursor_other.execute(sql1,[keywords,gmt_created])
        result=self.cursor_other.fetchone()
        if result:
            id=result[0]
            ip1=result[1]
            ip=ip1+','+ip
            numb1=result[2]
            numb=numb1+numb
            sql='update search_keywords set ip=%s,numb=%s where id=%s'
            self.cursor_other.execute(sql,[ip,numb,id])
        else:
            sql='insert into search_keywords(webtype,keywords,ip,gmt_created,detailtime,numb) values(%s,%s,%s,%s,%s,%s)'
            self.cursor_other.execute(sql,[webtype,keywords,ip,gmt_created,detailtime,numb])
        self.conn_other.commit()
    def getpagerundetail(self,id):
        sql='select typeid,in_page_ip from dataanalysis_page where id=%s'
        self.cursor_other.execute(sql,[id])
        result=self.cursor_other.fetchone()
        if result:
            typeid=result[0]
            typename=self.gettypename(typeid)
            iplist=result[1]
            list={'typeid':typeid,'typename':typename,'iplist':iplist.split(',')}
            return list
    def getpagenextdetail(self,upid):
        sql='select id,typeid,numb,gmt_created from data_pagerun where upid=%s order by id'
        self.cursor_other.execute(sql,[upid])
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                typeid=result[1]
                typename=self.gettypename(typeid)
                list={'id':result[0],'typeid':typeid,'typename':typename,'numb':result[2],'gmt_created':result[3]}
                listall.append(list)
        return listall

    #----获得多级栏目嵌套
    def getalltypelist(self,wtype):
        listall=[]
        sql='select id,typename from webtype where wtype=%s'
        self.cursor_other.execute(sql,[wtype])
        resultlist=self.cursor_other.fetchall()
        if resultlist:
            for result in resultlist:
                listall2=[]
                id=result[0]
                resultlist2=self.getnexttype(id)
                if resultlist2:
                    for result2 in resultlist2:
                        listall3=[]
                        id2=result2['id']
                        listall3=self.getnexttype(id2)
                        list2={'id':id2,'typename':result2['typename'],'typelist':''}
                        if listall3:
                            list2['typelist']=listall3
                        listall2.append(list2)
                list={'id':id,'typename':result[1],'typelist':''}
                if listall2:
                    list['typelist']=listall2
                listall.append(list)
        return listall
    def getnexttype(self,typeid):
        listall=[]
        sql='select id,typename from webtype where reid=%s'
        self.cursor_other.execute(sql,[typeid])
        resultlist=self.cursor_other.fetchall()
        if resultlist:
            for result in resultlist:
                id=result[0]
                listweb=[]
                list={'id':id,'typename':result[1]}
                listall.append(list)
        return listall
    def getaccountip(self,account):
        sql='select a.numb from data_ip as a,data_account as b where a.account_id=b.id and b.numb=%s'
        self.cursor_other.execute(sql,[account])
        result=self.cursor_other.fetchone()
        if result:
            return result[0]
    def getvisiturl(self,frompageCount,limitNum,account,arg=''):
        if arg==1:
            ip=self.getaccountip(account)
            sql1='select count(0) from data_visiturl where ip=%s'
            self.cursor_other.execute(sql1,[ip])
        else:
            sql1='select count(0) from data_visiturl where account=%s'
            self.cursor_other.execute(sql1,[account])
        result1=self.cursor_other.fetchone()
        if result1:
            count=result1[0]
        else:
            count=0
        if arg==1:
            sql='select url,urltime,gmt_created from data_visiturl where ip=%s order by urltime desc limit '+str(frompageCount)+','+str(limitNum)
            self.cursor_other.execute(sql,[ip])
        else:
            sql='select url,urltime,gmt_created from data_visiturl where account=%s order by urltime desc limit '+str(frompageCount)+','+str(limitNum)
            self.cursor_other.execute(sql,[account])
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'url':result[0],'urltime':formattime(result[1]),'gmt_created':formattime(result[2],1)}
                listall.append(list)
        return {'list':listall,'count':count}

    def deldata(self,gmt_created,gmt_created2):
        sql='delete from dataanalysis_page where gmt_created>=%s and gmt_created<=%s'
        self.cursor_other.execute(sql,[gmt_created,gmt_created2])
        sql='delete from data_pagerun where gmt_created>=%s and gmt_created<=%s'
        self.cursor_other.execute(sql,[gmt_created,gmt_created2])
        self.conn_other.commit()
        
    def delipvisit(self,gmt_created,gmt_created2):
        sql='delete from data_ipvisit where gmt_created>=%s and gmt_created<=%s'
        self.cursor_other.execute(sql,[gmt_created,gmt_created2])
        self.conn_other.commit()
    def deldatasis(self,id):
        sql='delete from dataanalysis where id=%s'
        self.cursor_other.execute(sql,[id])
        self.conn_other.commit()
    def getstatistics_page(self,gmt_created='',pubdate='',pubdate2=''):
        sql='select id,typeid,gmt_created,sum(in_page),sum(out_page),sum(log_page),sum(reg_page),in_page_ip from dataanalysis_page where id>0'
        argument=[]
        if gmt_created:
            sql=sql+' and gmt_created=%s'
            argument.append(gmt_created)
        else:
#            sql="select id,typeid,gmt_created,sum(in_page),sum(out_page),sum(log_page),sum(reg_page) from dataanalysis_page where gmt_created between %s and %s group by typeid"
            if pubdate:
                argument.append(pubdate)
                sql=sql+' and gmt_created>=%s'
            if pubdate2:
                argument.append(pubdate2)
                sql=sql+' and gmt_created<=%s'
        sql=sql+' group by typeid'
        sql=sql+' order by typeid'
        if pubdate and pubdate2:
            self.cursor_other.execute(sql,argument)
        else:
            return ''
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                typeid=result[1]
                typename=self.gettypename(typeid)
                iplist=result[7]
                if iplist:
                    iplist=iplist.split(',')
                list={'id':result[0],'typeid':typeid,'typename':typename,'gmt_created':formattime(result[2],1),'in_page':result[3],'out_page':result[4],'log_page':result[5],'reg_page':result[6],'iplist':iplist}
                listall.append(list)
        return listall
    def get_pagecount(self):
        sql='select count(0) from dataanalysis_page'
        self.cursor_other.execute(sql)
        result=self.cursor_other.fetchone()
        if result:
            return result[0]/21
    def gettypename(self,id):
        sql='select name from pagetype where id=%s'
        self.cursor_other.execute(sql,[id])
        result=self.cursor_other.fetchone()
        if result:
            return result[0]
    def getpagedetail(self,wherepage,typeid,pagecount,gmt_created,gmt_created2):
        sql='select typeid,numb from data_pagerun where wherepage=%s and reid=%s and pagecount=%s and gmt_created>=%s and gmt_created<=%s'
        self.cursor_other.execute(sql,[wherepage,typeid,pagecount,gmt_created,gmt_created2])
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                typeid=result[0]
                typename=self.gettypename(typeid)
                list={'typeid':typeid,'numb':result[1],'typename':typename}
                listall.append(list)
        return listall
    def gettypelist(self,frompageCount,limitNum):
        sql1='select count(0) from pagetype'
        self.cursor_other.execute(sql1)
        result1=self.cursor_other.fetchone()
        if result1:
            count=result1[0]
        else:
            count=0
        sql='select id,name,url from pagetype order by id'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        self.cursor_other.execute(sql)
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'name':result[1],'url':result[2]}
                listall.append(list)
        return {'list':listall,'count':count}
    def gettypelist2(self,idlist):
        sql='select id,name,url from pagetype where id in %s'
        self.cursor_other.execute(sql,[idlist])
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'name':result[1],'url':result[2]}
                listall.append(list)
        return listall
    def getjumpoutlist(self):
        sql1='select count(0) from jumpout'
        self.cursor_other.execute(sql)
        result1=self.cursor_other.fetchone()
        if result1:
            count=result[0]
        else:
            count=0
        sql='select id,gmt_created,reg,login,propub,comprice from jumpout limit 0,10'
        self.cursor_other.execute(sql)
        resultlist=self.cursor_other.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'gmt_created':result[1]}
                listall.append(list)
        return {'list':listall,'count':count}
    def getdatalist(self,frompageCount='',limitNum='',pubdate='',pubdate2=''):
        sql1='select count(0) from dataanalysis where id>0'
        argument=[]
        if pubdate:
            sql1=sql1+' and gmt_created>=%s'
            argument.append(pubdate)
        if pubdate2:
            sql1=sql1+' and gmt_created<=%s'
            argument.append(pubdate2)
        if argument:
            self.cursor_other.execute(sql1,argument)
        else:
            self.cursor_other.execute(sql1)
        result1=self.cursor_other.fetchone()
        if result1:
            count=result1[0]
        else:
            count=0
        listall=[]
        sql='select id,all_ipcount,reg_count,noreg_count,gmt_created,alr_count from dataanalysis where id>0'
        argument=[]
        if pubdate:
            sql=sql+' and gmt_created>=%s'
            argument.append(pubdate)
        if pubdate2:
            sql=sql+' and gmt_created<=%s'
            argument.append(pubdate2)
        sql=sql+' order by gmt_created desc'
        if limitNum:
            sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            self.cursor_other.execute(sql,argument)
        else:
            self.cursor_other.execute(sql)
        resultlist=self.cursor_other.fetchall()
        if resultlist:
            for result in resultlist:
                conversion=str(float(result[2])/(result[3]+result[2])*100)+"%"
                list={'id':result[0],'all_ipcount':result[1],'reg_count':result[2],'noreg_count':result[3],'gmt_created':formattime(result[4],1),'conversion':conversion,'alr_count':result[5]}
                listall.append(list)
        return {'list':listall,'count':count}
    def yearlogin(self,year):
        sql='select count from yearlogin where year=%s'
        self.cursor_other.execute(sql,[year])
        result1=self.cursor_other.fetchone()
        if result1:
            return result1[0]
    def getwebsitelist(self,frompageCount,limitNum,typeid='',recommend='',wtype='',order='',desc=''):
        sql1='select count(0) from website where isdelete=0'
        if typeid:
            sql1=sql1+' and typeid='+str(typeid)
        if wtype:
            sql1=sql1+' and wtype='+str(wtype)
        if recommend:
            sql1=sql1+' and recommend='+str(recommend)
        self.cursor_other.execute(sql1)
        result1=self.cursor_other.fetchone()
        if result1:
            count=result1[0]
        else:
            count=0
        listall=[]
        sql='select id,typeid,name,url,pic,gmt_created,sortrank,recommend from website where isdelete=0'
        if typeid:
            sql=sql+' and typeid='+str(typeid)
        if wtype:
            sql=sql+' and wtype='+str(wtype)
        if recommend:
            sql=sql+' and recommend='+str(recommend)
        if order:
            if desc==None:
                sql=sql+' order by '+order+' desc'
            else:
                sql=sql+' order by '+order+' '+desc
        else:
            sql=sql+' order by sortrank,updatetime desc,gmt_created desc'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        self.cursor_other.execute(sql)
        resultlist=self.cursor_other.fetchall()
        js=1
        if resultlist:
            for result in resultlist:
                typeid1=result[1]
                js=js+1
#                typename=gettypedetail(typeid1)['typename']
                list={'id':result[0],'typeid':typeid1,'typename':'','name':result[2],'url':result[3],'pic':result[4],'gmt_created':formattime(result[5],1),'sortrank':result[6],'recommend':result[7],'js':js}
                listall.append(list)
        return {'list':listall,'count':count}
    def getipvisit(self,pubdate='',pubdate2=''):
        sql1='select count(0) from data_ipvisit where id>0'
        sql='select pagecount,sum(allip),sum(loginip),sum(notloginip),gmt_created,sortrank from data_ipvisit where id>0'
        argument=[]
        if pubdate:
            argument.append(pubdate)
            sql=sql+' and gmt_created>=%s'
            sql1=sql1+' and gmt_created>=%s'
        if pubdate2:
            argument.append(pubdate2)
            sql=sql+' and gmt_created<=%s'
            sql1=sql1+' and gmt_created<=%s'
        sql=sql+' group by pagecount order by sortrank'
        self.cursor_other.execute(sql1,argument)
        result1=self.cursor_other.fetchone()
        if result1:
            count=result1[0]
        else:
            count=0
        listall=[]
        self.cursor_other.execute(sql,argument)
        resultlist=self.cursor_other.fetchall()
        if resultlist:
            for result in resultlist:
                pagecount=result[0]
                allip=result[1]
                loginip=result[2]
                notloginip=result[3]
                sortrank=result[4]
                if pagecount==u'IP总数':
                    allip=str(int(allip))+' 个'
                    loginip=str(int(loginip))+' 个'
                    notloginip=str(int(notloginip))+' 个'
                elif pagecount == u'平均页面访问量':
                    allip=str(allip)+' 个'
                    loginip=str(loginip)+' 个'
                    notloginip=str(notloginip)+' 个'
                else:
                    allip=str(allip)+'%'
                    loginip=str(loginip)+'%'
                    notloginip=str(notloginip)+'%'
                list={'pagecount':pagecount,'allip':allip,'loginip':loginip,'notloginip':notloginip,'gmt_created':formattime(result[4],1)}
                listall.append(list)
        return {'list':listall,'count':count}
    
