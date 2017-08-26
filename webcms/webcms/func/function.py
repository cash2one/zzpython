#-*- coding:utf-8 -*-
#----清空ftp上面的html缓存
def cleararticalhtml(artid=''):
    sql2='select reid,pinyin from py_user_arttype1 where id=%s'
    sql3='select pinyin from py_user_arttype1 where id=%s'
    sql4='update py_user_artical set is_make=0 where id=%s'
    if artid:
        id=artid
        typeid=dbp.fetchnumberdb('select typeid from py_user_artical where id=%s',[artid])
        result2=dbp.fetchonedb(sql2,[typeid])
        if result2:
            reid=result2[0]
            pinyin=result2[1]
            if reid:
                result3=dbp.fetchonedb(sql3,[reid])
                if result3:
                    repinyin=result3[0]
                    pinyin=repinyin+'/'+pinyin
            filename=str(id)+'.html'
            ftpath=ftpconn['ftpath']['pycms']+'/'+pinyin
            try:
                #pyftp.delfile(ftpath,filename)
                dbp.updatetodb(sql4,[id])
            except:
                pass#没有这个文件'''
    else:
        sql='select id,typeid from py_user_artical where is_del=1 and is_make=1'
        resultlist=dbp.fetchalldb(sql)
        for result in resultlist:
            id=result[0]
            typeid=result[1]
            result2=dbp.fetchonedb(sql2,[typeid])
            if result2:
                reid=result2[0]
                pinyin=result2[1]
                if reid:
                    result3=dbp.fetchonedb(sql3,[reid])
                    if result3:
                        repinyin=result3[0]
                        pinyin=repinyin+'/'+pinyin
                filename=str(id)+'.html'
                ftpath=ftpconn['ftpath']['pycms']+'/'+pinyin
                try:
                    #pyftp.delfile(ftpath,filename)
                    dbp.updatetodb(sql4,[id])
                except:
                    pass#没有这个文件'''
def gethostname(request):
    host = request.META['HTTP_HOST']
    subname=host.split(".")
    subname=subname[0]
    domain=host[len(subname)+1:len(host)]
    return {'subname':subname,'domain':domain}
class zzpycms:
    def __init__(self):
        self.dbp=dbp
    #----用户管理
    def getuserlist(self,frompageCount,limitNum):
        argument=[]
        sqlarg=' from py_user where id>0'
