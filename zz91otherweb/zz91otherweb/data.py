#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import datetime,time,urllib,csv,os,xlrd,sys,requests,pymongo
from zz91page import *
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import getToday,getYesterday,date_to_str,formattime,getnub_tostr,getpastoneday,date_to_strall,filter_tags,str_to_date,getnextdate,gettimedifference
from settings import pyuploadpath,pyimgurl
from zz91db_ast import companydb
from zz91db_130 import otherdb
from zz91conn import database_mongodbconn
dbo=otherdb()
dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/data_function.py")
execfile(nowpath+"/func/other_function.py")
execfile(nowpath+"/func/huanbao_function.py")

zzlogin=zz91login()
zzhuanbao=zz91huanbao()
zzother=zz91other()
comdata=company()
skeyword=searchkeyword()
zzproduct=product()
datalogin=login()
zzfeifa=feifakeywords()
mongodb_sensitive=database_mongodbconn()
conn = pymongo.MongoClient("10.171.223.228",27017)

def delcompro(request):
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    del1=request.GET.get('del1')
    del2=request.GET.get('del2')
    if gmt_begin and gmt_end:
        if del1:
            sql='delete from data_product where gmt_date>=%s and gmt_date<%s'
            dbo.updatetodb(sql,[gmt_begin,gmt_end])
        if del2:
            sql2='delete from data_company where gmt_date>=%s and gmt_date<%s'
            dbo.updatetodb(sql2,[gmt_begin,gmt_end])
    return HttpResponseRedirect(request_url)
def delkwdsearch(request):
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if gmt_begin and gmt_end:
        sql='delete from data_ip_search where gmt_created>=%s and gmt_created<%s'
        dbo.updatetodb(sql,[gmt_begin,gmt_end])
    return HttpResponseRedirect(request_url)

def upcompro_check(request):
    is_ok=request.GET.get('is_ok')
    auto_id=request.GET.get('auto_id')
    if is_ok=='1':
        gmt_date=request.GET.get('gmt_date')
        sql='delete from data_product where gmt_date=%s'
        sql2='delete from data_company where gmt_date=%s'
        dbo.updatetodb(sql,[gmt_date])
        dbo.updatetodb(sql2,[gmt_date])
        is_ok='0'
    else:
        is_ok='1'
    sql='update compro_check set is_check=%s where id=%s'
    dbo.updatetodb(sql,[is_ok,auto_id])
    return HttpResponse('1')

def compro_check(request):
    '''
    datetoday=datetime.date.today()
    sql='select id from compro_check where gmt_date=%s'
    result=dbo.fetchonedb(sql,datetoday)
    if not result:
        type=1
        is_check=0
        sql2='insert into compro_check(is_check,gmt_date,type) values(%s,%s,%s)'
        dbo.updatetodb(sql2,[is_check,datetoday,type])
    '''
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    comprochecklist=comdata.getcomprochecklist(frompageCount,limitNum)
    listcount=0
    if (comprochecklist):
        listall=comprochecklist['list']
        listcount=comprochecklist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('company/compro_check.html',locals())

