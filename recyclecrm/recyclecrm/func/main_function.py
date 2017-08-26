# -*- coding:utf-8 -*-
import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
class zzcompany():
    def _init_(self):
        self.db=db
        self.dbc=dbc
        
    def getnowurl(self,request=""):
        host=request.path_info
        qstring=request.META.get('QUERY_STRING','/')
        qstring=qstring.replace("&","^and^")
        if qstring:
            return host+"?"+qstring
        else:
            return host
#云线索公司详情信息
    def yundetails(self,request=""):
        company_id=request.GET.get('company_id')
        sql='select a.id,a.name,a.business,a.industry_code,a.address,a.website,b.contact,b.tel,b.fax,c.label as area from company as a left join company_account as b on a.id=b.company_id left join category as c on a.area_code=c.code where a.id=%s'
        companyinfo=dbc.fetchonedb(sql,[company_id])
        code=companyinfo.get('industry_code')
        if code:
            sqls='select label from category where code=%s'
            companyinfo['industry_code']=dbc.fetchonedb(sqls,[code]).get('label')
        sqls='select id,username,old_company_id from auth_user where old_company_id=%s'
        companyuserlist=dbc.fetchalldb(sqls,[company_id])
        return {'companyinfo':companyinfo,'companyuserlist':companyuserlist}
        
#公司详情信息
    def details(self,request=""):
        company_id=request.GET.get('company_id')
        sql='select id,my_user_id,company_id,name,area,tel,address,industry_code,business,website,fax from company_customer where company_id=%s'
        companyinfo=db.fetchonedb(sql,[company_id])
        if companyinfo:
            code=companyinfo.get('industry_code')
            if code:
                sqls='select label from category where code=%s'
                companyinfo['industry_code']=dbc.fetchonedb(sqls,[code]).get('label')
                sqls='select id,name,company_id,mobile,contact from user where company_id=%s'
                companyuserlist=db.fetchalldb(sqls,[company_id])
        else:
            companyinfo=''
            companyuserlist=''
        return {'companyinfo':companyinfo,'companyuserlist':companyuserlist}
#修改公司信息
    def company_modify(self,request=""):
        company_id=request.POST.get('company_id')
        name=request.POST.get('company_name')
        area=request.POST.get('company_area')
        business=request.POST.get('business')
        contact=request.POST.get('contact')
        mobile=request.POST.get('mobile')
        tel=request.POST.get('tel')
        address=request.POST.get('address')
        website=request.POST.get('website')
        fax=request.POST.get('fax')
        if name and area:
            sql='update company_customer set name=%s,area=%s where company_id=%s'
            result=db.updatetodb(sql,[name,area,company_id])
        if business:
            sql='update company_customer set business=%s where company_id=%s'
            result=db.updatetodb(sql,[business,company_id])
        if contact and mobile:
            sql='insert into user set company_id=%s,contact=%s,mobile=%s'
            result=db.updatetodb(sql,[company_id,contact,mobile])
        if tel:
            sql='update company_customer set tel=%s where company_id=%s'
            result=db.updatetodb(sql,[tel,company_id])
        if address:
            sql='update company_customer set address=%s where company_id=%s'
            result=db.updatetodb(sql,[address,company_id])
        if website:
            sql='update company_customer set website=%s where company_id=%s'
            result=db.updatetodb(sql,[website,company_id])
        if fax:
            sql='update company_customer set fax=%s where company_id=%s'
            result=db.updatetodb(sql,[fax,company_id])
        return result
#添加联系人
    def contact_add(self,request):
        mobile=request.POST.get('mobile_add')
        contact=request.POST.get('contact_add')
        gmt_created=datetime.datetime.now()
        sql="insert into user(contact,mobile,gmt_created) values(%s,%s,%s)"
        result=db.updatetodb(sql,[contact,mobile,gmt_created])
        return result
#修改联系人
    def contact_mod(self,request):
        mobile0=request.POST.get('mobile0')
        contact0=request.POST.get('contact0')
        mobile=request.POST.get('mobile')
        contact=request.POST.get('contact')
        gmt_modified=datetime.datetime.now()
        sql="update user set mobile=%s,contact=%s,gmt_modified=%s where mobile=%s and contact=%s"
        result=db.updatetodb(sql,[mobile,contact,gmt_modified,mobile0,contact0])
        return result
