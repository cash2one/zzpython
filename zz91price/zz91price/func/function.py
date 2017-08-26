#-*- coding:utf-8 -*-
#----20140701格式化为2014-07-01
suliaoname=[
            {'name':'PVC','label':'聚氯乙烯'},
            {'name':'PS','label':'聚苯乙烯'},
            {'name':'PP','label':'聚丙烯'},
            {'name':'PE','label':'聚乙烯'},
            {'name':'PC','label':'聚碳酸酯'},
            ]
def getsuliaoname(name):
    for sl in suliaoname:
        if name==sl['name']:
            return sl['label']
#---获得第前后多少天
def gettimecha(timedata,num):
    timedata=str_to_date(timedata)
    if num<0:
        num2=int(str(num)[1:])
    else:
        num2=num
    mdays=datetime.timedelta(days=num2)
    if num>0:
        nowday=timedata+mdays
    else:
        nowday=timedata-mdays
    return date_to_int(nowday)
#    return date_to_str(nowday)
def gettimeall(timedate):
    return timedate[:4]+'-'+timedate[4:6]+'-'+timedate[6:8]
def getnowyear():
    return time.strftime('%Y',time.localtime(time.time()))
def getnowmonth():
    return time.strftime('%m',time.localtime(time.time()))
def getnowmohthdaysnumb(year,month):
    monthRange = calendar.monthrange(int(year),int(month))
    return monthRange[1]
def getnowmonthdayslist():
    nowyear=getnowyear()
    nowmonth=getnowmonth()
    number=getnowmohthdaysnumb(nowyear,nowmonth)
    listall=[]
    for numb in range(1,number+1):
        numb=str(numb)
        if len(numb)==1:
            numb='0'+numb
        alldate=nowyear+nowmonth+numb
        list={'alldate':alldate,'numb':numb}
        listall.append(list)
    return {'list':listall,'nowyear':nowyear,'nowmonth':nowmonth}
#获得明感字符
def getmingganword(s):
    sql="select id,updateflag,content from data_feifacontent where id=1"
    result=dbc.fetchonedb(sql)
    if not result:
        r=requests.get("http://pyapp.zz91.com/feifa.html")
        content=r.text
        sql="insert into data_feifacontent(id,content,updateflag) values(%s,%s,%s)"
        dbc.updatetodb(sql,[1,content,0])
    else:
        updateflag=result[1]
        if str(updateflag)=="1":
            r=requests.get("http://pyapp.zz91.com/feifa.html?a=0")
            content=r.text
            sql="update data_feifacontent set content=%s where id=1"
            dbc.updatetodb(sql,[content])
        else:
            content=result[2]
    lines=eval(content)
    list=[]
    if lines:
        for line in lines:
            line=line['k']
            line=line.strip('\n').strip()
            if line in s:
                return line
                break
            list.append(line)
    if s in list:
        return 2
    if "激情" in s:
        return 2
    if "乱伦" in s:
        return 2
    
    return None
def isfield(s):
    ss=['title','typename','type_id','assist_type_id','label','priceid','label1','label2','spec','spec1','spec2','price','price1','price2','price3','price4','price5','price6','area','area1','area2','postdate','num','othertext','qushi','othertext1','qushi1','unit']
    if s in ss:
        return 1
    else:
        return None
#获得两段时间相差几天
def getimedifferent(gmt_begin,gmt_end):
    gmt_begin=str_to_int(gmt_begin)
    gmt_end=str_to_int(gmt_end)
    result=(gmt_end-gmt_begin)/(3600*24)
    return result
def getdaohanglist(keywords,num=10):
    port = SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,search_count desc" )
    cl.SetLimits (0,num,num)
    if keywords:
        keywords=keywords.replace(","," | ")
    res = cl.Query ("@(tname) "+keywords,'tagslist')
    listall=[]
    listcount=0
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            for match in itemlist:
                attrs=match['attrs']
                id=attrs['tid']
                tname=str(attrs['tags'])
                main_code=attrs['main_code']
                pingyin=attrs['pingyin']
                list={'id':id,'name':tname,'pingyin':pingyin,'main_code':main_code}
                listall.append(list)
    return listall
