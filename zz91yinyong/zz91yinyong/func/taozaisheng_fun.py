#-*- coding:utf-8 -*-
class funtaozaisheng:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbtao
    
    def taoprolist(self,limit="",keywords="",adposition="",imgsize=""):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
        cl.SetFilter('is_del',[0])
        cl.SetFilter('check_status',[1])
        cl.SetLimits (0,limit,limit)
        if keywords:
            res = cl.Query ('@(title,category_label1,category_label2,category_label3,category_label4,area1,area2,area3,area4,level,color,use_intro,process_intro,detail) '+keywords,'goods')
        else:
            res = cl.Query ('','goods')
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
                    title=subString(attrs['ptitle'],40)
                    if '供应' not in title:
                        title='供应'+title
                    take_price=attrs['price']
                    unit='元/'+attrs['unit']
                    take_price='%.2f'%take_price
                    
                    yurl="http://www.taozaisheng.com/goods"+str(id)+".htm"
                    #yurl="http://pyapp.zz91.com/app/ppchit.html?company_id="+str(company_id)+"&rd="+getjiami("http://yang.zz91.com/sale/"+str(id)+".htm")
                    list={'title':title,'take_price':take_price,'id':id,'pdt_images':pdt_images,'yurl':yurl,'unit':unit}
                    listall.append(list)
            listcount=len(listall)
            if listcount<4:
                listall=None
        return {'listall':listall,'listcount':listcount}
    def getunit(self,id):
        sql="select unit from yuanliao where id=%s"
        unitlist = dbtao.fetchonedb(sql,[id])
        if unitlist:
            return "元/"+unitlist[0]
    #---获取默认图片
    def getproductimg(self,id,size):
        #----
        sql1="select pic_address from picture where target_id=%s and target_type=1 and is_del=0 and status=1 order by id desc"
        productspic = dbtao.fetchonedb(sql1,[id])
        if productspic:
            pdt_images=productspic[0]
        else:
            pdt_images=""
        if (pdt_images == '' or pdt_images == '0'):
            pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
        else:
            pdt_images='http://img3.taozaisheng.com/'+str(size)+''+pdt_images+''
        return pdt_images