#跟进记录
    def history(self,request=""):
        user_id=''
        my_user_id=request.session.get('user_id')
        company_id=request.GET.get('company_id')
        sqls='select id from auth_user where old_company_id=%s'
        companyuserid=dbc.fetchalldb(sqls,[company_id])
        if companyuserid:
            for list in companyuserid:
                user_id+=str(list['id'])+','
                user_id = user_id[:-1]
            sql="select my_user_id,user_id,remark_type,content,star,recently_contact_time from user_remark_log where my_user_id=%s and user_id in("+user_id+")"
            listall=db.fetchalldb(sql,[my_user_id])
            for list in listall:
                time=list.get('recently_contact_time')
                if time:
                    list['recently_contact_time']=formattime(time,flag=2)
                    list['date']=formattime(time,flag=5)
                    content=list.get('content')
                    if not content:
                        list['content']=''
            return {'listall':listall}
        else:
            return {'listall':''}

#加入我的客户库
    def addto(self,request=""):
        my_user_id=request.session.get('user_id')
        company_id=request.POST.get('company_id')
        recently_contact_time=datetime.datetime.now()
        star=request.POST.get('star')
        gmt_created=datetime.datetime.now()
        register_time=datetime.datetime.now()
        sql='select id from company_customer where company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        if not result:
            sql1='select a.id,a.name,a.business,a.industry_code,a.address,a.website,b.fax,b.tel,c.label from company as a left join company_account as b on a.id=b.company_id left join category as c on c.code=a.area_code where a.id=%s'
            result1=dbc.fetchonedb(sql1,[company_id])
            sql2='insert into company_customer(my_user_id,company_id,isclue,name,area,address,industry_code,business,register_time,gmt_created,website,tel,fax) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result2=db.updatetodb(sql2,[my_user_id,result1['id'],1,result1['name'],result1['label'],result1['address'],result1['industry_code'],result1['business'],register_time,gmt_created,result1['website'],result1['tel'],result1['fax']])
            sql3='select id,contact,sex,position,tel,mobile,weixin,email from company_account where company_id=%s'
            result3=dbc.fetchalldb(sql3,[company_id])
            if result3:
                for list in result3:
                    sql4='insert into user_customer(my_user_id,user_id,contact,sex,position,tel,mobile,wechat,email,register_time,isflag) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    result4=db.updatetodb(sql4,[my_user_id,list['id'],list['contact'],list['sex'],list['position'],list['tel'],list['mobile'],list['weixin'],list['email'],register_time,0])
#提醒行动
    def action(self,request=""):
        my_user_id=request.session.get('user_id')
        user_id=request.POST.get('customer_id')
        if_useful_contact=request.POST.get('if_useful_contact')
        star=request.POST.get('star')
        recently_remark_type=request.POST.get('remark_type')
        remark_type=request.POST.get('remark_type')
        recently_contact_time=datetime.datetime.now()
        gmt_created=datetime.datetime.now()
        next_contact_time=request.POST.get('next_contact_time')
        sql='select id from user_remark where my_user_id=%s and user_id=%s'
        result=db.fetchonedb(sql,[my_user_id,user_id])
        if not result:
            sql='insert into user_remark(my_user_id,user_id,recently_remark_type,recently_contact_time,next_contact_time) values(%s,%s,%s,%s,%s)'
            result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,recently_contact_time,next_contact_time])
        else:
            sql='update user_remark set recently_remark_type=%s,recently_contact_time=%s,next_contact_time=%s where my_user_id=%s and user_id=%s'
            result=db.updatetodb(sql,[recently_remark_type,recently_contact_time,next_contact_time,my_user_id,user_id])
        sqls='insert into user_remark_log(my_user_id,user_id,remark_type,next_contact_time,gmt_created) values(%s,%s,%s,%s,%s)'
        result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,next_contact_time,gmt_created])