#seo
def seolistcontent(pageflag,page_type,maintypename,categoryid,categoryname,page,area="",attrbute="",pinyin="",maincategory='',areapinyin='',searcharg=''):
    if maintypename=='废金属':
        title=categoryname+'价格_'+categoryname+'价格最新行情_今日'+categoryname+'价格_报价中心-zz91再生网'
        keywords=categoryname+'价格，'+categoryname+'价格最新行情，今日'+categoryname+'价格'
        description='zz91再生网'+categoryname+'行情报价中心，每天准时为您提供'+categoryname+'价格最新行情以及今日'+categoryname+'价格，让您及时掌握一手'+categoryname+'价格，熟悉最新'+categoryname+'市场动态。'
        if pinyin=='qihuo':
            if areapinyin=='LMEjibenjinshu':
                title='lme基本金属期货价格_lme基本金属期货最新价格行情_伦敦期货价格_行情报价中心-zz91再生网'
            else:
                title=area+'期货价格_'+area+'期货最新价格行情_上海有色金属价格_行情报价中心-zz91再生网'
            keywords=area+'期货价格，'+area+'期货最新价格行情，上海有色金属价格_'
            description='zz91再生网'+area+'期货行情报价中心，为您提供'+area+'期货最新价价格行情，信息准确可靠，让您及时掌握一手'+area+'期货最新信息，熟悉最新'+area+'市场动态。'
        elif categoryid==52:
            title=searcharg+'废电瓶价格_'+searcharg+'废电瓶最新价格行情_'+searcharg+'废电瓶回收价格_第'+str(page)+'页_行情报价报价中心-zz91再生网'
            keywords=searcharg+'废电瓶价格，电瓶价格行情，'+searcharg+'废电瓶回收价格'
            description='zz91再生网'+searcharg+'废电瓶价格频道，每天为您准时整理'+searcharg+'废电瓶最新价格行情，了解最新'+searcharg+'废电瓶回收价格，就上zz91再生网，专业的数据，让您做生意更安心。'
        elif categoryid==79:
            seoarg=categoryname.replace('上海','上海'+attrbute)
            title=seoarg+'价格_'+seoarg+'价格最新行情_今日'+seoarg+'价格_行情报价中心-zz91再生网'
            keywords=seoarg+'价格，'+seoarg+'价格最新行情，今日'+seoarg+'价格'
            description='zz91再生网'+categoryname+'行情报价中心，每天准时为您提供'+seoarg+'价格最新行情以及今日'+seoarg+'价格，让您及时掌握一手'+seoarg+'价格信息，熟悉最新'+seoarg+'市场动态。'
        #各地有色
        elif categoryid==65:
            title=categoryname+'价格_'+categoryname+'价格最新行情_今日'+categoryname+'价格_行情报价中心-zz91再生网'
            keywords=categoryname+'价格，'+categoryname+'价格最新行情，今日'+categoryname+'价格'
            description='zz91再生网'+categoryname+'行情报价中心，每天准时为您提供'+attrbute+'价格最新行情以及今日'+categoryname+'价格，让您及时掌握一手'+categoryname+'价格信息，熟悉最新'+categoryname+'市场动态。'
            
        elif categoryname=='生铁':
            title='生铁价格_生铁价格走势_生铁价格最新行情_铸造生铁价格行情_炼钢生铁价格行情_生铁网_行情报价中心-zz91再生网生铁报价中心'
            keywords='生铁价格, 生铁价格走势, 生铁价格行情，铸造生铁价格，炼钢生铁价格'
            description='zz91再生网生铁行情报价中心，每天准时为您提供生铁、铸造生铁、炼钢生铁价格最新行情以及今日生铁价格，让您及时掌握一手生铁行情信息，了解生铁最新市场动态。'
        #长江有色
        elif categoryid==210:
            title='长江有色金属价格_长江有色价格行情_上海长江有色金属网_行情报价中心-zz91再生网'
            keywords='长江有色金属价格，长江有色金属价格行情，上海长江有色金属网'
            description='zz91再生网长江有色金属网频道，为您提供最新厂家有色金属价格行情，让您快速了解上海长江有色金属市场动态，获取长江有色金属价格，就上zz91再生网。'
            
        elif categoryid in [69,70,71,72,206]:
            #上海废金属
            title=categoryname+'期货价格_'+categoryname+'期货最新价格行情_上海有色金属价格_行情报价中心-zz91再生网'
            keywords=categoryname+'期货价格，'+categoryname+'期货最新价格行情，上海有色金属价格_'
            description='zz91再生网'+categoryname+'期货行情报价中心，为您提供'+categoryname+'期货最新价价格行情，信息准确可靠，让您及时掌握一手'+categoryname+'期货最新信息，熟悉最新'+categoryname+'市场动态。'
        elif categoryid in [64]:
            title=categoryname+'价格_'+categoryname+'最新价格行情_行情报价中心-zz91再生网'
            keywords=categoryname+'价格，'+categoryname+'最新价格行情，LME/期货_'
            description='zz91再生网'+categoryname+'期货行情报价中心，为您提供'+categoryname+'最新价价格行情，信息准确可靠，让您及时掌握一手'+categoryname+'最新信息，熟悉最新'+categoryname+'市场动态。'
        elif categoryid==51:
            #废金属网上报价
            title='废金属网上价格_废金属网上价格最新行情_今日废金属网上价格_行情报价中心-zz91再生网'
            keywords='废金属网上价格，废金属网上价格最新行情，今日废金属网上价格'
            description='zz91再生网废金属行情报价中心，每天准时为您提供废金属网上价格最新行情以及今日废金属网上价格，让您及时掌握一手废金属网上价格信息，熟悉最新废金属网上市场动态。'
        elif categoryid==52:
            #----废电瓶
            title='废电瓶价格_废电瓶最新价格行情_废电瓶回收价格_第'+str(page)+'页_行情报价报价中心-zz91再生网'
            keywords='废电瓶价格，电瓶价格行情，废电瓶回收价格'
            description='zz91再生网废电瓶价格频道，每天为您准时整理废电瓶最新价格行情，了解最新废电瓶回收价格，就上zz91再生网，专业的数据，让您做生意更安心。'
        elif categoryid==56:
            #汨罗地区废金属
            title='汨罗废金属价格行情_行情报价中心-zz91再生网'
            keywords='汨罗废金属价格，汨罗废金属行情'
            description='zz91再生网汨罗废金属行情报价中心，每天准时为您提供汨罗废金属价格行情，让您及时掌握一手汨罗废金属信息，熟悉汨罗废金属最新市场动态。'
        elif categoryid==58:
            #汨罗地区废金属
            title='长葛废金属价格行情_行情报价中心-zz91再生网'
            keywords='长葛废金属价格，长葛废金属行情'
            description='zz91再生网长葛废金属行情报价中心，每天准时为您提供长葛废金属价格行情，让您及时掌握一手长葛废金属信息，熟悉长葛废金属最新市场动态。'
        elif categoryid in [32,33,216]:
            #金属评论
            title='废金属评论_行情报价中心-zz91再生网'
            keywords='废金属评论'
            description='zz91再生网废金属评论频道，每天准时为您提供最新的废金属评论，第一时间了解国际废金属行情，就上zz91再生网。'
    elif maintypename=='废塑料':

        title=categoryname+area+'价格_'+categoryname+area+'价格行情_'+categoryname+area+'塑料价格_行情报价中心-zz91再生网'
        keywords=categoryname+area+'价格，'+categoryname+area+'价格行情，'+categoryname+area+'塑料价格'
        description='zz91再生网'+categoryname+area+'行情报价中心，每天准时为您提供'+categoryname+area+'价格行情，让您及时掌握一手'+categoryname+area+'信息，熟悉'+categoryname+area+'最新市场动态。'
        
        
        
        if pinyin in ['pvc','ps','pp','pe','pc']:
            slname=getsuliaoname(categoryname)
            title=area+categoryname+'价格_'+area+categoryname+'价格行情_'+area+categoryname+'塑料价格_'+slname+'价格_第'+str(page)+'页_行情报价中心-zz91再生网'
            keywords=''+area+categoryname+'价格，'+area+categoryname+'价格行情，'+area+categoryname+'塑料价格,'+slname+'价格'
            description='zz91再生网'+area+categoryname+'行情报价中心，每天准时为您提供'+area+categoryname+'（'+slname+'）价格行情，让您及时掌握一手'+area+categoryname+'信息，熟悉'+slname+'最新市场动态。'
        #废塑料网上报价
        elif categoryid==137:
            title='废塑料网上价格_价格走势_废塑料网上价格最新行情_今日废塑料网上价格_废塑料网上回收价格_废塑料网上价格网_行情报价中心-zz91再生网废塑料网上报价中心'
            keywords='废塑料网上价格，废塑料网上价格走势，废塑料网上价格最新行情，今日废塑料网上价格，废塑料网上回收价格，废塑料网上废塑料网上价格网'
            description='zz91再生网报价中心，每天准时为您提供废塑料网上价格最新行情以及今日废塑料网上价格，让您及时掌握一手废塑料网上价格信息，熟悉废塑料网上最新市场动态。'
        #----废塑料评论,废塑料周报
        elif categoryid in [34,35]:
            title='废塑料评论_行情报价中心-zz91再生网'
            keywords='废塑料评论'
            description='zz91再生网废塑料评论频道，每天准时为您提供最新的废塑料评论，第一时间了解国际废塑料行情，就上zz91再生网。'
        #LME/期货
        elif categoryid==64:
            title='LME基本金属期货价格_沪锌期货价格_沪铝期货价格_沪铜期货价格_沪钢期货价格 _行情报价中心-zz91再生网'
            keywords='LME基本金属期货价格，沪锌期货价格，沪铝期货价格，沪铜期货价格，沪钢期货价格'
            description='zz91再生网金属期货行情报价中心，每天为您准时提供LME基本金属、沪锌、沪铝、沪铜、沪钢期货价格，让您及时掌握一手金属期货价格，熟悉最新金属期货市场动态。'
        
        elif maincategory=='塑料地区':
            if pinyin=='suliaozaishengliaojiagehangqing':
                title=area+'再生颗粒价格_'+area+'再生塑料颗粒价格行情 _第'+str(page)+'页_行情报价中心-zz91再生网'
                keywords=area+'再生颗粒价格，塑料颗粒价格，塑料价格行情'
                description='zz91再生网'+area+'再生颗粒频道，每天准时为您提供再生'+area+'塑料颗粒价格行情，第一时间了解'+area+'再生塑料颗粒行情，就上zz91再生网。'
            elif categoryid in [60,61]:
                if page_type==2:
                    title=area+categoryname+'_行情报价中心-zz91再生网'
                    keywords=area+categoryname
                    description='zz91再生网'+area+categoryname+'频道，每天为您准时提供最新的'+area+categoryname+'，让您能够快速获取最新的'+area+'价格信息，掌握'+area+'市场动态。'
                else:
                    title='塑料新料'+categoryname+'_行情报价中心-zz91再生网'
                    keywords='塑料新料'+categoryname+'，国内石化塑料新料'+categoryname
                    description='zz91再生网国内石化塑料新料'+categoryname+'频道，每天准时为您提供新料'+categoryname+'格行情，第一时间了解塑料新料'+categoryname+'，就上zz91再生网。'
            elif categoryid in [62,63]:
                title=categoryname+area+'价格_ '+categoryname+area+'价格行情_行情报价中心-zz91再生网'
                keywords=categoryname+area+'价格，'+categoryname+area+'价格行情'
                description='zz91再生网'+categoryname+area+'行情报价中心，每天准时为您提供'+categoryname+area+'价格行情，让您及时掌握一手'+categoryname+area+'信息，熟悉'+categoryname+area+'最新市场动态。'
            elif pinyin=='yuyao':
                if areapinyin in ['PVC','PS','PP','PE','PC']:
                    slname=getsuliaoname(areapinyin)
                    title='余姚'+area+'价格_余姚'+area+'价格行情_余姚'+area+'塑料价格_余姚'+slname+'价格_行情报价中心-zz91再生网'
                    keywords='余姚'+area+'价格，余姚'+area+'价格行情，余姚'+area+'塑料价格, 余姚'+slname+'价格'
                    description='zz91再生网余姚'+area+'行情报价中心，每天准时为您提供余姚'+area+'（'+slname+'）价格行情，让您及时掌握一手余姚'+area+'信息，熟悉余姚'+slname+'最新市场动态。'
                else:
                    if pageflag==2:
                        title='余姚'+area+'价格_余姚'+area+'价格行情_余姚'+area+'塑料价格 _行情报价中心-zz91再生网'
                        keywords='余姚'+area+'价格，余姚'+area+'价格行情，余姚'+area+'塑料价格'
                        description='zz91再生网余姚'+area+'行情报价中心，每天准时为您提供余姚'+area+'价格行情，让您及时掌握一手余姚'+area+'信息，熟悉余姚'+area+'最新市场动态。'
                    else:
                        title='余姚塑料城最新价格_余姚塑料城最新报价_行情报价中心-zz91再生网'
                        keywords='余姚塑料市场最新价格，余姚塑料市场最新报价'
                        description='zz91再生网余姚塑料市场行情报价中心，每天准时为您提供余姚塑料市场最新价格（报价），第一时间了解中国余姚塑料市场塑料价格，就上zz91再生网。'
            elif pinyin in ['shanghai1','qilu1','dongguan1','shunde1']:
                nowlanmu=categoryname+area
                title=categoryname+area+'价格_'+categoryname+area+'最新价格行情_行情报价中心-zz91再生网'
                keywords=categoryname+area+'价格，'+categoryname+area+'行情，'+categoryname+area+'最新价格行情'
                description='zz91再生网'+categoryname+area+'行情报价中心，每天准时为您提供'+categoryname+area+'价格行情，让您及时掌握一手'+categoryname+area+'信息，熟悉'+categoryname+area+'最新市场动态。'
                
            elif categoryid in [111,112,113,114,115,118,119,120,121,126,324]:
                title=area+'塑料市场价_行情报价中心-zz91再生网'
                keywords=area+'塑料市场价'
                description='zz91再生网'+area+'塑料市场价频道，每天准时为您提供'+area+'塑料市场价格行情，第一时间了解'+area+'塑料市场价，就上zz91再生网。'
            else:
                if pageflag==1:
                    title=categoryname+'塑料市场价格行情_最新'+categoryname+'塑料市场价_行情报价中心-zz91再生网'
                    keywords=categoryname+'塑料市场价格行情，最新'+categoryname+'塑料市场价'
                    description='zz91再生网'+categoryname+'塑料频道，每天准时为您提供'+categoryname+'塑料最新市场价格（报价），第一时间了解'+categoryname+'塑料行情，就上zz91再生网。'
    else:
        if categoryid==140:
            title=categoryname+'塑料市场价格行情_最新'+categoryname+'塑料市场价_行情报价中心-zz91再生网'
            keywords=categoryname+'塑料市场价格行情，最新'+categoryname+'塑料市场价'
            description='zz91再生网'+categoryname+'塑料频道，每天准时为您提供'+categoryname+'塑料最新市场价格（报价），第一时间了解'+categoryname+'塑料行情，就上zz91再生网。'
        elif categoryid==190:
            title='原油期货价格_ 今日原油价格_ 国际原油期货价格_第'+str(page)+'页_行情报价中心-zz91再生网'
            keywords='原油期货价格，今日原油价格，国际原油期货价格'
            description='zz91再生网原油期货频道，每天准时为您提供国际原油期货价格（报价），第一时间了解国际原油期货行情，就上zz91再生网。'
        elif categoryid==13:
            title='废纸回收价格_废纸价格行情_废纸网_第'+str(page)+'页_行情报价中心-zz91再生网'
            keywords='废纸价格，废纸回收价格，废纸价格行情，废纸网'
            description='zz91再生网废纸网频道，及时为您提供最新的废纸回收价格、废纸价格行情等一系列精准报价，第一时间了解废纸行情，就上zz91再生网行情报价中心。'
    #            elif maintypename=='废橡胶':
        elif categoryid in [30,287]:
            title='废橡胶回收价格_废橡胶价格行情_废橡胶网_第'+str(page)+'页_行情报价中心-zz91再生网'
            keywords='废橡胶价格，废橡胶回收价格，废橡胶价格行情，废橡胶网'
            description='zz91再生网废橡胶网频道，及时为您提供最新的废橡胶回收价格、废橡胶价格行情等一系列精准报价，第一时间了解废橡胶行情，就上zz91再生网行情报价中心。'
        elif categoryid==231:
            categoryname='各地废纸'
            title=categoryname+'价格_'+categoryname+'价格走势_'+categoryname+'价格最新行情_今日'+categoryname+'价格_'+categoryname+'回收价格_'+categoryname+'价格网_行情报价中心-zz91再生网'+categoryname+'报价中心'
            keywords=categoryname+'价格，'+categoryname+'价格走势，'+categoryname+'价格最新行情，今日'+categoryname+'价格，'+categoryname+'回收价格，'+categoryname+'价格网'
            description='zz91再生网'+categoryname+'报价中心，每天准时为您提供'+categoryname+'价格最新行情以及今日'+categoryname+'价格，让您及时掌握一手'+categoryname+'价格信息，熟悉'+categoryname+'最新市场动态。'
        elif categoryid==25:
            categoryname='废纸网上'
            title=categoryname+'价格_'+categoryname+'价格走势_'+categoryname+'价格最新行情_今日'+categoryname+'价格_'+categoryname+'回收价格_'+categoryname+'价格网_行情报价中心-zz91再生网'+categoryname+'报价中心'
            keywords=categoryname+'价格，'+categoryname+'价格走势，'+categoryname+'价格最新行情，今日'+categoryname+'价格，'+categoryname+'回收价格，'+categoryname+'价格网'
            description='zz91再生网'+categoryname+'报价中心，每天准时为您提供'+categoryname+'价格最新行情以及今日'+categoryname+'价格，让您及时掌握一手'+categoryname+'价格信息，熟悉'+categoryname+'最新市场动态。'
        elif categoryid in [26,27,28,29]:
            title=categoryname+'价格_'+categoryname+'价格最新行情_今日'+categoryname+'价格_报价中心-zz91再生网'
            keywords=categoryname+'价格，'+categoryname+'价格最新行情，今日'+categoryname+'价格'
            description='zz91再生网'+categoryname+'行情报价中心，每天准时为您提供'+categoryname+'价格最新行情以及今日'+categoryname+'价格，让您及时掌握一手'+categoryname+'价格，熟悉最新'+categoryname+'市场动态。'
        else:
            title=categoryname+'_行情报价中心-zz91再生网'
            keywords=categoryname
            description='zz91再生网'+categoryname+'频道，每天准时为您提供最新'+categoryname+'，第一时间了解'+categoryname+'，请关注zz91再生网，专业的数据为您的生意保驾护航。'
    return {'title':title,'keywords':keywords,'description':description}

def get_img_url(html):#获得图片url
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

