#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91tools import *
import MySQLdb,os,StringIO,qrcode,re,time,datetime,random,chardet,requests
import Image,ImageDraw,ImageFont,ImageFilter
from datetime import timedelta,date
from django.utils.http import urlquote
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/conn.py")
execfile(nowpath+"/func/function.py")
conn=database()
cursor = conn.cursor()
#feiliao新增
from django.core.cache import cache
from zz91settings import SPHINXCONFIG
from settings import spconfig
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from sphinxapi import *
from zz91page import *
dbc=companydb()
dbn=newsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/feiliao123_function.py")
zzfei=zz91feiliao()

#---前台页面
def feiliao(request):
    websitelist=getwebsitelist(0,30,'','',1,'',1,1)
    if websitelist:
        recommendlist=websitelist['list']
    webtypelist=getindextypelist(1)
    return render_to_response('feiliao.html',locals())
#---更多
def listmore(request,typeid=''):
    typelist=getnexttype(typeid)
    typename=gettypename(typeid)
    return render_to_response('listmore.html',locals())

def verifycode(request):
    arg=request.GET.get('arg')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(arg)
    qr.make(fit=True)
    img = qr.make_image()
    mstream = StringIO.StringIO()
    img.save(mstream, "GIF")
    mstream.closed
    return HttpResponse(mstream.getvalue(),'image/gif')

#feiliao123改版
#--首页
def index(request):
    #网址导航栏目
    webtype=getnexttype(1)
    #废金属行情报价
    jinshu_area=zzfei.getprlist(0,6,15,'',[40,279,308,41,328,45,43,44,46,47,49,50],'','','1')['list']
    #废塑料行情报价
    suliao_guonei=zzfei.getpricedblist(0,9,20)['list']
    #综合废料行情报价
    zonghe_zongshu=zzfei.getprlist(0,6,8,'',[218,219])['list']
    #废料资讯
    columnid=zzfei.getcolumnid()
    hotnewslist=zzfei.getnewslistlatest(num=6,typeid=columnid)
    newsalllist=zzfei.getnewslist(allnum=1)
    #新公司--塑料
    company_suliao=zzfei.getcompanylist("塑料",0,7,7)
    #新公司--金属
    company_jinshu=zzfei.getcompanylist("金属",0,7,7)
    #新公司--综合
    company_zonghe=zzfei.getcompanylist("橡胶|废纸|电子电器|服务",0,7,7)
    return render_to_response('feiliao123/index.html',locals())
#--更多页
def feiliao123_more(request,typeid=''):
    typelist=getnexttype(typeid)
    typename=gettypename(typeid)
    return render_to_response('feiliao123/feiliao123_more.html',locals())
#--交易
def trade(request):
    #热门关键词
    #有图片的供求
    productlist=zzfei.getproductslist()
    
    #底部交易报价
    pricelist_suliao=zzfei.getpricelist_company(kname='废塑料',frompageCount=0,limitNum=7)
    listall_suliao=pricelist_suliao['list']
    pricelist_jinshu=zzfei.getpricelist_company(kname='废金属',frompageCount=0,limitNum=7)
    listall_jinshu=pricelist_jinshu['list']
    pricelist_feizhi=zzfei.getpricelist_company(kname='废纸',frompageCount=0,limitNum=7)
    listall_feizhi=pricelist_feizhi['list']
    pricelist_zonghe=zzfei.getpricelist_company(kname='综合',frompageCount=0,limitNum=7)
    listall_zonghe=pricelist_zonghe['list']
    return render_to_response('feiliao123/trade.html',locals())

#--资讯
def news(request):
    page=request.GET.get('page')
    kinds4=zzfei.getfuzhuindexlist()
    #id列表
    columnid=zzfei.getcolumnid()
    #获得最新
    #hotnewslist=zzfei.getnewslistlatest(num=3,typeid=columnid,has_txt=140)
    latesdnews=zzfei.getlatestnews()
    return render_to_response('feiliao123/news.html',locals())

