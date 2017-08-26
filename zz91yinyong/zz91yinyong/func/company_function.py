#-*- coding:utf-8 -*-

class zcompany:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
        self.dbsms=dbsms
    #----公司详情
    def getcompanydetail(self,company_id):
        #获得缓存
        mobile_companydetail=cache.get("mobile_companydetail"+str(company_id))
        if mobile_companydetail:
            return mobile_companydetail
        sqlc="select name,business,regtime,address,introduction,membership_code,domain_zz91 from company where id=%s"
        clist=self.dbc.fetchonedb(sqlc,company_id)
        if clist:
            compname=clist[0]
            business=clist[1]
            regtime=clist[2]
            address=clist[3]
            introduction=clist[4]
            viptype=clist[5]
            domain_zz91=clist[6]
            arrviptype={'vippic':'','vipname':'','vipcheck':'','ldb':''}
            if (viptype == '10051000'):
                arrviptype['vippic']=None
                arrviptype['vipname']='普通会员'
            if (viptype == '10051001'):
                arrviptype['vippic']='http://m.zz91.com/images/recycle.gif'
                arrviptype['vipname']='再生通'
            if (viptype == '100510021000'):
                arrviptype['vippic']='http://m.zz91.com/images/pptSilver.gif'
                arrviptype['vipname']='银牌品牌通'
            if (viptype == '100510021001'):
                arrviptype['vippic']='http://m.zz91.com/images/pptGold.gif'
                arrviptype['vipname']='金牌品牌通'
            if (viptype == '100510021002'):
                arrviptype['vippic']='http://m.zz91.com/images/pptDiamond.gif'
                arrviptype['vipname']='钻石品牌通'
            if (viptype == '10051003'):
                arrviptype['vippic']=''
                arrviptype['vipname']='来电宝客户'
            if (viptype == '10051000'):
                arrviptype['vipcheck']=None
            else:
                arrviptype['vipcheck']=1
            #来电宝客户
            sqll="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code in(1007,1008,1009) and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
            ldbresult=self.dbc.fetchonedb(sqll)
            if ldbresult:
                sqlg="select front_tel,tel from phone where company_id="+str(company_id)+""
                phoneresult=self.dbc.fetchonedb(sqlg)
                if phoneresult:
                    ldbtel=phoneresult[1]
                    ldbtel=ldbtel.replace("-",",")
                    arrviptype['ldb']={'ldbphone':phoneresult[0],'ldbtel':ldbtel}
                else:
                    arrviptype['ldb']=None
            else:
                arrviptype['ldb']=None
        sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
        sqlc=sqlc+",sex,position,qq "
        sqlc=sqlc+"from company_account where company_id=%s"
        alist=self.dbc.fetchonedb(sqlc,company_id)
        if alist:
            contact=alist[0]
            tel_country_code=alist[1]
            if (str(tel_country_code)=='None'):
                tel_country_code=""
            tel_area_code=alist[2]
            if (str(tel_area_code)=='None'):
                tel_area_code=""
            tel=alist[3]
            mobile=alist[4]
            mobilelist=[]
            if (mobile):
                mobile=mobile.strip()
                mobile1=mobile[0:11]
                if len(mobile)>21:
                    mobilelist=re.findall('[\d]+',mobile)
            fax_country_code=alist[5]
            fax_area_code=alist[6]
            fax=alist[7]
            email=alist[8]
            sex=alist[9]
            position=alist[10]
            if (position==None):
                position=""
            position=position.strip()
            qq=alist[11]
        list={'company_id':company_id,'name':compname,'business':business,'domain_zz91':domain_zz91,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'mobilelist':mobilelist,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype}
        #设置缓存
        cache.set("mobile_companydetail"+str(company_id),list,60*10)
        return list
    def savemessages(self,request):
        userName = str(request.POST.get('messPhone'))
        qq = str(request.POST.get('messQQ'))
        email = str(request.POST.get('messEmail'))
        contact = str(request.POST.get('messName'))
        mobile=userName
        messText=str(request.POST.get("messText"))
        
        regtime=gmt_created=datetime.datetime.now()
        title="移动端在线留言"
        contents="联系人："+contact+"<br />联系电话:"+mobile+"<br />邮箱："+email+"<br />QQ:"+qq+"<br />"+messText
        value=[title,contents,gmt_created]
        sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
        self.dbc.updatetodb(sql,value);
    #获得公司ID
    def getcompany_id(self,cname,regtime):
        #获得缓存
        #mobile_getcompany_id=cache.get("mobile_getcompany_id"+str(cname))
        #if mobile_getcompany_id:
            #return mobile_getcompany_id
        sql="select id from company where name=%s order by id desc limit 0,1"
        result=self.dbc.fetchonedb(sql,[str(cname)])
        if (not result):
            return '0'
        else:
            #设置缓存
            #cache.set("mobile_getcompany_id"+str(cname),result[0],60*10)
            return result[0]
    #获得公司ID    
    def getcompanyid(self,username):
        #获得缓存
        #mobile_getcompanyid=cache.get("mobile_getcompanyid"+str(username))
        #if mobile_getcompanyid:
            #return mobile_getcompanyid
        sql="select company_id from company_account where account=%s"
        result=self.dbc.fetchonedb(sql,[username])
        if (not result):
            return '0'
        else:
            #设置缓存
            #cache.set("mobile_getcompanyid"+str(username),result[0],60*10)
            return result[0]
        
    def getprofilerid(self,username):
        #获得缓存
        #mobile_getprofilerid=cache.get("mobile_getprofilerid"+str(username))
        #if mobile_getprofilerid:
            #return mobile_getprofilerid
        sql="select id from bbs_user_profiler where account=%s"
        result=self.dbc.fetchonedb(sql,[username])
        #cursor.execute(sql,[company_id])
        #newcode=cursor.fetchone()
        if (result == None):
            return '0'
        else:
            #设置缓存
            #cache.set("mobile_getprofilerid"+str(username),result[0],60*10)
            return result[0]
    #----注册保存
    def regsave(self,request):
        #获得缓存
        #mobile_regsave=cache.get("mobile_regsave"+str(username))
        #if mobile_regsave:
            #return mobile_regsave
        userName = request.POST.get('messPhone')
        passwd = random.randrange(10000000,99999999)
        qq = request.POST.get('messQQ')
        email = request.POST.get('messEmail')
        contact = request.POST.get('messName')
        mobile=userName
        regtime=gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        errflag=0
        errtext=""
        errflag1=0
        
        if (userName=='' or userName.isdigit()==False):
            errtext="填写手机或您填写的手机有误"
            errflag=1
            errflag1=1
        if (passwd==''):
            errtext="必须填写 密码"
            errflag=1
            errflag1=1
        if (email==''):
            errtext="请输入您的邮箱"
            errflag=1
            errflag1=1
        if (contact==''):
            errtext="必须填写 联系人"
            errflag=1
            errflag1=1
        
        if (errflag==0):
            #''判断邮箱帐号是否存在
            sql="select id  from auth_user where username=%s"
            accountlist=self.dbc.fetchonedb(sql,[str(userName)])
            if (accountlist):
                errflag=1
                errtext="您填写的手机号码已经注册！"
                
            sql="select id  from company_account where mobile=%s"
            accountlist=self.dbc.fetchonedb(sql,[str(userName)])
            if (accountlist):
                errflag=1
                errtext="您填写的手机号码已经注册！"
                
            sql="select id  from auth_user where email=%s"
            accountlist=self.dbc.fetchonedb(sql,[str(email)])
            if (accountlist):
                errflag=1
                errtext="您填写邮箱已经注册！请修改后重新提交！"
        #return errtext
        if (errflag==0):
            #帐号添加
            md5pwd = hashlib.md5(str(passwd))
            md5pwd = md5pwd.hexdigest()[8:-8]
            
            value1=[userName,md5pwd,email,gmt_created,gmt_modified]
            
            sql1="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
            self.dbc.updatetodb(sql1,value1)
            #添加公司信息
            industry_code=''
            business=''
            service_code=''
            area_code=''
            foreign_city=''
            category_garden_id='0'
            membership_code='10051000'
            classified_code='10101002'
            regfrom_code='10031024'
            domain=''
            address=''
            address_zip=''
            website=''
            introduction=''
            introduction=request.POST.get("messText")
            
            value2=[contact, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
            
            sql2="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
            sql2=sql2+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
            self.dbc.updatetodb(sql2,value2)
            
            
            company_id=self.getcompany_id(contact,gmt_created)
            is_admin='1'
            tel_country_code=''
            tel_area_code=''
            tel=mobile
    
            fax_country_code=''
            fax_area_code=''
            fax=''
            sex=''
            #'添加联系方式
            value3=[userName, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, passwd, gmt_modified, gmt_created]
            sql3="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
            sql3=sql3+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
            self.dbc.updatetodb(sql3,value3);
            #-互助用户表
            sqlh="select id from bbs_user_profiler where company_id=%s"
            userlist=self.dbc.fetchonedb(sqlh,[company_id])
            if (userlist==None):
                value=[company_id,userName,userName,email,tel,mobile,qq,userName,gmt_modified,gmt_created]
                sqlu="insert into bbs_user_profiler(company_id,account,nickname,email,tel,mobile,qq,real_name,gmt_modified,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.dbc.updatetodb(sqlu,value)
            
            receiver=mobile
            gmt_modified=gmt_created=gmt_send=datetime.datetime.now()
            content='您已在ZZ91再生网注册成功，您的用户名:'+str(userName)+' 密码：'+str(passwd)+',下载App获得20元，点击  http://zz91.com/m-'
            template_code='sms_mobile'
            send_status=0
            priority=1
            if (mobile!="" and mobile!=None):
                sqla="select id from sms_log where receiver=%s and template_code=%s"
                resaultlist=self.dbsms.fetchonedb(sqla,[mobile,template_code])
                value=[template_code,receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content]
                if (resaultlist==None):
                    sqlp="insert into sms_log(template_code,receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.dbsms.updatetodb(sqlp,value)
        dic_back={'errflag':errflag,'errtext':errtext,'errflag1':errflag1,'userName':userName}
        #设置缓存
        #cache.set("mobile_regsave",dic_back,60*10)
        return dic_back
        #return {'errflag':errflag,'errtext':errtext,'errflag1':errflag1,'userName':userName}