class zz91company:
    def __init__(self):
        self.dbc=dbc
    def getpricedblist(self,frompageCount='',limitNum='',typeid='',assist_type_id=''):
        #获得缓存
        #zz91price_getpricedblist=cache.get("zz91price_getpricedblist"+str(typeid)+str(assist_type_id))+str(frompageCount)+str(limitNum)
        #if zz91price_getpricedblist:
            #return zz91price_getpricedblist 
        sqlarg=''
        argument=[]
        if typeid:
            sqlarg+=' and a.type_id in ('+str(typeid)+')'
            #argument.append(typeid)
        if assist_type_id:
            sqlarg+=' and a.assist_type_id=%s'
            argument.append(assist_type_id)
        sql1='select count(0) from price as a where id>0'+sqlarg
        sql='select a.id,a.title,a.content,a.type_id,b.pinyin,a.gmt_order from price as a left join price_category as b on a.type_id=b.id where a.id>0'+sqlarg
        sql+=' order by a.id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            td_id=result[0]
            url='/detail/'+str(td_id)+'.html'
            ptitle=result[1]
            content=result[2]
            type_id=result[3]
            urlpath=result[4]
            gmt_order=formattime(result[5],1)
            content=filter_tags(content).replace(' ','')
            pcontent=subString(content,150)
            imgurl=get_img_url(result[2])
            pic=''
            if imgurl:
                pic=imgurl[0]
            if not pic:
                pic='http://img0.zz91.com/front/images/global/noimage.gif'
            list={'td_id':td_id,'url':url,'td_title':ptitle,'content':pcontent,'pic':pic,'urlpath':urlpath,'gmt_order':gmt_order}
            listall.append(list)
        #设置缓存
        #cache.set("zz91price_getpricedblist"+str(typeid)+str(assist_type_id)+str(frompageCount)+str(limitNum),{'list':listall,'count':count},60*10)
        return {'list':listall,'count':count}
        
    def getclist(self,provincecode):
        catelist=cache.get("price_clist"+str(provincecode))
        if catelist:
            return catelist
        sql='select code,label from category where parent_code=%s limit 0,30'
        resultlist=dbc.fetchalldb(sql,provincecode)
        listall=''
        for result in resultlist:
            code=result[0]
            label=result[1]
            listall+='<option value="'+code+'">'+label+'</option>'
        if listall:
            cache.set("price_clist"+str(provincecode),listall,60*20)
        return listall
    def getcompaccountdetail(self,company_id):
        catelist=cache.get("price_countdetail"+str(company_id))
        if catelist:
            return catelist
        sql='select contact,mobile from company_account where company_id=%s'
        result=self.dbc.fetchonedb(sql,company_id)
        if result:
            contact=result[0]
            mobile=result[1]
            listall={'contact':contact,'mobile':mobile}
            cache.set("price_countdetail"+str(company_id),listall,60*20)
            return {'contact':contact,'mobile':mobile}
    def getclabel(self,code):
        catelist=cache.get("price_clabel"+str(code))
        if catelist:
            return catelist
        sql='select label from category where code=%s'
        result=self.dbc.fetchonedb(sql,code)
        if result:
            cache.set("price_clabel"+str(code),result[0],60*20)
            return result[0]
    def getparentcategorylist(self,parent_code='10011000'):
        catelist=cache.get("parentcategorylist"+str(parent_code))
        if catelist:
            return catelist
        sql='select code,label from category where parent_code=%s limit 0,30'
        resultlist=self.dbc.fetchalldb(sql,parent_code)
        listall=[]
        for result in resultlist:
            code=result[0]
            label=result[1]
            list={'code':code,'label':label}
            listall.append(list)
        if listall:
            cache.set("parentcategorylist"+str(parent_code),listall,60*20)
        return listall
    def gethuilvlist(self,numb,miancountry,country):
        #获得缓存
        #zz91price_gethuilvlist=cache.get("zz91price_gethuilvlist"+str(numb)+str(miancountry)+str(country))
        #if zz91price_gethuilvlist:
            #return zz91price_gethuilvlist 
        listall=[]
        if miancountry==country:
            listall=[1*numb,1*numb]
        else:
            sql='select rate from exchange_rate where miancountry=%s and country=%s'
            sql1='select rate from exchange_rate where country=%s and miancountry=%s'
            result=self.dbc.fetchonedb(sql,[miancountry,country])
            result1=self.dbc.fetchonedb(sql1,[miancountry,country])
            if result and result1:
                if numb and result[0] and result1[0]:
                    listall.append(result[0]*float(numb))
                    listall.append(result1[0]*float(numb))
        #设置缓存
        #cache.set("zz91price_gethuilvlist"+str(numb)+str(miancountry)+str(country),listall,60*10)
        return listall
    def getdetailtypeid(self,content):
        shuzilist=re.findall('[\d]+',content)
        if shuzilist:
            for shuzi in shuzilist:
                if len(shuzi)>1:
                    return shuzi
    def replacedetaila(self,content):
#        content=re.sub('http://price.zz91.com/','/',content)
#        content=re.sub('priceDetails_','detail/',content)
        if '<div>' in content or '</div>' in content:
            #----处理特殊报价内容,否侧详细页样式会乱
            content=content.replace('<div>','')
            content=content.replace('</div>','')
            #content+='</div>'
#            content=content.replace('<div>','<div class="aboutContent">')
#        content=content.replace('.htm','.html')
#        content=content.replace('.htmll','.html')
#        acontent=re.findall('<a.*?>',content)
#        for acn in acontent:
#            if 'price.zz91' in acn:
#                categoryid=self.getdetailtypeid(acn)
#                if categoryid:
#                    categorypinyin=self.getpricecategorypinyin(categoryid)
#                    if categorypinyin:
#                        content=re.sub(acn,'<a href="/'+categorypinyin+'/" style="color:blue" target="_blank">',content)
#        re_py=r'<a.*?href="([^"]+)"'
#        urls_pat=re.compile(re_py)
#        arg_url=re.findall(urls_pat,html)
        listcontent=re.findall('<a.*?href="([^"]+)"',content)
        content=content.replace('http://jiage.zz91.com/','/')
        for list in listcontent:
            if 'priceDetails' in list:
                list2=list.replace('priceDetails_','detail/')
                list2=list2.replace('.htm','.html')
                list2=list2.replace('http://jiage.zz91.com/','/')
                content=content.replace(list,list2)
        return content

    def getpriceattrlabel(self,pinyin):
        sql='select label from price_category_attr where pinyin=%s'
        result=self.dbc.fetchonedb(sql,[pinyin])
        if result:
            return result[0]
        return ''
    def getpricecategoryname(self,pinyin):
        sql='select name from price_category where pinyin=%s'
        result=self.dbc.fetchonedb(sql,[pinyin])
        if result:
            return result[0]
        return ''
    def getpricecategoryid(self,id):
        sql='select type_id from price where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
        return ''
    #上一篇和下一篇
    def getpre_nextprice(self,id,typeid=''):
        nextid=''
        nexttitle=''
        nexturlpath=''
        parms=[id]
        sql="select a.id,a.type_id,a.title,b.pinyin from price as a left join price_category as b on a.type_id=b.id where a.id>%s "
        if typeid:
            sql+=" and type_id=%s "
            parms.append(typeid)
        sql+=" order by id asc limit 0,1"
        
        result=self.dbc.fetchonedb(sql,parms)
        if result:
            nextid=result[0]
            nexttitle=result[2]
            nexturlpath=result[3]
        preid=''
        pretitle=''
        preurlpath=''
        parms=[id]
        sql="select a.id,a.type_id,a.title,b.pinyin from price as a left join price_category as b on a.type_id=b.id where a.id<%s "
        if typeid:
            sql+=" and type_id=%s "
            parms.append(typeid)
        sql+=" order by id desc limit 0,1"
        result=self.dbc.fetchonedb(sql,parms)
        if result:
            preid=result[0]
            pretitle=result[2]
            preurlpath=result[3]
        return {'nextid':nextid,'nexttitle':nexttitle,'nexturlpath':nexturlpath,'preid':preid,'pretitle':pretitle,'preurlpath':preurlpath}
            
    def getpriceassistid(self,id):
        sql='select assist_type_id from price where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
        return ''
    def getpriceattrpinyin(self,label):
        sql='select pinyin from price_category_attr where label=%s'
        result=self.dbc.fetchonedb(sql,[label])
        if result:
            return result[0]
        return ''
    def getpricearealist(self,categoryid,parent_id,page_type='',morelist='',title=''):
        #获得缓存
        #zz91price_getpricearealist=cache.get("zz91price_getpricearealist"+str(categoryid)+str(parent_id)+str(page_type)+str(morelist))
        #if zz91price_getpricearealist:
            #return zz91price_getpricearealist 
        sql='select label,pinyin,page_type from price_category_attr where price_category_id=%s and parent_id=%s'
        if morelist:
            if page_type=='1':
                sql+=' and page_type=1'
            else:
                sql+=' and page_type=0'
        sql+=' order by sortrank asc'
        resultlist=self.dbc.fetchalldb(sql,[categoryid,parent_id])
        listall=[]
        numb=0
        for result in resultlist:
            numb+=1
            label=result[0]
            pinyin=result[1]
            page_type=result[2]
            if pinyin:
                pinyin=pinyin.replace('-','_')
            selectlabel=None
            if label in title:
                selectlabel=1
            list={'label':label,'pinyin':pinyin,'numb':numb,'page_type':page_type,'selectlabel':selectlabel}
            listall.append(list)
        #设置缓存
        #cache.set("zz91price_getpricearealist"+str(categoryid)+str(parent_id)+str(page_type)+str(morelist),listall,60*10)
        return listall
    def getpricecategorychildlist(self,parent_id):
        catelist=cache.get("price_categorychildlist"+str(parent_id))
        if catelist:
            return catelist
        sql='select name,pinyin,page_type,id from price_category where parent_id=%s and showflag=1 order by show_index asc'
        resultlist=self.dbc.fetchalldb(sql,[parent_id])
        listall=[]
        numb=0
        for result in resultlist:
            id=result[3]
            #过滤常州废塑料
            if id==114:
                continue
            numb+=1
            label=result[0]
            pinyin=result[1]
            page_type=result[2]
            if pinyin:
                pinyin=pinyin.replace('-','_')
            list={'label':label,'pinyin':pinyin,'numb':numb,'page_type':page_type,'id':id}
            listall.append(list)
        if listall:
            cache.set("price_categorychildlist"+str(parent_id),listall,60*20)
        return listall
    def getpricefield(self,priceid):
        catelist=cache.get("price_fieldid"+str(priceid))
        if catelist:
            return catelist
        sql='select DISTINCT filed,name from price_titlefild where priceid=%s order by id asc'
        resultlist=self.dbc.fetchalldb(sql,[priceid])
        listname=[]
        listfield=[]
        for result in resultlist:
            name=result[1]
            #if name:
                #name=name.upper()
            filed=result[0]
            listname.append(name)
            listfield.append(filed)
