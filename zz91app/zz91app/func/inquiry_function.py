#-*- coding:utf-8 -*-
class zzinquiry:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getleavewordsnumb(self,account):
        #获得缓存
        #zz91app_getleavewordsnumb=cache.get("zz91app_getleavewordsnumb"+str(account))
        #if zz91app_getleavewordsnumb:
            #return zz91app_getleavewordsnumb
        sql="select count(0) from inquiry where receiver_account=%s and is_viewed=0"
        count=self.dbc.fetchnumberdb(sql,[account])
        #设置缓存
        #cache.set("zz91app_getleavewordsnumb"+str(account),list,60*3)
        return count
    def getleavewordnew(self,account):
        sql='select content from inquiry where receiver_account=%s and is_viewed=0 order by send_time desc'
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    #询盘留言列表 翻页
    def getleavewordslist(self,frompageCount=0,limitNum=1,group="",scomid='',rcomid='',comtype='',is_viewed=''):
        listall=[]
        listcount=0
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if group:
            cl.SetGroupBy( 'scomid',SPH_GROUPBY_ATTR )
        if scomid:
            cl.SetFilter('scomid',[int(scomid)])
        if rcomid:
            cl.SetFilter('rcomid',[int(rcomid)])
        if comtype=='1':
            cl.SetFilter('scomid',[181475],True)
        if is_viewed:
            cl.SetFilter('is_viewed',[int(is_viewed)])
        cl.SetSortMode( SPH_SORT_EXTENDED,"qid desc" )
        cl.SetLimits (frompageCount,limitNum,20000)
        res = cl.Query ('','question')
        if res:
            if res.has_key('matches'):
                listcount=res['total_found']
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    list=self.getleavewords(id)
                    if limitNum==1:
                        list['txt']='最新询盘信息'
                        list['count']=listcount
                        return list
                    listall.append(list)
        if limitNum==1:
            return ''
        return {'list':listall,'count':listcount}
    #mongodb 留言
    def getchatlist(self,frompageCount=0,limitNum=1,scomid='',rcomid=''):
        sqlarg=''
        argument=[]
        if rcomid and scomid:
            a=1
        else:
            return None
        if int(scomid)>int(rcomid):
            chatgroup=str(scomid)+"-"+str(rcomid)
        else:
            chatgroup=str(rcomid)+"-"+str(scomid)
        if chatgroup:
            sqlarg+=' and conversation_group=%s'
            argument.append(chatgroup)
        sql1="select count(*) from inquiry where id>0 "+sqlarg
        sql="select id from inquiry where id>0 "+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        gmt_modified=datetime.datetime.now()
        for result in resultlist:
            id=result[0]
            chatarr=chatgroup.replace("-",",")
            
            sqla="select chat_count,id from app_chat where chat_group=%s"
            resultq=self.dbc.fetchonedb(sqla,[chatarr])
            if resultq:
                chat_count=resultq[0]
                cid=resultq[1]
                if chat_count:
                    #更新为已读
                    chat_countlist=eval(chat_count)
                    for ll in chat_countlist:
                        if str(ll)==str(scomid):
                            chat_countlist[ll]=0
                    chat_countarr=str(chat_countlist)
                    sqlb="update app_chat set gmt_modified=%s,chat_count=%s where id=%s"
                    self.dbc.updatetodb(sqlb,[gmt_modified,chat_countarr,cid]);
            
            list=self.getleavewords(id)
            listall.append(list)
        return {'list':listall,'count':count}
    def getleavewords(self,qid):
        #获得缓存
        zz91app_getleavewords=cache.get("zz91app_getleavewords"+str(qid))
        if zz91app_getleavewords:
            return zz91app_getleavewords
        sql="select title,content,send_time,sender_account,id,is_viewed from inquiry where id=%s"
        alist=self.dbc.fetchonedb(sql,qid)
        list=None
        if alist:
            companyarray=self.getcompanyname(alist[3])
            
            list={'id':alist[4],'title':alist[0],'content':alist[1],'is_viewed':alist[5],'stime':formattime(alist[2],0),'companyname':companyarray['companyname'],'company_id':companyarray['company_id'],'contact':companyarray['contact']}
        #设置缓存
        cache.set("zz91app_getleavewords"+str(qid),list,60*10)
        return list
    #获得头像
    def getfacepic(self,company_id):
        sql="select picture_path from bbs_user_profiler where company_id=%s"
        newcode=self.dbc.fetchonedb(sql,[company_id])
        if (newcode == None):
            return '../../image/noavatar.gif'
        else:
            if newcode[0]:
                return 'http://img3.zz91.com/200x15000/'+newcode[0]
            else:
                return '../../image/noavatar.gif'
    #获得公司名称
    def getcompanyname(self,uname):
        #获得缓存
        #zz91app_getcompanyname=cache.get("zz91app_getcompanyname"+str(uname))
        #if zz91app_getcompanyname:
        #    return zz91app_getcompanyname
        sql="select company_id,contact,sex from company_account where account=%s"
        newcode=self.dbc.fetchonedb(sql,[uname])
        if (newcode):
            company_id=newcode[0]
            contact=newcode[1]
            sex=newcode[2]
            facepic=self.getfacepic(company_id)
            if str(sex)=="0":
                if ("先生" not in contact) and ("女士" not in contact):
                    contact+="先生"
            else:
                if ("先生" not in contact) and ("女士" not in contact):
                    contact+="女士"
            sqlc="select name from company where id=%s"
            clist=self.dbc.fetchonedb(sqlc,[company_id])
            if clist:
                #设置缓存
                list={'company_id':company_id,'companyname':clist[0],'contact':"<img src='"+facepic+"' comid='"+str(company_id)+"' />"+contact,'facepic':facepic}
                #cache.set("zz91app_getcompanyname"+str(uname),list,60*10)
                return list
    #获得用户登录信息
    def getcompanylogininfo(self,company_id='',account=''):
        if account:
            sql="select company_id,account,contact,sex from company_account where account=%s"
            listc=dbc.fetchonedb(sql,[account])
        if company_id:
            sql="select company_id,account,contact,sex from company_account where company_id=%s"
            listc=dbc.fetchonedb(sql,[company_id])
        if listc:
            company_id=listc[0]
            contact=listc[2]
            sex=listc[3]
            if str(sex)=="0":
                if ("先生" not in contact) and ("女士" not in contact):
                    contact+="先生"
            else:
                if ("先生" not in contact) and ("女士" not in contact):
                    contact+="女士"
            return {'company_id':company_id,'contact':contact}