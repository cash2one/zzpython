#-*- coding:utf-8 -*-

class zzldb:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    # 获得来电宝信息
    def getlaidianbao(self,frompageCount,limitNum):
        sqlt="select count(0) from crm_company_service where exists(select crm_service_code from crm_service_group where crm_service_code=crm_company_service.crm_service_code and code='ldb') and apply_status='1' and gmt_end>gmt_start"
        listcount=self.dbc.fetchnumberdb(sqlt)
        sql="select company_id from crm_company_service where exists(select crm_service_code from crm_service_group where crm_service_code=crm_company_service.crm_service_code and code='ldb') and apply_status='1' and gmt_end>gmt_start order by id desc limit %s,%s"
        resultlist = self.dbc.fetchalldb(sql,[frompageCount,limitNum])
        if resultlist:
            listall=[]
            for result in resultlist:
                company_id=result[0]
                companydetail=self.getcompanydetail(company_id)
                listall.append(companydetail)
            return {'list':listall,'count':listcount}
    #----公司详情
    def getcompanydetail(self,company_id):
        #获得缓存
        zz91app_getcompanydetail=cache.get("zz91app_getcompanydetail"+str(company_id))
        if zz91app_getcompanydetail:
            return zz91app_getcompanydetail
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
            sqll="select id from crm_company_service where company_id=%s and crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
            ldbresult=self.dbc.fetchonedb(sqll,[company_id])
            if ldbresult:
                sqlg="select front_tel,tel from phone where company_id=%s and expire_flag=0"
                phoneresult=self.dbc.fetchonedb(sqlg,[company_id])
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
        cache.set("zz91app_getcompanydetail"+str(company_id),list,60*10)
        return list