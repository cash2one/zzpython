def showcommadscript(request):
    code = request.GET.get("code")
    adnum=getadnum(code)
    adlist=getadlistnew(code)
    return render_to_response('scripth.html',locals())
    
def showadscript(request):
    code = request.GET.get("code")
    type = request.GET.get("type")
    position=[1]
    if (type=="index1"):
        position=[1,2,3,4,5,6,7]
        picaddress="http://pyapp.zz91.com/images/noad1.jpg"
    if (type=="index2"):
        position=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
        picaddress="http://pyapp.zz91.com/images/noad.jpg"

        
    adlist=[]
    for a in position:
        list=getadlist(code,str(a))
        if (list==None):
            list={'url':'http://www.zz91.com/zst/','picaddress':'http://pyapp.zz91.com/images/noad.jpg'}
        adlist.append(list)
    return render_to_response('script.html',locals())
def showcompanyadscript(request):
    code = request.GET.get("code")
    position="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20"
    adlist=[]
    for a in position.split(","):
        list=getadlist(code,a)
        if (list==None):
            list={'url':'http://www.zz91.com/zst/','picaddress':'http://pyapp.zz91.com/images/noadc.jpg'}
        adlist.append(list)
    return render_to_response('scriptc.html',locals())
    
#环保网首页广告图片
def showhuanbaoindexpic(request):
    url = 'http://img1.zz91.com/ads/1377964800000/f53cb9e8-8fc5-4bf1-ae3b-468f5f814da0.gif'
    
    
    astr1="<div class='m3-content-box'>"
    
    code = request.GET.get("code")
    position="1,2,3,4,5,6,7,8,9,10"
    adlist=[]
    i=1
    for a in position.split(","):
        list=getadlist(code,a)
        
        if (list):
            url=list["url"]
            purl=list['picaddress']
            iheight=getpicturewh(purl)['height']
            astr1=astr1+"<div class='m3-box-one'><a href='"+url+"' target=_blank><img src='"+purl+"'></a></div>"
            
            if (iheight>=280 or i>2):
                astr1=astr1+"</div><div class='m3-content-box'>"
                i=1
            i=i+1
    astr1=astr1+"</div>"
    #print im.format, im.size, im.mode
    return render_to_response('script_showhuanbaoindexpic.html',locals())
    #
#来电宝客户全网推广
def getppccomplist(m,keywords,page,adposition=''):
    
    if page==None:
        page=1
    port = spconfig['port']
    cl = SphinxClient()
    cl.SetServer ( spconfig['serverid'], port )
    cl.SetLimits ((page-1)*m,m,200)
    if (keywords):
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR,"ordt desc, refresh_time desc")
        cl.SetSelect("*,max(sort) AS ordt")
        cl.SetSortMode( SPH_SORT_EXTENDED,"ordt desc, refresh_time desc" )
        
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
    else:
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR,"ordt desc, refresh_time desc")
        cl.SetSelect("*,max(sort) AS ordt")
        cl.SetSortMode( SPH_SORT_EXTENDED,"ordt desc, refresh_time desc" )
        res = cl.Query ('','offersearch_ppc')
    listall=[]
    if res:
        listcount=res['total_found']
    else:
        listcount=0
    lastpage=int(ceil(float(listcount) / int(m)))
    if (listcount==0):
        cl.SetMatchMode ( SPH_MATCH_ANY )
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
        cl.SetLimits ((page-1)*m,m,200)
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                company_id=attrs['company_id']
                ptitle=attrs['ptitle']
                ppckeywords1=attrs['ppckeywords']
                ppckeywords=subString(ppckeywords1,50)
                companyname=attrs['companyname']
                front_tel=attrs['front_tel']
                front_tel=front_tel.replace("转分机","转")
                pdt_kind=attrs['pdt_kind']
                pdttxt=""
                if (str(pdt_kind)=="0"):
                    pdttxt="供应"
                if (str(pdt_kind)=="1"):
                    pdttxt="求购"
                #----联系人信息
                saveshowppc(company_id,adposition)
                contact=None
                sqlp="select contact,sex from company_account where company_id=%s"
                companyaccount=dbc.fetchonedb(sqlp,[company_id])
                if companyaccount:
                    contact=companyaccount[0]
                    
                    sex=companyaccount[1]
                    sex=""
                    if str(sex)=="0":
                        sex="先生"
                    if str(sex)=="1":
                        sex="女士"
                    if "先生" in contact or "女士" in contact:
                        contact=contact
                    else:
                        contact=contact+sex
                sql1="select pic_address from products_pic where product_id=%s order by is_default desc,id desc"
                productspic=dbc.fetchonedb(sql1,id)
                if productspic:
                    pdt_images=productspic[0]
                    pdt_images='http://img3.zz91.com/100x100/'+pdt_images+''
                else:
                    pdt_images='http://img3.zz91.com/100x100/'
                sql2="select price,price_unit,quantity,quantity_unit from products where id=%s"
                products=dbc.fetchonedb(sql2,[id])
                quantity_info=''
                price_info=''
                if products:
                    if products[2] and products[2]!='0':
                        quantity_info =products[2]+products[3] 
                    if products[0] and products[0]!='0':
                        price_info=products[0]+products[1] 
                    
                purl="http://pyapp.zz91.com/app/ppchit.html?company_id="+str(company_id)+"&rd="+getjiami("http://www.zz91.com/ppc/productdetail"+str(id)+".htm")
                curl="http://pyapp.zz91.com/app/ppchit.html?company_id="+str(company_id)+"&rd="+getjiami("http://www.zz91.com/ppc/index"+str(company_id)+".htm")
                lis={'id':id,'ptitle':ptitle,'pdttxt':pdttxt,'pdt_images':pdt_images,'company_id':company_id,'ppckeywords':ppckeywords,'ppctel':front_tel,'companyname':companyname,'contact':contact,'curl':curl,'purl':purl,'quantityinfo':quantity_info,'priceinfo':price_info}
                listall.append(lis)
    return {'listall':listall,'lastpage':lastpage}

