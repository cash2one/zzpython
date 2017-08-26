#-*- coding:utf-8 -*-
class useradmin:
    def __init__(self):
        self.db=db
    #main文件框架，自定义菜单
    def getmain(self,username):
        sql0='select auth_category_id from user where username=%s'
        result0=db.fetchonedb(sql0,[username])
        if result0:
            auth_category_id=result0['auth_category_id']
            if auth_category_id:
                auth_category_id=auth_category_id[:-1]
                ac_id_list=auth_category_id.split(',')
            else:
                ac_id_list=""
        #     print ac_id_list
            listallcode=[]
            position=''
            for ac_id in ac_id_list:
                sql='SELECT u.id as id,a.auth_code,a.label as position FROM user as u left join auth_category as a on a.id=%s where username=%s'
                result=db.fetchonedb(sql,[ac_id,username])
                if result:
                    position=result['position']#职位
                    auth_code=result['auth_code']
                    if auth_code:
                        auth_code=auth_code[:-1]
                        a_code=auth_code.split(',')
                        listallcode.append(a_code)
            newset=set([])
            for i in listallcode:
                newset=set(i)|newset
            a_code=list(newset)
#             print a_code
            #获得当前登录用户的顶级菜单
            sql='select id,label from menu where parent_id=0  and closeflag=0 order by ord asc'
            topresult=db.fetchalldb(sql)
            # print topresult
            toplistall=[]
            
            for top in topresult:
                tid=top['id']
                if str(tid) in a_code:
                    #print 'ok'
                    tlabel=top['label']
                    sql1='select id,parent_id,label from menu where parent_id=%s and closeflag=0 order by ord desc'
                    firresult=db.fetchalldb(sql1,[tid])
                    firlistall=[]
                    i=0
                    for fir in firresult:
                        fid=fir['id']
                        if str(fid) in a_code:
                            parent_id=fir['parent_id']
                            flabel=fir['label']
                            sql2='select id,label,link from menu where parent_id=%s  and closeflag=0 order by ord desc'
                            secresult=db.fetchalldb(sql2,[fid])
                            seclistall=[]
                            ii=0
                            for sec in secresult:
                                sid=sec['id']
                                if str(sid) in a_code:
                                    slabel=sec['label']
                                    link=sec['link']
                                    sec_id=str(link)
                                    sec_id=re.sub(".html","",sec_id)
                                    slist={'slabel':slabel,'link':link,'sec_id':sec_id,'ii':ii}
                                    seclistall.append(slist)
                                    ii+=1
                                    
                            flist={'fid':fid,'flabel':flabel,'seclistall':seclistall,'i':i}
                            i=i+1
                            firlistall.append(flist)
                    tlist={'tid':tid,'tlabel':tlabel,'firlistall':firlistall}
                    toplistall.append(tlist)
            return {'toplistall':toplistall,'position':position,'status':'in_session_time'}
        else:
            return {'status':'outof_session_time'}
    
    def get_user_categorylist(self,closeflag=""):
        
        sql1="select id,code,label from user_category where code like '__'"
        if closeflag:
            sql1=sql1+" and closeflag=0"
        firstlist=db.fetchalldb(sql1)
        listall=[]
        for first in firstlist:
            id1=first['id']
            code1=first['code']
            label1=first['label']
            list={'label':label1,'id':id1,'code':code1}
            # listall.append(list)
            sql2="select id,code,label from user_category where code like '"+str(code1)+"__'"
            if closeflag:
                sql2=sql2+" and closeflag=0"
            secondlist=db.fetchalldb(sql2)
            if secondlist:
                listall2=[]
                for second in secondlist:
                    id2=second['id']
                    code2=second['code']
                    label2=second['label']
                    list2={'label':label2,'id':id2,'code':code2}
                    ##
                    sql3="select id,code,label from user_category where code like '"+str(code1)+"__'"
                    if closeflag:
                        sql3=sql3+" and closeflag=0"
                    thirdlist=db.fetchalldb(sql2)
                    if thirdlist:
                        listall3=[]
                        for third in thirdlist:
                            id3=third['id']
                            code3=third['code']
                            label3=third['label']
                            list3={'label':label3,'id':id3,'code':code3}
                            listall3.append(list3)
                        list2['children']=listall3
                    ##
                    listall2.append(list2)
                list['children']=listall2
                list['expanded']='true'#morenzhankai
            listall.append(list)
        return listall
    #获得团队
    def get_user_category(self,frompageCount,limitNum,code,user_category_label=''):
        sqlarg=''
        argument=[]
        if user_category_label:
            sqlarg+=' and label like %s'
            argument.append('%'+user_category_label+'%')
        sqlc="select count(0) as count from user_category where id>0 and code like '"+str(code)+"__'"+sqlarg
        result=db.fetchonedb(sqlc,argument)
        listcount=result['count']
        sql="select id,code,label,closeflag from user_category where id >0  and code like '"+str(code)+"__'"+sqlarg
        sql+='limit '+str(frompageCount)+','+str(limitNum)
        listall=db.fetchalldb(sql,argument)
        for dic in listall:
            code=dic['code']
            dic['has_son']=self.has_son(code)
            dic['has_father']=self.has_father(code)
            if self.has_father(code):
                dic['has_father']=1
                dic['father_code']=code[:-4]
            else:
                dic['has_father']=0
            statustxt=''
            closeflag=dic['closeflag']
            if closeflag==1:
                statustxt='<font color="#ff0000">已冻结</font>'
            if closeflag==0:
                statustxt='已开通'
            dic['statustxt']=statustxt
        return {"listall":listall,"listcount":listcount}
    #判断是否有子栏目
    def has_son(self,code):
        sql="select id from user_category where code like '"+str(code)+"__'"
        result=db.fetchalldb(sql)
        if result:
            return 1
        else:
            return 0
    #判断是否有上一级
    def has_father(self,code):
        if len(code)>2:
            return 1
        else:
            return 0
    #判断最大有几级类目
    def max_code(self):
        #选出code最长的那一条记录
        sql='select code from user_category where length(code) = (select max(length(code)) from user_category)'
        result=db.fetchonedb(sql)
        if result:
            code=result['code']
            n=len(code)/2