#            list={'name':name,'filed':filed}
#            listall.append(list)
        listdir={'listname':listname,'listfield':listfield}
        if listname and listfield:
            cache.set("price_field"+str(priceid),listdir,60*20)
        return listdir
    def getpricefield2(self,categoryid="",assist_type_id="",priceid=""):
        catelist=cache.get("price_field"+str(categoryid)+str(assist_type_id))
        if catelist:
            return catelist
        sql='select DISTINCT field,name from price_category_field where price_category_id=%s and assist_type_id=%s order by id asc'
        resultlist=self.dbc.fetchalldb(sql,[categoryid,assist_type_id])
        if resultlist:
            listname=[]
            listfield=[]
            for result in resultlist:
                name=result[1]
                #if name:
                    #name=name.upper()
                field=result[0]
                listname.append(name)
                listfield.append(field)
            listdir={'listname':listname,'listfield':listfield}
            if listname and listfield:
                cache.set("price_field2"+str(categoryid)+str(assist_type_id),listdir,60*20)
                return listdir
        else:
            return self.getpricefield(priceid)
    def getcategorydate(self,categoryid,a=0):
        if a==1:
            sql="select gmt_created from price where assist_type_id=%s and is_checked=1 order by gmt_created desc"
        else:
            sql="select gmt_created from price where type_id=%s and is_checked=1 order by gmt_created desc"
        resultlist=self.dbc.fetchonedb(sql,[categoryid])
        if resultlist:
            return resultlist[0]
    def getcategoryxml(self,categoryid,sx,p=0,a=0):
        if p==0:
            sql='select name,pinyin,page_type,id from price_category where parent_id=%s and showflag=1 order by show_index asc'
            resultlist=self.dbc.fetchalldb(sql,[categoryid])
        else:
            sql='select name,pinyin,page_type,id from price_category where id in ('+categoryid+') and showflag=1 order by show_index asc'
            resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[3]
            label=result[0]
            pinyin=result[1].lower()
            page_type=result[2]
            if pinyin:
                pinyin=pinyin.replace('-','_')
            loc="http://jiage.zz91.com/"+pinyin+"/"
            #lastmod=self.getcategorydate(id,a=a)
            lastmod=formattime(datetime.datetime.now(),2)
            priority="0.8"
            
            list={'loc':loc,'lastmod':lastmod,'priority':priority}
            listall.append(list)
            
            sqla='select label,pinyin,page_type,parent_id from price_category_attr where price_category_id=%s and parent_id=%s'
            sqla+=' order by sortrank asc'
            resultlista=self.dbc.fetchalldb(sqla,[id,sx])
            for resulta in resultlista:
                pinyina=resulta[1].lower()
                page_type=resulta[2]
                parent_id=resulta[3]
                if pinyina:
                    pinyina=pinyina.replace('-','_')
                if str(page_type)=="1" or a==1:
                    pinyina="a-"+pinyina+"-1"
                    if a==1 and str(parent_id)=="2":
                        pinyina="x-"+pinyina+"-1"
                else:
                    pinyina="a-"+pinyina
                loc="http://jiage.zz91.com/"+pinyin+"/"+pinyina+"/"
                prioritya="0.7"
                lista={'loc':loc,'lastmod':lastmod,'priority':prioritya}
                listall.append(lista)
        return listall
    #----获得报价得主类别,主类别类型
    def getmaindetail(self,categoryid):
        catelist=cache.get("price_maindetail"+str(categoryid))
        if catelist:
            return catelist
        parent_id=self.getparent_id(categoryid)
        parent_id2=self.getparent_id(parent_id)
        parent_id3=self.getparent_id(parent_id2)
        maintypename=''
        maincategory=''
        if parent_id in [3,5] or parent_id2 in [3,5] or parent_id3 in [3,5]:
            maintypename='废金属'
            if parent_id==3 or parent_id2==3 or parent_id3==3:
                maincategory='金属地区'
            else:
                maincategory='金属产品'
        elif parent_id in [4,6,11] or parent_id2 in [4,6,11] or parent_id3 in [4,6,11]:
            maintypename='废塑料'
            if parent_id==4 or parent_id2==4 or parent_id3==4:
                maincategory='塑料产品'
            else:
                maincategory='塑料地区'
        elif parent_id==7 or parent_id2==7 or parent_id3==7:
            maintypename='废纸'
        elif parent_id==8 or parent_id2==8 or parent_id3==8:
            maintypename='废橡胶'
        elif parent_id==213 or parent_id2==213 or parent_id3==213:
            maintypename='原油'
        listdir={'maintypename':maintypename,'maincategory':maincategory}
        if maintypename and maincategory:
            cache.set("price_maindetail"+str(categoryid),listdir,60*20)
        return listdir
    def getparent_id(self,id):
        sql='select parent_id from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getcategorydetail(self,pinyin):
        catelist=cache.get("price_categorydetail"+str(pinyin))
        if catelist:
            return catelist
        sql='select id,name,page_type from price_category where pinyin=%s and showflag=1 order by show_index asc'
        result=self.dbc.fetchonedb(sql,[pinyin])
        if result:
            listdir={'id':result[0],'name':result[1],'page_type':result[2]}
            cache.set("price_categorydetail"+str(pinyin),listdir,60*20)
            return listdir
        return {'id':'','name':'','page_type':''}
    def getdaohanglist(self,category_code):
        catelist=cache.get("price_daohanglist"+str(category_code))
        if catelist:
            return catelist
        sql='select title,link from data_index where category_code=%s order by sort asc,gmt_created asc'
        resultlist=self.dbc.fetchalldb(sql,[category_code])
        listall=[]
        numb=0
        for result in resultlist:
            numb+=1
            listall.append({'title':result[0],'link':result[1],'numb':numb})
        if listall:
            cache.set("price_daohanglist"+str(category_code),listall,60*20)
        return listall
    def getpricedetail(self,id):
        sql='select title,content,gmt_order from price where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            content=result[1]
            content=filter_tags(content).replace(' ','')
            pcontent=subString(content,150)
            gmt_order=formattime(result[2],1)
            return {'title':result[0],'content':result[1],'pcontent':pcontent,'gmt_order':gmt_order}
    def getpricecontentall(self,id):
        sql='select content from price where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getqihuolist(self):
        catelist=cache.get("price_qihuolist")
        if catelist:
            return catelist
        listall=[]
        qihuotong_id=self.getprlist(0,1,1,'',[72])['list']
        if qihuotong_id:
            qihuotong_id=qihuotong_id[0]['td_id']
        qihuoxin_id=self.getprlist(0,1,1,'',[71])['list']
        if qihuoxin_id:
            qihuoxin_id=qihuoxin_id[0]['td_id']
        qihuolv_id=self.getprlist(0,1,1,'',[69])['list']
        if qihuolv_id:
            qihuolv_id=qihuolv_id[0]['td_id']
        qihuogang_id=self.getprlist(0,1,1,'',[206])['list']
        if qihuogang_id:
            qihuogang_id=qihuogang_id[0]['td_id']
        if qihuotong_id and qihuoxin_id and qihuolv_id and qihuogang_id:
            listallid=[{'id':qihuotong_id,'title':'沪铜'},
                       {'id':qihuoxin_id,'title':'沪铝'},
                       {'id':qihuolv_id,'title':'沪锌'},
                       {'id':qihuogang_id,'title':'沪钢'}]
            for listp in listallid:
                id=listp['id']
                title=listp['title']
                qihuo_content=self.getpricecontentall(id)
                qihuodetail=self.getpricetablelist(qihuo_content)
                price=qihuodetail['price']
                zhangdie=qihuodetail['zhangdie']
                list={'id':id,'title':title,'price':price,'zhangdie':zhangdie}
                listall.append(list)
        if listall:
            cache.set("price_qihuolist",listall,60*20)
        return listall
    def getpricetablelist(self,content):
        #获得缓存
        #zz91price_getpricetablelist=cache.get("zz91price_getpricetablelist"+str(content))
        #if zz91price_getpricetablelist:
            #return zz91price_getpricetablelist 
        soup = BeautifulSoup(content)
        list={'price':'','zhangdie':''}
        for table in soup.findAll('table'):
            i=1
            for row in table.findAll('tr'):
                j=1
                for tr in row.findAll('td'):
                    textname=tr.text.encode("utf-8")
                    if j==2:
                        list['price']=textname
                    if j==3:
#                        textname2=re.findall('[\d]+',textname)
#                        if textname2:
#                            textname2=textname2[0]
#                            if int(textname2)>0:
#                                textname='<font color="red">↑</font> '+textname
#                            if int(textname2)<0:
#                                textname='↓ '+textname
                        if '-' in textname:
                            textname=textname.replace('-','<font color="red">↓</font> ')
                        elif textname=='0':
                            textname='0'
                        else:
                            textname='<font color="red">↑</font> '+textname
                            
                        list['zhangdie']=textname
                    j+=1
                i+=1
        #设置缓存
        #cache.set("zz91price_getpricetablelist"+str(content),list,60*10)
        return list
    def getchartgmtdetailist(self,title):
         #获得缓存
        #zz91price_getchartgmtdetailist=cache.get("zz91price_getchartgmtdetailist"+str(title))
        #if zz91price_getchartgmtdetailist:
            #return zz91price_getchartgmtdetailist 
        sql='select gmt_date from charts_info where title=%s group by gmt_date order by id desc limit 0,30'
        resultlist=self.dbc.fetchalldb(sql,[title])
        listall=[]
        for result in resultlist:
            gmt_date=result[0]
            if gmt_date:
                gmt_date=gmt_date.strftime('%m-%d')
            listall.append(gmt_date)
        if listall:
            listall=listall[::-1]
        #设置缓存
        cache.set("zz91price_getchartgmtdetailist"+str(title),listall,60*10)
        return listall
    #----4张走势图翻页数据
    def getchartdatalistall(self,frompageCount,limitNum,chart_category_id='',name='',zhangdie=''):
        #获得缓存
        #zz91price_getchartdatalistall=cache.get("zz91price_getchartdatalistall"+str(chart_category_id)+str(name)+str(zhangdie))
        #if zz91price_getchartdatalistall:
            #return zz91price_getchartdatalistall 
        sqlarg=''
        argument=[]
        if chart_category_id:
            sqlarg+=' and chart_category_id=%s'
            argument.append(chart_category_id)
        if name:
            sqlarg+=' and name=%s'
            argument.append(name)
        sql1='select count(0) from chart_data where id>0'+sqlarg
        sql='select id,chart_category_id,name,value,gmt_created from chart_data where id>0'+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        sql2='select value from chart_data where chart_category_id=%s order by id desc limit 1,1'
        for result in resultlist:
            id=result[0]
            chart_category_id=result[1]
            chart_category=self.getchart_category(chart_category_id)
            name=result[2]
            value=result[3]
            gmt_created=formattime(result[4])
            valuedf='0.0'
            if zhangdie:
                result1=self.dbc.fetchonedb(sql2,chart_category_id)
                if result1:
                    valuedf=value-result1[0]
            list={'id':id,'chart_category_id':chart_category_id,'chart_category':chart_category,'name':name,'value':value,'gmt_created':gmt_created,'valuedf':valuedf}
            listall.append(list)
        #设置缓存
        #cache.set("zz91price_getchartdatalistall"+str(chart_category_id)+str(name)+str(zhangdie),{'list':listall,'count':count},60*5)
        return {'list':listall,'count':count}
    def getchartdetailist(self,name,chart_category_id,gmt_begin='',gmt_end=''):
        #获得缓存
        #zz91price_getchartdetailist=cache.get("zz91price_getchartdetailist"+str(chart_category_id)+str(name)+str(chart_category_id)+str(gmt_begin)+str(gmt_end))
        #if zz91price_getchartdetailist:
            #return zz91price_getchartdetailist 
        sql='select value from chart_data where name=%s and chart_category_id=%s'
        argument=[name,chart_category_id]
        if gmt_begin and gmt_end:
            argument.append(gmt_begin)
            argument.append(gmt_end)
            sql+=' and gmt_created>=%s and gmt_created<=%s'
        sql+=' order by id desc'
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            listall.append(result[0])
        #设置缓存
        #cache.set("zz91price_getchartdetailist"+str(chart_category_id)+str(name)+str(chart_category_id)+str(gmt_begin)+str(gmt_end),listall,60*5)
        return listall
    def getchartgmtlist(self,title,gmt_begin='',gmt_end=''):
        #获得缓存
        #zz91price_getchartgmtlist=cache.get("zz91price_getchartgmtlist"+str(title)+str(gmt_begin)+str(gmt_end))
        #if zz91price_getchartgmtlist:
            #return zz91price_getchartgmtlist 
        sql='select gmt_date from charts_info where title=%s'
        argument=[title]
        if gmt_begin and gmt_end:
            argument.append(gmt_begin)
            argument.append(gmt_end)
            sql+=' and gmt_created>=%s and gmt_created<=%s'
        sql+=' group by gmt_date order by id desc'
        if not gmt_begin and not gmt_end:
            sql+=' limit 0,7'
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            gmt_date=result[0]
            if gmt_date:
                gmt_date=gmt_date.strftime('%m-%d')
            listall.append(gmt_date)
        if listall:
            listall=listall[::-1]
        #设置缓存
        #cache.set("zz91price_getchartgmtlist"+str(title)+str(gmt_begin)+str(gmt_end),listall,60*3)
        return listall
    def getchartdata(self,chart_info_id):
        #获得缓存
        zz91price_getchartdata=cache.get("zz91price_getchartdata"+str(chart_info_id))
        if zz91price_getchartdata:
            return zz91price_getchartdata 
        sql2='select chart_category_id from chart_data where chart_info_id=%s group by chart_category_id order by id desc'
        resultlist2=self.dbc.fetchalldb(sql2,[chart_info_id])
        listall=[]
        for result2 in resultlist2:
            chart_category_id=result2[0]
            chart_category=self.getchart_category(chart_category_id)
            sql='select value from chart_data where chart_category_id=%s group by TO_DAYS(gmt_created) order by id desc limit 0,30'
            resultlist=self.dbc.fetchalldb(sql,[chart_category_id])
            listall2=[]
            for result in resultlist:
                value=result[0]
                listall2.append(value)
            if listall2:
                listall2=listall2[::-1]
            list={'chart_category':chart_category,'valuelist':listall2}
            listall.append(list)
        #设置缓存
        cache.set("zz91price_getchartdata"+str(chart_info_id),listall,60*3)
        return listall
    def getchart_category(self,id):
        sql='select name from chart_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getdomain_zz91(self,id):
        sql='select domain_zz91 from company where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getcompany_url(self,company_id):
        domain_zz91=self.getdomain_zz91(company_id)
        if domain_zz91:
            company_url="http://"+domain_zz91+".zz91.com"
        else:
            company_url="http://company.zz91.com/compinfo"+str(company_id)+".htm"
        return company_url
        
    def getchartlist(self,title):
        #获得缓存
        #zz91price_getchartlist=cache.get("zz91price_getchartlist"+str(title))
        #if zz91price_getchartlist:
            #return zz91price_getchartlist 
        sql='select id,gmt_date from charts_info where title=%s limit 0,1'
        result=self.dbc.fetchonedb(sql,[title])
        if result:
            id=result[0]
            chartlist=self.getchartdata(id)