#        if user_id:
#            sqlarg+=' and user_id=%s'
#            argument.append(user_id)
        sql1='select count(0)'+sqlarg
        sql='select id,username,password,sortrank,website'+sqlarg
        sql+=' order by id limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbp.fetchnumberdb(sql1,argument)
        resultlist=self.dbp.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            username=result[1]
            password=result[2]
            sortrank=result[3]
            website=result[4]
            list={'id':id,'username':username,'password':password,'sortrank':sortrank,'website':website}
            listall.append(list)
        return {'list':listall,'count':count}
    def getuser_id(self,username):
        sql='select id from py_user where username=%s'
        result=self.dbp.fetchonedb(sql,[username])
        if result:
            return result[0]
    def getfriendlinklist(self):
        sql='select id,sortrank,url,name,logo,remark from py_friendlink order by sortrank,id desc limit 0,20'
        resultlist=self.dbp.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            sortrank=result[1]
            url=result[2]
            name=result[3]
            logo=result[4]
            remark=result[5]
            list={'id':id,'sortrank':sortrank,'url':url,'name':name,'logo':logo,'remark':remark}
            listall.append(list)
        return listall
    def getpyliuyan(self,frompageCount,limitNum,is_hand=''):
        listall=[]
        argument=[]
        sqlarg=''
        if is_hand:
            sqlarg+=' and is_handle=%s'
            argument.append(is_hand)
        sql1='select count(0) from py_liuyan where id>=0'+sqlarg
        sql='select id,name,phone,mail,content,ip,sendtime,province,city,is_handle from py_liuyan where id>=0'+sqlarg
        sql=sql+' order by sendtime desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbp.fetchnumberdb(sql1,argument)
        resultlist=self.dbp.fetchalldb(sql,argument)
        for result in resultlist:
            is_handle=result[9]
            list={'id':result[0],'name':result[1],'phone':result[2],'mail':result[3],'content':result[4],'ip':result[5],'sendtime':formattime(result[6]),'province':result[7],'city':result[8],'is_handle':is_handle}
            listall.append(list)
        return {'list':listall,'count':count}
    def getusername(self,id):
        sql='select username from py_user where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        if result:
            return result[0]
    def getempdetail(self,id):
        sql='select name,pic,pinyin from py_template where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        list={'name':'','pic':''}
        if result:
            list['name']=result[0]
            list['pic']=result[1]
            list['pinyin']=result[2]
        return list
    def getempinyin(self,id):
        sql='select pinyin from py_template where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        if result:
            return result[0]
    def gettempinyinuser(self,user_id):
        sql1='select temp_id from py_user_template where user_id=%s'
        result1=self.dbp.fetchonedb(sql1,user_id)
        if result1:
            temp_id=result1[0]
            sql='select pinyin from py_template where id=%s'
            result=self.dbp.fetchonedb(sql,temp_id)
            if result:
                return result[0]
    def getarttypename(self,id):
        sql='select typename from py_user_arttype1 where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        if result:
            return result[0]
    def getarttypepinyin(self,id):
        sql='select pinyin from py_user_arttype1 where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        if result:
            return result[0]
    #--根据域名获得uerid
    def getuseridfromsite(self,website):
        sql="select id from py_user where website=%s"
        result=self.dbp.fetchonedb(sql,[website])
        if result:
            return result[0]
    #---根据拼音获得id和pageid
    def getvaluefrompinyinsite(self,pinyin,user_id):
        if pinyin:
            sql='select id,typename,tempname,reid,pageid from py_user_arttype1 where pinyin=%s and user_id=%s'
            result=self.dbp.fetchonedb(sql,[pinyin,user_id])
            if result:
                return {'id':result[0],'typename':result[1],'tempname':result[2],'reid':result[3],'pageid':result[4]}
    def gettypereid(self,id):
        sql='select reid from py_user_arttype1 where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        if result:
            return result[0]
    def getartdtypepinyin(self,artid):
        sql1='select typeid from py_user_artical where id=%s'
        result1=self.dbp.fetchonedb(sql1,artid)
        if result1:
            typeid=result1[0]
            sql='select pinyin from py_user_arttype1 where id=%s'
            result=self.dbp.fetchonedb(sql,typeid)
            if result:
                return result[0]
    def getarttempname(self,id):
        sql='select tempname from py_user_arttype1 where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        if result:
            return result[0]
    def gettypenamepinyin(self,id):
        sql='select tempname,pinyin from py_user_arttype1 where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        list={'typename':'','pinyin':''}
        if result:
            typename=result[0]
            pinyin=result[1]
            list={'typename':typename,'pinyin':pinyin}
        return list
    def getarttypedetail(self,id):
        sql='select reid,typename,pinyin,tempname from py_user_arttype1 where id=%s'
        resultlist=self.dbp.fetchalldb(sql,[id])
        listall=[]
        for result in resultlist:
            reid=result[0]
            retypename=''
            repinyin=''
            if reid:
                retypenamepinyin=self.gettypenamepinyin(reid)
                retypename=retypenamepinyin['typename']
                repinyin=retypenamepinyin['pinyin']
            typename=result[1]
            pinyin=result[2]
            tempname=result[3]
            list={'id':id,'typename':typename,'reid':reid,'retypename':retypename,'repinyin':repinyin,'pinyin':pinyin,'tempname':tempname}
            listall.append(list)
            return list
    #----栏目列表
    def getarttypelist(self,frompageCount,limitNum,user_id='',reid='',all=''):
        argument=[]
        sqlarg=''
        if user_id:
            sqlarg+=' and user_id=%s'
            argument.append(user_id)
        if reid:
            sqlarg+=' and reid=%s'
            argument.append(reid)
        sql1='select count(0) from py_user_arttype1 where id>0'+sqlarg
        sql='select id,reid,typename,pinyin,tempname,sortrank,user_id,pageid from py_user_arttype1 where id>0'+sqlarg
        sql+=' order by sortrank,id limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbp.fetchnumberdb(sql1,argument)
        resultlist=self.dbp.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            reid=result[1]
            #上级栏目的名字
            retypename=''
            if reid:
                retypename=self.getarttypename(reid)
            typename=result[2]
            pinyin=result[3]
            tempname=result[4]
            sortrank=result[5]
            user_id=result[6]
            pageid=result[7]
            if user_id:
                user_name=self.getusername(user_id)
            nexttplist=[]
            hasnext=self.hasnexttype(id)
            if all==1:
                nexttplist=self.getnexttypelist(id)
            pagename=""
            if pageid:
                if pageid==1:
                    pagename="首页"
                if pageid==2:
                    pagename="栏目页"
                if pageid==3:
                    pagename="最终页"
            list={'id':id,'typename':typename,'pageid':pageid,'pagename':pagename,'user_id':user_id,'user_name':user_name,'hasnext':hasnext,'reid':reid,'retypename':retypename,'pinyin':pinyin,'tempname':tempname,'sortrank':sortrank,'nexttplist':nexttplist}
            listall.append(list)
        return {'list':listall,'count':count}
    def hasnexttype(self,reid):
        sql='select id from py_user_arttype1 where reid=%s'
        result=self.dbp.fetchonedb(sql,[reid])
        if result:
            return result[0]
    def getnexttypelist(self,reid):
        sql='select id,typename,pinyin,tempname,sortrank,reid from py_user_arttype1 where reid=%s'
        resultlist=self.dbp.fetchalldb(sql,[reid])
        listall=[]
        for result in resultlist:
            id=result[0]
            typename=result[1]
            pinyin=result[2]
            tempname=result[3]
            sortrank=result[4]
            reid=result[5]
            if reid:
                retypename=self.getarttypename(reid)
            list={'id':id,'typename':typename,'reid':reid,'retypename':retypename,'pinyin':pinyin,'tempname':tempname,'sortrank':sortrank}
            listall.append(list)
        return listall
    
    #----上一篇下一篇(一期)
    def getarticalup(self,id,typeid,user_id,typepinyin):
        sqlt="select id,title from py_user_artical where typeid=%s and user_id=%s and id>%s order by id limit 0,1"
        resultu = self.dbp.fetchonedb(sqlt,[typeid,user_id,id])
        if resultu:
            uid=resultu[0]
