#-*- coding:utf-8 -*-
class yang:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    
    def yangprolist(self,limit="",keywords="",adposition="",imgsize=""):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
        cl.SetFilterRange('havesample',1,100)
        cl.SetFilterRange('havepic',1,100)
        cl.SetFilter('sampleDel',[0])
        cl.SetFilter('is_del',[0])
        cl.SetFilter('is_pause',[0])
        cl.SetFilter('check_status',[1])
        
        cl.SetLimits (0,limit,limit)
        if keywords and keywords!="":
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags)  '+keywords,'offersearch_new,offersearch_new_vip')
        else:
            res = cl.Query ('','offersearch_new,offersearch_new_vip')
        listall=[]
        listcount=0
        if res:
            if res.has_key('matches'):
                keylist=res['matches']
                for match in keylist:
                    id=match['id']
                    if imgsize=="" or imgsize==None:
                        imgsize="150x170"
                    pdt_images=self.getproductimg(id,imgsize)
                    attrs=match['attrs']
                    company_id=attrs['company_id']
                    self.saveshowppc(company_id,adposition)
                    title=subString(attrs['ptitle'],40)
                    take_price=attrs['take_price']
                    yurl="http://pyapp.zz91.com/app/ppchit.html?company_id="+str(company_id)+"&rd="+getjiami("http://yang.zz91.com/sale/"+str(id)+".htm")
                    list={'title':title,'take_price':'%.2f'%take_price,'id':id,'pdt_images':pdt_images,'yurl':yurl}
                    listall.append(list)
            listcount=len(listall)
        return {'listall':listall,'listcount':listcount}
    #---获取默认图片
    def getproductimg(self,id,size):
        #----
        sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc"
        productspic = self.dbc.fetchonedb(sql1,[id])
        if productspic:
            pdt_images=productspic[0]
        else:
            pdt_images=""
        if (pdt_images == '' or pdt_images == '0'):
            pdt_images='../cn/img/noimage.gif'
        else:
            pdt_images='http://img3.zz91.com/'+str(size)+'/'+pdt_images+''
        return pdt_images
    #----统计展示数
    def saveshowppc(self,company_id,adposition,adtype=''):
        gmt_created=datetime.datetime.now()
        phour=gmt_created.strftime("%-H")
        pdate=formattime(gmt_created,1)
        if adtype=="":
            adtype="1"
        showcount=1
        checkcount=0
        if adposition==None:
            adposition="sy"
        sql="select id from analysis_ppc_adlog where company_id=%s and  pdate=%s and phour=%s and adposition=%s"
        ppclog=self.dbc.fetchonedb(sql,[company_id,pdate,phour,adposition])
        if ppclog:
            id=ppclog[0]
            if adtype=="1":
                sqld="update analysis_ppc_adlog set showcount=showcount+1 where id=%s"
                self.dbc.updatetodb(sqld,[id])
            else:
                sqld="update analysis_ppc_adlog set checkcount=checkcount+1 where id=%s"
                self.dbc.updatetodb(sqld,[id])
        else:
            
            value=[company_id,showcount,checkcount,phour,pdate,gmt_created,adposition]
            sql="insert into analysis_ppc_adlog(company_id,showcount,checkcount,phour,pdate,gmt_created,adposition) values(%s,%s,%s,%s,%s,%s,%s)"
            self.dbc.updatetodb(sql,value)
            
            
            