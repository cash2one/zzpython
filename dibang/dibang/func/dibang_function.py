#-*- coding:utf-8 -*-
import datetime,random,hashlib,md5
class zzdibang:
    def __init__(self):
        self.dbd=dbd
    
    def company_list(self,frompageCount,limitNum,name='',group_id="",company_id=""):
        sqls=''
        argument=[]
        if name:
            sqls+=' and a.name like %s'
            argument.append('%'+name+'%')
        if company_id:
            sqls+=' and a.id=%s'
            argument.append(company_id)
        if group_id:
            sqls+=' and a.group_id=%s'
            argument.append(group_id)
        sql='select a.id,a.group_id,a.name,a.ctype,a.gmt_created,a.gmt_modified,a.address,b.name as groupname from company as a left join grouplist as b on a.group_id=b.id where a.id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from company as a where a.isdel=0 '+sqls+''
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
            groupname=result['groupname']
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
            list={'id':id,'group_id':group_id,'groupname':groupname,'name':name,'ctype':ctype,'gmt_created':gmt_created,'gmt_modified':gmt_modified,'address':result['address']}
            listall.append(list)
        return {'list':listall,'count':count}
    def company_save(self,request):
        id=request.POST.get('id')
        name=request.POST.get('name')
        ctype=request.POST.get('ctype')
        address=request.POST.get('address')
        group_id=request.POST.get('group_id',default=None)
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update company set name=%s,ctype=%s,address=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[name,ctype,address,gmt_modified,id])
        else:
            sql='insert into company(group_id,name,ctype,address,gmt_created) values(%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[group_id,name,ctype,address,gmt_created])
            
    def user_list(self,frompageCount,limitNum,contact='',company_id='',group_id='',utype=''):
        sqls=''
        argument=[]
        if contact:
            sqls+=' and contact=%s'
            argument.append(contact)
        if company_id:
            sqls+=' and company_id=%s'
            argument.append(company_id)
        if group_id:
            sqls+=' and group_id=%s'
            argument.append(group_id)
        if utype:
            if str(utype)!="1":
                sqls+=" and utype!='1'"
        sql='select id,group_id,company_id,clientid,utype,username,contact,sex,mobile,bz,gmt_created,gmt_modified from users where isdel=0 '+sqls+' order by id desc limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from users where isdel=0 '+sqls+''
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
            groupname=self.getgroupname(group_id)
            companyname=self.getcompanyname(company_id)
            if utype=='1':
                utype='集团管理员'
            elif utype=='2':
                utype='校验人员'
            elif utype=='3':
                utype='财务人员'
            elif utype=='4':
                utype='分站管理员'
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
            list={'id':id,'group_id':group_id,'groupname':groupname,'company_id':company_id,'companyname':companyname,'clientid':clientid,'utype':utype,'username':username,'contact':contact,'sex':sex,'mobile':mobile,'bz':bz,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}
    
    def user_save(self,request):
        id=request.POST.get('id')
        isapp=request.POST.get('isapp')
        group_id=request.POST.get('group_id')
        company_id=request.POST.get('company_id')
        ischange_pwd=request.POST.get('ischange_pwd')
        list=['0','1','2','3','4','5','6','7','8','9']
        clientid=str(time.time())[:-3]+str(company_id)+random.choice(list)+random.choice(list)+random.choice(list)
        md5clientid = hashlib.md5(clientid)
        clientid = md5clientid.hexdigest()[8:-8]
        utype=request.POST.get('utype')
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        if pwd:
            md5pwd = hashlib.md5(pwd)
            pwd = md5pwd.hexdigest()[8:-8]
        contact=request.POST.get('contact')
        sex=request.POST.get('sex')
        mobile=request.POST.get('mobile')
        bz=request.POST.get('bz')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if isapp and id:
            sql='update users set contact=%s,sex=%s,mobile=%s where id=%s'
            result=self.dbd.updatetodb(sql,[contact,sex,mobile,id])
        if id and ischange_pwd and not isapp:
            sql='update users set utype=%s,username=%s,pwd=%s,contact=%s,sex=%s,mobile=%s,bz=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[utype,username,pwd,contact,sex,mobile,bz,gmt_modified,id])
        elif id and not ischange_pwd and not isapp:
            sql='update users set utype=%s,username=%s,contact=%s,sex=%s,mobile=%s,bz=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[utype,username,contact,sex,mobile,bz,gmt_modified,id])
        elif id and ischange_pwd and not isapp:
            sql='update users set utype=%s,username=%s,pwd=%s,contact=%s,sex=%s,mobile=%s,bz=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[utype,username,pwd,contact,sex,mobile,bz,gmt_modified,id])
        elif not id:
            sql='insert into users(group_id,company_id,clientid,utype,username,pwd,contact,sex,mobile,bz,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[group_id,company_id,clientid,utype,username,pwd,contact,sex,mobile,bz,gmt_created])
            
    def storage_list(self,frompageCount,limitNum,searchlist='',company_id='',group_id=''):
        sqls=''
        argument=[]
        time_today=datetime.datetime.now()
        pricing=searchlist.get('pricing')
        iccode=searchlist.get('iccode')
        pricing_today=searchlist.get('pricing_today')
        supplier=searchlist.get('supplier')
        gw=searchlist.get('gw')
        gmt_created=searchlist.get('gmt_created')
        price=searchlist.get('price')
        products_selfid=searchlist.get('products_selfid')
        suppliers_selfid=searchlist.get('suppliers_selfid')
        time_min=searchlist.get('time_min')
        time_max=searchlist.get('time_max')
        proname=searchlist.get('proname')
        ispay=searchlist.get('ispay')
        contact=searchlist.get("contact")
        nw=searchlist.get("nw")
        jiesuan=searchlist.get("jiesuan")
        
        sqls+=" and a.company_id=%s "
        argument.append(company_id)
        if pricing:
            sqls+=' and a.status!=2 and a.status!=4'
        elif pricing_today:
            sqls+=' and a.price_time<%s and a.status = 2'
            argument.append(time_today)
        elif jiesuan:
            sqls+=' and a.price_time<%s and a.status = 4'
            argument.append(time_today)
        elif iccode:
            sqls+=' and b.iccode=%s'
            argument.append(iccode)
        elif contact:
            sqls+=' and b.contact like %s'
            argument.append("%"+contact+"%")
        elif gw:
            sqls+=' and a.gw>%s'
            argument.append(gw)
        elif nw:
            sqls+=' and (a.gw-a.tare)>%s'
            argument.append(nw)
        elif gmt_created:
            sqls+=' and a.gmt_created > %s'
            argument.append(gmt_created)
        elif price:
            sqls+=' and a.price > %s'
            argument.append(price)
        elif suppliers_selfid:
            sqls+=' and a.suppliers_selfid=%s'
            argument.append(suppliers_selfid)
        elif time_min:
            sqls+=' and a.price_time > %s'
            argument.append(time_min)
        elif time_max:
            sqls+=' and a.price_time < %s'
            argument.append(time_max)
        elif products_selfid:
            sqls+=' and a.products_selfid=%s'
            argument.append(products_selfid)
        elif proname:
            sqls+=' and c.name like %s'
            argument.append('%'+proname+'%')
        elif group_id:
            sqls+=' and a.group_id=%s'
            argument.append(group_id)
        elif ispay:
            sqls+=' and a.ispay>=%s'
            argument.append(ispay)
        sql='select a.id,a.selfid,a.group_id,a.company_id,a.code,a.products_selfid,a.suppliers_selfid,a.price,a.gw,a.nw,a.tare,a.total,a.status,a.price_users_selfid,a.price_time,a.ispay,a.scorecheck,a.pay_time,a.pay_users_selfid,a.gmt_created,a.gmt_modified,a.out_time,b.iccode,b.name as supplier_name,b.contact,c.name as product_name,c.unit from storage as a left join suppliers as b on a.suppliers_selfid=b.selfid left join products as c on a.products_selfid=c.selfid where a.status<99 '+sqls+' order by id desc limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from storage as a left join suppliers as b on a.suppliers_selfid=b.selfid left join products as c on a.products_selfid=c.selfid where a.status<99 '+sqls+''
        sqlp='select sum(total) as total_price from storage as a left join suppliers as b on a.products_selfid=b.selfid left join products as c on a.products_selfid=c.selfid where a.status<99 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        total_price=self.dbd.fetchonedb(sqlp,argument)['total_price']
        if count is None:
            count=0
        else:
            count=count['count']
        if total_price is None:
            total_price=0
        listall=[]
        for result in resultlist:
            id=result['id']
            selfid=result['selfid']
            group_id=result['group_id']
            company_id=result['company_id']
            code=result['code']
            contact=result['contact']
            if contact is None:
                contact=''
            out_time=result['out_time']
            if out_time is None:
                out_time=''
            else:
                out_time=formattime(out_time,flag=2)
            
            products_selfid=result['products_selfid']
            category_name=''
            if products_selfid:
                category_name=self.getcategoryproname(products_selfid)
            suppliers_selfid=result['suppliers_selfid']
            price=result['price']
            gw=result['gw']
            nw=result['nw']
            tare=result['tare']
            total=result['total']
            if gw and tare:
                nw=float(gw)-float(tare)
                if price:
                    total='%.2f'%(float(price)*nw)
            
            
            
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
            pricename=self.getusersname(price_users_selfid)
            price_time=result['price_time']
            ispay=result['ispay']
            if ispay==0:
                ispay='<font color=red>未支付</font>'
            elif ispay==1:
                ispay='已支付'
            scorecheck=result['scorecheck']
            if scorecheck==0:
                scorecheck='未提现'
            elif scorecheck==1:
                scorecheck='已提现'
            pay_time=result['pay_time']
            pay_users_selfid=result['pay_users_selfid']
            payname=self.getusersname(pay_users_selfid)
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
            orderdate=formattime(result['gmt_created'],flag=1)
            if group_id is None:
                group_id=''
            iccode=result['iccode']
            if not iccode:
                iccode=''
            supplier_name=result['supplier_name']
            if not supplier_name:
                supplier_name=''
            product_name=result['product_name']
            if not product_name:
                product_name=''
            unit=result['unit']
            if not unit:
                unit=''
            list={'id':id,'selfid':selfid,'group_id':group_id,'company_id':company_id,'code':code,'products_selfid':products_selfid,'proname':proname,'suppliers_selfid':suppliers_selfid,'price':price,'gw':gw,'nw':nw,'tare':tare,'total':total,'status':status,'price_users_selfid':price_users_selfid,'pricename':pricename,'payname':payname,'price_time':price_time,'ispay':ispay,'scorecheck':scorecheck,'pay_time':pay_time,'pay_users_selfid':pay_users_selfid,'gmt_created':gmt_created,'gmt_modified':gmt_modified,'iccode':iccode,'supplier_name':supplier_name,'category_name':category_name,'product_name':product_name,'unit':unit,'contact':contact,'out_time':out_time,'orderdate':orderdate}
            listall.append(list)
        return {'list':listall,'count':count,'total_price':total_price}
    
    def storage_save(self,request):
        id=request.POST.get('id')
        pricing_now=request.POST.get('pricing_now')
        group_id=request.POST.get('group_id',default=None)
        company_id=request.POST.get('company_id')
        if not pricing_now:
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
            sqls+=' and name=%s'
            argument.append(name)
        sql='select id,name,address,ctype,gmt_created,gmt_modified from grouplist where isdel=0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from grouplist where isdel=0 '+sqls+''
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
            
            
    def supplier_list(self,frompageCount,limitNum,searchlist='',company_id='',group_id=''):
        sqls=''
        argument=[]
        name=searchlist.get("name")
        iccode=searchlist.get("iccode")
        if name:
            sqls+=' and name=%s'
            argument.append(name)
        if iccode:
            sqls+=' and iccode=%s'
            argument.append(iccode)
        if group_id:
            sqls+=' and group_id=%s'
            argument.append(group_id)
        if company_id:
            sqls+=' and company_id=%s'
            argument.append(company_id)
        sql='select id,selfid,iccode,ctype,group_id,company_id,name,htype,contact,mobile,pwd,address,bz,gmt_created,gmt_modified from suppliers where isdel=0 '+sqls+' order by id desc limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from suppliers where isdel=0 '+sqls+''
        resultlist=self.dbd.fetchalldb(sql,argument)
        count=self.dbd.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count['count']
        listall=[]
        for result in resultlist:
            id=result['id']
            sql='select sum(tare) as total_supply from storage where suppliers_selfid=%s'
            total_supply=self.dbd.fetchonedb(sql,[id])['total_supply']
            if not total_supply:
                total_supply=''
            selfid=result['selfid']
            iccode=result['iccode']
            ctype=result['ctype']
            if ctype==1:
                ctype='公司'
            elif ctype==2:
                ctype='个人'
            group_id=result['group_id']
            company_id=result['company_id']
            name=result['name']
            htype=result['htype']
            if htype=='0':
                htype='长期'
            elif htype=='1':
                htype='短期'
            contact=result['contact']
            mobile=result['mobile']
            pwd=result['pwd']
            address=result['address']
            bz=result['bz']
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            list={'id':id,'selfid':selfid,'iccode':iccode,'ctype':ctype,'group_id':group_id,'company_id':company_id,'name':name,'htype':htype,'contact':contact,'mobile':mobile,'pwd':pwd,'address':address,'bz':bz,'total_supply':total_supply,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}

    def supplier_save(self,request):
        id=request.POST.get('id')
        ischange_pwd=request.POST.get('ischange_pwd')
        isapp=request.POST.get('isapp')
        iccode=request.POST.get('iccode')
        ctype=request.POST.get('ctype')
        group_id=request.POST.get('group_id')
        company_id=request.POST.get('company_id')
        
        list=['0','1','2','3','4','5','6','7','8','9']
        selfid=str(time.time())[:-3]+str(company_id)+random.choice(list)+random.choice(list)+random.choice(list)
        md5selfid = hashlib.md5(selfid)
        selfid = md5selfid.hexdigest()[8:-8]
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        if pwd:
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
            sql="select id from suppliers where iccode=%s and id!=%s"
            result=self.dbd.fetchonedb(sql,[iccode,id])
        else:
            sql="select id from suppliers where iccode=%s"
            result=self.dbd.fetchonedb(sql,[iccode])
        if result:
            return {'err':'true','errtext':sql}
        argument=[]
        if id:
            sql="update suppliers set iccode=%s"
            argument.append(iccode)
            if not ctype:
                ctype=''
            sql+=",ctype=%s"
            argument.append(ctype)
            if not htype:
                htype=''
            sql+=",htype=%s"
            argument.append(htype)
            if not contact:
                contact=''
            sql+=",contact=%s"
            argument.append(contact)
            if not mobile:
                mobile=''
            sql+=",mobile=%s"
            argument.append(mobile)
            #修改密码
            if ischange_pwd:
                if pwd:
                    sql+=",pwd=%s"
                    argument.append(pwd)
            if not address:
                address=''
            sql+=",address=%s"
            argument.append(address)
            if not bz:
                bz=''
            sql+=",bz=%s"
            argument.append(bz)
            sql+=",gmt_modified=%s"
            argument.append(gmt_modified)
            sql+=" where id=%s"
            argument.append(id)
            result=self.dbd.updatetodb(sql,argument)
        else:
            sql='insert into suppliers(selfid,iccode,ctype,group_id,company_id,name,htype,contact,mobile,pwd,address,bz,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[selfid,iccode,ctype,group_id,company_id,name,htype,contact,mobile,pwd,address,bz,gmt_created,gmt_modified])
        return {'err':'false','errtext':''}
    def product_list(self,frompageCount,limitNum,name='',category_selfid='',company_id='',group_id=''):
        sqls=''
        argument=[]
        if name:
            sqls+=' and name=%s'
            argument.append(name)
        if category_selfid:
            sqls+=' and category_selfid=%s'
            argument.append(category_selfid)
        if company_id:
            sqls+=' and company_id=%s'
            argument.append(company_id)
        if group_id:
            sqls+=' and group_id=%s'
            argument.append(group_id)
        sql='select id,selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,stock,bz,gmt_created,gmt_modified from products where isdel=0 '+sqls+' order by id desc limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from products where isdel=0 '+sqls+''
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
            categoryname=self.getcategoryname(category_selfid)
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
            list={'id':id,'selfid':selfid,'group_id':group_id,'company_id':company_id,'name':name,'name_py':name_py,'category_selfid':category_selfid,'categoryname':categoryname,'spec':spec,'unit':unit,'stock':stock,'bz':bz,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}

    def product_save(self,request):
        id=request.POST.get('id')
        company_id=request.POST.get('company_id')
        isapp=request.POST.get('isapp')
        group_id=request.POST.get('group_id')
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
        
        argument=[]
        if id:
            sql="update products set name=%s"
            argument.append(name)
            if not name_py:
                name_py=''
            sql+=",name_py=%s"
            argument.append(name_py)
            if not spec:
                spec=''
            sql+=",spec=%s"
            argument.append(spec)
            if not unit:
                unit=''
            sql+=",unit=%s"
            argument.append(unit)
            if not stock:
                stock=''
            sql+=",stock=%s"
            argument.append(stock)
            if not bz:
                bz=''
            sql+=",bz=%s"
            argument.append(bz)
            sql+=",gmt_modified=%s"
            argument.append(gmt_modified)
            if not category_selfid:
                category_selfid=''
            sql+=",category_selfid=%s"
            argument.append(category_selfid)
            sql+=" where id=%s"
            argument.append(id)
            result=self.dbd.updatetodb(sql,argument)
        else:
            sql='insert into products(selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,stock,bz,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,stock,bz,gmt_created])
            
    def category_list(self,frompageCount,limitNum,name='',company_id='',group_id=''):
        sqls=''
        argument=[]
        if name:
            sqls+=' and name=%s'
            argument.append(name)
        if company_id:
            sqls+=' and company_id=%s'
            argument.append(company_id)
        if group_id:
            sqls+=' and group_id=%s'
            argument.append(group_id)
        sqls+=" and sub_selfid='0'"
        sql='select id,selfid,sub_selfid,company_id,name,gmt_created,gmt_modified from category_products where isdel=0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        sqlc='select count(0) as count from category_products where isdel=0 '+sqls+''
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
            sub_selfid=result['sub_selfid']
            company_id=result['company_id']
            name=result['name']
            gmt_created=result['gmt_created']
            gmt_created=formattime(gmt_created,flag=2)
            gmt_modified=result['gmt_modified']
            if gmt_modified is None:
                gmt_modified=''
            else:
                gmt_modified=formattime(gmt_modified,flag=2)
            list={'id':id,'selfid':selfid,'sub_selfid':sub_selfid,'company_id':company_id,'name':name,'gmt_created':gmt_created,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}

    def category_save(self,request):
        id=request.POST.get('id')
        sub_selfid=request.POST.get('sub_selfid')
        if sub_selfid=='None':
            sub_selfid=0
        company_id=request.POST.get('company_id')
        list=['0','1','2','3','4','5','6','7','8','9']
        selfid=str(time.time())[:-3]+str(company_id)+random.choice(list)+random.choice(list)+random.choice(list)
        md5selfid = hashlib.md5(selfid)
        selfid = md5selfid.hexdigest()[8:-8]
        name=request.POST.get('name')
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        if id:
            sql='update category_products set name=%s,gmt_modified=%s where id=%s'
            result=self.dbd.updatetodb(sql,[name,gmt_modified,id])
        else:
            sql='insert into category_products(selfid,sub_selfid,company_id,name,gmt_created) values(%s,%s,%s,%s,%s)'
            result=self.dbd.updatetodb(sql,[selfid,sub_selfid,company_id,name,gmt_created])
            

    def getsupplierlist(self,company_id='',group_id=''):
        argument=[]
        sql='select selfid,name from suppliers where isdel=0'
        if group_id:
            sql+=' and group_id=%s'
            argument.append(group_id)
        if company_id:
            sql+=' and company_id=%s'
            argument.append(company_id)
        result=self.dbd.fetchalldb(sql,argument)
        return result
    #----获取供应商名称
    def getsuppliername(self,supplier_selfid):
        sql="select name from suppliers where selfid=%s"
        result=dbd.fetchonedb(sql,[supplier_selfid])
        if result:
            return result['name']
        else:
            return ''
    
    def getcompanylist(self,group_id='',company_id=''):
        argument=[]
        sql='select id,name from company where isdel=0'
        if group_id:
            sql+=' and group_id=%s'
            argument.append(group_id)
        if company_id:
            sql+=' and id=%s'
            argument.append(company_id)
        result=self.dbd.fetchalldb(sql,argument)
        return result
    def getcategorylist(self,company_id=''):
        sqls=''
        argument=[]
        if company_id:
            sqls+='and company_id=%s'
            argument.append(company_id)
        sql='select id,selfid,name from category_products where isdel=0 '+sqls+' '
        result=self.dbd.fetchalldb(sql,argument)
        return result
    
    def getproductlist(self,company_id=''):
        sqls=''
        argument=[]
        if company_id:
            sqls+='and company_id=%s'
            argument.append(company_id)
        sql='select selfid,name from products where isdel=0 '+sqls
        result=self.dbd.fetchalldb(sql,argument)
        return result
    
    def getuserlist(self):
        sql='select id,selfid,contact from users where isdel=0'
        result=self.dbd.fetchalldb(sql)
        return result
    #获取集团名称
    def getgroupname(self,group_id):
        sql="select name from grouplist where id=%s"
        result=self.dbd.fetchonedb(sql,[group_id])
        if result:
            return result['name']
        else:
            return ''
    #获取用户名称
    def getusersname(self,users_selfid):
        sql="select contact from users where selfid=%s"
        result=self.dbd.fetchonedb(sql,[users_selfid])
        if result:
            return result['contact']
        else:
            return ''
    #获取用户名称
    def getproductsname(self,products_selfid):
        sql="select name from products where selfid=%s"
        result=self.dbd.fetchonedb(sql,[products_selfid])
        if result:
            return result['name']
        else:
            return ''
    #获取分站名称
    def getcompanyname(self,company_id):
        sql="select name from company where id=%s"
        result=self.dbd.fetchonedb(sql,[company_id])
        if result:
            return result['name']
        else:
            return ''
    def getcategoryproname(self,id):
        sql="select b.name from products as a left join category_products as b on a.category_selfid=b.selfid where a.selfid=%s"
        result=self.dbd.fetchonedb(sql,[id])
        if result:
            return result['name']
        else:
            return ''
    #获取类别名称
    def getcategoryname(self,category_selfid):
        sql="select name from category_products where selfid=%s"
        result=self.dbd.fetchonedb(sql,[category_selfid])
        if result:
            return result['name']
        else:
            return ''
    #----对于产品的入库量
    def getproducts_storage(self,products_selfid,ndate=""):
        sql="select sum(total) as total,sum(nw) as nw from storage where products_selfid=%s and status=4 and status<99"
        if ndate:
            sql+=" and date_format(gmt_created,'%%Y-%%m-%%d')='"+str(ndate)+"'"
        result=self.dbd.fetchonedb(sql,[products_selfid])
        if result:
            return {'total':result['total'],'nw':result["nw"]}
    #----对于日期入口
    
    
    def alldata(self,request,time_min='',time_max='',company_id=''):
        sqls=''
        argument=[]
        if time_min and time_max:
            sqls+='and a.price_time between %s and %s'
            argument.append(time_min)
            argument.append(time_max)
        if time_min and not time_max:
            sqls+=' and a.price_time>%s'
            argument.append(time_min)
        if time_max and not time_min:
            sqls+=' and a.price_time<%s'
            argument.append(time_max)
        if company_id:
            sqls+='and a.company_id=%s'
            argument.append(company_id)
        sql='select round(sum(gw-tare),2) as total_weight from storage as a where a.status<99 '+sqls+''
        total_weight=self.dbd.fetchonedb(sql,argument)['total_weight']
        sql='select round(sum((gw-tare)*price),2) as total_price from storage as a where a.status<99 '+sqls+''
        total_price=self.dbd.fetchonedb(sql,argument)['total_price']
        if total_price is None:
            total_price=''
        sql='select round(sum(a.gw-a.tare),2) as total_gw,round(sum((gw-tare)*price),2) as total_price,b.name,round(sum(a.gw-a.tare)/sum((gw-tare)*price),2) as average from storage as a left join products as b on a.products_selfid=b.selfid where a.status<99 '+sqls+' group by products_selfid'
        listall=self.dbd.fetchalldb(sql,argument)
        return {'total_weight':total_weight,'total_price':total_price,'listall':listall}
    
    #----是否管理员
    def isadmin(self,utype):
        if str(utype)=="1" or str(utype)=="4":
            return 1