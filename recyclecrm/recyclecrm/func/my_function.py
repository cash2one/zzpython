# -*- coding:utf-8 -*-
import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
class zzmy():
    def __init__(self):
        self.db=db
        self.dbc=dbc
        
    def getmyinfo(self,request=""):
        my_user_id=request.session.get('user_id',default=None)
        sql="select a.contact,b.name,a.company_id from user as a left join company as b on a.company_id=b.id where a.id=%s"
        result=db.fetchonedb(sql,[my_user_id])
        if not result:
            name=""
            company_name=""
            company_id=""
        else:
            name=result['contact']
            company_name=result['name']
            company_id=result['company_id']
        sql1="select count(0) as count from company_customer where my_user_id=%s"
        result1=db.fetchonedb(sql1,[my_user_id])
        customer_count=result1['count']
        sql2="select count(0) as count from user_customer where my_user_id=%s"
        result2=db.fetchonedb(sql2,[my_user_id])
        contact_count=result2['count']
        return {'name':name,'company_name':company_name,'customer_count':customer_count,'contact_count':contact_count,'company_id':company_id}
    
    def getcompinfo(self,request=""):
        company_id=request.POST.get("company_id")
        sql="select name,industry_code,area,address,tel,fax,zip,business from company where id=%s"
        result=db.fetchonedb(sql,[company_id])
        return result
    
    def getmycontact(self,request=""):
        my_user_id=request.session.get('user_id',default=None)
        sql="select contact,mobile,user_id from user_customer where my_user_id=%s"
        result=db.fetchalldb(sql,[my_user_id])
        return result
    
    def contact_mod(self,request=""):
        my_user_id=request.session.get('user_id',default=None)
        user_id=request.POST.get('user_id')
        sql='select id,my_user_id,user_id,contact,position,sex,wechat,mobile,tel,email,address from user_customer where my_user_id=%s and user_id=%s'
        result=db.fetchonedb(sql,[my_user_id,user_id])
        return result
    
    def contact_save(self,request=""):
        my_user_id=request.session.get('user_id',default=None)
        user_id=request.POST.get('user_id')
        contact=request.POST.get('contact')
        position=request.POST.get('position')
        sex=request.POST.get('sex')
        wechat=request.POST.get('wechat')
        mobile=request.POST.get('mobile')
        tel=request.POST.get('tel')
        email=request.POST.get('email')
        area=request.POST.get('area')
        address=request.POST.get('address')
        sql='update user_customer set contact=%s,position=%s,sex=%s,wechat=%s,mobile=%s,tel=%s,email=%s,address=%s where my_user_id=%s and user_id=%s'
        result=db.updatetodb(sql,[contact,position,sex,wechat,mobile,tel,email,address,my_user_id,user_id])
    
    def security_save(self,request=""):
        my_user_id=request.session.get('user_id',default=None)
        name=request.POST.get('mobile')
        password=request.POST.get('password')
        password = hashlib.md5(password)
        password = password.hexdigest()[8:-8]
        sql="update user set name=%s,password=%s where id=%s"
        result=db.updatetodb(sql,[name,password,my_user_id])
        
    def compinfo_save(self,request):
        company_id=request.POST.get('company_id')
        name=request.POST.get('name')
        address=request.POST.get('address')
        tel=request.POST.get('tel')
        fax=request.POST.get('fax')
        zip=request.POST.get('zip')
        business=request.POST.get('business')
        sql="update company set name=%s,address=%s,tel=%s,fax=%s,zip=%s,business=%s where id=%s"
        result=db.updatetodb(sql,[name,address,tel,fax,zip,business,company_id])