#----翻页
def showppccomplist(request):
    adposition=request.GET.get("adposition")
    page = request.GET.get("page")
    if (page=="" or page==None):
        page=1
    mm=request.GET.get("mm")
    keywords = request.GET.get("keywords")
    listall=getppccomplist(int(mm),keywords,int(page),adposition=adposition)['listall']
    return render_to_response('script_showppccomplist.html',locals())
def showppccomplist_pic(request):
    adposition=request.GET.get("adposition")
    page = request.GET.get("page")
    if (page=="" or page==None or page=="0"):
        page=1
    mm=request.GET.get("mm")
    keywords = request.GET.get("keywords")
    listall=getppccomplist(int(mm),keywords,int(page),adposition=adposition)['listall']
    return render_to_response('script_showppccomplist_pic.html',locals())

#来电宝广告点击跳转
def ppchit(request):
    company_id=request.GET.get("company_id")
    adposition=request.GET.get("adposition")
    adtype="2"
    rd=request.GET.get("rd")
    url=getjiemi(rd)
    saveshowppc(company_id,adposition,adtype="2")
    return HttpResponseRedirect(url)
#----来电宝全网广告
def showppcscript_pic(request):
    adposition=request.GET.get("adposition")
    keywords = request.GET.get("keywords")
    page = request.GET.get("page")
    lastpage=0
    if (page==None or page==""):
        page=1
    showposition = request.GET.get("showposition")
    w=request.GET.get("w")
    num=request.GET.get("num")
    if (num==None or str(num)==""):
        num=1
    if int(num)>1:
        boxright=1
    padding=request.GET.get("padding")
    if (padding==None or str(padding)==""):
        padding=0
    showborder=request.GET.get("showborder")
    if (w==None):
        w=430
    h=request.GET.get("h")
    if (h==None):
        h=100
    m=request.GET.get("m")
    if (m==None):
        m=20
    if (int(w)<200):
        pw=170
    else:
        pw=(int(w)-5*int(num)-2*int(num))/int(num)
        
    
    ppclist=getppccomplist(int(m),keywords,int(page),adposition=adposition)
    listall=ppclist['listall']
    lastpage=ppclist['lastpage']
    return render_to_response('app/ppc_ad_pic.html',locals())
def showppcscript(request):
    adposition=request.GET.get("adposition")
    keywords = request.GET.get("keywords")
    page = request.GET.get("page")
    lastpage=0
    if (page==None or page==""):
        page=1
    showposition = request.GET.get("showposition")
    w=request.GET.get("w")
    num=request.GET.get("num")
    if (num==None or str(num)==""):
        num=1
    if int(num)>1:
        boxright=1
    padding=request.GET.get("padding")
    if (padding==None or str(padding)==""):
        padding=0
    showborder=request.GET.get("showborder")
    if (w==None):
        w=430
    h=request.GET.get("h")
    if (h==None):
        h=100
    m=request.GET.get("m")
    if (m==None):
        m=20
    if (int(w)<200):
        pw=170
    else:
        pw=(int(w)-5*int(num))/int(num)
    
    ppclist=getppccomplist(int(m),keywords,int(page),adposition=adposition)
    listall=ppclist['listall']
    lastpage=ppclist['lastpage']
    return render_to_response('app/ppc_ad.html',locals())

def showppctxtadscript(request):
    
    
    
    num=request.GET.get("num")
    if (num==None or str(num)==""):
        num=1
        
    
    adtype=request.GET.get("adtype")
    if adtype==None:
        adtype="3"
    if num==1:
        adtype="2"
        
    if adtype=="2":
        return showppcscript(request)
    if adtype=="3":
        return showppcscript_pic(request)
    
    
    
#zz91注册页面  临时
def zz91regGetemail(request):
    email=request.GET.get("email")
    sql="select id  from auth_user where email='%s'"
    accountlist=dbc.fetchonedb(sql,str(email))
    if (accountlist):
        returnvalue="err"
    else:
        returnvalue="succ"
    return render_to_response('reg/returnvalue.html',locals())
    
def zz91regGetusername(request):
    username=request.GET.get("username")
    sql="select id  from auth_user where username='%s'"
    accountlist=dbc.fetchonedb(sql,str(username))
    if (accountlist):
        returnvalue="err"
    else:
        returnvalue="succ"
    return render_to_response('reg/returnvalue.html',locals())
    
def zz91regGetmobile(request):
    mobile=request.GET.get("mobile")
    sql="select id from company_account where mobile='%s'"
    accountlist=dbc.fetchonedb(sql,str(mobile))
    if (accountlist):
        returnvalue="err"
    else:
        returnvalue=""
    return render_to_response('reg/returnvalue.html',locals())
    