#            url='/web/weili/'+typepinyin+'/'+str(uid)+'.html'
            url=str(uid)+'.html'
            list={'id':uid,'title':resultu[1],'url':url}
            return list
    def getarticalnx(self,id,typeid,user_id,typepinyin):
        sqlt="select id,title from py_user_artical where typeid=%s and user_id=%s and id<%s order by id desc limit 0,1"
        resultn = self.dbp.fetchonedb(sqlt,[typeid,user_id,id])
        if resultn:
            nid=resultn[0]
#            url='/web/weili/'+typepinyin+'/'+str(nid)+'.html'
            url=str(nid)+'.html'
            list={'id':nid,'title':resultn[1],'url':url}
            return list
    def getarticaldetail(self,id):
        sql='select typeid,title,gmt_modified,sortrank,litpic,body from py_user_artical where id=%s'
        result=self.dbp.fetchonedb(sql,[id])
        if result:
            typeid=result[0]
            typename=''
            pinyin=''
            retypename=''
            retypename=''
            if typeid:
                arttypedetail=self.getarttypedetail(typeid)
                typename=arttypedetail['typename']
                pinyin=arttypedetail['pinyin']
                retypename=arttypedetail['retypename']
                repinyin=arttypedetail['repinyin']
            url=str(id)+'.html'
            title=result[1]
            gmt_modified=formattime(result[2],1)
            sortrank=result[3]
            litpic=result[4]
            content=result[5]
            litpic=litpic.replace('img1.zz91.com/','img3.zz91.com/231x177/')
            content=content.replace('img1.zz91.com/','img3.zz91.com/1000x600/')
            list={'id':id,'title':title,'typeid':typeid,'url':url,'pinyin':pinyin,'typename':typename,'repinyin':repinyin,'retypename':retypename,'gmt_modified':gmt_modified,'sortrank':sortrank,'litpic':litpic,'content':content}
            return list
    #----文章列表
    def getarticalist(self,frompageCount,limitNum,user_id='',typeid='',is_del='',is_make=''):
        sqlarg=''
        argument=[]
        if typeid:
            if '(' in str(typeid):
                sqlarg+=' and typeid in '+typeid
            else:
                sqlarg+=' and typeid=%s'
                argument.append(typeid)
        if user_id:
            sqlarg+=' and user_id=%s'
            argument.append(user_id)
        if is_make:
            sqlarg+=' and is_make=%s'
            argument.append(is_make)
        if is_del:
            sqlarg+=' and is_del=%s'
            argument.append(is_del)
        else:
            sqlarg+=' and is_del=0'
        sql1='select count(0) from py_user_artical where id>0'+sqlarg
        sql='select id,typeid,title,gmt_modified,sortrank,litpic,is_make,user_id from py_user_artical where id>0'+sqlarg
        sql+=' order by sortrank,gmt_modified desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbp.fetchnumberdb(sql1,argument)
        resultlist=self.dbp.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            typeid=result[1]
            if typeid:
                typename=''
                pinyin=''
                retypename=''
                repinyin=''
                arttypedetail=self.getarttypedetail(typeid)
                if arttypedetail:
                    typename=arttypedetail['typename']
                    pinyin=arttypedetail['pinyin']
                    retypename=arttypedetail['retypename']
                    repinyin=arttypedetail['repinyin']
            url=str(id)+'.html'
            title=result[2]
            gmt_modified=formattime(result[3])
            sortrank=result[4]
            litpic=result[5]
            is_make=result[6]
            user_id=result[7]
            if user_id:
                user_name=self.getusername(user_id)
            adminpic=litpic.replace('img1.zz91.com/','img3.zz91.com/60x45/')
            litpic=litpic.replace('img1.zz91.com/','img3.zz91.com/231x177/')
            list={'id':id,'title':title,'typeid':typeid,'pinyin':pinyin,'url':url,'typename':typename,'gmt_modified':gmt_modified,'sortrank':sortrank,'litpic':litpic,'adminpic':adminpic,'is_make':is_make,'user_id':user_id,'user_name':user_name}
            listall.append(list)
        return {'list':listall,'count':count}
    def gettpnpy(self,id):
        sql='select typename,pinyin from py_user_arttype1 where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        list={'typename':'','pinyin':''}
        if result:
            list={'typename':result[0],'pinyin':result[1]}
        return list
    #----用户模版列表
    def getuseremplatelist(self,frompageCount,limitNum,user_id=''):
        argument=[]
        sqlarg=''
        if user_id:
            sqlarg+=' and user_id=%s'
            argument.append(user_id)
        sql1='select count(0) from py_user_template where id>0'+sqlarg
        sql='select id,temp_id,user_id from py_user_template where id>0'+sqlarg
        sql+=' order by id limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbp.fetchnumberdb(sql1,user_id)
        resultlist=self.dbp.fetchalldb(sql,user_id)
        listall=[]
        for result in resultlist:
            id=result[0]
            temp_id=result[1]
            user_id=result[2]
            if user_id:
                user_name=self.getusername(user_id)
            tempdetail=self.getempdetail(temp_id)
            name=tempdetail['name']
            pic=tempdetail['pic']
            pinyin=tempdetail['pinyin']
            list={'id':id,'name':name,'pic':pic,'pinyin':pinyin,'user_id':user_id,'user_name':user_name}
            listall.append(list)
        return {'list':listall,'count':count}
    #----模版列表
    def getemplatelist(self,frompageCount,limitNum,user_id):
        sql1='select count(0) from py_template'
        sql='select id,name,pic,pinyin,sortrank from py_template'
        sql+=' order by sortrank,id limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbp.fetchnumberdb(sql1)
        resultlist=self.dbp.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            name=result[1]
            pic=result[2]
            pinyin=result[3]
            sortrank=result[4]
            list={'id':id,'name':name,'pic':pic,'pinyin':pinyin,'sortrank':sortrank}
            listall.append(list)
        return {'list':listall,'count':count}
    #读取html的url
    def htmlurl(self,request,type="",user_id="",artid="",arttypeid="",page=""):
        if not type:
            type=request.GET.get('type')
        if not user_id:
            user_id=request.GET.get('user_id')
        if not artid:
            artid=request.GET.get('artid')
        type=str(type)
        friendlinklist=zzp.getfriendlinklist()
        freshtime=time.time()
        if not user_id:
            user_id=request.session.get('user_id')
        if user_id:
            pinyin=zzp.gettempinyinuser(user_id)
            #首页
            if type=='1':
                pinyin=zzp.gettempinyinuser(user_id)
                alltypelist=zzp.getarttypelist(0,20,user_id,'0')['list']
                cqcmlist=zzp.getarticalist(0,5,user_id,typeid=11)['list']
                propiclist=zzp.getarticalist(0,5,user_id,typeid='(2,3)')['list']
                shouindex=1
                return render_to_response('user/'+pinyin+'/index.html',locals())
            #栏目页
            elif type=='2':
                if not arttypeid:
                    arttypeid=request.GET.get('arttypeid')
                if user_id and arttypeid:
                    arttypedetail=zzp.getarttypedetail(arttypeid)
                    if arttypedetail:
                        typename=arttypedetail['typename']
                        urltype=arttypedetail['tempname']
                        pinyinname=arttypedetail['pinyin']
                        reid=arttypedetail['reid']
                        repinyin=arttypedetail['repinyin']
                        if not urltype:
                            urltype='list'
                        alltypelist=zzp.getarttypelist(0,20,user_id,'0')['list']
                        if reid:
                            nowtypelist=zzp.getarticalist(0,20,user_id,typeid=arttypeid)['list']
                            topid=reid
                            jibie='../../'
                        else:
                            topid=int(arttypeid)
                            if arttypeid=='1':
                                articalist=zzp.getarticalist(0,4,user_id,typeid=20)['list']
                                gsjjtxt=zzp.getarticaldetail(24)
                            elif arttypeid=='4':
                                articalist1=zzp.getarticalist(0,4,user_id,typeid=2)['list']
                                articalist2=zzp.getarticalist(0,4,user_id,typeid=3)['list']
                            elif arttypeid=='5':
                                listtypeall=[]
                                sql='select id,typename,pinyin from py_user_arttype1 where reid=5'
                                resultlist=dbp.fetchalldb(sql)
                                for result in resultlist:
                                    sontypeid=result[0]
                                    sontypename=result[1]
                                    sonpinyin=result[2]
                                    list1=zzp.getarticalist(0,4,user_id,typeid=sontypeid)['list']
                                    list2={'typeid':sontypeid,'typename':sontypename,'pinyin':sonpinyin,'artlist':list1}
                                    listtypeall.append(list2)
                            #有翻页的栏目
    #                        elif arttypeid in ['2','3']:
                            else:
                                if not page:
                                    page=request.GET.get('page')
                                if not page:
                                    page=1
                                funpage=zz91page()
                                limitNum=funpage.limitNum(16)
                                nowpage=funpage.nowpage(int(page))
                                frompageCount=funpage.frompageCount()
                                after_range_num = funpage.after_range_num(3)
                                before_range_num = funpage.before_range_num(6)
                                articalist=zzp.getarticalist(frompageCount,limitNum,user_id,typeid=arttypeid)
                                listcount=0
                                listall=articalist['list']
                                listcount=articalist['count']
                                if (int(listcount)>1000000):
                                    listcount=1000000-1
                                listcount = funpage.listcount(listcount)
                                page_listcount=funpage.page_listcount()
                                firstpage = funpage.firstpage()
                                lastpage = funpage.lastpage()
                                page_range  = funpage.page_range()
                                if len(page_range)>7:
                                    page_range=page_range[:7]
                                nextpage = funpage.nextpage()
                                prvpage = funpage.prvpage()
    #                            articalist=zzp.getarticalist(0,20,user_id,typeid=arttypeid)['list']
                            jibie='../'
                        
                        
                        
                        
                        
                        
                        return render_to_response('user/'+pinyin+'/'+urltype+'.html',locals())
            #最终页
            elif type=='3':
                if user_id and artid:
                    alltypelist=zzp.getarttypelist(0,20,user_id,'0')['list']
                    sql='select typeid,title,litpic,body from py_user_artical where id=%s'
                    result=dbp.fetchonedb(sql,artid)
                    if result:
                        typeid=result[0]
                        arttypedetail=zzp.getarttypedetail(typeid)
                        if arttypedetail:
    #                        typename=arttypedetail['typename']
    #                        urltype=arttypedetail['tempname']
                            pinyinname=arttypedetail['pinyin']
                            reid=arttypedetail['reid']
    #                        repinyin=arttypedetail['repinyin']
                        title=result[1]
                        litpic=result[2]
                        content=result[3]
                        litpic=litpic.replace('img1.zz91.com/','img3.zz91.com/398x398/')
                        content=content.replace('img1.zz91.com/','img3.zz91.com/900x600/')
                        upartical=zzp.getarticalup(artid,typeid,user_id,pinyinname)#上一篇
                        nextartical=zzp.getarticalnx(artid,typeid,user_id,pinyinname)#下一篇
                        detail='zxdt_detail'
                        if typeid in [2,3]:
                            detail='gyxx_detail'
                        if typeid==7:
                            detail='zxdt_detail'
                        if typeid:
                            topid=int(typeid)
                        if reid:
                            jibie='../../'
                        else:
                            jibie='../'
                    return render_to_response('user/'+pinyin+'/'+detail+'.html',locals())
        return HttpResponse()