#获取我的联系人
    def contact_list(self,request=""):
        sqls=""
        argument=[]
        my_user_id=request.session.get('user_id',default=None)
        star=request.GET.get('star')
        today=request.GET.get('today')
        time_today=datetime.date.today()
        losecontact=request.GET.get('losecontact')
        if my_user_id:
            sqls+=" and a.my_user_id=%s"
            argument.append(my_user_id)
        if star:
            sqls+=" and c.star=%s"
            argument.append(star)
        if today:
            sqls+=" and c.next_contact_time=%s and c.recently_remark_type=%s"
            argument.append(time_today)
            argument.append(today)
        if losecontact:
            sqls+=" and c.next_contact_time<%s"
            argument.append(time_today)
        sql="select a.id,a.user_id,a.mobile,a.position,a.sex,b.name,b.area,a.contact,c.recently_contact_time,c.next_contact_time,c.star,c.recently_remark_type from user_customer as a left join company_customer as b on a.user_id=b.my_user_id left join user_remark as c on c.user_id=a.user_id where a.id>0 "+sqls+""
        listall=db.fetchalldb(sql,argument)
        for list in listall:
            if list['star']==6:
                list['star']='待回访客户'
            elif list['star']==1:
                list['star']='无意向客户'
            elif list['star']==2:
                list['star']='潜在客户'
            elif list['star']==3:
                list['star']='有意向客户'
            elif list['star']==4:
                list['star']='确认合作客户'
            elif list['star']==5:
                list['star']='重点客户'
            if list['recently_remark_type']==1:
                list['recently_remark_type']='打电话'
            if list['recently_remark_type']==2:
                list['recently_remark_type']='发短信'
            if list['recently_remark_type']==3:
                list['recently_remark_type']='约见面'
            if list['next_contact_time']==None:
                list['next_contact_time']=''
            else:
                next_contact_time=list['next_contact_time']
                list['next_contact_time']=formattime(next_contact_time,2)
            if list['recently_contact_time']==None:
                list['recently_contact_time']=''
            else:
                recently_contact_time=list['recently_contact_time']
                list['recently_contact_time']=formattime(recently_contact_time,2)
        return {'listall':listall}
#获取公司联系人信息
    def contact(self,request=""):
        my_user_id=request.POST.get('user_id')
        user_id=request.POST.get('user_id')
        recently_remark_type=request.POST.get('action')
        remark_type=request.POST.get('action')
        recently_contact_time=datetime.datetime.now()
        company_id=request.POST.get('company_id')
        content=request.POST.get('text')
        sqls='select mobile,name,position,id from user where company_id=%s'
        listall=db.fetchalldb(sqls,[company_id])
        return {'listall':listall}
#获取联系人信息
    def getcontact(self,request=""):
        company_id=request.GET.get('company_id')
        sqls='select mobile,name,position from user where company_id=%s'
        listall=db.fetchalldb(sqls,[company_id])
        return {'listall':listall}