def zz91verifycode(request):
    host = request.META['HTTP_REFERER']
    zposition=host.find("zz91.com")
    if (zposition>0):
        mstream = StringIO.StringIO()
        validate_code = create_validate_code()
        img = validate_code[0]
        img.save(mstream, "GIF")
        mstream.closed
        t = request.GET.get("t")
        OBASN = request.GET.get("s")
        code=validate_code[1]
        cache.set("yzmdgda"+str(OBASN),code,60*60)
        #request.session['yzm']=validate_code[1]
        #浏览器关闭时失效
        #request.session.set_expiry(0)
        
        return HttpResponse(mstream.getvalue(),'image/gif')
    
def zz91register(request):
    return HttpResponseRedirect('http://127.0.0.1')
    return False
    s = random.randrange(0,10000000)
    s=str(s)
    #yzm=cache.get("yzmdgda98071416286")
    
    #return render_to_response('reg/default.html',locals())
    
def zz91registerSucceed(request):
    username=request.GET.get("username")
    
    return render_to_response('reg/regsuc.html',locals())
    
def zz91registerSave(request):
    userName = request.POST['zz91_memberName']
    password1 = request.POST['zz91_password']
    password2 = request.POST['zz91_passwordConfirm']
    email = request.POST['zz91_regemailname']+'@'+request.POST['zz91_regemailadr']
    mobile = request.POST['zz91_mobile']
    #mobile1 = request.POST['zz91_mobile1']
    #tel = request.POST['zz91_telcountry']+'-'+request.POST['zz91_telcity']+'-'+request.POST['zz91_tel']
    zz91_telcountry=request.POST['zz91_telcountry']
    zz91_telcity=request.POST['zz91_telcity']
    tel=request.POST['zz91_tel']
    company = request.POST['zz91_regCompName']
    contact = request.POST['zz91_trueName']
    sex = request.POST['cdesi']
    productslist = request.POST['zz91_regProducts']
    valcode1 = request.POST['zz91_verifyInfo']
    regtime=gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    s = request.POST['s']
    yzm=cache.get("yzmdgda"+str(s))
    #sessonyzm=request.session.get('yzm',None)
    errflag=0
    host = request.META['HTTP_REFERER']
    zposition=host.find("zz91.com")
    if (zposition<=0):
        errflag=1
        response = HttpResponse()
        response.write("<script>alert('"+str(zposition)+"错误');parent.document.getElementById('Submitsave').disabled=false;parent.document.getElementById('Submitsave').value='提交注册信息'</script>")
        return response
    if (str(yzm).lower()!=str(valcode1).lower()):
        errtext8="验证码错误"
        errflag=1
        response = HttpResponse()
        response.write("<script>alert('"+errtext8+"');parent.document.getElementById('Submitsave').disabled=false;parent.document.getElementById('Submitsave').value='提交注册信息'</script>")
        return response
    cache.delete("yzmdgda"+str(s),0)
    errtext1=""
    errtext2=""
    errtext3=""
    errtext4=""
    errtext5=""
    errtext6=""
    errtext7=""
    errtext8=""
    errtext9=""
    errtext10=""
    if (userName==''):
        errtext1="必须填写 会员名"
        errflag=1
    if (password1==''):
        errtext2="必须填写 密码"
        errflag=1
    if (password2==''):
        errtext3="必须填写 密码验证"
        errflag=1
    if (email==''):
        errtext4="必须填写 邮箱"
        errflag=1
    if (mobile==''):
        errtext5="必须填写 手机号"
        errflag=1
    """
    if (mobile1==mobile):
        errtext10="两次填写的手机号码不一致"
        errflag=1
    
    if (tel==''):
        errtext6="必须填写 电话"
        errflag=1
    """
    if (company==''):
        errtext7="必须填写 公司名称"
        errflag=1
    if (valcode1==''):
        errtext8="必须填写 验证码"
        errflag=1
    if (contact==''):
        errtext9="必须填写 联系人"
        errflag=1
    
    if (errflag==0):
        #''判断邮箱帐号是否存在
        sql="select id  from auth_user where username='"+str(userName)+"'"
        accountlist=dbc.fetchonedb(sql)
        if (accountlist):
            errflag=1
            errtext1="您填写的用户名已经存在！请修改用户名后重新提交！"
        sql="select id  from auth_user where email='"+str(email)+"'"
        accountlist=dbc.fetchonedb(sql)
        if (accountlist):
            errflag=1
            errtext4="您填写的邮箱已经注册！请修改邮箱后重新提交！"
        if (password1!=password2):
            errflag=1
            errtext2="两次填写的密码不一致，请重新确认！"
    if (errflag==0):
        #''帐号添加
        md5pwd = hashlib.md5(password1)
        md5pwd = md5pwd.hexdigest()[8:-8]
        value=[userName,md5pwd,email,gmt_created,gmt_modified]
        sql="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
        #添加公司信息
        industry_code=''
        business=productslist
        service_code=''
        area_code=''
        foreign_city=''
        category_garden_id='0'
        membership_code='10051000'
        classified_code='10101002'
        regfrom_code='10031024'
        #10031000
        domain=''
        address=''
        address_zip=''
        website=''
        introduction=''
        
        value=[company, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
        sql="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
        sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        dbc.updatetodb(sql,value);
        company_id=getcompany_id(company,gmt_created)
        is_admin='1'
        tel_country_code=zz91_telcountry
        tel_area_code=zz91_telcity

        fax_country_code=''
        fax_area_code=''
        fax=''
        if (sex==None):
            sex="0"
        #sex=''
        #'添加联系方式
        value=[userName, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password1, gmt_modified, gmt_created]
        sql="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
        sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        dbc.updatetodb(sql,value);
        response = HttpResponse()
        response.write("<script>parent.window.location.href='/zz91registerSucceed/?username="+userName+"';</script>")
        return response
        #return render_to_response('reg/regsuc.html',locals())
    if (errflag==1):
        response = HttpResponse()
        errtext=str(errtext1)+"\n"+errtext2+"\n"+errtext3+"\n"+errtext4+"\n"+errtext5+"\n"+errtext6+"\n"+errtext7+"\n"+errtext8+"\n"+errtext9+"\n"+errtext10
        response.write("<script>alert('"+errtext+"');parent.document.getElementById('Submitsave').disabled=false;parent.document.getElementById('Submitsave').value='提交注册信息'</script>")
        return response
        

def tradedetail_price(request):
    num=request.GET.get("listnum")
    tradeID=request.GET.get("tradeID")
    if (num!='' and num!=None):
        num=int(num)
    else:
        num=10
    keywords=request.GET.get("keywords")
    if (keywords!=None):
        keywords=keywords.replace('%20',' ')
        keywords=keywords.replace(',','|')
        keywords=keywords.replace('%7C','|')
        keywords=keywords.replace('%2C','|')
        keywords=keywords.replace('-','|')
    if (tradeID!=None and tradeID!=''):
        keywords=gettradetags(tradeID)
        if keywords:
            keywords=keywords.replace(',','|')
        else:
            keywords=''
    wordslen=request.GET.get("wordslen")
    if (wordslen!='' and wordslen!=None):
        wordslen=int(wordslen)
    else:
        wordslen=50
    wordslen=40
    pricelist=getindexpricelist(kname=keywords,limitcount=num,titlelen=wordslen)
    if (pricelist==[]):
        pricelist=getcompanypricelist(kname=keywords,limitcount=num,titlelen=wordslen)
    return render_to_response('tradedetail_price.html',locals())
#颗粒网报价信息抓取zz91报价信息用
def kl91price(request):
    page=request.GET.get("page")
    p=request.GET.get("p")
    t=request.GET.get("t")
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    sql="select title,gmt_order,id from price where type_id=%s order by gmt_order desc limit "+str(frompageCount)+","+str(int(frompageCount)+int(limitNum))+" "
    alist=dbc.fetchalldb(sql,str(t))
    listvalue=[]
    listcount=0
    for list in alist:
        title=list[0]
        putdate=list[1]
        id=list[2]
        list1={'id':id,'title':title,'putdate':putdate}
        listvalue.append(list1)
        listcount=listcount+1
    
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('kl91/list.html',locals())
def kl91pricedetail(request):
    id=request.GET.get("id")
    sql="select title,content,gmt_order from price where id=%s"
    pricelistone=dbc.fetchonedb(sql,str(id))
    if (pricelistone):
        list={'title':pricelistone[0],'content':pricelistone[1],'putdate':pricelistone[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')}
    return render_to_response('kl91/detail.html',locals())

#城市联动js
def areahtml(request):
    code=request.GET.get("code")
    code0=code
    navlist0=getnavareavalue(code0)
    navlist1=getnavareavalue(code0[:-4])
    navlist2=getnavareavalue(code0[:-8])
    navlist3=getnavareavalue(code0[:-12])
    navlist=""
    navlist00=""
    if (navlist3):
        navlist=navlist+"<span class=navselect onClick=getprovince('','"+navlist3[1]+"',1)>"+navlist3[0]+"</span>&nbsp;>&nbsp;"
        navlist00=navlist00+navlist3[0]+"&nbsp;>&nbsp;"
    if (navlist2):
        navlist=navlist+"<span class=navselect onClick=getprovince('','"+navlist2[1]+"',1)>"+navlist2[0]+"</span>&nbsp;>&nbsp;"
        navlist00=navlist00+navlist2[0]+"&nbsp;>&nbsp;"
    if (navlist1):
        navlist=navlist+"<span class=navselect onClick=getprovince('','"+navlist1[1]+"',1)>"+navlist1[0]+"</span>&nbsp;>&nbsp;"
        navlist00=navlist00+navlist1[0]+"&nbsp;>&nbsp;"
    if (navlist0):
        navlist=navlist+"<span class=navselect onClick=getprovince('','"+navlist0[1]+"',1)>"+navlist0[0]+"</span>&nbsp;>&nbsp;"
        navlist00=navlist00+navlist0[0]+"&nbsp;>&nbsp;"
    arealist=getareavalue(code)
    return render_to_response('areahtml.html',locals())
def jsprovince(request):
    sql="select code,label from category where code like '1001____'"
    result=dbc.fetchonedb(sql)
    strvalue="dsy.add('1001',["
    listall=[]
    if (result):
        for list in result:
            strvalue=strvalue+"['"+str(list[1])+"','"+list[0]+"'],"
            list={'code':list[0],'label':list[1]}
            listall.append(list)
        strvalue=strvalue+"]);"
    
        for a in listall:
            sql="select code,label from category where code like '"+a['code']+"____'"
            result=dbc.fetchonedb(sql)
            if result:
                strvalue=strvalue+"dsy.add('"+a['code']+"',["
                listall1=[]
                for list1 in result:
                    strvalue=strvalue+"['"+str(list1[1])+"','"+list1[0]+"'],"
                    list2={'code':list1[0],'label':list1[1]}
                    listall1.append(list2)
                strvalue=strvalue+"]);"

                for a in listall1:
                    sql="select code,label from category where code like '"+a['code']+"____'"
                    result=dbc.fetchonedb(sql)
                    if result:
                        strvalue=strvalue+"dsy.add('"+a['code']+"',["
                        listall2=[]
                        for list1 in result:
                            strvalue=strvalue+"['"+str(list1[1])+"','"+list1[0]+"'],"
                            list2={'code':list1[0],'label':list1[1]}
                            listall2.append(list2)
                        strvalue=strvalue+"]);"

                        for a in listall2:
                            sql="select code,label from category where code like '"+a['code']+"____'"
                            result=dbc.fetchonedb(sql)
                            if result:
                                strvalue=strvalue+"dsy.add('"+a['code']+"',["
                                listall3=[]
                                for list1 in result:
                                    strvalue=strvalue+"['"+str(list1[1])+"','"+list1[0]+"'],"
                                    list2={'code':list1[0],'label':list1[1]}
                                    listall3.append(list2)
                                strvalue=strvalue+"]);"        
    return render_to_response('province.html',locals())

#城市联动js
def provincejs(request):
    sql="select code,label from category where code like '1001____'"
    result=dbc.fetchonedb(sql)
    listall=[]
    if (result):
        for list in result:
            list={'code':list[0],'label':list[1],'child':''}
            listall.append(list)
    
        for a in listall:
            sql="select code,label from category where code like '"+a['code']+"____'"
            result=dbc.fetchonedb(sql)
            if result:
                listall1=[]
                for list1 in result:
                    list2={'code':list1[0],'label':list1[1],'child':''}
                    listall1.append(list2)
                a['child']=listall1

                for b in listall1:
                    sql="select code,label from category where code like '"+b['code']+"____'"
                    result=dbc.fetchonedb(sql)
                    if result:
                        listall2=[]
                        for list3 in result:
                            list4={'code':list3[0],'label':list3[1],'child':''}
                            listall2.append(list4)
                        b['child']=listall2

                        for c in listall2:
                            sql="select code,label from category where code like '"+c['code']+"____'"
                            result=dbc.fetchonedb(sql)
                            if result:
                                listall3=[]
                                for list5 in result:
                                    list6={'code':list5[0],'label':list5[1]}
                                    listall3.append(list6)
                                c['child']=listall3
    return render_to_response('provincejs.html',locals())
    
def keywordsearch(request):
    #-------------智能搜索提示
    keywords = request.GET.get("keywords")
    port = spconfig['port']
    cl = SphinxClient()
    cl.SetServer ( spconfig['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"showcount desc" )
    cl.SetLimits (0,10,10)
    res = cl.Query ('@(label,pingyin) '+keywords,'daohangkeywords')
    if res:
        if res.has_key('matches'):
            keylist=res['matches']
            listall_keywordsearch=[]
            for match in keylist:
                id=match['id']
                attrs=match['attrs']
                tags=attrs['plabel']
                list1={'keyword':tags}
                listall_keywordsearch.append(list1)
            listall=listall_keywordsearch
    return render_to_response('keywordsearch.html',locals())

#未登录提示登录
def calllogin(request):
    backurl=request.META['HTTP_HOST']
    backurl = request.META.get('HTTP_REFERER','/')
    #backurl = backurl+request.get_full_path()
    return render_to_response('calllogin.html',locals())

def areyouknow(request):
    randnum=random.randrange(0,1000)
    newslist=getnewslist(frompageCount=randnum,limitNum=1,contentflag=None)
    return render_to_response('app/areyouknow.html',locals())
def areyouknowmore(request):
    page=request.GET.get("page")
    if page==None:
        page=1
    nextpage=int(page)+1
    prepage=int(page)-1
    if prepage<=0:
        prepage=0
    newslist=getnewslist(frompageCount=int(page),limitNum=1,contentflag=None)
    return render_to_response('app/areyouknowmore.html',locals())    
#公司库首页最新供求 
def companyindexnewproducts(request):
    offerlist=getindexofferlist_pic(None,None,3)
    return render_to_response('app/companyindexnewproducts.html',locals())
def companyindexnewcomplist(request):
    complist=getcompanyindexcomplist(None,11)
    return render_to_response('app/companyindexnewcomplist.html',locals())
#----微站二维码html
def getdomainhtml(request,company_id):
    sqll="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code ='10001007' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
    wzresult=dbc.fetchonedb(sqll)
    
    if wzresult:
        html="<div class=weixin_code><div style='text-align:center;font-color:#000'>用手机查看我的微站</div><img src='http://pyapp.zz91.com/getdomainpic"+str(company_id)+".html'></div>"
    else:
        html=""
    return render_to_response('app/getdomainhtml.html',locals())
#----首页直达广告
def getzhidahtml(request):
    keywords = request.GET.get("keywords")
    sqll="select id,company_id from crm_company_service where crm_service_code ='10001008' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0 and remark=%s"
    wzresult=dbc.fetchalldb(sqll,[keywords])
    html='var _suggest_result_={"result":"'
    if wzresult:
        for list in wzresult:
            company_id=list[1]
            sql="select b.name from crm_company_service as a left join company as b on a.company_id=b.id where exists(select crm_service_code from crm_service_group where crm_service_code=a.crm_service_code and code='ldb') and a.apply_status='1'  and a.company_id=%s"
            resultlist=dbc.fetchonedb(sql,[company_id])
            if resultlist:
                name=resultlist[0]
                html+='<div class=compinfotext><a href=http://www.zz91.com/ppc/index'+str(company_id)+'.htm target=_blank>'+name+'</a></div>'
            else:
                sqlc="select domain_zz91,name from company where id=%s"
                result=dbc.fetchonedb(sqlc,[company_id])
                if result:
                    domain_zz91=result[0]
                    name=result[1]
                    html+='<div class=compinfotext><a href=http://'+domain_zz91+'.zz91.com target=_blank>'+name+'</a></div>'
    
    html+='"}'
    return HttpResponse(""+html+"")
#-----微站二维码
def getdomainpic(request,company_id):
    sql="select domain_zz91 from company where id=%s"
    returnresult=dbc.fetchonedb(sql,[company_id])
    if returnresult:
        domain_zz91=returnresult[0]
        domain="http://"+domain_zz91+".m.zz91.com"
    else:
        domain_zz91=None
        domain=None
    if domain:
        qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=4,
                        border=2,
                        )
        qr.add_data(domain)
        qr.make(fit=True)
        img = qr.make_image()
        mstream = StringIO.StringIO()
        img.save(mstream, "GIF")
        mstream.closed
        return HttpResponse(mstream.getvalue(),'image/gif')
    else:
        return None
#----资讯调用
def javagetnewslist(request):
    keywords = request.GET.get("keywords")
    num=request.GET.get("num")
    newslist=getnewslist(keywords=keywords,frompageCount=0,limitNum=int(num))
    return render_to_response('app/getnews.html',locals())
#----资讯调用
def javagetnewslist_json(request):
    keywords = request.GET.get("keywords")
    num=request.GET.get("num")
    if not num:
        num=6
    newslist=getnewslist(keywords=keywords,frompageCount=0,limitNum=int(num))
    return HttpResponse(simplejson.dumps(newslist, ensure_ascii=False))
#----企业报价调用
def javagetcompanyprice_json(request):
    keywords = request.GET.get("keywords")
    if (gethextype(keywords)==True):
        keywords=getjiemi(keywords)
    else:
        keywords=""
    num=request.GET.get("num")
    newslist=""
    if not num:
        num=10
    if not keywords:
        keywords=""
    newslist=getcompanypricelist(kname=keywords,limitcount=int(num))
    return HttpResponse(simplejson.dumps(newslist, ensure_ascii=False))
#----url 二维码
def qrcodeimg(request):
    id=request.GET.get('id')
    type=request.GET.get('type')
    if type=="trade":
        arg="http://m.zz91.com/detail/?id="+str(id)
    if type=="price":
        arg="http://m.zz91.com/priceviews/?id="+str(id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(arg)
    qr.make(fit=True)
    img = qr.make_image()
    mstream = StringIO.StringIO()
    img.save(mstream, "GIF")
    mstream.closed
    return HttpResponse(mstream.getvalue(),'image/gif')
   
#支付宝支付
def zz91pay(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    apptype = request.POST.get('apptype')
    if apptype:
        company_id=request.POST.get('company_id')
        #if company_id:
            #username=getcompanyaccount(company_id)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/zz91pay.html")
    
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    
    user_ip=getIPFromDJangoRequest(request)
    if not user_ip:
        user_ip="0.0.0.0"
    #user_ip="127.0.0.1"
    total_fee = request.POST.get('total_fee')
    relfee=total_fee
    #relfee=float(total_fee)/100
    total_fee=float(total_fee)*100
    subject = request.POST.get('subject')
    todate=datetime.datetime.now()
    today=todate.strftime('%Y%m%d')
    t=random.randrange(100000,999999)
    out_trade_no=str(today)+str(t)
    is_success="F"
    payreturn_url=request.POST.get("payreturn_url")
    paytype=request.POST.get("paytype")
    #中断返回
    merchant_url=request.META['HTTP_REFERER']
    #total_fee=0.1
    gmt_created=datetime.datetime.now()
    
    valu=[out_trade_no,subject,relfee,contact,mobile,is_success,payreturn_url,paytype,company_id,gmt_created]
    sql="insert into pay_order(out_trade_no,subject,total_fee,contact,mobile,is_success,payreturn_url,paytype,company_id,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dbc.updatetodb(sql,valu)
    
    """
    pingpp.api_key = 'sk_live_dHUzL3M5N8EblzOkPlO2kJHs'
    ch = pingpp.Charge.create(
        order_no=out_trade_no,
        channel="alipay_wap",
        amount=relfee,
        subject=subject,
        body=contact+mobile,
        currency='cny',
        app=dict(id='app_SqrzfLn5iDq5K0Om'),
        extra=dict(success_url='http://m.zz91.com/zz91payreturn_url.html'),
        client_ip=user_ip
    )
    return HttpResponse(simplejson.dumps(ch, ensure_ascii=False))
    """
    
    #payload={'out_trade_no':out_trade_no,'subject':subject,'total_fee':total_fee,'merchant_url':merchant_url}
    #r= requests.post("http://www.zz91.com/zzpay/alipay/alipayapi.jsp",data=payload)
    #r= requests.post("http://phppay.zz91.com/alipay/alipayapi.php",data=payload)
    #return HttpResponse(r.content)

    payload={'order_id':out_trade_no,'identity_id':out_trade_no,'product_name':subject,'product_desc':'','amount':total_fee,'merchant_url':merchant_url,'user_ip':user_ip}
    #return HttpResponse(urllib.urlencode(payload))
    url="http://m.zz91.com/pingxx/pay.html?"+urllib.urlencode(payload)
    
    #url="http://phppay.zz91.com/toMobilepay.php?"+urllib.urlencode(payload)
    return HttpResponseRedirect(url)

    #alipay = Alipay(pid='2088511051388426', key='ovtvgwuew1zdfmbiydepr0k9m8b25exp', seller_email='zhifu@asto-inc.com')
    #payurl=alipay.create_direct_pay_by_user_url(out_trade_no=out_trade_no, subject=subject, total_fee=total_fee, return_url='http://m.zz91.com/zz91payreturn_url.html', notify_url='http://m.zz91.com/zz91payverify_notify.html')
    #return HttpResponseRedirect(payurl)
def yeepaysave(request):
    
    payload={'order_id':out_trade_no,'identity_id':out_trade_no+user_ip.replace(".",""),'product_name':subject,'product_desc':'','amount':total_fee,'merchant_url':merchant_url,'user_ip':user_ip}
    url="http://phppay.zz91.com/toMobilepay.php?"+urllib.urlencode(payload)
    return HttpResponseRedirect(url)
#易宝支付返回，异步通知返回
def callback_post(request):
    sql="insert into pingxx (content) values(%s)"
    #dbc.updatetodb(sql,[str(request)])
    mer=MerchantAPI()
    data=request.POST.get("data")
    encryptkey=request.POST.get("encryptkey")
    ll={'data':data,'encryptkey':encryptkey}
    resualt1=mer.result_decrypt1(ll)
    #resualt=simplejson.dumps(resualt, ensure_ascii=False)
    resualt=simplejson.loads(resualt1)
    amount=resualt['amount']
    out_trade_no=resualt['orderid']
    trade_status=resualt['status']
    trade_no=resualt['yborderid']
    if (trade_status==1):
        sql="update pay_order set is_success=%s,trade_no=%s where out_trade_no=%s"
        dbc.updatetodb(sql,[trade_status,trade_no,out_trade_no])
        sql="select payreturn_url,paytype,total_fee,company_id from pay_order where out_trade_no=%s"
        result=dbc.fetchonedb(sql,[out_trade_no])
        if result:
            payreturn_url=result[0]
            paytype=result[1]
            fee=result[2]
            company_id=result[3]
            payresult=paysave(paytype,out_trade_no,company_id,fee)
            return HttpResponse("success")
        else:
            return HttpResponse("fail")
    else:
        return HttpResponse("fail")
    
def callback_get(request):
    mer=MerchantAPI()
    data=request.GET.get("data")
    encryptkey=request.GET.get("encryptkey")
    ll={'data':data,'encryptkey':encryptkey}
    resualt1=mer.result_decrypt1(ll)
    #resualt=simplejson.dumps(resualt, ensure_ascii=False)
    resualt=simplejson.loads(resualt1)
    amount=resualt['amount']
    out_trade_no=resualt['orderid']
    trade_status=resualt['status']
    trade_no=resualt['yborderid']
    if (trade_status==1):
        sql="update pay_order set is_success=%s,trade_no=%s where out_trade_no=%s"
        dbc.updatetodb(sql,[trade_status,trade_no,out_trade_no])
        sql="select payreturn_url,paytype,total_fee,company_id from pay_order where out_trade_no=%s"
        result=dbc.fetchonedb(sql,[out_trade_no])
        if result:
            payreturn_url=result[0]
            paytype=result[1]
            fee=result[2]
            company_id=result[3]
            payresult=paysave(paytype,out_trade_no,company_id,fee)
            return HttpResponseRedirect(payreturn_url)
        else:
            return HttpResponse("fail")
    else:
        return HttpResponse("fail")
def zz91paypingxx_notify(request):

    #return HttpResponse(request)
    # 读取异步通知数据
    #ch = pingpp.Charge.all()
    notify = request.POST
    #object=request.POST.get("object")
    # 对异步通知做处理
    if 'object' not in notify:
        notitext= 'fail'
    else:
        if notify['object'] == 'charge':
            paid=notify['paid']
            order_no=notify['order_no']
            amount=notify['amount']
            if str(paid)=="true":
                sql="update pay_order set is_success=%s where out_trade_no=%s"
                dbc.updatetodb(sql,[paid,order_no])
                sql="select payreturn_url,paytype,total_fee,company_id from pay_order where out_trade_no=%s"
                result=dbc.fetchonedb(sql,[out_trade_no])
                if result:
                    payreturn_url=result[0]
                    paytype=result[1]
                    fee=result[2]
                    company_id=result[3]
                    payresult=paysave(paytype,order_no,company_id,fee)
                    return HttpResponse("success")
            else:
                return HttpResponse("fail")
        else:
            return HttpResponse("fail")
    return HttpResponse(notitext)
#支付宝支付完成通知，异步返回通知
def zz91payverify_notify(request):
    out_trade_no=request.POST.get("out_trade_no")
    trade_no=request.POST.get("trade_no")
    trade_status=request.POST.get("trade_status")
    sql="insert into pingxx (content) values(%s)"
    dbc.updatetodb(sql,[str(request)])
    #return HttpResponse("SUCCESS")
    if not out_trade_no:
        xml = ET.fromstring(request.POST.get("notify_data"))
        out_trade_no = xml.find("out_trade_no").text
        trade_no= xml.find("trade_no").text
        trade_status=xml.find("trade_status").text
    if trade_status in ("TRADE_FINISHED","TRADE_SUCCESS"):
        sql="update pay_order set is_success=%s,trade_no=%s where out_trade_no=%s"
        dbc.updatetodb(sql,[trade_status,trade_no,out_trade_no])
        sql="select payreturn_url,paytype,total_fee,company_id from pay_order where out_trade_no=%s"
        result=dbc.fetchonedb(sql,[out_trade_no])
        if result:
            payreturn_url=result[0]
            paytype=result[1]
            fee=result[2]
            company_id=result[3]
            payresult=paysave(paytype,out_trade_no,company_id,fee)
            return HttpResponse("success")
            
        else:
            return HttpResponse("fail")
    else:
        return HttpResponse("fail")
#----支付成功开通服务
def paysave(paytype,trade_no,company_id,fee):
    if paytype=="qianbao":
        sql="select id from pay_mobileWallet where trade_no=%s"
        result=dbc.fetchonedb(sql,[trade_no])
        if result:
            id=result[0]
            gmt_created=gmt_modified=datetime.datetime.now()
            gmt_date=gmt_created.strftime( '%Y-%m-%d')
            ftype=5
            #value=[company_id,fee,ftype,trade_no,gmt_date,gmt_created,gmt_modified]
            #sqlp="insert into pay_mobileWallet(company_id,fee,ftype,trade_no,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s)"
            #cursor.execute(sqlp,value)
            return 1
        else:
                
            gmt_created=gmt_modified=datetime.datetime.now()
            gmt_date=gmt_created.strftime( '%Y-%m-%d')
            ftype=5
            paytype="在线支付"
            value=[company_id,fee,ftype,trade_no,gmt_date,gmt_created,gmt_modified,paytype]
            sqlp="insert into pay_mobileWallet(company_id,fee,ftype,trade_no,gmt_date,gmt_created,gmt_modified,paytype) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sqlp,value)
            sql="update pay_order set is_success=%s where out_trade_no=%s"
            dbc.updatetodb(sql,[1,trade_no])

            #----(充值做活动)
            timeall=datetime.datetime.now()
            sqlgg='select begin_time,end_time,infee,sendfee,ftype from qianbao_gg where closeflag=0 order by begin_time desc'
            resultgg=dbc.fetchonedb(sqlgg)
            if resultgg:
                begin_time=resultgg[0]
                end_time=resultgg[1]
                infee=resultgg[2]
                sendfee=resultgg[3]
                ftype=resultgg[4]
                if begin_time and end_time and infee and sendfee:
                    #beilv=str(float(fee)/infee).split('.')[0]
                    #fee1=int(beilv)*sendfee
                    if timeall>=begin_time and timeall<end_time:
                        ftype1=ftype
                        fee1=sendfee
                        paytype="活动赠送"
                        value2=[company_id,fee1,ftype1,trade_no,gmt_date,gmt_created,gmt_modified,paytype]
                        dbc.updatetodb(sqlp,value2)
            return 1
    if paytype=="ldb":
        sql=""
        return 1
    return 1
#----支付成功返回页面    ,同步返回
def zz91payreturn_url(request):
    tn = request.GET.get("out_trade_no")
    trade_status=request.GET.get("trade_status")
    buyer_email=request.GET.get("buyer_email")
    result=request.GET.get("result")
    notify_id=request.GET.get("notify_id")
    notify_time=request.GET.get("notify_time")
    subject=request.GET.get("subject")
    trade_no=request.GET.get("trade_no")
    
    
    suc="您已经成功完成支付，我们将在1个工作日内容为您开通服务。或咨询：0571-56612345 <a href='javascript:window.close()'>关闭</a>"
    err="可能因为网络的原因，没有支付,请重新下单再试。"
    if result=="success":
        
        sql="select payreturn_url,paytype,total_fee,company_id from pay_order where out_trade_no=%s"
        result=dbc.fetchonedb(sql,[tn])
        if result:
            payreturn_url=result[0]
            company_id=result[3]
            #return HttpResponseRedirect(payreturn_url)
            
            paytype=result[1]
            fee=result[2]
            payresult=paysave(paytype,tn,company_id,fee)
            return HttpResponseRedirect(payreturn_url)
            if payresult:
                return HttpResponse(suc)
            else:
                return HttpResponse(suc)
        else:
            return HttpResponse(err)
    else:
        return HttpResponse(err)
    