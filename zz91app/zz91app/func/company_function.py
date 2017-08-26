#-*- coding:utf-8 -*-

class zzcompany:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #----公司信息列表 翻页
    def getcompanylist(self,kname,frompageCount,limitNum,ldb=''):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if ldb!='' and ldb:
            cl.SetFilter('apply_status',[1])
        cl.SetSortMode( SPH_SORT_EXTENDED,"mobile_order desc,gmt_start desc" )
        cl.SetLimits (frompageCount,limitNum,10000)
        if (kname):
            res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
        else:
            res = cl.Query ('','company')
        listcount_comp=0
        listall_comp=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    compname=attrs['compname']
                    viptype=str(attrs['membership_code'])
                    membership="普通会员"
                    if (viptype == '10051000'):
                        membership='普通会员'
                    if (viptype == '10051001'):
                        membership='再生通'
                    if (viptype == '1725773192'):
                        membership='银牌品牌通'
                    if (viptype == '1725773193'):
                        membership='金牌品牌通'
                    if (viptype == '1725773194'):
                        membership='钻石品牌通'
                    pbusiness=subString(filter_tags(attrs['pbusiness']),150)
                    parea_province=attrs['parea_province']
                    ldbphone=self.getldbphone(id)
                    list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'membership':membership,'viptype':viptype,'ldbphone':ldbphone}
                    listall_comp.append(list1)
                listcount_comp=res['total_found']
        return {'list':listall_comp,'count':listcount_comp}
    #----公司详情
    def getcompanydetail(self,company_id):
        companydetail=cache.get("app_acompanydetail"+str(company_id))
        if companydetail:
            return companydetail
        if company_id:
            list=[]
            sqlc="select a.name,a.business,a.regtime,a.address,a.introduction,a.membership_code,a.domain_zz91,b.label as industry ,c.label,d.label from company as a LEFT OUTER JOIN category as b on a.industry_code=b.code LEFT OUTER JOIN category as c on left(a.area_code,12)=c.code LEFT OUTER JOIN category as d on left(a.area_code,16)=d.code where a.id=%s and a.is_block=0"
            clist=self.dbc.fetchonedb(sqlc,[company_id])
            if clist:
                compname=clist[0]
                business=clist[1]
                regtime=str(clist[2])
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
                mobile1=""
                if (mobile):
                    mobile=mobile.strip()
                    mobile1=mobile[0:11]
                    if len(mobile)>21:
                        mobilelist=re.findall('[\d]+',mobile)
                if not mobile1:
                    mobile1=""
                if arrviptype['ldb']:
                    mobile1=arrviptype['ldb']['ldbphone']
                fax_country_code=alist[5]
                fax_area_code=alist[6]
                fax=alist[7]
                email=alist[8]
                sex=alist[9]
                position=alist[10]
                if str(sex)=="0":
                    if ("先生" not in contact) and ("女士" not in contact):
                        contact+="先生"
                else:
                    if ("先生" not in contact) and ("女士" not in contact):
                        contact+="女士"
                if (position==None):
                    position=""
                position=position.strip()
                qq=alist[11]
                if not qq:
                    qq=""
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
            
                list={'company_id':company_id,'industry':industry,'province':province,'city':city,'faceurl':faceurl,'name':compname,'business':business,'domain_zz91':domain_zz91,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'mobilelist':mobilelist,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype}
            cache.set("app_acompanydetail"+str(company_id),list,60*60)
            return list
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
    #---获得来电宝电话
    def getldbphone(self,company_id):
        ldbphone=cache.get("app_aldbphonep"+str(company_id))
        #ldbphone=None
        if ldbphone:
            return ldbphone
        if company_id:
            sqlg="select front_tel,tel from phone where company_id=%s and expire_flag=0 and exists(select company_id from crm_company_service where crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and company_id=phone.company_id)"
            phoneresult=self.dbc.fetchonedb(sqlg,[company_id])
            if phoneresult:
                tel=phoneresult[1]
                tel=tel.replace("-",",,,")
                ldbphone= {'front_tel':phoneresult[0],'tel':tel}
            else:
                ldbphone= None
        else:
            ldbphone= None
        
        cache.set("app_aldbphonep"+str(company_id),ldbphone,60*60*24)
        return ldbphone
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
            account=listc[1]
            if str(sex)=="0":
                if ("先生" not in contact) and ("女士" not in contact):
                    contact+="先生"
            else:
                if ("先生" not in contact) and ("女士" not in contact):
                    contact+="女士"
            return {'company_id':company_id,'contact':contact,'account':account}
    #---获得联系信息
    def get_contactinfo(self,company_id):
        sql="select contact,sex,tel_country_code,tel_area_code,tel,fax_country_code,fax_area_code,fax,mobile,email,back_email,qq,weixin,msn from company_account where company_id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            contact=result[0]
            sex=result[1]
            tel_country_code=result[2]
            tel_area_code=result[3]
            tel=result[4]
            fax_country_code=result[5]
            fax_area_code=result[6]
            fax=result[7]
            mobile=result[8]
            email=result[9]
            back_email=result[10]
            qq=result[11]
            weixin=result[12]
            msn=result[13]
            list={"contact":contact,"sex":sex,"tel_country_code":tel_country_code,"tel_area_code":tel_area_code,"tel":tel,"fax_country_code":fax_country_code,"fax_area_code":fax_area_code,"fax":fax,"mobile":mobile,"email":email,"back_email":back_email,"qq":qq,"weixin":weixin,"msn":msn}
            return list
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
    #---获得公司信息
    def get_companyinfo(self,company_id):
        sql="select name,service_code,industry_code,area_code,address,address_zip,introduction,business,website from company where id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            name=result[0]
            service_code=result[1]
            industry_code=result[2]
            area_code=result[3]
            address=result[4]
            address_zip=result[5]
            introduction=result[6]
            business=result[7]
            website=result[8]
            #获得园区集散地
            sql1="select name,shorter_name,industry_code,garden_type_code from category_garden where area_code=%s"
            res_garden=self.dbc.fetchonedb(sql1,[area_code])
            if res_garden:
                garden_name=res_garden[0]
                shorter_name=res_garden[1]
                #industry_code=res_garden[2]
                garden_type_code=res_garden[3]
                list={"name":name,"service_code":service_code,"industry_code":industry_code,"area_code":area_code,"address":address,"address_zip":address_zip,"introduction":introduction,"business":business,"garden_name":garden_name,"shorter_name":shorter_name,"industry_code":industry_code,"garden_type_code":garden_type_code,"website":website}
            else:
                list={"name":name,"service_code":service_code,"industry_code":industry_code,"area_code":area_code,"address":address,"address_zip":address_zip,"introduction":introduction,"business":business,"website":website}    
            return list
    #是否显示联系方式
    def show_contact(self,company_id='',forcompany_id=''):
        companyinfoall={'list':'','viewflag':0}
        if forcompany_id:
            list=self.getcompanydetail(forcompany_id)
            #被查看者是高会直接显示联系方式
            iszstflag=zzt.getiszstcompany(forcompany_id)
            if iszstflag:
                companyinfoall['list']=list
                companyinfoall['viewflag']=1
            #----判断是否为来电宝用户
            viptype=zzq.getviptype(forcompany_id)
            #来电宝客户联系方式公开
            if viptype=='10051003':
                if list['viptype']:
                    if list['viptype']['ldb']:
                        list['mobile1']=None
                        if list['viptype']['ldb']['ldbphone']:
                            list['mobile1']=list['viptype']['ldb']['ldbphone']
                
                list['mobilelist']=[]
                companyinfoall['list']=list
                companyinfoall['viewflag']=1
        
            #是否已经查看过联系方式公开
            isseecompany=zzq.getisseecompany(company_id,forcompany_id)
            if isseecompany:
                companyinfoall['list']=list
                companyinfoall['viewflag']=1
                
            return companyinfoall
        