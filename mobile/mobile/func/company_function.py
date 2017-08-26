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
        sqlc="select a.name,a.business,a.regtime,a.address,a.introduction,a.membership_code,a.domain_zz91,b.label as industry ,c.label,d.label from company as a LEFT OUTER JOIN category as b on a.industry_code=b.code LEFT OUTER JOIN category as c on left(a.area_code,12)=c.code LEFT OUTER JOIN category as d on left(a.area_code,16)=d.code where a.id=%s and a.is_block=0"
        clist=self.dbc.fetchonedb(sqlc,[company_id])
        if clist:
            compname=clist[0]
            business=clist[1]
            regtime=formattime(clist[2],0)
            address=clist[3]
            introduction=clist[4]
            viptype=clist[5]
            domain_zz91=clist[6]
            industry=clist[7]
            province=clist[8]
            city=clist[9]
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
            sqll="select id from crm_company_service where company_id=%s and crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
            ldbresult=self.dbc.fetchonedb(sqll,[company_id])
            if ldbresult:
                sqlg="select front_tel,tel from phone where company_id=%s"
                phoneresult=self.dbc.fetchonedb(sqlg,[company_id])
                if phoneresult:
                    ldbtel=phoneresult[1]
                    ldbtel=ldbtel.replace("-",",")
                    arrviptype['ldb']={'ldbphone':phoneresult[0],'ldbtel':ldbtel}
                else:
                    arrviptype['ldb']=None
            else:
                arrviptype['ldb']=None
            #头像
            faceurl=None
            sql="select picture_path from bbs_user_profiler where company_id=%s"
            piclist=dbc.fetchonedb(sql,[company_id])
            faceurl=None
            if piclist:
                if piclist[0]:
                    if piclist[0]:
                        faceurl="http://img3.zz91.com/100x100/"+piclist[0]
            if not faceurl:
                faceurl='http://static.m.zz91.com/aui/images/noavatar.gif'
        else:
            return None
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
            mobile1=''
            if (mobile):
                mobile=mobile.strip()
                mobile1=mobile[0:11]
                if len(mobile)>21:
                    mobilelist=re.findall('[\d]+',mobile)
                else:
                    mobilelist=[mobile1]
            if tel:
                tellist=''
                if tel_country_code:
                    tellist+=tel_country_code+"-"
                if tel_area_code:
                    tellist+=tel_area_code+"-"
                tellist+=tel
                if tellist!=mobile1:
                    mobilelist.append(tellist)
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
        list={'company_id':company_id,'industry':industry,'province':province,'city':city,'faceurl':faceurl,'name':compname,'business':business,'domain_zz91':domain_zz91,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'mobilelist':mobilelist,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype}
        #设置缓存
        cache.set("mobile_companydetail"+str(company_id),list,60*30)
        return list
    def savemessages(self,request,s,paytype=47):
        username=request.session.get("username",None)
        company_id=request.session.get("company_id",None)
        merchant_url=request.POST.get("merchant_url")
        
        if not username:
            #userName = str(request.POST.get('messPhone'))
            #mobile=userName
            #qq = str(request.POST.get('messQQ'))
            #email = str(request.POST.get('messEmail'))
            #contact = str(request.POST.get('messName'))
            company_id=s['company_id']
        messText=str(request.POST.get("messText"))
        regtime=gmt_created=datetime.datetime.now()
        contents=str(messText)+str(merchant_url)
        value=[company_id,contents,gmt_created,paytype]
        sql="insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)"
        self.dbc.updatetodb(sql,value);
    #获得公司ID
    def getcompany_id(self,cname,regtime):
        #获得缓存
        #mobile_getcompany_id=cache.get("mobile_getcompany_id"+str(cname))
        #if mobile_getcompany_id:
            #return mobile_getcompany_id
        sql="select id from company where gmt_created=%s order by id desc limit 0,1"
        result=self.dbc.fetchonedbmain(sql,[regtime])
        if (not result):
            return 0
        else:
            #设置缓存
            #cache.set("mobile_getcompany_id"+str(cname),result[0],60*10)
            return result[0]
    #----是否来电宝客户
    def getisldb(self,company_id):
        sqlg="select front_tel from phone where company_id=%s and expire_flag=0 and exists(select company_id from crm_company_service where crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and company_id=phone.company_id)"
        phoneresult=dbc.fetchonedb(sqlg,company_id)
        if phoneresult:
            return 1
        else:
            return None
    #----是否已经加入通讯录
    def isaddressbook(self,company_id,forcompany_id):
        sql="select id from company_addressbook where company_id=%s and forcompany_id=%s"
        result=dbc.fetchonedb(sql,[company_id,forcompany_id])
        if result:
            return 1
        else:
            return None
    #加入通信录
    def joinaddressbook(self,company_id,forcompany_id):
        sql="select id from company_addressbook where company_id=%s and forcompany_id=%s"
        result=dbc.fetchonedb(sql,[company_id,forcompany_id])
        gmt_created=datetime.datetime.now()
        if not result:
            sqlc="insert into company_addressbook(company_id,forcompany_id,gmt_created) values(%s,%s,%s)"
            dbc.updatetodb(sqlc,[company_id,forcompany_id,gmt_created])
            return 1
        else:
            return None
    #获得公司名
    def getcompanyname(self,company_id):
        sql="select name from company where id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
        else:
            return ''
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
    #是否完善诚信档案
    def getcxinfo(self,company_id):
        sql="select check_status from company_attest where company_id=%s and check_status in (0,1)"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
        sql="select check_status from credit_file where company_id=%s and check_status in (0,1)"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
        return None
    def getcxinfocheck(self,company_id):
        sql="select check_status from company_attest where company_id=%s and check_status='1'"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return 1
        sql="select check_status from credit_file where company_id=%s and check_status='1'"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return 1
        return None
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
    #获得头像
    def getfacepic(self,company_id):
        sql="select picture_path from bbs_user_profiler where company_id=%s"
        newcode=self.dbc.fetchonedb(sql,[company_id])
        if (newcode == None):
            return 'http://static.m.zz91.com/aui/images/noavatar.gif'
        else:
            if newcode[0]:
                return 'http://img3.zz91.com/200x15000/'+newcode[0]
            else:
                return 'http://static.m.zz91.com/aui/images/noavatar.gif'
    #----注册保存
    def regsave(self,request,sendmsg=1):
        #获得缓存
        #mobile_regsave=cache.get("mobile_regsave"+str(username))
        #if mobile_regsave:
            #return mobile_regsave
        userName = request.POST.get('messPhone')
        password = request.POST.get('password')
        if not password:
            passwd = random.randrange(10000000,99999999)
        else:
            passwd=password
        
        qq = request.POST.get('messQQ')
        email = request.POST.get('messEmail')
        if not email:
            email=userName+"@139.com"
        contact = request.POST.get('messName')
        messbusiness = request.POST.get('messbusiness')
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
        if (len(userName)<=10):
            errtext="填写手机号码必须大于11位"
            errflag=1
            errflag1=1
        if (passwd==''):
            errtext="必须填写 密码"
            errflag=1
            errflag1=1
        if (email=='' or validateEmail(email)==0):
            errtext="请输入您的邮箱或邮箱格式有错误！"
            errflag=1
            errflag1=1
        if (contact==''):
            errtext="必须填写 联系人"
            errflag=1
            errflag1=1
        company_id=request.session.get("company_id",None)
        if (errflag==0):
            #''判断邮箱帐号是否存在
            sql="select id  from auth_user where username=%s or mobile=%s"
            accountlist=self.dbc.fetchonedb(sql,[str(userName),userName])
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
            sql="select id  from company_account where email=%s"
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
            industry_code=request.POST.get("industry_code")
            if not industry_code:
                industry_code=''
            if not messbusiness:
                business=''
            else:
                business=messbusiness
            service_code=''
            area_code=''
            foreign_city=''
            category_garden_id='0'
            membership_code='10051000'
            classified_code='10101002'
            regfrom_code='10031039'
            if request.POST.get("regfrom_code"):
                regfrom_code=request.POST.get("regfrom_code")
            domain=''
            address=''
            address_zip=''
            website=''
            introduction=''
            introduction=request.POST.get("messText")
            companyname=request.POST.get("companyname")
            if not companyname:
                companyname="("+str(contact)+")"
            
            value2=[companyname, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
            
            sql2="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
            sql2=sql2+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
            result=self.dbc.updatetodb(sql2,value2)
            if not result:
                return
            else:
                company_id=result[0]
            
            #company_id=self.getcompany_id(contact,gmt_created)
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
            userlist=self.dbc.fetchonedbmain(sqlh,[company_id])
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
            if (mobile!="" and mobile!=None and sendmsg):
                sqla="select id from sms_log where receiver=%s and template_code=%s"
                resaultlist=self.dbsms.fetchonedbmain(sqla,[mobile,template_code])
                value=[template_code,receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content]
                if (resaultlist==None):
                    sqlp="insert into sms_log(template_code,receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.dbsms.updatetodb(sqlp,value)
        dic_back={'errflag':errflag,'errtext':errtext,'errflag1':errflag1,'userName':userName,'company_id':company_id}
        #设置缓存
        #cache.set("mobile_regsave",dic_back,60*10)
        return dic_back
        #return {'errflag':errflag,'errtext':errtext,'errflag1':errflag1,'userName':userName}