#----图片上传
def otherimgupload(request):
    #source 
    source=request.GET.get("source")
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    #return HttpResponse(request.FILES)
    if request.FILES:
        file = request.FILES.getlist('file')
        if not file:
            return None
        listall=[]
        for f in file:
            
            # 获取文件名后缀
            filetype=f.name.split(".")[-1]
            #视频上传
            if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
                mediatype="video"
                tmp = random.randint(100, 999)
                newpath="/mnt/data/resources/other/"+timepath
                imgpath=newpath+str(nowtime)+str(tmp)+"."+filetype
                databasepath="other/"+timepath+str(nowtime)+str(tmp)+"."+filetype
                if not os.path.isdir(newpath):
                    os.makedirs(newpath)
        
                des_origin_f = open(imgpath,"w")
                for chunk in f.chunks():
                    des_origin_f.write(chunk)  
                des_origin_f.close()
                picurl="http://img1.zz91.com/other/"+timepath+str(nowtime)+str(tmp)+"."+filetype
            else:
                mediatype="pic"
                suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG','jpg','mp4']
                tempim = StringIO.StringIO()
                mstream = StringIO.StringIO(f.read())
                im = Image.open(mstream)
                
                
                rheight=800
                rwidth=800
                pwidth=im.size[0]
                pheight=im.size[1]
                rate = int(pwidth/pheight)
                if rate==0:
                    rate=1
                nwidth=800
                nheight=800
                if (pwidth>rwidth):
                    nwidth=rwidth
                    nheight=nwidth /rate
                else:
                    nwidth=pwidth
                    nheight=pheight
                if (pheight>rheight):
                    nheight=rheight
                    nwidth=rheight*rate
                else:
                    nwidth=pwidth
                    nheight=pheight
                kzname=im.format
                
                if kzname not in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]:
                    im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
                    #logo水印
                    
                    if nwidth/2>130:
                        wm = Image.open(nowpath+"/media/logo.png")
                        layer = Image.new('RGBA', im.size, (0,0,0,0))
                        layer.paste(wm, (im.size[0] - 120, im.size[1] - 50))
                        im = Image.composite(layer, im, layer)
                    #加字体水印
                    fontPath=nowpath+'/media/SIMHEI.TTF'
                    fontSize=18
                    font = ImageFont.truetype(fontPath,fontSize)
                    draw = ImageDraw.Draw(im)
                    if nwidth/2>130:
                        draw.text((nwidth/2-60,nheight/2-25),u'www.zz91.com',(0,0,0),font=font)
                        draw.text((nwidth/2-70,nheight/2),unicode('ZZ91再生网专用','utf-8'),(0,0,0),font=font) 
                    del draw
                
                tmp = random.randint(100, 999)
                newpath="/mnt/data/resources/other/"+timepath
                imgpath=newpath+str(nowtime)+str(tmp)+"."+kzname
                databasepath="other/"+timepath+str(nowtime)+str(tmp)+"."+kzname
                if not os.path.isdir(newpath):
                    os.makedirs(newpath)
                im.save(imgpath,kzname,quality = 80)
                mstream.closed
                tempim.closed
                picurl="http://img3.zz91.com/300x15000/other/"+timepath+str(nowtime)+str(tmp)+"."+kzname
            picid=0
            if source=="products":
                sql="insert into products_pic(product_id,pic_address,gmt_created) values(0,%s,%s)"
                result=dbc.updatetodb(sql,[databasepath,gmt_created])
                if result:
                    picid=result[0]
            else:
                sql="insert into other_piclist(path,source,gmt_created) values(%s,%s,%s)"
                result=dbc.updatetodb(sql,[databasepath,source,gmt_created])
                if result:
                    picid=result[0]
            list={'path':picurl,'id':picid,'databasepath':databasepath,'mediatype':mediatype}
            listall.append(list)
        return listall
    return None