#-*- coding:utf-8 -*-
import datetime,random,hashlib,md5
class zzdibang:
    def __init__(self):
        self.dbd=dbd
    
    def company_list(self,frompageCount,limitNum,name=''):
        sqls=''
        argument=[]
        if name:
            sqls+='and name=%s'
            argument.append(name)
        sql='select id,group_id,name,ctype,gmt_created,gmt_modified from company where id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from company where id>0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            group_id=result['group_id']
            name=result['name']
            ctype=result['ctype']
            if ctype=='1':
                ctype='公司'
            elif ctype=='2':
                ctype='个人'
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            if group_id is None:
                group_id=''
            list={'id':id,'group_id':group_id,'name':name,'ctype':ctype,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}
    
    def company_save(self,request):
        id=request.POST.get('id')
        name=request.POST.get('name')
        ctype=request.POST.get('ctype')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update company set name=%s,ctype=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[name,ctype,gmt_modified,id])
        else:
            sql='insert into company(group_id,name,ctype,gmt_created) values(%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[group_id,name,ctype,gmt_created])
            
    def user_list(self,frompageCount,limitNum,name=''):
        sqls=''
        argument=[]
        if name:
            sqls+='and username=%s'
            argument.append(name)
        sql='select id,group_id,company_id,clientid,utype,username,contact,sex,mobile,bz,gmt_created,gmt_modified from users where id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from users where id>0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            group_id=result['group_id']
            company_id=result['company_id']
            clientid=result['clientid']
            utype=result['utype']
            if utype=='1':
                utype='管理员'
            elif utype=='2':
                utype='校验员'
            elif utype=='3':
                utype='财务人员'
            username=result['username']
            contact=result['contact']
            sex=result['sex']
            mobile=result['mobile']
            bz=result['bz']
            gmt_created=result['gmt_created']
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            gmt_created=formattime(gmt_created,flag=2)
            if group_id is None:
                group_id=''
            list={'id':id,'group_id':group_id,'company_id':company_id,'clientid':clientid,'utype':utype,'username':username,'contact':contact,'sex':sex,'mobile':mobile,'bz':bz,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}
    
    def user_save(self,request):
        id=request.POST.get('id')
        group_id=request.POST.get('group_id')
        company_id=request.POST.get('company_id')
        list=['0','1','2','3','4','5','6','7','8','9']
        clientid=str(time.time())[:-3]+str(company_id)+random.choice(list)+random.choice(list)+random.choice(list)
        md5clientid = hashlib.md5(clientid)
        clientid = md5clientid.hexdigest()[8:-8]
        utype=request.POST.get('utype')
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        md5pwd = hashlib.md5(pwd)
        pwd = md5pwd.hexdigest()[8:-8]
        contact=request.POST.get('contact')
        sex=request.POST.get('sex')
        mobile=request.POST.get('mobile')
        bz=request.POST.get('bz')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update users set utype=%s,username=%s,pwd=%s,contact=%s,sex=%s,mobile=%s,bz=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[utype,username,pwd,contact,sex,mobile,bz,gmt_modified,id])
        else:
            sql='insert into users(group_id,company_id,clientid,utype,username,pwd,contact,sex,mobile,bz,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[group_id,company_id,clientid,utype,username,pwd,contact,sex,mobile,bz,gmt_created])
            
    def storage_list(self,frompageCount,limitNum,code=''):
        sqls=''
        argument=[]
        if code:
            sqls+='and code=%s'
            argument.append(code)
        sql='select id,selfid,group_id,company_id,code,products_selfid,suppliers_selfid,price,gw,nw,tare,total,status,price_users_selfid,price_time,ispay,scorecheck,pay_time,pay_users_selfid,gmt_created,gmt_modified from storage where id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from storage where id>0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            selfid=result['selfid']
            group_id=result['group_id']
            company_id=result['company_id']
            code=result['code']
            products_selfid=result['products_selfid']
            suppliers_selfid=result['suppliers_selfid']
            price=result['price']
            gw=result['gw']
            nw=result['nw']
            tare=result['tare']
            total=result['total']
            status=result['status']
            if status==0:
                status='过磅中'
            elif status==1:
                status='过磅完成'
            elif status==2:
                status='定价完成'
            elif status==3:
                status='完成皮重'
            elif status==4:
                status='结算完成'
            elif status==99:
                status='作废'
            price_users_selfid=result['price_users_selfid']
            price_time=result['price_time']
            ispay=result['ispay']
            if ispay==0:
                ispay='未支付'
            elif ispay==1:
                ispay='已支付'
            scorecheck=result['scorecheck']
            if scorecheck==0:
                scorecheck='未提现'
            elif scorecheck==1:
                scorecheck='已提现'
            pay_time=result['pay_time']
            pay_users_selfid=result['pay_users_selfid']
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if price_time is None:
                price_time=''
            else:
                price_time=formattime(price_time,flag=2)
            if pay_time is None:
                pay_time=''
            else:
                pay_time=formattime(pay_time,flag=2)
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            if group_id is None:
                group_id=''
            list={'id':id,'selfid':selfid,'group_id':group_id,'company_id':company_id,'code':code,'products_selfid':products_selfid,'suppliers_selfid':suppliers_selfid,'price':price,'gw':gw,'nw':nw,'tare':tare,'total':total,'status':status,'price_users_selfid':price_users_selfid,'price_time':price_time,'ispay':ispay,'scorecheck':scorecheck,'pay_time':pay_time,'pay_users_selfid':pay_users_selfid,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}
    
    def storage_save(self,request):
        id=request.POST.get('id')
        group_id=request.POST.get('group_id')
        company_id=request.POST.get('company_id')
        sql='select id from suppliers where group_id=%s and company_id=%s'
        result=dbd.fetchonedb(sql,[group_id,company_id])
        suppliers_selfid=result['id']
        list=['0','1','2','3','4','5','6','7','8','9']
        selfid=str(time.time())[:-3]+str(company_id)+random.choice(list)+random.choice(list)+random.choice(list)
        md5selfid = hashlib.md5(selfid)
        selfid = md5selfid.hexdigest()[8:-8]
        code=request.POST.get('code')
        products_selfid=request.POST.get('products_selfid')
        price=request.POST.get('price')
        gw=request.POST.get('gw')
        nw=request.POST.get('nw')
        tare=request.POST.get('tare')
        total=request.POST.get('total')
        status=request.POST.get('status')
        price_users_selfid=request.POST.get('price_users_selfid')
        price_time=request.POST.get('price_time')
        ispay=request.POST.get('ispay')
        scorecheck=request.POST.get('scorecheck')
        pay_time=request.POST.get('pay_time')
        pay_users_selfid=request.POST.get('pay_users_selfid')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update storage set code=%s,price=%s,gw=%s,nw=%s,tare=%s,total=%s,status=%s,price_time=%s,ispay=%s,scorecheck=%s,pay_time=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[code,price,gw,nw,tare,total,status,price_time,ispay,scorecheck,pay_time,gmt_modified,id])
        else:
            sql='insert into storage(selfid,group_id,company_id,code,products_selfid,suppliers_selfid,price,gw,nw,tare,total,status,price_users_selfid,price_time,ispay,scorecheck,pay_time,pay_users_selfid,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[selfid,group_id,company_id,code,products_selfid,suppliers_selfid,price,gw,nw,tare,total,status,price_users_selfid,price_time,ispay,scorecheck,pay_time,pay_users_selfid,gmt_created])
    
    def group_list(self,frompageCount,limitNum,name=''):
        sqls=''
        argument=[]
        if name:
            sqls+='and name=%s'
            argument.append(name)
        sql='select id,name,address,ctype,gmt_created,gmt_modified from grouplist where id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from grouplist where id>0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            name=result['name']
            address=result['address']
            ctype=result['ctype']
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            list={'id':id,'name':name,'address':address,'ctype':ctype,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}

    def group_save(self,request):
        id=request.POST.get('id')
        name=request.POST.get('name')
        address=request.POST.get('address')
        ctype=request.POST.get('ctype')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update grouplist set name=%s,address=%s,ctype=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[name,address,ctype,gmt_modified,id])
        else:
            sql='insert into grouplist(name,address,ctype,gmt_created) values(%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[name,address,ctype,gmt_created])
            
            
    def supplier_list(self,frompageCount,limitNum,name=''):
        sqls=''
        argument=[]
        if name:
            sqls+='and name=%s'
            argument.append(name)
        sql='select id,selfid,ctype,group_id,company_id,name,htype,contact,mobile,address,bz,gmt_created,gmt_modified from suppliers where id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from suppliers where id>0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            selfid=result['selfid']
            ctype=result['ctype']
            if ctype==1:
                ctype='公司'
            elif ctype==2:
                ctype='个人'
            group_id=result['group_id']
            company_id=result['company_id']
            name=result['name']
            htype=result['htype']
            contact=result['contact']
            mobile=result['mobile']
            address=result['address']
            bz=result['bz']
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            list={'id':id,'selfid':selfid,'ctype':ctype,'group_id':group_id,'company_id':company_id,'name':name,'htype':htype,'contact':contact,'mobile':mobile,'address':address,'bz':bz,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}

    def supplier_save(self,request):
        id=request.POST.get('id')
        ctype=request.POST.get('ctype')
        group_id=request.POST.get('group_id')
        company_id=request.POST.get('company_id')
        list=['0','1','2','3','4','5','6','7','8','9']
        selfid=str(time.time())[:-3]+str(company_id)+random.choice(list)+random.choice(list)+random.choice(list)
        md5selfid = hashlib.md5(selfid)
        selfid = md5selfid.hexdigest()[8:-8]
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        md5pwd = hashlib.md5(pwd)
        pwd = md5pwd.hexdigest()[8:-8]
        htype=request.POST.get('htype')
        contact=request.POST.get('contact')
        mobile=request.POST.get('mobile')
        address=request.POST.get('address')
        bz=request.POST.get('bz')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update suppliers set ctype=%s,name=%s,htype=%s,contact=%s,mobile=%s,pwd=%s,address=%s,bz=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[ctype,name,htype,contact,mobile,pwd,address,bz,gmt_modified,id])
        else:
            sql='insert into suppliers(selfid,ctype,group_id,company_id,name,htype,contact,mobile,pwd,address,bz,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[selfid,ctype,group_id,company_id,name,htype,contact,mobile,pwd,address,bz,gmt_created])
            
            
    def product_list(self,frompageCount,limitNum,name=''):
        sqls=''
        argument=[]
        if name:
            sqls+='and name=%s'
            argument.append(name)
        sql='select id,selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,stock,bz,gmt_created,gmt_modified from products where id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from products where id>0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            selfid=result['selfid']
            group_id=result['group_id']
            company_id=result['company_id']
            name=result['name']
            name_py=result['name_py']
            category_selfid=result['category_selfid']
            spec=result['spec']
            unit=result['unit']
            stock=result['stock']
            bz=result['bz']
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            list={'id':id,'selfid':selfid,'group_id':group_id,'company_id':company_id,'name':name,'name_py':name_py,'category_selfid':category_selfid,'spec':spec,'unit':unit,'stock':stock,'bz':bz,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}

    def product_save(self,request):
        id=request.POST.get('id')
        company_id=request.POST.get('company_id')
        sql='select group_id from company where id=%s'
        result=dbd.fetchonedb(sql,[company_id])
        group_id=result['group_id']
        list=['0','1','2','3','4','5','6','7','8','9']
        selfid=str(time.time())[:-3]+str(company_id)+random.choice(list)+random.choice(list)+random.choice(list)
        md5selfid = hashlib.md5(selfid)
        selfid = md5selfid.hexdigest()[8:-8]
        name=request.POST.get('name')
        name_py=request.POST.get('name_py')
        category_selfid=request.POST.get('category_selfid')
        spec=request.POST.get('spec')
        unit=request.POST.get('unit')
        stock=request.POST.get('stock')
        bz=request.POST.get('bz')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update products set name=%s,name_py=%s,spec=%s,unit=%s,stock=%s,bz=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[name,name_py,spec,unit,stock,bz,gmt_modified,id])
        else:
            sql='insert into products(selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,stock,bz,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,stock,bz,gmt_created])
            
            
    def category_list(self,frompageCount,limitNum,name=''):
        sqls=''
        argument=[]
        if name:
            sqls+='and name=%s'
            argument.append(name)
        sql='select id,sub_selfid,company_selfid,name,gmt_created,gmt_modified from category_products where id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from category_products where id>0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            sub_selfid=result['sub_selfid']
            company_selfid=result['company_selfid']
            name=result['name']
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            list={'id':id,'sub_selfid':sub_selfid,'company_selfid':company_selfid,'name':name,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}

    def category_save(self,request):
        id=request.POST.get('id')
        sub_selfid=request.POST.get('sub_selfid')
        company_selfid=request.POST.get('company_selfid')
        list=['0','1','2','3','4','5','6','7','8','9']
        selfid=str(time.time())[:-3]+str(company_selfid)+random.choice(list)+random.choice(list)+random.choice(list)
        md5selfid = hashlib.md5(selfid)
        selfid = md5selfid.hexdigest()[8:-8]
        name=request.POST.get('name')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update category_products set sub_selfid=%s,name=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[sub_selfid,name,gmt_modified,id])
        else:
            sql='insert into category_products(selfid,sub_selfid,company_selfid,name,gmt_created) values(%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[selfid,sub_selfid,company_selfid,name,gmt_created])