#操作记录
    def remark(self,request=""):
        my_user_id=request.session.get('user_id')
        user_id=request.POST.get('user_id')
        recently_remark_type=request.POST.get('remark_type')
        remark_type=request.POST.get('remark_type')
        recently_contact_time=datetime.datetime.now()
        content=request.POST.get('content')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        star=request.POST.get('star')
        next_contact=request.POST.get('next_contact')
        next_contact_time=request.POST.get('next_contact_time')
        timestamp=time.time()
        timestamp_today=timestamp-timestamp%86400
        next_contact_timestamp=0
        if next_contact is None:
            next_contact_time=next_contact_time
        else:
            if next_contact=='1':
                next_contact_timestamp+=time.time()+60*60
            elif next_contact=='2':
                next_contact_timestamp+=timestamp_today+24*60*60+60*60
            elif next_contact=='3':
                next_contact_timestamp+=timestamp_today+24*60*60+7*60*60
            elif next_contact=='4':
                next_contact_timestamp+=timestamp_today+2*24*60*60+60*60
            elif next_contact=='5':
                next_contact_timestamp+=timestamp_today+2*24*60*60+7*60*60
            next_contact_time=timestamp_to_date(float(next_contact_timestamp))
        sql='select id from user_remark where my_user_id=%s and user_id=%s'
        result=db.fetchonedb(sql,[my_user_id,user_id])
        if remark_type=="2":
            if not result:
                sql='insert into user_remark(my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,call_count,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)'
                result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,1,recently_contact_time,1,gmt_created])
            else:
                sqls='update user_remark set recently_remark_type=%s,recently_contact_time=%s,my_user_id=%s,user_id=%s,recently_remark_type=%s,recently_contact_time=%s,call_count=call_count+1,gmt_modified=%s where my_user_id=%s and user_id=%s'
                result=db.updatetodb(sqls,[recently_remark_type,recently_contact_time,my_user_id,user_id,recently_remark_type,recently_contact_time,gmt_modified,my_user_id,user_id])
            sqls='insert into user_remark_log(my_user_id,user_id,remark_type,iscontact,recently_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,1,recently_contact_time,gmt_created])
        elif remark_type=="1":
            if not result:
                sql='insert into user_remark(my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,message_count,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)'
                result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,1,recently_contact_time,1,gmt_created])
            else:
                sqls='update user_remark set recently_remark_type=%s,recently_contact_time=%s,message_count=message_count+1,gmt_modified=%s where my_user_id=%s and user_id=%s'
                result=db.updatetodb(sqls,[recently_remark_type,recently_contact_time,gmt_modified,my_user_id,user_id])
            sqls='insert into user_remark_log(my_user_id,user_id,remark_type,iscontact,recently_contact_time,gmt_created,content) values(%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,1,recently_contact_time,gmt_created,content])
        elif remark_type=="3":
            if not result:
                sql='insert into user_remark(my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,next_contact_time,visit_count,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,1,recently_contact_time,next_contact_time,1,gmt_created])
            else:
                sqls='update user_remark set recently_remark_type=%s,recently_contact_time=%s,next_contact_time=%s,visit_count=visit_count+1,gmt_modified=%s where my_user_id=%s and user_id=%s'
                result=db.updatetodb(sqls,[recently_remark_type,recently_contact_time,next_contact_time,gmt_modified,my_user_id,user_id])
            sqls='insert into user_remark_log(my_user_id,user_id,remark_type,iscontact,recently_contact_time,star,next_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,1,recently_contact_time,star,next_contact_time,gmt_created])
#客户小计
    def bz(self,request=""):
        my_user_id=request.session.get('user_id')
        user_id=request.POST.get('user_id')
        content=request.POST.get('bz')
        star=request.POST.get('star')
        gmt_created=datetime.datetime.now()
        recently_contact_time=datetime.datetime.now()
        next_contact=request.POST.get('next_contact')
        timestamp=time.time()
        timestamp_today=timestamp-timestamp%86400
        next_contact_timestamp=0
        if next_contact=='1':
            next_contact_timestamp+=time.time()+60*60
        elif next_contact=='2':
            next_contact_timestamp+=timestamp_today+24*60*60+60*60
        elif next_contact=='3':
            next_contact_timestamp+=timestamp_today+24*60*60+7*60*60
        elif next_contact=='4':
            next_contact_timestamp+=timestamp_today+2*24*60*60+60*60
        elif next_contact=='5':
            next_contact_timestamp+=timestamp_today+2*24*60*60+7*60*60
        next_contact_time=timestamp_to_date(float(next_contact_timestamp))
        sql='select id from user_remark where my_user_id=%s and user_id=%s'
        result=db.fetchonedb(sql,[my_user_id,user_id])
        if not result:
            sql='insert into user_remark(my_user_id,user_id,recently_contact_time,star,next_contact_time) values(%s,%s,%s,%s,%s)'
            result=db.updatetodb(sql,[my_user_id,user_id,recently_contact_time,star,next_contact_time])
        else:
            sqls='update user_remark set recently_contact_time=%s,star=%s,next_contact_time=%s where my_user_id=%s and user_id=%s'
            result=db.updatetodb(sqls,[recently_contact_time,star,my_user_id,user_id,next_contact_time])
        sql='insert into user_remark_log(my_user_id,user_id,content,star,recently_contact_time,next_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)'
        result=db.updatetodb(sql,[my_user_id,user_id,content,star,recently_contact_time,next_contact_time,gmt_created])
