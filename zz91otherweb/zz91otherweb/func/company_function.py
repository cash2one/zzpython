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
                sqlg="select front_tel,tel from phone where company_id="+str(company_id)+" and expire_flag=0"
                phoneresult=self.dbc.fetchonedb(sqlg)
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
        
        list={'company_id':company_id,'name':compname,'business':business,'domain_zz91':domain_zz91,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'mobilelist':mobilelist,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype}
        return list
    #---获得来电宝电话
    def getldbphone(self,company_id):
        if company_id:
            sqlg="select front_tel,tel from phone where company_id=%s and expire_flag=0"
            phoneresult=self.dbc.fetchonedb(sqlg,[company_id])
            if phoneresult:
                tel=phoneresult[1]
                tel=tel.replace("-",",,,")
                return {'front_tel':phoneresult[0],'tel':tel}
            else:
                return None
        else:
            return None