#            gmt_date=result[1].strftime('%m-%d')
            #设置缓存
            #cache.set("zz91price_getchartlist"+str(title),chartlist,60*10)
            return chartlist
        
    #----微门户关键词
    def getcplist(self,SPHINXCONFIG,keywords,limitcount):
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC" )
        cl.SetLimits (0,limitcount,limitcount)
        if keywords=='':
            res = cl.Query ('','daohangkeywords')
        else:
            res = cl.Query ('@label '+keywords,'daohangkeywords')
        listall=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    label=attrs['plabel']
                    pingyin=attrs['ppinyin']
                    if pingyin!="":
                        list={'label':label,'pingyin':pingyin}
                        listall.append(list)
        if listall==[]:
            res = cl.Query ('','daohangkeywords')
            if res:
                if res.has_key('matches'):
                    tagslist=res['matches']
                    listall_news=[]
                    for match in tagslist:
                        id=match['id']
                        attrs=match['attrs']
                        label=attrs['plabel']
                        pingyin=attrs['ppinyin']
                        if pingyin!="":
                            list={'label':label,'pingyin':pingyin}
                            listall.append(list)
        return listall
    def getcompanynamecomid(self,company_id):
        sql='select name from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def gettypecodelist(self,category_code):
        #获得缓存
        zz91price_gettypecodelist=cache.get("zz91price_gettypecodelist"+str(category_code))
        if zz91price_gettypecodelist:
            return zz91price_gettypecodelist 
        sql='select title,link from data_index where category_code=%s'
        self.dbc.cursor_comp.execute(sql,[category_code])
        resultlist=self.dbc.cursor_comp.fetchall()
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'title':result[0],'link':result[1],'title_hex':getjiami(result[0])}
                listall.append(list)
        #设置缓存
        cache.set("zz91price_gettypecodelist"+str(category_code),listall,60*10)
        return listall
    def getpricecategory(self,id):
        sql1='select name from price_category where id=%s'
        result1=self.dbc.fetchonedb(sql1,[id])
        if result1:
            return result1[0]
        return ''
    def getpricecategorydetail(self,id):
        sql='select name,pinyin from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        list={'name':'','pinyin':''}
        if result:
            list={'name':result[0],'pinyin':result[1]}
        return list
    def getpricecategorypinyin(self,id):
        sql='select pinyin from price_category where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getpricetable(self,priceid):
        #获得缓存
        zz91price_getpricetable=cache.get("zz91price_getpricetable"+str(priceid))
        if zz91price_getpricetable:
            return zz91price_getpricetable 
        sql='select DISTINCT filed from price_titlefild where priceid=%s'
        resultlist=self.dbc.fetchalldb(sql,[priceid])
        return resultlist
        selectarg=u'id,'
        area=''
        price=''
        price1=''
        qushi=''
        area_numb=None
        price_numb=None
        price1_numb=None
        qushi_numb=None
        numb=0
        for result in resultlist:
            numb+=1
            filed=result[0]
            if filed=='area':
                selectarg+=u'area,'
                area_numb=numb
            elif filed=='price':
                selectarg+=u'price,'
                price_numb=numb
            elif filed=='price1':
                selectarg+=u'price1,'
                price1_numb=numb
            elif filed=='qushi':
                selectarg+=u'qushi,'
                qushi_numb=numb
        selectarg=selectarg[:-1]
        sql2='select '+selectarg+' from price_list where priceid=%s'
        resultlist2=self.dbc.fetchalldb(sql2,[priceid])
        for list2 in resultlist2:
            if area_numb:
                area=list2[area_numb]
            if price_numb:
                price=list2[price_numb]
            if price1_numb:
                price1=list2[price1_numb]
            if qushi_numb:
                qushi=list2[qushi_numb]
            list={'area':area,'price':price,'price1':price1,'qushi':qushi}
            #设置缓存
            cache.set("zz91price_getpricetable"+str(priceid),list,60*10)
            return list
    #新版  选择类别获得最新报价ID
    def getpricesearchlabel(self,kname='',category_id='',assist_id='',gmt_begin=''):
        price=SPHINXCONFIG['name']['price']['name']
        serverid=SPHINXCONFIG['name']['price']['serverid']
        port=SPHINXCONFIG['name']['price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid,port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
        if category_id:
            cl.SetFilter('type_id',[int(category_id)])
        if assist_id:
            cl.SetFilter('assist_type_id',[int(assist_id)])
        if gmt_begin:
            cl.SetFilter('assist_type_id',[int(gmt_begin)])
        cl.SetLimits (0,1,1)
        listall_baojia=[]
        if kname:
            kname=kname.replace('|',' ')
            res = cl.Query ('@(title,tags,search_label) '+kname,price)
        else:
            res = cl.Query ('',price)
        pid=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    pid=match['id']
        return pid
    #----相关最近几天的其他报价时间列表
    def getpricetimelist(self,limitNum='',kname='',category_id='',assist_id='',gmt_begin='',gmt_end='',id=''):
        price=SPHINXCONFIG['name']['price']['name']
        serverid=SPHINXCONFIG['name']['price']['serverid']
        port=SPHINXCONFIG['name']['price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid,port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
        if category_id:
            cl.SetFilter('type_id',category_id)
        if assist_id:
            cl.SetFilter('assist_type_id',assist_id)
        cl.SetFilterRange('gmt_order',gmt_begin,gmt_end)
        cl.SetLimits (0,limitNum,limitNum)
        listall_baojia=[]
        if kname:
            kname=kname.replace('|',' ')
            res = cl.Query ('@(title,tags,search_label) '+kname,price)
        else:
            res = cl.Query ('',price)
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    pid=match['id']
                    url='/detail/'+str(pid)+'.html'
                    attrs=match['attrs']
                    type_id=attrs['type_id']
                    gmt_time=attrs['gmt_time']
                    selecttime=None
                    if (str(id)==str(pid)):
                        selecttime=1
                    list1={'url':url,'id':pid,'gmt_time':gmt_time,'selecttime':selecttime}
                    listall_baojia.append(list1)
        return listall_baojia
    #----报价列表
    def getprlist(self,frompageCount="",limitNum="",maxcount=100000,kname='',category_id='',assist_id='',categoryname='',arg='',gmt_begin='',gmt_end=''):
        price=SPHINXCONFIG['name']['price']['name']
        serverid=SPHINXCONFIG['name']['price']['serverid']
        port=SPHINXCONFIG['name']['price']['port']
        
        cl = SphinxClient()
        cl.SetServer ( serverid,port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
        if category_id:
            cl.SetFilter('type_id',category_id)
        if assist_id:
            cl.SetFilter('assist_type_id',assist_id)
        if arg=='1':
            cl.SetGroupBy( 'type_id',SPH_GROUPBY_ATTR )
        elif arg=='2':
            cl.SetGroupBy( 'assist_type_id',SPH_GROUPBY_ATTR )
        elif arg=='3':
            cl.SetFilterRange('gmt_order',gmt_begin,gmt_end)
        cl.SetLimits (frompageCount,limitNum,maxcount)
        listall_baojia=[]
        listcount_baojia=0
        js=0
        if kname:
            kname=kname.replace('|',' ')
            res = cl.Query ('@(title,tags,search_label) '+kname,price)
        else:
            res = cl.Query ('',price)
        if res:
#            return res
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    td_id=match['id']
                    url='/detail/'+str(td_id)+'.html'
                    attrs=match['attrs']
                    type_id=attrs['type_id']
                    pricetable=self.getpricetable(td_id)
                    pricecategorydetail=self.getpricecategorydetail(type_id)
                    pricecategory=pricecategorydetail['name']
                    pinyin=pricecategorydetail['pinyin']
                    title=attrs['ptitle']
                    ptitle=re.sub('[\d]+月[\d]+日','',title)
                    ptitle=re.sub('价格','',ptitle)
                    ptitle=re.sub('地区','',ptitle)
                    hexptitle=getjiami(ptitle)
                    area=''
                    if kname:
                        area=re.sub(kname.encode('utf-8'),'',ptitle)
                    assist_type_id=attrs['assist_type_id']
                    assist_type=self.getpricecategory(assist_type_id)
                    pinyin2=self.getpriceattrpinyin(assist_type)
                    pcontent=self.getpricecontent(td_id,98)
                    company_numb=0
                    if categoryname:
                        company_numb=self.getpricelist_company_count(ptitle)
#                    title=getlightkeywords(cl,[title],kname,"company_price")
                    gmt_time=attrs['gmt_time']
                    str_time=gmt_time[-5:].replace('-','月')+'日'
                    list1={'td_title':title,'ptitle':ptitle,'hexptitle':hexptitle,'area':area,'fulltitle':title,'td_id':td_id,'td_time':gmt_time,'str_time':str_time,'url':url,'pcontent':pcontent,'pricecategory':pricecategory,'categoryid':type_id,'assist_type_id':assist_type_id,'pinyin':pinyin,'pinyin2':pinyin2,'evennumber':'','assist_type':assist_type,'company_numb':company_numb,'pricetable':pricetable}
                    js=js+1
                    if js%2==0:
                        evennumber=1
                    else:
                        evennumber=0
                    list1['evennumber']=evennumber
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
        return {'list':listall_baojia,'count':listcount_baojia}

#------最新报价信息
    def getpricelist(self,frompageCount='',limitNum='',maxcount=100000,kname='',category_id='',assist_id='',arg=''):
        price=SPHINXCONFIG['name']['price']['name']
        serverid=SPHINXCONFIG['name']['price']['serverid']
        port=SPHINXCONFIG['name']['price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
        if arg==1:
            if category_id:
                cl.SetFilter('type_id',category_id,False)
            if assist_id:
                cl.SetFilter('assist_type_id',assist_id,True)
        else:
            if category_id:
                cl.SetFilter('type_id',category_id)
            if assist_id:
                cl.SetFilter('assist_type_id',assist_id)
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if kname:
            res = cl.Query ('@(title,tags) '+kname+'',price)
        else:
            res = cl.Query ('',price)
        listall_baojia=[]
        listcount_baojia=0
        havelist=None
        js=0
        if res:
#            return res
            if res.has_key('matches'):
                tagslist=res['matches']
                
                for match in tagslist:
                    td_id=match['id']
                    attrs=match['attrs']
                    type_id=attrs['type_id']
                    pricecategory=self.getpricecategory(type_id)
                    title=attrs['ptitle']
                    pcontent=self.getpricecontent(td_id,98)
#                    title=getlightkeywords(cl,[title],kname,"company_price")
                    gmt_time=attrs['gmt_time']
                    list1={'td_title':title,'fulltitle':title,'td_id':td_id,'td_time':gmt_time,'url':'http://jiage.zz91.com/detail/'+str(td_id)+'.html','urlnew':'/detail/'+str(td_id)+'.html','pcontent':pcontent,'pricecategory':pricecategory,'evennumber':''}
                    js=js+1
                    if js%2==0:
                        evennumber=1
                    else:
                        evennumber=0
                    list1['evennumber']=evennumber
                    listall_baojia.append(list1)
                    havelist=listall_baojia
            listcount_baojia=res['total_found']
            """
            if (listcount_baojia==0):
                
                res = cl.Query ('','price')
                if res:
                    if res.has_key('matches'):
                        tagslist=res['matches']
                        for match in tagslist:
                            td_id=match['id']
                            attrs=match['attrs']
                            title=attrs['ptitle']
                            type_id=attrs['type_id']
                            categoryurl=None
                            pricecategory=None
                            pricecategory=self.getpricecategory(type_id)
                            pcontent=self.getpricecontent(td_id,98)
                            title=getlightkeywords(cl,[title],kname,"company_price")
                            gmt_time=attrs['gmt_time']
                            list1={'td_title':title,'fulltitle':title,'td_id':td_id,'td_time':gmt_time,'url':'http://price.zz91.com/priceDetails_'+str(td_id)+'.htm','pcontent':pcontent,'pricecategory':pricecategory,'categoryurl':categoryurl,'evennumber':''}
                            js=js+1
                            if js%2==0:
                                evennumber=1
                            else:
                                evennumber=0
                            list1['evennumber']=evennumber
                            listall_baojia.append(list1)
                    listcount_baojia=0
            """
        return {'list':listall_baojia,'count':listcount_baojia,'havelist':havelist}
    def getpricecontent(self,id,len):
        #获得缓存
        #zz91price_getpricecontent=cache.get("zz91price_getpricecontent"+str(id))
        #if zz91price_getpricecontent:
            #return zz91price_getpricecontent 
        sql='select content from price where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            content=result[0]
            if content:
                #设置缓存
                #cache.set("zz91price_getpricecontent"+str(id)+str(len),filter_tags(content).replace(' ','')[:len]+'......',60*5)
                return filter_tags(content).replace(' ','')[:len]+'......'
            else:
                #设置缓存
                #cache.set("zz91price_getpricecontent"+str(id)+str(len),content,60*5)
                return content
    def getcomppricedetails(self,id,len):
        #获得缓存
        #zz91price_getcomppricedetails=cache.get("zz91price_getcomppricedetails"+str(id)+str(len))
        #if zz91price_getcomppricedetails:
            #return zz91price_getcomppricedetails 
        sql='select details from company_price where id=%s'
        self.dbc.cursor_comp.execute(sql,[id])
        result=self.dbc.cursor_comp.fetchone()
        if result:
            if result[0]:
                #设置缓存
                #cache.set("xxxx"+str(id)+str(len),result[0][:len]+'......',60*5)
                return result[0][:len]+'......'
    def getcomppricecategory(self,id):
        sql='select category_company_price_code from company_price where id=%s'
        self.dbc.cursor_comp.execute(sql,[id])
        result=self.dbc.cursor_comp.fetchone()
        if result:
            type_id=result[0]
            sql1='select label from category_company_price where code =%s'
            self.dbc.cursor_comp.execute(sql1,[type_id])
            result1=self.dbc.cursor_comp.fetchone()
            if result1:
                return {'category':result1[0],'categorycode':type_id}
    #----供应详情2条
    def getproducts_detail(self,product_id):
        #获得缓存
        zz91price_getproducts_detail=cache.get("zz91price_getproducts_detail"+str(product_id))
        if zz91price_getproducts_detail:
            return zz91price_getproducts_detail 
        sql='select quantity,quantity_unit,price,price_unit,refresh_time from products where id=%s'
        result=self.dbc.fetchonedb(sql,[product_id])
        if result:
            price=result[2]
            if price=="" or price==" ":
                price=None
            if price=="0.0" or price=="0":
                price=None
            list={'quantity':result[0],'quantity_unit':result[1],'price':price,'price_unit':result[3],'refresh_time':result[4]}
           #设置缓存
            cache.set("zz91price_getproducts_detail"+str(product_id),list,60*10)
            return list
    #----供求地区详情
    def getproducts_area(self,company_id):
        catelist=cache.get("products_area"+str(company_id))
        if catelist:
            return catelist
        sql='select label from category where code=(select area_code from company where id=%s)'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            list={'source':result[0]}
            cache.set("products_area"+str(company_id),list,60*20)
            return list
    def getpic_address(self,product_id):
        #获得缓存
        zz91price_getpic_address=cache.get("zz91price_getpic_address"+str(product_id))
        if zz91price_getpic_address:
            return zz91price_getpic_address 
        sql='select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc'
        result=self.dbc.fetchonedb(sql,[product_id])
        if result:
            #设置缓存
            cache.set("zz91price_getpic_address"+str(product_id),result[0],60*10)
            return result[0]
        #----供求列表
    def getofferlist(self,kname="",pdt_type="",limitcount="",havepic="",fromlimit=""):
        #-------------供求列表
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
        if (fromlimit):
            cl.SetLimits (fromlimit,limitcount+fromlimit,limitcount+fromlimit)
        else:
            cl.SetLimits (0,limitcount,limitcount,limitcount)
        if (pdt_type!="" and pdt_type!=None):
            cl.SetFilter('pdt_kind',[int(str(pdt_type))])
        if (havepic):
            cl.SetFilterRange('havepic',1,100)
        if (kname=='' or kname==None):
            res = cl.Query ('','offersearch_new_vip')
        else:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        listall_offerlist=[]
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                numb=0
                arg=''
                for match in itemlist:
                    numb=numb+1
                    if numb==1:
                        arg='l'
                    if numb==2:
                        arg='r'
                    pid=match['id']
                    purl='http://trade.zz91.com/productDetails'+str(pid)+'.htm'
                    attrs=match['attrs']
                    company_id=attrs['company_id']
                    parea=self.getproducts_area(company_id)
                    
                    
                    pdt_date=int_to_str(attrs['refresh_time'])
                    short_time=pdt_date[5:]
                    
                    products_detail=self.getproducts_detail(pid)
                    
                    productspic=self.getpic_address(pid)
                    if productspic:
                        pdt_images=productspic
                    else:
                        pdt_images=""
                    if (pdt_images == '' or pdt_images == '0'):
                        pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                    else:
                        pdt_images='http://img3.zz91.com/100x100/'+pdt_images+''
                    pic_address=pdt_images
                    fulltitle=attrs['ptitle']
                    title=subString(fulltitle,40)
                    #title=getlightkeywords(cl,[title],kname,"offersearch_new")
                    
                    list={'id':pid,'url':purl,'title':title,'fulltitle':fulltitle,'gmt_time':pdt_date,'short_time':short_time,'pic_address':pic_address,'products_detail':products_detail,'arg':arg,'parea':parea}
                    listall_offerlist.append(list)
        return listall_offerlist
    def getcompany_price_label(self,code):
        #获得缓存
        zz91price_getcompany_price_label=cache.get("zz91price_getcompany_price_label"+str(code))
        if zz91price_getcompany_price_label:
            return zz91price_getcompany_price_label 
        sql='select label from category_company_price where code=%s'
        result=self.dbc.fetchonedb(sql,code)
        if result:
            #设置缓存
            cache.set("zz91price_getcompany_price_label"+str(code),result[0],60*10)
            return result[0]
    def getnext_category_comprice(self,code):
        #获得缓存
        zz91price_getnext_category_comprice=cache.get("zz91price_getnext_category_comprice"+str(code))
        if zz91price_getnext_category_comprice:
            return zz91price_getnext_category_comprice 
        sql="select label,code from category_company_price where code like %s"'"____"'" order by id asc"
        resultlist=self.dbc.fetchalldb(sql,code)
        listall=[]
        for result in resultlist:
            label=result[0]
            code=result[1]
            list={'label':label,'code':code}
            listall.append(list)
        #设置缓存
        cache.set("zz91price_getnext_category_comprice"+str(code),listall,60*10)
        return listall
        
    #------企业报价
    def getpricelist_company(self,kname='',frompageCount='',limitNum='',maxcount=100000,gmt_begin='',gmt_end='',min_price='',max_price='',company_id=''):
        company_price=SPHINXCONFIG['name']['company_price']['name']
        serverid=SPHINXCONFIG['name']['company_price']['serverid']
        port=SPHINXCONFIG['name']['company_price']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        
        if gmt_begin and gmt_end:
            cl.SetFilterRange('refresh_time',gmt_begin,gmt_end)
        if max_price:
            cl.SetFilterRange('minPrice',min_price,max_price)
        if company_id:
            cl.SetFilter('company_id',[company_id])
#            cl.SetFilterRange('max_price',min_price,max_price)
#            cl.SetFilterRange('price_unit',min_price,max_price)
        cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if kname:
            res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'',company_price)
        else:
            res = cl.Query ('',company_price)
        listall_baojia=[]
        listcount_baojia=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    td_id=match['id']
                    curl='/cdetail/'+str(td_id)+'.html'
                    pcontent=""
                    pcontent=self.getcomppricedetails(td_id,108)
                    pricecategoryall=self.getcomppricecategory(td_id)
                    if pricecategoryall:
                        pricecategory=pricecategoryall['category']
                        categorycode=pricecategoryall['categorycode']
                    else:
                        pricecategory=0
                        categorycode=0
                    attrs=match['attrs']
                    fulltitle=attrs['ptitle']
                    company_id=attrs['company_id']
                    companyname=self.getcompanynamecomid(company_id)
                    province=attrs['province']
                    city=attrs['city']
                    title=subString(fulltitle,60)
                    hextitle=getjiami(title)
#                    title=getlightkeywords(cl,[title],kname,"company_price")
                    gmt_time=attrs['prefresh_time']
                    price_unit=attrs['price_unit']
                    min_price=attrs['min_price']
                    max_price=attrs['max_price']
                    price=""
                    if (min_price!="" and min_price!="none" and min_price!="0.0"):
                        if (max_price!="" and max_price!="none" and max_price!="0.0"):
                            price=min_price+"-"+max_price+price_unit
                        else:
                            price=min_price+price_unit
                            
                    company_numb=''
#                    company_numb=self.getpricelist_company_count(title)
                    #td_time=gmt_time.strftime('%Y-%m-%d')
                    companyurl=''
                    domain_zz91=self.getdomain_zz91(company_id)
                    if domain_zz91:
                        companyurl="http://"+domain_zz91+".zz91.com"
                    else:
                        companyurl="http://company.zz91.com/compinfo"+str(company_id)+".htm"
                    list1={'td_title':title,'hextitle':hextitle,'province':province,'city':city,'company_numb':company_numb,'categorycode':categorycode,'companyurl':companyurl,'companyname':companyname,'company_id':company_id,'fulltitle':fulltitle,'td_id':td_id,'td_time':gmt_time,'price':price,'curl':curl,'url':'http://jiage.zz91.com/cdetail/'+str(td_id)+'.html','pcontent':pcontent,'pricecategory':pricecategory}
                    listall_baojia.append(list1)
            listcount_baojia=res['total_found']
        return {'list':listall_baojia,'count':listcount_baojia}
    #----最终页price_list数据
    def getdetailpricelist(self,priceid,listfield,fromdata="",todate=""):
        #获得缓存
        #zz91price_getdetailpricelist=cache.get("zz91price_getdetailpricelist"+str(priceid)+str(listfield))
        #if zz91price_getdetailpricelist:
            #return zz91price_getdetailpricelist 
        listall=[]
        if len(listfield)>1:
            listfield2=','.join(listfield)
            sqlarg='id,postdate,label,label1,spec,type_id,assist_type_id,'+listfield2
            sql2='select '+sqlarg+' from price_list where priceid=%s'
            if fromdata:
                sql2+=' and postdate>=%s'
            if todate:
                sql2+=' and postdate<=%s'
            sql2+=' group by num'
            resultlist2=self.dbc.fetchalldb(sql2,[priceid])
            for result2 in resultlist2:
                id=result2[0]
                postdate=formattime(result2[1],1)
                label=result2[2]
                label1=result2[3]
                spec=result2[4]
                if spec:
                    spec=spec.replace("　","")
                type_id=result2[5]
                assist_type_id=result2[6]
                listvalue=[]
                list={}
                num=6
                curl='/chart/'+str(id)+'.html'
                for ltfied in listfield:
                    num+=1
                    
                    fidvalue=result2[num]
                    proname=label
                    #废铜
                    if type_id in [40]:
                        if ltfied=="label":
                            proname=fidvalue
                            if spec:
                                fidvalue=result2[num]+"("+str(spec)+")"
                                proname=fidvalue
                    if not fidvalue:
                        fidvalue=""
                    listvalue.append(fidvalue)
                company_numb=0
                if not label:
                    label=label1
                hexptitle=""
                if label:
                    #company_numb=self.getpricelist_company_count(label)
                    hexptitle=getjiami(label)
                list2={'id':id,'postdate':postdate,'curl':curl,'hexptitle':hexptitle,'listvalue':listvalue,'proname':proname}
                listall.append(list2)
        #设置缓存
        #cache.set("zz91price_getdetailpricelist"+str(priceid)+str(listfield),listall,60*10)
        return listall
    #----列表页price_list数据
    def getprice_list(self,keywords='',frompageCount='',limitNum='',timedate='',gmt_begin='',gmt_end='',area='',group='',listfiled=[],attrbute='',maxcount=50000,categoryid=""):
        
    
        keywords=re.sub('\/.*',' ',keywords)
        keywords=re.sub('\(',' ',keywords)
        keywords=re.sub('\)',' ',keywords)
        keywords=re.sub(',',' ',keywords)
        keywords=re.sub('%',' ',keywords)
        keywords=re.sub('-',' ',keywords)
        pricelist=SPHINXCONFIG['name']['pricelist']['name']
        serverid=SPHINXCONFIG['name']['pricelist']['serverid']
        port=SPHINXCONFIG['name']['pricelist']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if group:
            cl.SetGroupBy(group,SPH_GROUPBY_ATTR )
        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'postdate' )
#        if priceid:
#            cl.SetFilter('priceid',[priceid])
        if timedate:
            cl.SetFilter('postdate',[timedate])
        if categoryid:
            cl.SetFilter('type_id',[categoryid])
        if gmt_begin and gmt_end:
            if gmt_begin!="" and gmt_end!="":
                cl.SetFilterRange('postdate',gmt_begin,gmt_end)
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if attrbute:
            res = cl.Query ('@(label,label1,spec,spec1,spec2) '+attrbute,pricelist)
        else:
            keyww=''
            if area:
                if area in ['浙江地区','上海地区','江苏地区']:
                    keyww+='@(typename,title,label,label1,label1,area,area1,area2,spec,spec1,spec2) '+area
                else:
                    keyww+='@(title,label,label1,label1,area,area1,area2,spec,spec1,spec2) '+area
            if keywords:
                #keyww+=' @(typename,title,label,label1,spec,spec1,spec2) '+keywords
                keyww+=' '+keywords
            if keyww:
                res = cl.Query (keyww,pricelist)
            else:       
                res = cl.Query ('',pricelist)
        listall=[]
        listchart=[]
        count=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                js=0
                sql='select label,label1,area,title,priceid,postdate,type_id,assist_type_id,price,price1,price2,qushi from price_list where id=%s'
                for match in tagslist:
                    id=match['id']
                    if not area:
                        area=""
                    curl='/chart/'+str(id)+'.html?area='+area
                    
                    result=self.dbc.fetchonedb(sql,[id])
                    if result:
                        label=result[0]
                        label1=result[1]
                        parea=result[2]
                        title=result[3]
                        priceid=result[4]
                        postdate=result[5]
                        type_id=result[6]
                        assist_type_id=result[7]
                        postdate=formattime(postdate,1)
    #                    attrs=match['attrs']
    #                    parea=attrs['parea']
    #                    curl2=''
    #                    if parea in ['浙江地区','上海地区','江苏地区']:
    #                        curl2='/chart/'+str(id)+'.html?area='+parea
    #                    title=attrs['ptitle']
    #                    priceid=attrs['priceid']
                        purl='/detail/'+str(priceid)+'.html'
    #                    postdate=attrs['postdate']
    #                    label=attrs['plabel']
#                        if not label:
#                            label=attrs['plabel1']
                        if not label:
                            label=label1
                        if not label:
                            label=re.sub('.*?日','',title)
                        hexptitle=getjiami(label)
                        company_numb=0
                        if label:
                            company_numb=self.getpricelist_company_count(label)
                        
                        if type_id==41 and assist_type_id==180:
                            price=result[8]
                            if '-' in price:
                                pricelist=price.split('-')
                                price=pricelist[0]
                                price1=pricelist[1]
                                price2=(int(price1)+int(price))/2
                            else:
                                price1=result[9]
                                price2=result[10]
                            qushi=result[11]
                            listvalue=[label,price,price1,price2,qushi]
                        else:
                            listvalue=[]
                            if len(listfiled)>1:
                                listfield2=','.join(listfiled)
    #                            sqlarg='id,postdate,label,label1,'+listfield2
                                sql2='select spec,type_id,'+listfield2+' from price_list where id=%s'
                                result2=self.dbc.fetchonedb(sql2,[id])
                                if result2:
    #                                id=result2[0]
    #                                postdate=formattime(result2[1],1)
    #                                label=result2[2]
    #                                label1=result2[3]
    #                                list={}
    #                                num=3
                                    spec=result2[0]
                                    num=2
                                    type_id=result2[1]
    #                                curl='/chart/'+str(id)+'.html'
                                    for ltfied in listfiled:
                                        fidvalue=result2[num]
                                        #废铜
                                        if type_id in [40]:
                                            if ltfied=="label":
                                                if spec:
                                                    fidvalue=result2[num]+"("+str(spec)+")"
                                        if not fidvalue:
                                            fidvalue=""
                                        listvalue.append(fidvalue)
                                        num+=1
                        '''
                        for ltfied in listfiled:
                            if isfield(ltfied):
                                nowfield=attrs['p'+ltfied].upper()
                                if nowfield in ['浙江地区','上海地区','江苏地区']:
                                    nowfield='<a href="'+curl2+'" target="_blank">'+nowfield+'</a>'
                                else:
                                    nowfield='<a href="'+curl+'" target="_blank">'+nowfield+'</a>'
                                listvalue.append(nowfield)'''
                        list={'id':id,'title':title,'priceid':priceid,'postdate':postdate,'postdate2':postdate,'purl':purl,'curl':curl,'aveprice':'','hexptitle':hexptitle,'company_numb':company_numb,'listvalue':listvalue}
                        listall.append(list)
                count=res['total_found']
        return {'list':listall,'count':count}
#----走势图数据
    def getchartpricelist(self,keywords='',frompageCount='',limitNum=30,timedate='',gmt_begin='',gmt_end='',area='',group='',attrbute='',maxcount=30,categoryid=""):
       
    
        keywords=re.sub('\/.*',' ',keywords)
        keywords=re.sub('\(',' ',keywords)
        keywords=re.sub('\)',' ',keywords)
        keywords=re.sub(',',' ',keywords)
        keywords=re.sub('%',' ',keywords)
        keywords=re.sub('-',' ',keywords)
        pricelist=SPHINXCONFIG['name']['pricelist']['name']
        serverid=SPHINXCONFIG['name']['pricelist']['serverid']
        port=SPHINXCONFIG['name']['pricelist']['port']
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if group:
            cl.SetGroupBy(group,SPH_GROUPBY_ATTR )
        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'postdate' )
        if timedate:
            cl.SetFilter('postdate',[timedate])
        if categoryid:
            cl.SetFilter('type_id',[categoryid])
        if gmt_begin and gmt_end:
            if gmt_begin!="" and gmt_end!="":
                cl.SetFilterRange('postdate',gmt_begin,gmt_end)
                limitNum=maxcount=500
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if attrbute:
            res = cl.Query ('@(label,label1,spec,spec1,spec2) '+attrbute,pricelist)
        else:
            keyww=''
            if area:
                keyww+='@(title,typename,label,label1,label1,area,area1,area2,spec,spec1,spec2) '+area
            if keywords:
                #keyww+=' @(typename,title,label,label1,spec,spec1,spec2) '+keywords
                keyww+=' '+keywords
            if keyww:
                res = cl.Query (keyww,pricelist)
            else:       
                res = cl.Query ('',pricelist)
        listchart=[]
        count=0
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                js=0
                maxprice=0
                minprice=0
                sql='select label,label1,area,title,priceid,postdate,price,price1 from price_list where id=%s'
                for match in tagslist:
                    id=match['id']
                    if not area:
                        area=""
                    curl='/chart/'+str(id)+'.html?area='+area
                    
                    result=self.dbc.fetchonedb(sql,[id])
                    if result:
                        label=result[0]
                        label1=result[1]
                        parea=result[2]
                        title=result[3]
                        priceid=result[4]
                        postdate=result[5]
                        price=result[6]
                        if not price:
                            price=''
                        price1=result[7]
                        if not price1:
                            price1=''
                        if not price and not price1:
                            continue
                        postdate=formattime(postdate,1)
                    
    #                    attrs=match['attrs']
    #                    title=attrs['ptitle']
    #                    priceid=attrs['priceid']
                        purl='/detail/'+str(priceid)+'.html'
    #                    postdate=attrs['postdate']
    #                    label=attrs['plabel']
    #                    if not label:
    #                        label=attrs['plabel1']
                        if not label:
                            label=label1
                        if not label:
                            label=re.sub('.*?日','',title)
                        
    #                    price=attrs['pprice']
                        if '元' in price:
                            price11=re.findall('[\d]+',price)
                            if price11:
                                price=price11[0]
    #                    list['price']=price
    #                    price1=attrs['pprice1']
                        if '跌' in price1:
                            price1=price1.split('跌')[0]
                        elif '涨' in price1:
                            price1=price1.split('涨')[0]
                        elif '-' in price1:
                            price1=price1.split('-')[0]
                        lowprice=''
                        heiprice=''
                        splitarg=''
                        if '-' in price:
                            splitarg='-'
                        elif '/' in price:
                            splitarg='/'
                        if splitarg:
                            prilh=price.split(splitarg)
                            lowprice=prilh[0]
                            if lowprice.isdigit()==False:
                                lowprice=re.findall('[\d]+',lowprice)
                                if lowprice:
                                    lowprice=int(lowprice[0])
                                else:
                                    lowprice=0
                            else:
                                lowprice=int(lowprice)
    #                        list['lowprice']=lowprice
                            heiprice=prilh[1]
                            if heiprice.isdigit()==False:
                                heiprice=re.findall('[\d]+',heiprice)
                                if heiprice:
                                    heiprice=int(heiprice[0])
                                else:
                                    heiprice=0
                            else:
                                heiprice=int(heiprice)
    #                        list['heiprice']=heiprice
                        aveprice=0
                        if lowprice and heiprice:
                            aveprice=(lowprice+heiprice)/2
    #                        list['aveprice']=aveprice
#                            listchart.append(list)
                        else:
                            if not price1:
                                price1=price
                            if price.isdigit()==True and price1.isdigit()==True:
                                lowprice=int(price)
                                heiprice=int(price1)
                                aveprice=(lowprice+heiprice)/2
    #                            list['aveprice']=aveprice
                        
                        list={'posttime':str_to_int(postdate),'postdate2':postdate,'aveprice':aveprice}
                        listchart.append(list)
                count=res['total_found']
        return listchart
    
    def getareapricelist(self,keywords='',frompageCount='',limitNum='',arealist='',gmt_begin='',gmt_end=''):
       
        listall2=[]
        pricelist=SPHINXCONFIG['name']['pricelist']['name']
        serverid=SPHINXCONFIG['name']['pricelist']['serverid']
        port=SPHINXCONFIG['name']['pricelist']['port']
        for area in arealist:
            cl = SphinxClient()
            cl.SetServer ( serverid, port )
            cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
            if gmt_begin and gmt_end:
                cl.SetFilterRange('postdate',gmt_begin,gmt_end)
            cl.SetLimits (frompageCount,limitNum,limitNum)
            if area:
                res = cl.Query ('@(area,area1,area2) '+area,pricelist)
            else:
                res = cl.Query ('',pricelist)
            listall=[]
            count=0
            if res:
                if res.has_key('matches'):
                    tagslist=res['matches']
                    for match in tagslist:
                        attrs=match['attrs']
                        title=attrs['ptitle']
                        label=attrs['plabel']
                        if not label:
                            label=attrs['plabel1']
                        priceid=attrs['priceid']
                        price=attrs['price']
                        price2=attrs['pprice2']
                        area=attrs['parea']
                        spec=attrs['spec']
                        spec1=attrs['spec1']
                        postdate=attrs['postdate']
                        othertext=attrs['othertext']
                        list={'title':title,'label':label,'priceid':priceid,'price':'','area':area,'spec':spec,'spec1':spec1,'postdate':int_to_str(postdate),'othertext':othertext}
                        price=price.split('-')[0]
                        price=filter(str.isdigit,price)
                        if price:
                            list['price']=price
                            listall.append(list)
            list2={'list':listall,'area':area}
            listall2.append(list2)
        return listall2

    #企业报价条数
    def getpricelist_company_count(self,kname):
        company_price=SPHINXCONFIG['name']['company_price']['name']
        serverid=SPHINXCONFIG['name']['company_price']['serverid']
        port=SPHINXCONFIG['name']['company_price']['port']
        
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
        cl.SetLimits (0,1,1)
        try:
            res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'',company_price)
            if res:
                return res['total_found']
            return 0
        except:
            return 0

    def getarealist(self,keywords='',frompageCount='',limitNum='',area='',group='',maxcount=100):
        
        cl = SphinxClient()
        pricelist=SPHINXCONFIG['name']['pricelist']['name']
        serverid=SPHINXCONFIG['name']['pricelist']['serverid']
        port=SPHINXCONFIG['name']['pricelist']['port']
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if group:
            cl.SetGroupBy(group,SPH_GROUPBY_ATTR )
        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'postdate' )
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if area:
            if keywords:
                res = cl.Query ('@(title,area,area1,area2,typename,title,label,label1,spec,spec1,spec2) '+area+' '+keywords,pricelist)
            else:
                res = cl.Query ('@(title,area,area1,area2) '+area,pricelist)
        else:
            if keywords:
                res = cl.Query ('@(typename,title,label,label1,spec,spec1,spec2) '+keywords,pricelist)
            else:
                res = cl.Query ('',pricelist)
        listall=[]
        if res:
