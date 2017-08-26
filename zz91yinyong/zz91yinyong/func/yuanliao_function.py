#-*- coding:utf-8 -*-
class yuanliao:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    
    def yuanliaoprolist(self,limit="",keywords="",adposition="",imgsize=""):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"rrefresh_time desc" )
        cl.SetFilterRange('havepic',1,100)
        #cl.SetFilter('is_del',[0])
        #cl.SetFilter('is_pause',[0])
        cl.SetFilter('check_status',[1])
        
        cl.SetLimits (0,limit,limit)
        if keywords and keywords!="":
            res = cl.Query ('@(title,label1,label2,label3,name,trade_mark,process_level,useful_level,color,density,hardness,tensile,bending,location,trade_intro,description,province)  '+keywords,'yuanliao')
        else:
            res = cl.Query ('','yuanliao')
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
                    title=subString(attrs['ttitle'],40)
                    take_price=attrs['pprice']
                    unit=self.getunit(id)
                    if take_price==0:
                        take_price="0.00"
                        if attrs['min_price']:
                            take_price=str(attrs['min_price'])
                        if attrs['min_price'] and attrs['max_price']:
                            take_price+="-"+str(attrs['max_price'])
                    else:
                        take_price='%.2f'%take_price
                    
                    yurl="http://www.yousuyuan.com/detail/"+str(id)+".html"
                    #yurl="http://pyapp.zz91.com/app/ppchit.html?company_id="+str(company_id)+"&rd="+getjiami("http://yang.zz91.com/sale/"+str(id)+".htm")
                    list={'title':title,'take_price':take_price,'id':id,'pdt_images':pdt_images,'yurl':yurl,'unit':unit}
                    listall.append(list)
            listcount=len(listall)
            if listcount<4:
                listall=None
        return {'listall':listall,'listcount':listcount}
    def getunit(self,id):
        sql="select unit,price_unit from yuanliao where id=%s"
        unitlist = self.dbc.fetchonedb(sql,[id])
        if unitlist:
            return unitlist[1]+"/"+unitlist[0]
    #---获取默认图片
    def getproductimg(self,id,size):
        #----
        sql1="select pic_address from yuanliao_pic where yuanliao_id=%s and check_status=1 order by is_default desc,id desc"
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
    
            
            
            