#             level=[{'':},{},{}]
            return n
    #用户列表
    def get_user(self,frompageCount,limitNum,username='',user_category_code='',closeflag='',categorylist=''):
        sqlarg=''
        argument=[]
        if username:
            sqlarg+=' and u.username like %s'
            argument.append('%'+username+'%')
        if user_category_code:
            sqlarg+=' and u.user_category_code=%s'
            argument.append(user_category_code)
        if categorylist:
            qxl="0"
            for a in categorylist:
                qxl=qxl+","+str(a['code'])
            if qxl:
                sqlarg+=' and u.user_category_code in ('+qxl+')'
                #argument.append(qxl)
        if not closeflag:
            closeflag="0"
        if closeflag:
            sqlarg+=' and u.closeflag=%s'
            argument.append(closeflag)
        sqlc="select count(0) as count from user as u left outer join user_category as c on u.user_category_code=c.code  left outer join auth_category as a on u.auth_category_id=a.id where u.id>0 "+sqlarg
        result=db.fetchonedb(sqlc,argument)
        listcount=result['count']
        sql="select u.id,u.username,u.password,u.user_category_code,u.auth_category_id,u.closeflag,c.label as user_category,a.label as auth_category,u.realname from user as u left outer join user_category as c on u.user_category_code=c.code  left outer join auth_category as a on u.auth_category_id=a.id where u.id>0"+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        listall=db.fetchalldb(sql,argument)
        for list in listall:
            statustxt=''
            closeflag=list['closeflag']
            if closeflag==1:
                statustxt='<font color="#ff0000">已冻结</font>'
            if closeflag==0:
                statustxt='已开通'
            list['statustxt']=statustxt
            auth_category=list['auth_category']
            if not auth_category:
                list['auth_category']=''
            #客户数
            sqlc="select count(0) as count from kh_assign where user_id=%s"
            resultc=db.fetchonedb(sqlc,[list['id']])
            list['icdcount']=resultc['count']
            sqlc="select count(0) as count from kh_assign_vap where user_id=%s"
            resultc=db.fetchonedb(sqlc,[list['id']])
            list['vapcount']=resultc['count']
            sqlc="select count(0) as count from kh_assign_zsh where user_id=%s"
            resultc=db.fetchonedb(sqlc,[list['id']])
            list['zshcount']=resultc['count']
            
        return {"listall":listall,"listcount":listcount,'ret':sql}
    #获得所有团队
    def getusercategory(self):
        sql='select code,label from user_category where id>0'
        listall=db.fetchalldb(sql)
        return listall
    #获得所有团队4位code
    def getusercategory_code4(self):
        sql="select code,label from user_category where code like '__' and closeflag=0"
        listall=db.fetchalldb(sql)
        llall=[]
        for list in listall:
            sqlc="select code,label from user_category where code like '"+str(list['code'])+"__' and closeflag=0"
            child=db.fetchalldb(sqlc)
            list['child']=child
            llall.append(list)
        return llall
    #一键删除所有用户
    def del_alluser(self,checkid):
        sql="delete from user where id in (%s)"
        self.db.updatetodb(sql,[checkid])
        return
    #获得所有权限
    def getauthcategory(self,user_id=''):
        
        sql='select id,label from auth_category where id >0'
        listall=db.fetchalldb(sql)
        return listall
    #权限列表
    def get_auth(self,frompageCount,limitNum,authname):
        sqlarg=''
        argument=[]
        if authname:
            sqlarg+=' and label like %s'
            argument.append('%'+authname+'%')
        sqlc="select count(0) as count from auth_category where id>0"+sqlarg
        result=db.fetchonedb(sqlc,argument)
        listcount=result['count']
        sql='SELECT id as aid,label,(select count(0) from user where auth_category_id =aid) as count FROM auth_category where id>0'+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        listall=db.fetchalldb(sql,argument)
        return {"listall":listall,"listcount":listcount}
    #获得菜单列表
    def get_menu(self,frompageCount,limitNum,next_id,up_id,menuname=''):
        sqlarg=''
        argument=[]
        if menuname:
            sqlarg+=' and label like %s'
            argument.append('%'+menuname+'%')
        if up_id:
            #获得上一级
            sql0="select parent_id from menu where id=%s"
            result0=db.fetchonedb(sql0,[up_id])
            parent_id=result0['parent_id']
            sqlc="select count(0) as count from menu where parent_id=%s "
            result=db.fetchonedb(sqlc,[parent_id])
            listcount=result['count']
            sql="select id,parent_id,label,link,closeflag from menu where parent_id=%s "
            listall=db.fetchalldb(sql,[parent_id])
            for dic in listall:
                dic['menu_category']=''#菜单类型
                parent_id=dic['parent_id'] 
                if parent_id==0:
                    dic['menu_category']=0
                if parent_id==1:
                    dic['menu_category']=1
                if parent_id==2:
                    dic['menu_category']=2
                id=dic['id']
                dic['has_son_menu']=self.has_son_menu(id)
                dic['has_father_menu']=self.has_father_menu(parent_id)
                statustxt=''
                closeflag=dic['closeflag']
                if closeflag==1:
                    statustxt='已冻结'
                if closeflag==0:
                    statustxt='已开通'
                dic['statustxt']=statustxt
            return {"listall":listall,"listcount":listcount}
        else:
            sqlc="select count(0) as count from menu where parent_id=%s "
            result=db.fetchonedb(sqlc,[next_id])
            listcount=result['count']
            sql="select id,parent_id,label,link,closeflag,ord from menu where parent_id=%s "
            listall=db.fetchalldb(sql,[next_id])
            for dic in listall:
                dic['menu_category']=''#菜单类型
                parent_id=dic['parent_id'] 
                if parent_id==0:
                    dic['menu_category']=0
                if self.fir_or_sec(parent_id)==1:
                    dic['menu_category']=1
                if self.fir_or_sec(parent_id)==2:
                    dic['menu_category']=2
                id=dic['id']
                dic['has_son_menu']=self.has_son_menu(id)
                dic['has_father_menu']=self.has_father_menu(parent_id)
                statustxt=''
                closeflag=dic['closeflag']
                if closeflag==1:
                    statustxt='已冻结'
                if closeflag==0:
                    statustxt='已开通'
                dic['statustxt']=statustxt
            return {"listall":listall,"listcount":listcount}
    #判断是否有子菜单
    def has_son_menu(self,id):
        sql="select id from menu where parent_id=%s"
        result=db.fetchonedb(sql,[id])
        if result:
            return 1
        else:
            return 0
    #判断是否有上一级菜单
    def has_father_menu(self,parent_id):
        sql="select id from menu where id=%s"
        result=db.fetchonedb(sql,[parent_id])
        if result:
            return 1
        else:
            return 0
    #判断是一级栏目还是二级栏目
    def fir_or_sec(self,id):
        sql='select id,parent_id from menu where id=%s'
        result=db.fetchonedb(sql,[id])
        if result:
            if result['parent_id']==0:
                return 1
            else:
                return 2
    #菜单选择（取出顶级和一级栏目）
    def getmenulist(self):
        sql='select id,parent_id,label from menu where parent_id=0'
        top_menu=db.fetchalldb(sql)
        if top_menu:
            for res in top_menu:
                id=res['id']
                sql1='select id,parent_id,label from menu where parent_id=%s'
                first_menu=db.fetchalldb(sql1,[id])
                res['first_menu']=first_menu
        return top_menu
    #取出三级菜单
    def getmenulistall(self):
        sql='select id,parent_id,label from menu where parent_id=0'
        top_menu=db.fetchalldb(sql)
        if top_menu:
            for res in top_menu:
                id=res['id']
                sql1='select id,parent_id,label from menu where parent_id=%s'
                first_menu=db.fetchalldb(sql1,[id])
                if first_menu:
                    #res['first_menu']=first_menu
                    for fir in first_menu:
                        id=fir['id']
                        sql2='select id,parent_id,label from menu where parent_id=%s'
                        second_menu=db.fetchalldb(sql2,[id])
                        if second_menu:
                            fir['second_menu']=second_menu
                    res['first_menu']=first_menu
        return top_menu