#            return res
            numb=0
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    attrs=match['attrs']
                    area=attrs['parea']
#                    if area and not '-' in area and
                    larea=len(area.decode('utf-8'))
                    if larea<8 and larea>1:
                        numb=numb+1
                        pinyin=self.getpriceattrpinyin(area)
                        list={'label':area,'pinyin':pinyin,'numb':numb}
                        listall.append(list)
        return listall

    def getbbslist(self,kname='',limitcount='',gmt_begin='',gmt_end='',arg=1):
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if gmt_begin and gmt_end:
            cl.SetFilterRange('post_time',gmt_begin,gmt_end)
        #cl.SetSortMode( SPH_SORT_ATTR_DESC,"visited_count" )
        cl.SetSortMode( SPH_SORT_EXTENDED,"reply_time desc,post_time desc" )
        cl.SetLimits (0,limitcount,limitcount)
        if kname:
            res = cl.Query ('@(title,tags) '+kname,'huzhu')
        else:
            res = cl.Query ('','huzhu')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                for match in tagslist:
                    id=match['id']
                    url='http://huzhu.zz91.com/viewReply'+str(id)+'.htm'
                    attrs=match['attrs']
                    title=attrs['ptitle']
                    visited_count=attrs['visited_count']
                    gmt_time=attrs['ppost_time']
                    list1={'title':title,'id':id,'url':url,'gmt_time':gmt_time}
                    if arg==1:
                        if not '我画你猜' in title:
                            listall_news.append(list1)
                    else:
                        listall_news.append(list1)
                return listall_news

        #---公司库首页有图片的最新供求列表
    def getindexofferlist_pic(self,SPHINXCONFIG,kname="",pdt_type="",limitcount="",membertype=""):
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
        
        cl.SetLimits (0,limitcount,limitcount)
        if (pdt_type!=None and pdt_type!=""):
            cl.SetFilter('pdt_kind',[int(pdt_type)])
        cl.SetFilterRange('havepic',1,100)
        cl.SetFilterRange('haveprice',2,1000)
        if membertype:
            searchindex="offersearch_new_vip"
            cl.SetFilterRange('length_price',1,100000)
        else:
            searchindex="offersearch_new,offersearch_new_vip"
        if (kname==None):
            res = cl.Query ('',searchindex)
        else:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,searchindex)
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                listall_offerlist=[]
                for match in itemlist:
                    pid=match['id']
                    price=self.getofferprice(pid)
                    attrs=match['attrs']
                    pdt_date=attrs['pdt_date']
                    pdt_kind=attrs['pdt_kind']
                    kindtxt=''
                    if (pdt_kind=='1'):
                        kindtxt="供应"
                    else:
                        kindtxt="求购"
                    title=subString(attrs['ptitle'],40)
                    sql1="select pic_address from products_pic where product_id=%s order by is_default desc,id desc"
                    self.dbc.cursor_comp.execute(sql1,[pid])
                    productspic = self.dbc.cursor_comp.fetchone()
                    if productspic:
                        pdt_images=productspic[0]
                    else:
                        pdt_images=""
                    if (pdt_images == '' or pdt_images == '0'):
                        pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
                    else:
                        pdt_images='http://pyapp.zz91.com/img/120x120/img1.zz91.com/'+pdt_images+''
                    list={'id':pid,'title':title,'gmt_time':pdt_date,'kindtxt':kindtxt,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images,'price':price}
                    listall_offerlist.append(list)
                return listall_offerlist
    def getofferprice(self,id):
        #获得缓存
        zz91price_getofferprice=cache.get("zz91price_getofferprice"+str(id))
        if zz91price_getofferprice:
            return zz91price_getofferprice 
        sql="select p.min_price,p.max_price,p.price_unit from products as p where p.id=%s"
        self.dbc.cursor_comp.execute(sql,[id])
        plist = self.dbc.cursor_comp.fetchone()
        if plist:
            #价格范围判断
            allprice=""
            min_price=plist[0]
            if (min_price==None):
                min_price=''
            else:
                min_price=str(min_price)
                if (min_price!='0.0'):
                    allprice=allprice+min_price
            max_price=plist[1]
            if (max_price==None):
                max_price=''
            else:
                max_price=str(max_price)
                if (max_price!='0.0' and max_price!=min_price):
                    allprice=allprice+'-'+max_price
            price_unit=plist[2]
            #
            if (price_unit==None):
                price_unit=''
            else:
                if (allprice!=''):
                    allprice=allprice+price_unit
            if (allprice==""):
                allprice="电议或面议"
            #设置缓存
            cache.set("zz91price_getofferprice"+str(id),allprice,60*10)
            return allprice

    def getviptype(self,company_id):
        sql='select membership_code,domain_zz91 from company where id=%s'
        self.dbc.cursor_comp.execute(sql,[company_id])
        result=self.dbc.cursor_comp.fetchone()
        if result:
            viptype=result[0]
            domain_zz91=result[1]
            if domain_zz91:
                domain_zz91='http://'+domain_zz91+'.zz91.com/'
            else:
                domain_zz91='http://company.zz91.com/compinfo'+str(company_id)+'.htm'
            arrviptype={'vippic':'','vipname':'','isweixin':'','zstNum':'','compurl':'','domain_zz91':domain_zz91}
            if (viptype == '10051000'):
                arrviptype['vippic']=None
                arrviptype['vipname']='普通会员'
            if (viptype == '10051001'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/recycle.gif'
                arrviptype['vipname']='再生通'
            if (viptype == '100510021000'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/pptSilver.gif'
                arrviptype['vipname']='银牌品牌通'
            if (viptype == '100510021001'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/pptGold.gif'
                arrviptype['vipname']='金牌品牌通'
            if (viptype == '100510021002'):
                arrviptype['vippic']='http://img.zz91.com/zz91images/pptDiamond.gif'
                arrviptype['vipname']='钻石品牌通'
            if (viptype == '10051000'):
                arrviptype['vipcheck']=None
            else:
                arrviptype['vipcheck']=1
            
            compurl=self.getcompurl(company_id)
            arrviptype['compurl']=compurl
            
            sqld="select qq,account from company_account where company_id=%s"
            self.dbc.cursor_comp.execute(sqld,[company_id])
            compqq = self.dbc.cursor_comp.fetchone()
            if compqq:
                qq=compqq[0]
                if qq:
                    qq=qq.strip()
                if (qq==""):
                    qq=None
                if (qq):
                    arrviptype['qq']=qq
                account=compqq[1]
                bindweixin=self.isbindweixin(account)
                if bindweixin:
                    arrviptype['isweixin']=1
                
            #年限
            sql2="select sum(zst_year) from crm_company_service where company_id="+str(company_id)+" and apply_status=1"
            self.dbc.cursor_comp.execute(sql2)
            zstNumvalue = self.dbc.cursor_comp.fetchone()
            if zstNumvalue:
                zst_year=zstNumvalue[0]
            arrviptype['zstNum']=zst_year
            return arrviptype
    #----是否绑定微信
    def isbindweixin(self,account):
        sql="select id from oauth_access where target_account=%s and open_type='weixin.qq.com'"
        self.dbc.cursor_comp.execute(sql,[account]);
        plist=self.dbc.cursor_comp.fetchone()
        if plist:
            return 1
        else:
            return None
    def getcompanyname_byid(self,company_id):
        sql='select name from company where id=%s'
        self.dbc.cursor_comp.execute(sql,[company_id])
        result=self.dbc.cursor_comp.fetchone()
        if result:
            return result[0]
    def getpic_address(self,product_id):
        sql='select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc'
        self.dbc.cursor_comp.execute(sql,[product_id])
        ldbresult=self.dbc.cursor_comp.fetchone()
        if ldbresult:
            return ldbresult[0]
    def getcompurl(self,id):
        sql='select domain_zz91 from company where id=%s'
        self.dbc.cursor_comp.execute(sql,[id])
        result=self.dbc.cursor_comp.fetchone()
        if result:
            return result[0]
    def getoffertype(self,kname="",pdt_type="",limitcount="",havepic="",fromlimit=""):
        #-------------供求类型
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
        if (fromlimit):
            cl.SetLimits (fromlimit,limitcount+fromlimit,limitcount+fromlimit)
        else:
            cl.SetLimits (0,limitcount,limitcount)
        if (pdt_type!="" and pdt_type!=None):
            cl.SetFilter('pdt_kind',[int(str(pdt_type))])
        if (havepic):
            cl.SetFilterRange('havepic',1,100)
        if (kname=='' or kname==None):
            res = cl.Query ('','offersearch_new_vip')
        else:
            res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                for match in itemlist:
                    pid=match['id']
                    offertype_code=self.getoffermain_code(pid)
                    return offertype_code
    def getoffermain_code(self,id):
        sql='select category_products_main_code from products where id=%s'
        self.dbc.cursor_comp.execute(sql,[id])
        result=self.dbc.cursor_comp.fetchone()
        if result:
            return result[0][:4]
    #相关供求类别
    def getcategorylist(self,SPHINXCONFIG,kname='',limitcount=''):
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_ANY )
        #cl.SetSortMode( SPH_SORT_EXTENDED,"sort desc" )
        if (limitcount!=''):
            cl.SetLimits (0,limitcount,limitcount)
        if (kname!=""):
            res = cl.Query (''+kname,'category_products')
        else:
            res = cl.Query ('','category_products')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    label=attrs['plabel']
                    code=attrs['pcode']
                    list1={'id':id,'code':code,'label':label,'label_hex':label.encode("hex")}
                    listall.append(list1)
                return listall
    def getproductstags(self,proid):
        #获得缓存
        zz91price_getproductstags=cache.get("zz91price_getproductstags"+str(proid))
        if zz91price_getproductstags:
            return zz91price_getproductstags 
        sql="select tags from products where id=%s"
        resultlist=self.dbc.fetchonedb(sql,[proid])
        if resultlist:
            tags=resultlist[0]
            if tags:
                tagslist=tags.split(",")
                list=[]
                for i in tagslist:
                    l={'label':i,'label_hex':getjiami(i)}
                    list.append(l)
                #设置缓存
                cache.set("zz91price_getproductstags"+str(proid),list,60*10)
                return list
    def getpricedatalist(self,id):
        catelist=cache.get("price_datalist"+str(id))
        if catelist:
            return catelist
        sql='select product_name,quote,area,company_name,company_id from price_data where price_id=%s'
        resultlist=self.dbc.fetchalldb(sql,[id])
        listall=[]
        for result in resultlist:
            company_id=result[4]
            domain_zz91=self.getdomain_zz91(company_id)
            if domain_zz91:
                company_url="http://"+domain_zz91+".zz91.com"
            else:
                company_url="http://company.zz91.com/compinfo"+str(company_id)+".htm"
            list={'product_name':result[0],'area':result[2],'quote':result[1],'company_name':result[3],'company_id':company_id,'company_url':company_url}
            listall.append(list)
        if listall:
            cache.set("price_datalist"+str(id),listall,60*20)
        return listall
    #----获得网上报价
    def getnetpricelist(self,keywords='',categoryid='',frompageCount='',limitNum='',gmt_begin='',gmt_end='',area='',maxcount=100000):
        
        price_data=SPHINXCONFIG['name']['price_data']['name']
        serverid=SPHINXCONFIG['name']['price_data']['serverid']
        port=SPHINXCONFIG['name']['price_data']['port']
        
        cl = SphinxClient()
        cl.SetServer ( serverid, port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
#        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'id' )
        cl.SetSortMode( SPH_SORT_EXTENDED," id desc" )
#        if group:
#            cl.SetGroupBy(group,SPH_GROUPBY_ATTR )
        if categoryid:
            cl.SetFilter('type_id',[categoryid])
        if gmt_begin and gmt_end:
            cl.SetFilterRange('pgmt_created',gmt_begin,gmt_end)
        cl.SetLimits (frompageCount,limitNum,maxcount)
        if area:
            if keywords:
                res = cl.Query ('@(area,product_name,label,label1,label2) '+area+' '+keywords,price_data)
            else:
                res = cl.Query ('@(area) '+area,price_data)
        else:
            if keywords:
                res = cl.Query ('@(product_name,label,label1,label2) '+keywords,price_data)
            else:
                res = cl.Query ('',price_data)
        listall=[]
        count=0
        if res:
#            return res
            if res.has_key('matches'):
                tagslist=res['matches']
                js=0
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    price_id=attrs['pprice_id']
#                    type_id=attrs['ptype_id']
                    company_name=attrs['pcompany_name']
                    gmt_created=int_to_str(attrs['pgmt_created'])
                    product_name=attrs['pproduct_name']
                    area=attrs['parea']
                    quote=attrs['pquote']
                    company_id=attrs['pcompany_id']
                    company_url='http://company.zz91.com/compinfo.htm?id='+str(id)
                    list={'id':id,'price_id':price_id,'company_name':company_name,'gmt_created':gmt_created,'product_name':product_name,'area':area,'quote':quote,'company_id':company_id,'company_url':company_url}
                    listall.append(list)
                count=res['total_found']
        return {'list':listall,'count':count}
    #产业带
    def getmarketlist(self,keywords=None):
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        #cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
        cl.SetLimits (0,10,10)
        if keywords:
            res = cl.Query ('@(name,area,industry,business,category,introduction,address) '+keywords,'market')
        else:
            res = cl.Query (' ','market')
        listall=[]
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall_news=[]
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    company_num=attrs['company_num']
                    product_num=attrs['product_num']
                    pname=attrs['pname']
                    words=attrs['words']
                    list={'id':id,'name':pname,'company_num':company_num,'product_num':product_num,'words':words}
                    listall.append(list)
        return listall