#----pyftp的Class
class pyftp:
    from ftplib import FTP
    import os
    def __init__(self,ip,username,password):
        self._ip=ip
        self._username=username
        self._password=password
        self._timeout = 30
        self._port = 21
    #上传文件
    def upload(self,ftpath,nowpath,name):
        ftp = self.FTP()
        ftp.connect(self._ip,self._port,self._timeout) # 连接FTP服务器  
        ftp.login(self._username,self._password) # 登录  
        ftp.cwd(ftpath+'/')    # 设置FTP路径  
#        listfile=os.listdir(nowpath)
#        for name in listfile:
        src = os.path.join(nowpath,name)
        if os.path.isfile(src):
            path = nowpath+'/' + name
            ftp.storbinary('STOR '+name, open(path, 'rb')) # 上传FTP文件  
        ftp.quit()
    #创建文件夹
    def mkdir(self,ftpath,dirname):
        ftp = self.FTP()  
        ftp.connect(self._ip,self._port,self._timeout) # 连接FTP服务器
        ftp.login(self._username,self._password) # 登录
        ftp.cwd(ftpath+'/')    # 设置FTP路径  
        ftp.mkd(dirname)
    #文件夹改名
    def rename(self,ftpath,dirname,dirnameold):
        ftp = self.FTP()  
        ftp.connect(self._ip,self._port,self._timeout) # 连接FTP服务器
        ftp.login(self._username,self._password) # 登录
        ftp.cwd(ftpath+'/')    # 设置FTP路径  
        ftp.rename(dirnameold,dirname)
    #删除文件夹
    def deldir(self,ip,username,password,ftpath,dirname):
        ftp = self.FTP()  
        ftp.connect(self._ip,self._port,self._timeout) # 连接FTP服务器
        ftp.login(self._username,self._password) # 登录
        ftp.cwd(ftpath+'/')    # 设置FTP路径  
        ftp.rmd(dirname)
    #删除文件
    def delfile(self,ftpath,filename):
        ftp = self.FTP()  
        ftp.connect(self._ip,self._port,self._timeout) # 连接FTP服务器  
        ftp.login(self._username,self._password) # 登录  
        ftp.cwd(ftpath+'/')    # 设置FTP路径  
        ftp.delete(filename)
        