#----查询搜索词
def search_keywords(request):
    gmt_end2=''
    gmt_begin2=''
    typelist=zzother.gettypelist2([5,11])
    page=request.GET.get('page')
    gmt_end=request.GET.get('gmt_end')
    pagetype=request.GET.get('pagetype')
    gmt_begin=request.GET.get('gmt_begin')
    if gmt_begin and gmt_end:
        gmt_end2=gmt_end+' 00:00:00'
        gmt_begin2=gmt_begin+' 00:00:00'
    if pagetype:
        typename=zzother.gettypename(pagetype)
    searchlist={}
    if pagetype:
        searchlist['pagetype']=pagetype
    if gmt_begin and gmt_end:
        searchlist['gmt_begin']=gmt_begin
        searchlist['gmt_end']=gmt_end
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    search_keywords=zzother.getsearch_keywords(frompageCount,limitNum,pagetype,gmt_begin2,gmt_end2)
    listcount=0
    if (search_keywords):
        listall=search_keywords['list']
        listcount=search_keywords['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('company/search_keywords.html',locals())

#----登陆统计
def logindata(request):
    page=request.GET.get('page')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    logcount_begin=request.GET.get('logcount_begin')
    logcount_end=request.GET.get('logcount_end')
    area_code=request.GET.get('area_code')
    company_name=request.GET.get('company_name')
    company_id=request.GET.get('company_id')
    is_senior=request.GET.get('is_senior')
    industry_code=request.GET.get('industry_code')
    timetype=request.GET.get('timetype')
    order=request.GET.get('order')
    online=request.GET.get('online')
    company_idlist=[]
    addarg=''
    if timetype=='1':
        timename='登录时间'
        if gmt_begin or gmt_end:
            if gmt_begin:
                addarg+=' and last_logtime>="'+gmt_begin+'"'
            if gmt_end:
                addarg+=' and last_logtime<"'+gmt_end+'"'
        else:
            order='last_logtime desc'
    elif timetype=='2':
        timename='注册时间'
        if gmt_begin or gmt_end:
            if gmt_begin:
                addarg+=' and regtime>="'+gmt_begin+'"'
            if gmt_end:
                addarg+=' and regtime<"'+gmt_end+'"'
        else:
            order='regtime desc'
    searchlist={}
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if logcount_begin:
        searchlist['logcount_begin']=logcount_begin
    if logcount_end:
        searchlist['logcount_end']=logcount_end
    if company_name:
        searchlist['company_name']=company_name
    if is_senior:
        searchlist['is_senior']=is_senior
    if timetype:
        searchlist['timetype']=timetype
    if company_id:
        searchlist['company_id']=company_id
    if area_code:
        searchlist['area_code']=area_code
        area_name=skeyword.getclabel(area_code)
    if industry_code:
        searchlist['industry_code']=industry_code
        industry_name=skeyword.getclabel(industry_code)
    searchurl=urllib.urlencode(searchlist)
    allindustry=zzlogin.getallindustry()
    allarea=zzlogin.getallarea()
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if company_id:
        loginlist=datalogin.getlogindetails(frompageCount,limitNum,company_id,gmt_begin,gmt_end)
    else:
        loginlist=datalogin.getlogindatalist(frompageCount,limitNum,gmt_begin,gmt_end,logcount_begin,logcount_end,area_code,industry_code,company_name,is_senior,order,addarg)
    listcount=0
    listall=loginlist['list']
    listcount=loginlist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('company/logindata.html',locals())
def getpublishdata(request):
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    type=request.GET.get('type')
    if gmt_begin and gmt_end:
        gmt_datelist=gettimedifference(gmt_begin.encode('utf-8'),gmt_end.encode('utf-8'))
        for gmt_date in gmt_datelist:
            timetoday=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if gmt_date<timetoday:
                sql2='select id from compro_check where gmt_date=%s'
                result=dbo.fetchonedb(sql2,gmt_date)
                if not result:
                    sql='insert into compro_check(is_check,gmt_date,type) values(%s,%s,%s)'
                    dbo.updatetodb(sql,[0,gmt_date,type])
    return HttpResponse('ok')
#----发布统计
def publishdata(request):
    sql='select gmt_date from compro_check where is_check=0'
    result=dbo.fetchonedb(sql)
    if result:
        result=date_to_str(result[0])
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    type_code=request.GET.get('type_code')
    is_senior=request.GET.get('is_senior')
    type_name=''
    if type_code=='10331000':
        type_name='供应'
    elif type_code=='10331001':
        type_name='求购'
    elif type_code=='10331002':
        type_name='合作'
    elif type_code=='10331003':
        type_name='全部供求类型'
    if not type_code:
        type_code='10331003'
        type_name='全部供求类型'
    productlist=zzproduct.getproductlist(gmt_begin,gmt_end,type_code,is_senior)
    return render_to_response('company/publishdata.html',locals())
#----发布详情统计
def publishdetaildata(request):
    procategorylist=zzproduct.getprocategorylist()
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    company_name=request.GET.get('company_name')
    is_senior=request.GET.get('is_senior')
    pubtype=request.GET.get('pubtype')
    procode=request.GET.get('procode')
    if procode:
        prolabel=zzproduct.getcategory_name(procode)
    order=request.GET.get('order')
    company_id=request.GET.get('company_id')
    type=request.GET.get('type')
    nowdate=request.GET.get('nowdate')
    if pubtype=='1':
        pubname='供求发布'
        order='refresh_time desc'
    elif pubtype=='2':
        pubname='询盘发布'
        order='send_time desc'
    page=request.GET.get('page')
    searchlist={}
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if company_name:
        searchlist['company_name']=company_name
    if pubtype:
        searchlist['pubtype']=pubtype
    if is_senior:
        searchlist['is_senior']=is_senior
    if procode:
        searchlist['procode']=procode
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if company_id:
        companydatalist=comdata.getcompanyprodetail(company_id,type,procode,nowdate,gmt_begin,gmt_end)
    else:
        companydatalist=comdata.getcompany_data(frompageCount,limitNum,gmt_begin,gmt_end,company_name,is_senior,pubtype,procode,order)
    listall=companydatalist['list']
    listcount=companydatalist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('company/publishdetaildata.html',locals())

#----关键词搜索统计
def keywordssearchdata(request):
    industrylist=skeyword.getindustrylist()
    page=request.GET.get('page')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    account=request.GET.get('account')
    islog=request.GET.get('islog')
    if islog=='1':
        islog_name='已注册'
    elif islog=='0':
        islog_name='未注册'
    is_senior=request.GET.get('is_senior')
    ip=request.GET.get('ip')
    keyword=request.GET.get('keyword')
    company_id=request.GET.get('company_id')
#    compdetail=request.GET.get('compdetail')
    industry_code=request.GET.get('industry_code')
    if industry_code:
        industry_name=skeyword.getclabel(industry_code)
    order=request.GET.get('order')
    searchlist={}
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if account:
        searchlist['account']=account
    if ip:
        searchlist['ip']=ip
    if keyword:
        searchlist['keyword']=keyword
    if company_id:
        searchlist['company_id']=company_id
    if industry_code:
        searchlist['industry_code']=industry_code
    if islog:
        searchlist['islog']=islog
    if is_senior:
        searchlist['is_senior']=is_senior
    searchurl=urllib.urlencode(searchlist)
    allindustry=zzlogin.getallindustry()
    allarea=zzlogin.getallarea()
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    searchkeyword=skeyword.getsearchkeyword(frompageCount,limitNum,gmt_begin,gmt_end,account,ip,keyword,company_id,islog,is_senior,industry_code,order)
    listcount=0
    listall=searchkeyword['list']
    listcount=searchkeyword['count']
    if int(listcount>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('company/keywordssearchdata.html',locals())

def keywordsscreening(request):
    return render_to_response('company/keywordsscreening.html',locals())
def huanbaodetail(request,id=''):
    if id:
        huanbaodetail=zzhuanbao.gethuanbaodetail(id)
        title=huanbaodetail['title']
        details=huanbaodetail['details']
#        details=details.replace('/uploads/uploads/media/',pyimgurl)
    return render_to_response('company/huanbaodetail.html',locals())
def huanbaolist(request):
    page=request.GET.get('page')
    category_code=request.GET.get('category_code')
    searchlist={}
    if category_code:
        searchlist['category_code']=category_code
    searchurl=urllib.urlencode(searchlist)
    allindustry=zzlogin.getallindustry()
    allarea=zzlogin.getallarea()
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(30)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    huanbaolist=zzhuanbao.gethuanbaolist(frompageCount,limitNum,category_code)
    listcount=0
    listall=huanbaolist['list']
    listcount=huanbaolist['count']
    if int(listcount>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('company/huanbaolist.html',locals())

#环保资讯一键删除
def del_all_huanbaolist(request):
    checkid=request.GET.getlist('checkid')
    zzhuanbao.delallhuanbaolist(checkid)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

arealist=[
          "全国","各地","江浙沪","沪",
          "国外","日本","美国","英国","法国","德国","新加坡",
          "A","安徽","阿坝","阿拉善","阿里","安康","安庆","鞍山","安顺","安阳","澳门",
          "B","北京","白银","保定","宝鸡","保山","包头","巴中","北海","蚌埠","本溪","毕节","滨州","百色","亳州",
          "C","长葛","重庆","成都","长沙","长春","沧州","常德","昌都","长治","常州","巢湖","潮州","承德","郴州","赤峰","池州","崇左","楚雄","滁州","朝阳",
          "D","大连","东莞","大理","丹东","大庆","大同","大兴安岭","德宏","德阳","德州","定西","迪庆","东营",
          "E","鄂尔多斯","恩施","鄂州",
          "F","福建","福州","防城港","佛山","抚顺","抚州","阜新","阜阳",
          "G","甘肃","贵州","广东","广西","广州","桂林","贵阳","甘南","赣州","甘孜","广安","广元","贵港","果洛",
          "H","湖北","湖南","河南","黑龙江","河北","杭州","哈尔滨","合肥","海口","呼和浩特","海北","海东","海南","海西","邯郸","汉中","鹤壁","河池","鹤岗","黑河","衡水","衡阳","河源","贺州","红河","淮安","淮北","怀化","淮南","黄冈","黄南","黄山","黄石","惠州","葫芦岛","呼伦贝尔","湖州","菏泽",
          "J","江西","江苏","吉林省","济南","佳木斯","吉安","江门","焦作","嘉兴","嘉峪关","揭阳","吉林","金昌","晋城","景德镇","荆门","荆州","金华","济宁","晋中","锦州","九江","酒泉",
          "K","昆明","开封",
          "L","辽宁","兰州","拉萨","来宾","莱芜","廊坊","乐山","凉山","连云港","聊城","辽阳","辽源","丽江","临沧","临汾","临夏","临沂","林芝","丽水","六安","六盘水","柳州","陇南","龙岩","娄底","漯河","洛阳","泸州","吕梁",
          "M","汨罗","马鞍山","茂名","眉山","梅州","绵阳","牡丹江",
          "N","宁夏","内蒙古","南海","南京","南昌","南宁","宁波","南充","南平","南通","南阳","那曲","内江","宁德","怒江",
          "P","盘锦","攀枝花","平顶山","平凉","萍乡","莆田","濮阳",
          "Q","青海","青岛","黔东南","黔南","黔西南","庆阳","清远","秦皇岛","钦州","齐齐哈尔","泉州","曲靖","衢州",
          "R","日喀则","日照",
          "S","陕西","四川","山西","山东","上海","深圳","苏州","沈阳","石家庄","三门峡","三明","三亚","商洛","商丘","上饶","山南","汕头","汕尾","韶关","绍兴","邵阳","十堰","朔州","四平","绥化","遂宁","随州","宿迁","宿州",
          "T","天津","太原","泰安","泰州","台州","唐山","天水","铁岭","铜川","通化","通辽","铜陵","铜仁","台湾",
          "W","武汉","乌鲁木齐","无锡","威海","潍坊","文山","温州","乌海","芜湖","乌兰察布","武威","梧州",
          "X","新疆","西藏","厦门","西安","西宁","襄樊","湘潭","湘西","咸宁","咸阳","孝感","邢台","新乡","信阳","新余","忻州","西双版纳","宣城","许昌","徐州","香港","锡林郭勒","兴安",
          "Y","云南","银川","雅安","延安","延边","盐城","阳江","阳泉","扬州","烟台","宜宾","宜昌","宜春","营口","益阳","永州","岳阳","榆林","运城","云浮","玉树","玉溪","玉林",
          "Z","杂多县","赞皇县","枣强县","枣阳市","枣庄","泽库县","增城市","曾都区","泽普县","泽州县","札达县","扎赉特旗","扎兰屯市","扎鲁特旗","扎囊县","张北县","张店区","章贡区","张家港","张家界","张家口","漳平市","漳浦县","章丘市","樟树市","张湾区","彰武县","漳县","张掖","漳州","长子县","湛河区","湛江","站前区","沾益县","诏安县","召陵区","昭平县","肇庆","昭通","赵县","昭阳区","招远市","肇源县","肇州县","柞水县","柘城县","浙江","镇安县","振安区","镇巴县","正安县","正定县","正定新区","正蓝旗","正宁县","蒸湘区","正镶白旗","正阳县","郑州","镇海区","镇江","浈江区","镇康县","镇赉县","镇平县","振兴区","镇雄县","镇原县","志丹县","治多县","芝罘区","枝江市","芷江侗族自治县","织金县","中方县","中江县","钟楼区","中牟县","中宁县","中山","中山区","钟山区","钟山县","中卫","钟祥市","中阳县","中原区","周村区","周口","周宁县","舟曲县","舟山","周至县","庄河市","诸城市","珠海","珠晖区","诸暨市","驻马店","准格尔旗","涿鹿县","卓尼","涿州市","卓资县","珠山区","竹山县","竹溪县","株洲","株洲县","淄博","子长县","淄川区","自贡","秭归县","紫金县","自流井区","资溪县","资兴市","资阳"]



def loadfile(request):
    username=request.session.get("username",None)
#    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        file = request.FILES['file']
#        newpath=os.getcwd()+'/load/'+timepath
        filename=file.name
        filetype=filename.split('.')[-1]
        filetype=filetype.upper()
        data=[]
        if filetype=='XLS':
            npath=os.path.dirname(__file__)
            newpath=npath+'/load/'
            imgpath=newpath+filename
            if not os.path.isdir(newpath):
                os.makedirs(newpath)
            des_origin_f = open(imgpath,"w")
            for chunk in file.chunks():
                des_origin_f.write(chunk)
            des_origin_f.close()
            book1=xlrd.open_workbook(imgpath)
            sheet1 = book1.sheet_by_name(filename[:8])
            data = sheet1.col_values(1)
            os.remove(imgpath)
        elif filetype=='CSV':
            file.readline()
            data = csv.reader(file)
        else:
            return HttpResponse("不支持该格式")
        listall=[]
        allnumb=0
        for d in data:
            allnumb=allnumb+1
            if filetype=='XLS':
                title=d
            elif filetype=='CSV':
                title=d[1].decode('gbk')
            list={'title':title}
            try:
                if u'价' in title:
                    for area in arealist:
                        if area.isalpha()==False and area.decode('utf-8') in title:
                            listall.append(list)
            except:
                pass
        if listall:
            numb=len(listall)
            percentage=str(float(numb)*100/allnumb)+'%'
        return render_to_response('company/loadimg.html',locals())
    return HttpResponse("请选择一个文件.")

#非法关键词管理
def feifa_list(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    page=request.GET.get('page')
    if not page:
        page=1
    keywords=request.GET.get('keywords')
    searchlist={}
    if keywords:
        searchlist['keywords']=keywords
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzfeifa.getfeifalist(frompageCount=frompageCount,limitNum=limitNum,keywords=keywords)
    listcount=userallr['count']
    listall=userallr['listall']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('feifa/feifa_list.html',locals())
#非法关键词添加
def feifa_add(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    return render_to_response('feifa/feifa_add.html',locals())
#非法关键词添加
def feifa_daoru(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    return render_to_response('feifa/feifa_daoru.html',locals())
#非法关键词保存
def feifa_save(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
      
    result=zzfeifa.addfeifawords(request)
    request_url=request.POST.get("request_url")
    return HttpResponseRedirect(request_url)
    return HttpResponseRedirect('feifa_list.html')
def feifa_listsave(request):
    collection=conn.sensitive.info
    keywordslist=request.POST.get('keywordslist')
    gmt_created=datetime.datetime.now()
    if keywordslist:
        arrkeywordslist=keywordslist.split(",")
        arrkeywordslist=keywordslist.split("\r\n")
        for list in arrkeywordslist:
            keywords=list
            if keywords:
                sql="select id from data_feifawords where keywords=%s"
                result=dbc.fetchonedb(sql,[keywords])
                if not result:
                    collection.insert({'words':keywords})
                    sql="insert into data_feifawords(keywords,gmt_created) values(%s,%s)"
                    result=dbc.updatetodb(sql,[keywords,gmt_created])
    return HttpResponseRedirect('feifa_list.html')
#非法关键词修改
def feifa_mod(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    result=zzfeifa.modfeifawords(request)
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('feifa/feifa_mod.html',locals())
#非法关键词删除
def feifa_del(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    check_box_list = request.REQUEST.getlist("check_box_list")
    result=zzfeifa.delfeifawords(request,check_box_list)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#更新
def feifa_update(request):
    collection=conn.sensitive.info
    gmt_created=datetime.datetime.now()
    r=requests.get("http://pyapp.zz91.com/feifa.html?"+str(gmt_created))
    content=r.text
    sql="update data_feifacontent set content=%s where id=1"
    dbc.updatetodb(sql,[content])
    """
    sql="select keywords from data_feifawords"
    result=dbc.fetchalldb(sql)
    listall=[]
    for list in result:
        keyw=list[0]
        result1=collection.find({'words':keyw})
        if not result1:
            collection.insert({'words':keyw})
    """
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
       