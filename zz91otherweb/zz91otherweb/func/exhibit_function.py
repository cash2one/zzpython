#-*- coding:utf-8 -*-
class zzexhibit:
    def __init__(self):
        self.dbc=dbc
    def zhlist(self,frompageCount,limitNum,searchlist=""):
        sqlarg=' from exhibit as a left outer join category as b on a.plate_category_code=b.code left outer join category as c on c.code=a.exhibit_category_code left outer join category as d on a.area_code=d.code where a.id>0'
        argument=[]
        if searchlist.has_key("area_code"):
            area_code=searchlist['area_code']
            sqlarg+=' and a.area_code=%s'
            argument.append(area_code)
        if searchlist.has_key("name"):
            name=searchlist['name']
            sqlarg+=' and a.name like %s'
            argument.append('%'+name+'%')
        if searchlist.has_key("area"):
            area=searchlist['area']
            sqlarg+=' and a.area like %s'
            argument.append('%'+area+'%')
        if searchlist.has_key("plate_category_code"):
            plate_category_code=searchlist['plate_category_code']
            sqlarg+=' and a.plate_category_code=%s'
            argument.append(plate_category_code)
        if searchlist.has_key("exhibit_category_code"):
            exhibit_category_code=searchlist['exhibit_category_code']
            sqlarg+=' and a.exhibit_category_code=%s'
            argument.append(exhibit_category_code)
        sql1='select count(0)'+sqlarg
        sql='select a.id,a.name,a.area_code,a.area,a.start_time,a.end_time,a.plate_category_code,a.exhibit_category_code,a.gmt_created,a.checked,a.tags,b.label as bktypename,c.label as hytypename,d.label as area_name,a.tags,a.photo_cover,a.content '+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=self.dbc.fetchnumberdb(sql1,argument)
            resultlist=self.dbc.fetchalldb(sql,argument)
        else:
            count=self.dbc.fetchnumberdb(sql1)
            resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            name=result[1]
            area_code=result[2]
            area=result[3]
            start_time=formattime(result[4])
            end_time=formattime(result[5])
            plate_category_code=result[6]
            exhibit_category_code=result[7]
            gmt_created=formattime(result[8])
            checked=result[9]
            bktypename=result[11]
            hytypename=result[12]
            area_name=result[13]
            tags=result[14]
            photo_cover=result[15]
            imgurl=''
            if not photo_cover:
                imgurl=self.get_img_url(result[16])
            photo_cover=''
            if imgurl:
                photo_cover=imgurl[0]
            if not photo_cover:
                photo_cover='http://img0.zz91.com/front/images/global/noimage.gif'
            if area:
                area_name=area
            if checked==1:
                checkvalue='已审'
            else:
                checkvalue='<font color=red>未审</font>'
            list={'id':id,'name':name,'area_code':area_code,'area_name':area_name,'tags':tags,'area':area,'start_time':start_time,'end_time':end_time,'bktypename':bktypename,'hytypename':hytypename,'gmt_created':gmt_created,'checkvalue':checkvalue,'photo_cover':photo_cover}
            listall.append(list)
        return {'list':listall,'count':count}
    def getcategorylist(self,code):
        sql="select code,label from category where parent_code=%s"
        resultlist=self.dbc.fetchalldb(sql,[code])
        listall=[]
        if resultlist:
            for result in resultlist:
                code=result[0]
                label=result[1] 
                list={'code':code,'label':label}
                listall.append(list)
        return listall
    #获取内容图片
    def get_img_url(self,html):#获得图片url
        #html=html.lower()
        if html:
            html=html.replace("data-original=","src=").replace("IMG",'img').replace("SRC",'src').replace("data-src","src")
            re_py3=r'<img.*?src="(.*?)".*?>'
            urls_pat3=re.compile(re_py3)
            img_url3=re.findall(urls_pat3,html)
            if img_url3:
                return img_url3
            re_py3=r"<img.*?src='(.*?)'.*?>"
            urls_pat3=re.compile(re_py3)
            img_url3=re.findall(urls_pat3,html)
            if img_url3:
                return img_url3
            re_py3=r'<img.*?src=(.*?) .*?>'
            urls_pat3=re.compile(re_py3)
            img_url3=re.findall(urls_pat3,html)
            if img_url3:
                return img_url3