#----汉字转拼音的Class
class pinyin:
    listDict = [
        {'a':-20319},
        {'ai':-20317},
        {'an':-20304},
        {'ang':-20295},
        {'ao':-20292},
        {'ba':-20283},
        {'bai':-20265},
        {'ban':-20257},
        {'bang':-20242},
        {'bao':-20230},
        {'bei':-20051},
        {'ben':-20036},
        {'beng':-20032},
        {'bi':-20026},
        {'bian':-20002},
        {'biao':-19990},
        {'bie':-19986},
        {'bin':-19982},
        {'bing':-19976},
        {'bo':-19805},
        {'bu':-19784},
        {'ca':-19775},
        {'cai':-19774},
        {'can':-19763},
        {'cang':-19756},
        {'cao':-19751},
        {'ce':-19746},
        {'ceng':-19741},
        {'cha':-19739},
        {'chai':-19728},
        {'chan':-19725},
        {'chang':-19715},
        {'chao':-19540},
        {'che':-19531},
        {'chen':-19525},
        {'cheng':-19515},
        {'chi':-19500},
        {'chong':-19484},
        {'chou':-19479},
        {'chu':-19467},
        {'chuai':-19289},
        {'chuan':-19288},
        {'chuang':-19281},
        {'chui':-19275},
        {'chun':-19270},
        {'chuo':-19263},
        {'ci':-19261},
        {'cong':-19249},
        {'cou':-19243},
        {'cu':-19242},
        {'cuan':-19238},
        {'cui':-19235},
        {'cun':-19227},
        {'cuo':-19224},
        {'da':-19218},
        {'dai':-19212},
        {'dan':-19038},
        {'dang':-19023},
        {'dao':-19018},
        {'de':-19006},
        {'deng':-19003},
        {'di':-18996},
        {'dian':-18977},
        {'diao':-18961},
        {'die':-18952},
        {'ding':-18783},
        {'diu':-18774},
        {'dong':-18773},
        {'dou':-18763},
        {'du':-18756},
        {'duan':-18741},
        {'dui':-18735},
        {'dun':-18731},
        {'duo':-18722},
        {'e':-18710},
        {'en':-18697},
        {'er':-18696},
        {'fa':-18526},
        {'fan':-18518},
        {'fang':-18501},
        {'fei':-18490},
        {'fen':-18478},
        {'feng':-18463},
        {'fo':-18448},
        {'fou':-18447},
        {'fu':-18446},
        {'ga':-18239},
        {'gai':-18237},
        {'gan':-18231},
        {'gang':-18220},
        {'gao':-18211},
        {'ge':-18201},
        {'gei':-18184},
        {'gen':-18183},
        {'geng':-18181},
        {'gong':-18012},
        {'gou':-17997},
        {'gu':-17988},
        {'gua':-17970},
        {'guai':-17964},
        {'guan':-17961},
        {'guang':-17950},
        {'gui':-17947},
        {'gun':-17931},
        {'guo':-17928},
        {'ha':-17922},
        {'hai':-17759},
        {'han':-17752},
        {'hang':-17733},
        {'hao':-17730},
        {'he':-17721},
        {'hei':-17703},
        {'hen':-17701},
        {'heng':-17697},
        {'hong':-17692},
        {'hou':-17683},
        {'hu':-17676},
        {'hua':-17496},
        {'huai':-17487},
        {'huan':-17482},
        {'huang':-17468},
        {'hui':-17454},
        {'hun':-17433},
        {'huo':-17427},
        {'ji':-17417},
        {'jia':-17202},
        {'jian':-17185},
        {'jiang':-16983},
        {'jiao':-16970},
        {'jie':-16942},
        {'jin':-16915},
        {'jing':-16733},
        {'jiong':-16708},
        {'jiu':-16706},
        {'ju':-16689},
        {'juan':-16664},
        {'jue':-16657},
        {'jun':-16647},
        {'ka':-16474},
        {'kai':-16470},
        {'kan':-16465},
        {'kang':-16459},
        {'kao':-16452},
        {'ke':-16448},
        {'ken':-16433},
        {'keng':-16429},
        {'kong':-16427},
        {'kou':-16423},
        {'ku':-16419},
        {'kua':-16412},
        {'kuai':-16407},
        {'kuan':-16403},
        {'kuang':-16401},
        {'kui':-16393},
        {'kun':-16220},
        {'kuo':-16216},
        {'la':-16212},
        {'lai':-16205},
        {'lan':-16202},
        {'lang':-16187},
        {'lao':-16180},
        {'le':-16171},
        {'lei':-16169},
        {'leng':-16158},
        {'li':-16155},
        {'lia':-15959},
        {'lian':-15958},
        {'liang':-15944},
        {'liao':-15933},
        {'lie':-15920},
        {'lin':-15915},
        {'ling':-15903},
        {'liu':-15889},
        {'long':-15878},
        {'lou':-15707},
        {'lu':-15701},
        {'lv':-15681},
        {'luan':-15667},
        {'lue':-15661},
        {'lun':-15659},
        {'luo':-15652},
        {'ma':-15640},
        {'mai':-15631},
        {'man':-15625},
        {'mang':-15454},
        {'mao':-15448},
        {'me':-15436},
        {'mei':-15435},
        {'men':-15419},
        {'meng':-15416},
        {'mi':-15408},
        {'mian':-15394},
        {'miao':-15385},
        {'mie':-15377},
        {'min':-15375},
        {'ming':-15369},
        {'miu':-15363},
        {'mo':-15362},
        {'mou':-15183},
        {'mu':-15180},
        {'na':-15165},
        {'nai':-15158},
        {'nan':-15153},
        {'nang':-15150},
        {'nao':-15149},
        {'ne':-15144},
        {'nei':-15143},
        {'nen':-15141},
        {'neng':-15140},
        {'ni':-15139},
        {'nian':-15128},
        {'niang':-15121},
        {'niao':-15119},
        {'nie':-15117},
        {'nin':-15110},
        {'ning':-15109},
        {'niu':-14941},
        {'nong':-14937},
        {'nu':-14933},
        {'nv':-14930},
        {'nuan':-14929},
        {'nue':-14928},
        {'nuo':-14926},
        {'o':-14922},
        {'ou':-14921},
        {'pa':-14914},
        {'pai':-14908},
        {'pan':-14902},
        {'pang':-14894},
        {'pao':-14889},
        {'pei':-14882},
        {'pen':-14873},
        {'peng':-14871},
        {'pi':-14857},
        {'pian':-14678},
        {'piao':-14674},
        {'pie':-14670},
        {'pin':-14668},
        {'ping':-14663},
        {'po':-14654},
        {'pu':-14645},
        {'qi':-14630},
        {'qia':-14594},
        {'qian':-14429},
        {'qiang':-14407},
        {'qiao':-14399},
        {'qie':-14384},
        {'qin':-14379},
        {'qing':-14368},
        {'qiong':-14355},
        {'qiu':-14353},
        {'qu':-14345},
        {'quan':-14170},
        {'que':-14159},
        {'qun':-14151},
        {'ran':-14149},
        {'rang':-14145},
        {'rao':-14140},
        {'re':-14137},
        {'ren':-14135},
        {'reng':-14125},
        {'ri':-14123},
        {'rong':-14122},
        {'rou':-14112},
        {'ru':-14109},
        {'ruan':-14099},
        {'rui':-14097},
        {'run':-14094},
        {'ruo':-14092},
        {'sa':-14090},
        {'sai':-14087},
        {'san':-14083},
        {'sang':-13917},
        {'sao':-13914},
        {'se':-13910},
        {'sen':-13907},
        {'seng':-13906},
        {'sha':-13905},
        {'shai':-13896},
        {'shan':-13894},
        {'shang':-13878},
        {'shao':-13870},
        {'she':-13859},
        {'shen':-13847},
        {'sheng':-13831},
        {'shi':-13658},
        {'shou':-13611},
        {'shu':-13601},
        {'shua':-13406},
        {'shuai':-13404},
        {'shuan':-13400},
        {'shuang':-13398},
        {'shui':-13395},
        {'shun':-13391},
        {'shuo':-13387},
        {'si':-13383},
        {'song':-13367},
        {'sou':-13359},
        {'su':-13356},
        {'suan':-13343},
        {'sui':-13340},
        {'sun':-13329},
        {'suo':-13326},
        {'ta':-13318},
        {'tai':-13147},
        {'tan':-13138},
        {'tang':-13120},
        {'tao':-13107},
        {'te':-13096},
        {'teng':-13095},
        {'ti':-13091},
        {'tian':-13076},
        {'tiao':-13068},
        {'tie':-13063},
        {'ting':-13060},
        {'tong':-12888},
        {'tou':-12875},
        {'tu':-12871},
        {'tuan':-12860},
        {'tui':-12858},
        {'tun':-12852},
        {'tuo':-12849},
        {'wa':-12838},
        {'wai':-12831},
        {'wan':-12829},
        {'wang':-12812},
        {'wei':-12802},
        {'wen':-12607},
        {'weng':-12597},
        {'wo':-12594},
        {'wu':-12585},
        {'xi':-12556},
        {'xia':-12359},
        {'xian':-12346},
        {'xiang':-12320},
        {'xiao':-12300},
        {'xie':-12120},
        {'xin':-12099},
        {'xing':-12089},
        {'xiong':-12074},
        {'xiu':-12067},
        {'xu':-12058},
        {'xuan':-12039},
        {'xue':-11867},
        {'xun':-11861},
        {'ya':-11847},
        {'yan':-11831},
        {'yang':-11798},
        {'yao':-11781},
        {'ye':-11604},
        {'yi':-11589},
        {'yin':-11536},
        {'ying':-11358},
        {'yo':-11340},
        {'yong':-11339},
        {'you':-11324},
        {'yu':-11303},
        {'yuan':-11097},
        {'yue':-11077},
        {'yun':-11067},
        {'za':-11055},
        {'zai':-11052},
        {'zan':-11045},
        {'zang':-11041},
        {'zao':-11038},
        {'ze':-11024},
        {'zei':-11020},
        {'zen':-11019},
        {'zeng':-11018},
        {'zha':-11014},
        {'zhai':-10838},
        {'zhan':-10832},
        {'zhang':-10815},
        {'zhao':-10800},
        {'zhe':-10790},
        {'zhen':-10780},
        {'zheng':-10764},
        {'zhi':-10587},
        {'zhong':-10544},
        {'zhou':-10533},
        {'zhu':-10519},
        {'zhua':-10331},
        {'zhuai':-10329},
        {'zhuan':-10328},
        {'zhuang':-10322},
        {'zhui':-10315},
        {'zhun':-10309},
        {'zhuo':-10307},
        {'zi':-10296},
        {'zong':-10281},
        {'zou':-10274},
        {'zu':-10270},
        {'zuan':-10262},
        {'zui':-10260},
        {'zun':-10256},
        {'zuo':-10254}
    ]
    def get(self, str, first=False, retList=False):
        str = str.strip()
        str = unicode(str, 'utf-8')
        str = str.encode('gbk')
        sLen = len(str)
        i, ret = 0, []
        while i < sLen:
            p = ord(str[i:i+1])
            if p > 160:
                q = ord(str[i+1:i+2])
                p = p * 256 + q - 65536
                i += 2
            else:
                i += 1
            zhi = self.chr(p)
            if first:
                zhi = zhi[0]
            ret.append(zhi)
        return ret if retList else "".join(ret)
    def chr(self, num):
        if 0 < num < 160:
            return chr(num)
        elif num < -20319 or num > -10247:
            return ''
        else:
            start = len(self.listDict) - 1
            for i in range(start, -1, -1):
                if self.listDict[i].values()[0] <= num:
                    break
            return self.listDict[i].keys()[0]