#保存注册信息
    def reg_save(self,request=""):
        name=request.POST.get('name')
        password=request.POST.get('password')
        password = hashlib.md5(password)
        password = password.hexdigest()[8:-8]
        contact=request.POST.get('contact')
        position=request.POST.get('position')
        sex=request.POST.get('sex')
        wechat=request.POST.get('wechat')
        address=request.POST.get('address')
        obj=request.FILES.get('fileField')
        timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
        tmp = random.randint(100, 999)
        nowtime=int(time.time())
        time_now=datetime.datetime.now()
        resumeUrl=''
        if obj:
            filename=obj.name
            kzname=''
            if filename:
                arrfile=filename.split(".")
                kzname=arrfile[len(arrfile)-1]
            newpath=nowpath+"/file/"+timepath
            imgpath=newpath+str(nowtime)+str(tmp)+"."+kzname
            if not os.path.isdir(newpath):
                os.makedirs(newpath)
            f=open(imgpath, 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
                f.close()
            resumeUrl=timepath+str(nowtime)+str(tmp)+"."+kzname
        sql='select id from user where name=%s'
        result=db.fetchonedb(sql, [name])
        if not result:
            sql='insert into user(name,password,contact,position,sex,wechat,address,header_path) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sql,[name,password,contact,position,sex,wechat,address,resumeUrl])
#获取公司信息
    def getcompanylist(self,keywords,area,industry,jisd,frompageCount,limitNum,allnum):
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
        cl.SetLimits (frompageCount,limitNum,allnum)
        if (keywords):
            res = cl.Query ('@(name,sale_details,buy_details) '+keywords,'company')
        elif (area):
            res = cl.Query ('@(area_name,area_province) '+area,'company')
        elif (industry):
            res = cl.Query ('@(business) '+industry,'company')
        elif (jisd):
            res = cl.Query('@(area_name,area_province)'+jisd,'company')
        else:
            res = cl.Query ('','company')
        if res:
            if res.has_key('matches'):
                clist=res['matches']
                listall_comp=[]
                for match in clist:
                    id=match['id']
                    attrs=match['attrs']
                    compname=attrs['compname']
                    viptype=str(attrs['membership_code'])
                    domain_zz91=attrs['domain_zz91']
                    address=attrs['paddress']
                    membership="普通会员"
                    vipflag=None
                    if (viptype == '10051000'):
                        membership='普通会员'
                        vipflag=None
                    if (viptype == '10051001'):
                        membership='再生通'
                        vipflag=1
                    if (viptype == '1725773192'):
                        membership='银牌品牌通'
                        vipflag=1
                    if (viptype == '1725773193'):
                        membership='金牌品牌通'
                        vipflag=1
                    if (viptype == '1725773194'):
                        membership='钻石品牌通'
                        vipflag=1
                    pbusiness=attrs['pbusiness']
                    if pbusiness:
                        pbusiness=subString(filter_tags(pbusiness),500)
                    parea_province=attrs['parea_province']
                    list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'address':address,'membership':membership,'viptype':viptype,'vipflag':vipflag,'domain_zz91':domain_zz91}
                    listall_comp.append(list1)
                listcount_comp=res['total_found']
    
                return {'list':listall_comp,'count':listcount_comp}
#获取行业类别
def getindexcategorylist(code,showflag):
    catelist=cache.get("mobile_categrc"+str(code))
    if (catelist==None):
        if (showflag==2):
            sql="select label,code,pinyin from category_products where code like %s order by sort asc"
        else:
            sql="select label,code,pinyin from category_products where code like %s"'"____"'" order by sort asc"
        #cursor.execute(sql,[str(code)])
        listall_cate=[]
        #catelist=cursor.fetchall()
        catelist=dbc.fetchalldb(sql,[str(code)])
        numb=0
        for a in catelist:
            numb=numb+1
            if (showflag==1):
                sql1="select label,pinyin,code from category_products where code like '"+str(a[1])+"____' order by sort asc"
                #cursor.execute(sql1)
                listall_cate1=[]
                #catelist1=cursor.fetchall()
                catelist1=dbc.fetchalldb(sql1)
                for b in catelist1:
                    pinyin=b[1]
                    if pinyin:
                        pinyin=pinyin.lower()
                    list1={'label':b[0],'label_hex':getjiami(b[0]),'pinyin':pinyin,'code':b[2]}
                    listall_cate1.append(list1)
            else:
                listall_cate1=None
            pinyin=a[2]
            if pinyin:
                pinyin=pinyin.lower()
            list={'label':a[0],'label_hex':getjiami(a[0]),'code':a[1],'catelist':listall_cate1,'numb':numb,'pinyin':pinyin}
            listall_cate.append(list)
        cache.set("mobile_categrc"+str(code),listall_cate,60*6)
    else:
        listall_cate=catelist
    
    return listall_cate