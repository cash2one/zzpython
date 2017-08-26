import re
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseNotFound
vodiolist=["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]
def tradeorderby(listall):
	listall = sorted(listall, key=itemgetter(1))
	changeflag="0"
	listallvip1=[]
	listallvip2=[]
	m=0
	for i in listall:
		m+=1
		if (changeflag==str(i[1])):
			list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
			listallvip2.append(list1)
			if (len(listall)==m):
				listallvip1+=listallvip2
		else:
			listallvip2=sorted(listallvip2, key=itemgetter(4,2,5,3),reverse=True)
			listallvip1+=listallvip2
			listallvip2=[]
			list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
			listallvip2.append(list1)
			if (len(listall)==m):
				listallvip1+=listallvip2
		changeflag=str(i[1])
	return listallvip1

def getbuycontact(company_id,pdtid,cursort):
	sql2='select company_id from products where id=%s'
	result=dbc.fetchonedb(sql2,[pdtid])
	if result:
		forcompany_id=result[0]
		sql='select id from pay_mobileWallet where company_id=%s and forcompany_id=%s'
		buycontact=dbc.fetchonedb(sql,[company_id,forcompany_id])
		#cursort.execute(sql,[company_id,forcompany_id])
		#buycontact=cursort.fetchone()
		if buycontact:
			return 1
def getisbuyshowphone(company_id,cursort):
	gmt_created=datetime.datetime.now()
	sql='select id from shop_showphone where company_id=%s and gmt_end>=%s order by id desc'
	result=dbc.fetchonedb(sql,[company_id,gmt_created])
	if result:
		return 1
def getqianbaoblance2(company_id,cursort):
	sql='select sum(fee) from pay_mobileWallet where company_id=%s'
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		return result[0]
	return 0.0
#----获得来电宝帐号总余额
def getldblaveall(company_id,cursort,datefrom=''):
	#----查看未接来电费用
	phone400=getldbphone(company_id)
	if phone400:
		phone400=phone400['tel']
	sqls='select sum(click_fee) from phone_call_click_fee where company_id=%s'
	if datefrom!='':
		sqls=sqls+" and gmt_created>'"+str(datefrom)+"'"
	#cursort.execute(sqls,[company_id])
	#results=cursort.fetchone()
	results=dbc.fetchonedb(sqls,[company_id])
	phone_call_click_fee=0
	if results:
		phone_call_click_fee=results[0]
		if phone_call_click_fee==None:
			phone_call_click_fee=0
	#----电话费用
	sqls='select sum(call_fee) from phone_log where tel=%s'
	if datefrom!='':
		sqls=sqls+" and start_time>'"+str(datefrom)+"'"
	#cursort.execute(sqls,[phone400])
	#results=cursort.fetchone()
	results=dbc.fetchonedb(sqls,[phone400])
	call_fee=0
	if results:
		call_fee=results[0]
		if call_fee==None:
			call_fee=0
	#----点击查看联系方式费用
	sqls='select sum(click_fee) from phone_click_log where company_id=%s'
	if datefrom!='':
		sqls=sqls+" and gmt_created>'"+str(datefrom)+"'"
	#cursort.execute(sqls,[company_id])
	#results=cursort.fetchone()
	results=dbc.fetchonedb(sqls,[company_id])
	phone_click_fee_fee=0
	if results:
		phone_click_fee_fee=results[0]
		if phone_click_fee_fee==None:
			phone_click_fee_fee=0
						
	sql='select amount from phone where company_id=%s and expire_flag=0'
	#cursort.execute(sql,[company_id])
	#result=cursort.fetchone()
	result=dbc.fetchonedb(sql,[company_id])
	lave=0
	if result:
		lave=int(result[0])
		if lave:
			lave=lave-phone_call_click_fee-phone_click_fee_fee-call_fee
		else:
			lave=0
	if datefrom!='':
		return phone_call_click_fee+phone_click_fee_fee+call_fee
	return lave
#获取来电宝服务
def getldbservice():
	service=[]
	sql="select crm_service_code from crm_service_group where code=%s"
	result=dbc.fetchalldb(sql,['ldb'])
	if result:
		for list in result:
			service.append(list[0])
	return service
def getcompinfo(pdtid,cursort,keywords,company_id=''):
	isbuycontact=None
	isbuyshowphone=None
	if company_id:
		isbuycontact=getbuycontact(company_id,pdtid,cursort)
	productsinfo=cache.get("mobile_productsinfo"+str(pdtid))
	if (productsinfo==None):
		sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%%Y/%%m/%%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit,p.check_status FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code where p.id=%s;"
		productlist=dbc.fetchonedb(sql,pdtid)
		if productlist:
			arrpdt_kind={'kindtxt':'','kindclass':''}
			pdt_kind=productlist[3]
			viptype=str(productlist[9])
			if (str(pdt_kind) == '1'):
				arrpdt_kind['kindtxt']='求购'
				arrpdt_kind['kindclass']='buy'
			else:
				arrpdt_kind['kindtxt']='供应'
				arrpdt_kind['kindclass']='sell'
			arrviptype={'vippic':'','vipname':'','vipsubname':'','vipcheck':'','com_fqr':'','litname':None}
			if (viptype == '10051000'):
				arrviptype['vippic']=None
				arrviptype['vipname']='普通会员'
				arrviptype['litname']=''
				arrviptype['classname']=''
			if (viptype == '10051001'):
				arrviptype['vippic']='http://m.zz91.com/images/recycle.gif'
				arrviptype['vipname']='再生通'
				arrviptype['litname']='再'
				arrviptype['classname']='hy-type5'
			if (viptype == '100510021000'):
				arrviptype['vippic']='http://m.zz91.com/images/pptSilver.gif'
				arrviptype['vipname']='银牌品牌通'
				arrviptype['litname']='银'
				arrviptype['classname']='hy-type6'
			if (viptype == '100510021001'):
				arrviptype['vippic']='http://m.zz91.com/images/pptGold.gif'
				arrviptype['vipname']='金牌品牌通'
				arrviptype['litname']='金'
				arrviptype['classname']='hy-type4'
			if (viptype == '100510021002'):
				arrviptype['vippic']='http://m.zz91.com/images/pptDiamond.gif'
				arrviptype['vipname']='钻石品牌通'
				arrviptype['litname']='钻'
				arrviptype['classname']='hy-type1'
			if (viptype == '10051000'):
				arrviptype['vipcheck']=None
			else:
				arrviptype['vipcheck']=1
			com_id=productlist[0]
			if com_id:
				isbuyshowphone=getisbuyshowphone(com_id,cursort)
				if isbuyshowphone:
					arrviptype['litname']='显'
					arrviptype['classname']='hy-type3'
			arrviptype['vipsubname'] = productlist[7]
			arrviptype['com_fqr']=''
			com_province=productlist[10]
			if (com_province==None):
				com_province=''
			pdt_images=""
			#价格范围判断
			allprice=""
			min_price=productlist[11]
			if (min_price==None):
				min_price=''
			else:
				min_price=str(min_price)
				if (min_price!='0.0'):
					allprice=allprice+min_price
			max_price=productlist[12]
			if (max_price==None):
				max_price=''
			else:
				max_price=str(max_price)
				if (max_price!='0.0' and max_price!=min_price):
					allprice=allprice+'-'+max_price
			price_unit=productlist[13]
			check_status=productlist[14]
			if (price_unit==None):
				price_unit=''
			else:
				if (allprice!=''):
					allprice=allprice+price_unit
			#---接听率
			sql1="select phone_rate,level from ldb_level where company_id=%s and exists(select company_id from crm_company_service where crm_service_code in(select crm_service_code from crm_service_group where code='ldb') and apply_status=1 and company_id=ldb_level.company_id)"
			ldbrate=dbc.fetchonedb(sql1,[productlist[0]])
			if ldbrate:
				phone_rate=ldbrate[0]
				ldblevel=ldbrate[1]
				arrviptype['litname']='电'
				arrviptype['classname']='hy-type2'
			else:
				phone_rate=None
				ldblevel=None
			
			#----
			sql1="select pic_address from products_pic where product_id=%s and check_status=1"
			productspic=dbc.fetchonedb(sql1,productlist[2])
			if productspic:
				pdt_images=productspic[0]
			else:
				pdt_images=""
			if (pdt_images == '' or pdt_images == '0'):
				pdt_images='../cn/img/noimage.gif'
			else:
				pdt_images='http://img3.zz91.com/135x135/'+pdt_images+''
			
			ldbtel=getldbphone(productlist[0])
			
			list1={'com_id':com_id,'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
			,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5]
			,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype
			,'pdt_images':pdt_images,'pdt_price':allprice
			,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'ldbtel':ldbtel,'phone_rate':phone_rate,'ldblevel':ldblevel,'check_status':check_status}
		else:
			list1=None
			
		#list1=getproid(pdtid)
		if (list1 == None):
			return None
		else:
			pdt_images=list1['pdt_images']
			if (pdt_images=='../cn/img/noimage.gif'):
				list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
			pdt_detail=list1['pdt_detail']
			if pdt_detail:
				pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
				docs=[pdt_detail]
				list1['pdt_detail']=subString(filter_tags(pdt_detail),50)+'...'
			pdt_name=list1['pdt_name']
			docs=[pdt_name]
			list1['pdt_name']=pdt_name
		productsinfo=list1
		cache.set("mobile_productsinfo"+str(pdtid),list1,60*60)
	productsinfo['isbuycontact']=isbuycontact
	productsinfo['isbuyshowphone']=isbuyshowphone
	return productsinfo
#获得会员服务类型
def getcompanytype(company_id):
	sql="select crm_service_code from crm_company_service where company_id=%s"
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		crm_service_code=result[0]
		if (crm_service_code == '1000' or crm_service_code == '1006'):
			return 1
		else:
			return None
#----产品属性字典
def getmoreproperty(listmore,text,value,fildname):
	if (value!="" and value!=None):
		value=value.strip()
		listmore.append({'property':text,'content':value,'fildname':fildname})
	return listmore
#----获取供求类别名称
def getcategorylabel(code):
	if code:
		sql="select label from category where code=%s"
		result=dbc.fetchonedb(sql,[code])
		if result:
			return result[0]
#判断是否为HEX码
def gethextype(keywords):
	zwtype=0
	zwflag=0
	strvalue="abcdef0123456789"
	for a in keywords:
		if (a >= u'\u4e00' and a<=u'\u9fa5'):
			zwflag=zwflag+1
	if zwflag>0:
		zwtype=1
	zwflag=0
	if zwtype==0:
		for a in keywords:
			if (strvalue.find(a)==-1):
				zwflag=zwflag+1
		if zwflag>0:
			zwtype=1
	if zwtype==1:
		return False
	else:
		return True
#加密
def getjiami(strword):
	if strword:
		return strword.encode('utf8','ignore').encode("hex")
	else:
		return ""
def getjiemi(strword):
	if strword:
		return strword.decode("hex").decode('utf8','ignore')
	else:
		return ""
def changezw(strvalue):
	if(strvalue == None):
		tempstr=""
	else:
		tempstr=str(strvalue).encode('gbk','ignore').replace("'","")
	return tempstr
def changezhongwen(strvalue):
	if(strvalue == None):
		tempstr=""
	else:
		tempstr=strvalue.decode('GB18030','ignore').encode('utf-8')
		#tempstr=strvalue.decode('GB18030').encode('utf-8')
	return tempstr
def subString(string,length):
	if string:
		if length >= len(string):   
			return string
	else:
		return None
	result = ''  
	i = 0  
	p = 0  
	while True:   
		ch = ord(string[i])   
		#1111110x   
		if ch >= 252:   
			p = p + 6  
		#111110xx   
		elif ch >= 248:   
			p = p + 5  
		#11110xxx   
		elif ch >= 240:   
			p = p + 4  
		#1110xxxx   
		elif ch >= 224:   
			p = p + 3  
		#110xxxxx   
		elif ch >= 192:
			p = p + 2  
		else:   
			p = p + 1	   
		if p >= length:   
			break;
		else:   
			i = p   
	return string[0:i]
	pass
def formattime(value,flag):
	if value:
		if (flag==1):
			return value.strftime( '%-Y-%-m-%-d')
		if (flag==2):
			return value.strftime( '%-m-%-d %-H:%-M')
		if (flag==3):
			return value.strftime( '%Y-%-m-%d &nbsp;%-H:%M')
		else:
			return value.strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
	else:
		return ''

#静态文件保存
def _key_to_file(pth):
	pth = str(pth)
	return '/usr/data/offerlist/'+pth+'/'
def getstaticValue(pth,key):
	fname = _key_to_file(pth)
	if not (os.path.exists(fname+str(key)+'.pkl')):
		return None
	else:
		pkl_file = open(fname+str(key)+'.pkl','rb')
		return pickle.load(pkl_file)
		pkl_file.close()
def updatetaticValue(pth,key,list):
	fname = _key_to_file(pth)
	if not os.path.exists(fname):
		os.makedirs(fname)
	output = open(fname+str(key)+".pkl", 'wb')
	pick = pickle.Pickler(output)
	pick.dump(list)
	output.close()

#验证码

_letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper() # 大写字母
_numbers = ''.join(map(str, range(3, 10))) # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
#memcache



def create_validate_code(size=(120, 30),
						chars=init_chars,
						img_type="PNG",
						mode="RGB",
						bg_color=(255, 255, 255),
						fg_color=(0, 0, 255),
						font_size=18,
						font_type="/var/pythoncode/mobileweb/arial.ttf",
						length=4,
						draw_lines=True,
						n_line=(1, 4),
						draw_points=True,
						point_chance = 2):
	'''
	@todo: 生成验证码图片
	@param size: 图片的大小，格式（宽，高），默认为(120, 30)
	@param chars: 允许的字符集合，格式字符串
	@param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
	@param mode: 图片模式，默认为RGB
	@param bg_color: 背景颜色，默认为白色
	@param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
	@param font_size: 验证码字体大小
	@param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
	@param length: 验证码字符个数
	@param draw_lines: 是否划干扰线
	@param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
	@param draw_points: 是否画干扰点
	@param point_chance: 干扰点出现的概率，大小范围[0, 100]
	@return: [0]: PIL Image实例
	@return: [1]: 验证码图片中的字符串 
	'''
 
	width, height = size # 宽， 高
	img = Image.new(mode, size, bg_color) # 创建图形
	draw = ImageDraw.Draw(img) # 创建画笔
 
	def get_chars():
		'''生成给定长度的字符串，返回列表格式'''
		return random.sample(chars, length)
 
	def create_lines():
		'''绘制干扰线'''
		line_num = random.randint(*n_line) # 干扰线条数
 
		for i in range(line_num):
			# 起始点
			begin = (random.randint(0, size[0]), random.randint(0, size[1]))
			#结束点
			end = (random.randint(0, size[0]), random.randint(0, size[1]))
			draw.line([begin, end], fill=(0, 0, 0))
 
	def create_points():
		'''绘制干扰点'''
		chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]
		 
		for w in xrange(width):
			for h in xrange(height):
				tmp = random.randint(0, 100)
				if tmp > 100 - chance:
					draw.point((w, h), fill=(0, 0, 0))
 
	def create_strs():
		'''绘制验证码字符'''
		c_chars = get_chars()
		strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开
		 
		font = ImageFont.truetype(font_type, font_size)
		font_width, font_height = font.getsize(strs)
 
		draw.text(((width - font_width) / 3, (height - font_height) / 3),
					strs, font=font, fill=fg_color)
		 
		return ''.join(c_chars)
 
	if draw_lines:
		create_lines()
	if draw_points:
		create_points()
	strs = create_strs()
 
	# 图形扭曲参数
	params = [1 - float(random.randint(1, 2)) / 100,
			0,
			0,
			0,
			1 - float(random.randint(1, 10)) / 100,
			float(random.randint(1, 2)) / 500,
			0.001,
			float(random.randint(1, 2)) / 500
			]
	img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
	
	img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）
 
	return img, strs
def get_img_url(html):#获得图片url
	re_py=r'<img.*?src="([^"]+)"'
	urls_pat=re.compile(re_py)
	img_url=re.findall(urls_pat,html)
	re_py2=r'<IMG.*?src="([^"]+)"'
	urls_pat2=re.compile(re_py2)
	img_url2=re.findall(urls_pat2,html)
	if img_url:
		return img_url
	if img_url2:
		return img_url2
def get_img_url2(htmlstr):
	nowhtml=htmlstr
	for n in range(1,20):
		head = nowhtml.find('<img')
		tail=len(nowhtml)
		if head != -1:
			cut = nowhtml[head:tail]
			src = cut.find('http')
			cut2 = cut[src:tail]
			quo = cut2.find('"')
			url = cut2[0:quo]
			
			cc = nowhtml[head-4:tail]
			dd = cc.find('>')
			ee = cc[0:dd+1]
			
			nowhtml=cut2
	return url
#图片替换
def replacepic(htmlstr):
	nowhtml=htmlstr
	for n in range(1,20):
		head = nowhtml.find('<img')
		tail=len(nowhtml)
		if head != -1:
			cut = nowhtml[head:tail]
			src = cut.find('http')
			cut2 = cut[src:tail]
			quo = cut2.find('"')
			url = cut2[0:quo]
			
			cc = nowhtml[head-4:tail]
			dd = cc.find('>')
			ee = cc[0:dd+1]
			
			if (url.find("13327300632836987")!=-1):
				htmlstr=htmlstr.replace(ee,"")
			nowhtml=cut2
			if (url!=''):
				
				#url=url.replace("http://img1.zz91.com/","")
				#url=url.replace("http://","")
				newpicurl=url
				if (url.find("img3.zz91.com")<0 and url.find("img0.zz91.com")<=0):
					newpicurl="http://img3.zz91.com/300x15000/"+url+""
				newpicurl=newpicurl.replace("http://img1.zz91.com/","")
				#newpicurl=url
				#htmlstr=htmlstr
				htmlstr=htmlstr.replace(url,newpicurl)
				#htmlstr=htmlstr.replace(ee,"")
				#htmlstr=htmlstr.replace("http://img1.zz91.com/bbsPost/2012/3/26/13327300632836987.jpg","")
			#htmlstr=htmlstr.replace("style='margin: 0px; padding: 0px; width: 482px; height: 115px;'","")
	return htmlstr
def havepicflag(htmlstr):
	head = htmlstr.find('<img')
	tail=len(htmlstr)
	if head >0:
		return {'no':1}
	else:
		return None
##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
	if htmlstr:
		#先过滤CDATA
		re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
		re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
		re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
		re_br=re.compile('<br\s*?/?>')#处理换行
		re_h=re.compile('</?\w+[^>]*>')#HTML标签
		re_comment=re.compile('<!--[^>]*-->')#HTML注释
		s=re_cdata.sub('',htmlstr)#去掉CDATA
		s=re_script.sub('',s) #去掉SCRIPT
		s=re_style.sub('',s)#去掉style
		s=re_br.sub('\n',s)#将br转换为换行
		s=re_h.sub('',s) #去掉HTML 标签
		s=re_comment.sub('',s)#去掉HTML注释
		#去掉多余的空行
		blank_line=re.compile('\n+')
		s=blank_line.sub('\n',s)
		s=replaceCharEntity(s)#替换实体
		s=s.replace(" ","")
	else:
		return None
	return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
	CHAR_ENTITIES={'nbsp':' ','160':' ',
				'lt':'<','60':'<',
				'gt':'>','62':'>',
				'amp':'&','38':'&',
				'quot':'"','34':'"',}
   
	re_charEntity=re.compile(r'&#?(?P<name>\w+);')
	sz=re_charEntity.search(htmlstr)
	while sz:
		entity=sz.group()#entity全称，如&gt;
		key=sz.group('name')#去除&;后entity,如&gt;为gt
		try:
			htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
			sz=re_charEntity.search(htmlstr)
		except KeyError:
			#以空串代替
			htmlstr=re_charEntity.sub('',htmlstr,1)
			sz=re_charEntity.search(htmlstr)
	return htmlstr
#时间戳转为正常时间
def timestamp_datetime(value):
	format = '%Y-%m-%d %H:%M:%S'
	value = time.localtime(value)
	dt = time.strftime(format, value)
	return dt
#昨天
def getYesterday():   
	today=datetime.date.today()   
	oneday=datetime.timedelta(days=1)   
	yesterday=today-oneday	
	return yesterday  

#今天	 
def getToday():   
	return datetime.date.today()	 
 
#获取给定参数的前几天的日期，返回一个list   
def getDaysByNum(num):   
	today=datetime.date.today()   
	oneday=datetime.timedelta(days=1)	   
	li=[]		
	for i in range(0,num):   
		#今天减一天，一天一天减   
		today=today-oneday   
		#把日期转换成字符串   
		#result=datetostr(today)   
		li.append(datetostr(today))   
	return li   
 
#将字符串转换成datetime类型  
def strtodatetime(datestr,format):	   
	return datetime.datetime.strptime(datestr,format)   
 
#时间转换成字符串,格式为2008-08-02   
def datetostr(date):	 
	return   str(date)[0:10]   
 
#两个日期相隔多少天，例：2008-10-03和2008-10-01是相隔两天  
def datediff(beginDate,endDate):   
	format="%Y-%m-%d";
	bd=strtodatetime(beginDate,format)   
	ed=strtodatetime(endDate,format)	   
	oneday=datetime.timedelta(days=1)   
	count=0
	if ed>bd:
		while bd!=ed:   
			ed=ed-oneday   
			count+=1 
	return count   
 
#获取两个时间段的所有时间,返回list  
def getDays(beginDate,endDate):   
	format="%Y-%m-%d";   
	bd=strtodatetime(beginDate,format)   
	ed=strtodatetime(endDate,format)   
	oneday=datetime.timedelta(days=1)	
	num=datediff(beginDate,endDate)+1	
	li=[]   
	for i in range(0,num):	
		li.append(datetostr(ed))   
		ed=ed-oneday   
	return li   
 
#获取当前年份 是一个字符串  
def getYear():   
	return str(datetime.date.today())[0:4]	
 
#获取当前月份 是一个字符串  
def getMonth():   
	return str(datetime.date.today())[5:7]   
 
#获取当前天 是一个字符串  
def getDay():
	return str(datetime.date.today())[8:10]	  
def getNow():   
	return datetime.datetime.now()

def getdatelist():
	nyear=getYear()
	nmonth=getMonth()
	yearlist=[]
	monthlist=[]
	for i in range(1,int(nmonth)+1):
		monthlist.append(i)
	for i in range(int(nyear),2004,-1):
		if (i!=int(nyear)):
			monthl=[1,2,3,4,5,6,7,8,9,10,11,12]
		else:
			monthl=monthlist
		list={'year':i,'month':monthl}
		yearlist.append(list)
	return yearlist
def gethtml(url):
	f = urllib.urlopen(url)
	html = f.read()
	return html
def get_access_token():
	appid="wx2891ef70c5a770d6"
	secret="d3f9436cfc50cd9e4f62f96893a1ee0c"
	url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+appid+"&secret="+secret
	ACCESS_TOKEN=json.loads(gethtml(url))['access_token']
	return ACCESS_TOKEN
#获得远程图片宽和高
def getpicturewh(url):
	#url = 'http://img1.zz91.com/ads/1377964800000/f53cb9e8-8fc5-4bf1-ae3b-468f5f814da0.gif'
	file = urllib.urlopen(url)
	tmpIm = StringIO.StringIO(file.read())
	im = Image.open(tmpIm)
	isize={'width':im.size[0],'height':im.size[1]}
	return isize
def getreplacepic(content):
	if content:
		co=content.replace("/uploads/uploads/media/","http://pyapp.zz91.com/app/changepic.html?height=300&width=300&url=http://newsimg.zz91.com/uploads/uploads/media/")
		return co
def getIPFromDJangoRequest(request):
	if 'HTTP_X_FORWARDED_FOR' in request.META:
		return request.META.get('HTTP_X_FORWARDED_FOR')
	else:
		return request.META.get('REMOTE_ADDR')
def validateEmail(email):
	if len(email) > 5:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
		   return 1
	return 0
def getloginurl(url):
	if url:
		url=url.replace("&","^and^")
		url=url.replace("#","^jing^")
		url=url.replace("?","^wenhao^")
	return url
def getlogintourl(tourl):
	if tourl:
		tourl=tourl.replace("^and^","&")
		tourl=tourl.replace("%5Eand%5E","&")
		tourl=tourl.replace("^jing^","#")
		tourl=tourl.replace("%5Ejing%5E","#")
		tourl=tourl.replace("^wenhao^","?")
		tourl=tourl.replace("%5Ewenhao%5E","?")
	return tourl
def remove_script(html):#移除script
	if '<script' in html:
		re_py=r'<script.*?</script>'
		urls_pat=re.compile(re_py,re.DOTALL)
		img_url=re.findall(urls_pat,html)
		for img_url in img_url:
			html=html.replace(img_url,'')
	return html
def remove_content_a(html):#移除a链接
	html=re.sub('<A.*?>','',html)
	html=re.sub('</A>','',html)
	html=re.sub('<a.*?>','',html)
	html=re.sub('style=".*?"','',html)
	html=re.sub('</a>','',html)
	return html
#替换可拨打电话
def replacetel(content):
	if content:
		rpl1=re.findall('[0-9\ ]+',content)
		for r1 in rpl1:
			if len(r1)>10 and len(r1)<=12:
				if 'tel:' in r1:
					content=content
				else:
					content=content.replace(r1,'<a href="tel:'+r1+'">'+r1+'</a>')
	return content
def replaceurl(content):
	if content:
		regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
		regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)
		s=regex.findall(content)
		for l in s:
			if "http://" in l:
				content=content
			else:
				content=content.replace(l,"<a href='"+l+"'>"+l+"</a>")
	return content
def remove_content_value(html):#移除a链接
	html=re.sub('<A.*?>','',html)
	html=re.sub('</A>','',html)
	html=re.sub('<a.*?>','',html)
	html=re.sub('</a>','',html)
	html=re.sub('</div>','',html)
	html=re.sub('<table.*?>','',html)
	html=re.sub('<tr.*?>','',html)
	html=re.sub('<td.*?>','',html)
	html=re.sub('</table>','',html)
	html=re.sub('</tr>','',html)
	html=re.sub('</td>','',html)
	html=re.sub('\r','',html)
	html=re.sub('\n','',html)
	html=re.sub('\t','',html)
	html=re.sub('<tbody.*?>','',html)
	html=re.sub('<tbody.*?>','',html)
	html=re.sub('<!--.*?-->','',html)
	html=re.sub('<span.*?>','',html)
	html=re.sub('</span>','',html)
	
	html=re.sub('<wb.*?>','',html)
	html=re.sub('</wb.*?>','',html)
	html=re.sub('<iframe.*?>','',html)
	html=re.sub('</iframe>','',html)
	
	html=re.sub('<h.*?>','',html)
	html=re.sub('</h.*?>','',html)
	html=re.sub('<li.*?>','',html)
	html=re.sub('</li>','<br />',html)
	html=re.sub('<ul.*?>','',html)
	html=re.sub('</ul>','',html)
	html=re.sub('<ol.*?>','',html)
	html=re.sub('</ol>','',html)
	
	html=re.sub('<div.*?>','',html)
	html=re.sub('</div>','<br />',html)
	
	html=re.sub('align=".*?"','',html)
	
	html=re.sub('STYLE=".*?"','',html)
	html=re.sub('style=".*?"','',html)
	html=re.sub('class=".*?"','',html)
	html=re.sub('ALIGN=".*?"','',html)
	html=re.sub('align=center','',html)
	html=re.sub('width=".*?"','',html)
	html=re.sub('height=".*?"','',html)
	html=re.sub('<input.*?>','',html)
	html=re.sub('<blockquote.*?>','',html)
	html=re.sub('</blockquote>','',html)
	
	
	return html
def page404(request):
	nowlanmu="<a href='/'>页面不存在</a>"
	t = get_template('404.html')
	html = t.render(Context({'nowlanmu':nowlanmu}))
	return HttpResponseNotFound(html)

#微信发送定制商家
def weixinorder(weixinid):
	if weixinid[0:3]=="okX":
		wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
	else:
		wxc = Client(weixinconfig['zz91dingyue']['appid'], weixinconfig['zz91dingyue']['secret'])
	Url="http://m.zz91.com/wechat/auth_login.html?clientid="+str(weixinid)
	token=wxc.send_text_message(weixinid,"商机订阅！\n <a href='"+Url+"&tourl=/order/price.html'>点此订阅行情。</a>\n <a href='"+Url+"&tourl=/order/business.html'>点此订阅供求。</a>")
#关注语
def subscribewelcome(weixinid):
	if weixinid[0:3]=="okX":
		wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
	else:
		wxc = Client(weixinconfig['zz91dingyue']['appid'], weixinconfig['zz91dingyue']['secret'])
	title="感谢关注ZZ91再生网,从今儿起，再生君就可以在微信给亲提供最新废料行情和供求商机啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(weixinid)+"'>点击绑定ZZ91再生网帐号</a>！\n\n <a href='http://m.zz91.com/register/?weixinid="+str(weixinid)+"'>木有帐号？用3秒钟注册一个</a>\n"
	token=wxc.send_text_message(weixinid,title)
#关注语
def sendweixinmsg(weixinid,title):
	if weixinid[0:3]=="okX":
		wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
	else:
		wxc = Client(weixinconfig['zz91dingyue']['appid'], weixinconfig['zz91dingyue']['secret'])
	#title="感谢关注ZZ91再生网,从今儿起，再生君就可以在微信给亲提供最新废料行情和供求商机啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(weixinid)+"'>点击绑定ZZ91再生网帐号</a>！\n\n <a href='http://m.zz91.com/register/?weixinid="+str(weixinid)+"'>木有帐号？用3秒钟注册一个</a>\n"
	token=wxc.send_text_message(weixinid,title)
	
#pc登录成功提醒
def loginsuctishi(weixinid):
	if weixinid[0:3]=="okX":
		wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
	else:
		wxc = Client(weixinconfig['zz91dingyue']['appid'], weixinconfig['zz91dingyue']['secret'])
	title="微信认证完毕，电脑端将自动登录，如未能登录，请点击电脑端”确认扫描登录“"
	token=wxc.send_text_message(weixinid,title)
#错误帮助
def weixinhelp(weixinid):
	if weixinid[0:3]=="okX":
		wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
	else:
		wxc = Client(weixinconfig['zz91dingyue']['appid'], weixinconfig['zz91dingyue']['secret'])
	title='使用帮助：\r\n'
	title+='==============\r\n'
	title+='除了菜单外\r\n'
	title+="您还可以：\r\n"
	title+="1、查看报价：\r\n回复：地区+产品+报价 \n如：上海废铝报价、国内PP报价\r\n"
	title+="2、查看供求：\r\n回复：供求+产品名称 \r\n如：求购PP、供应废铁\r\n"
	title+="3、微信打卡活动：\r\n回复：打卡\r\n"
	title+="4、电脑端微信认证：\r\n回复：1\r\n"
	#title+="查看“企业库”，\n回复：企业\n"
	title+="5、查看再生网“联系方式”，\r\n回复：联系\r\n"
	title+="6、查看再生网“支付方式”，\r\n回复：支付\r\n"
	title+='==============\r\n'
	#title+='更多下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
	#title+="“AQSIQ咨询”，\n回复：aqsiq\n"
	token=wxc.send_text_message(weixinid,title)
#阿里大于短信系统
def postsms_dayu(mobile,sms_template_code,sms_free_sign_name,sms_param):
	req = top.api.AlibabaAliqinFcSmsNumSendRequest()
	req.set_app_info(top.appinfo("23410861", "72b4d7f51b757714b946d82ff9376a55"))
	req.sms_type = "normal"
	req.rec_num = mobile
	req.sms_template_code=sms_template_code
	req.sms_free_sign_name=sms_free_sign_name
	req.sms_param = json.dumps(sms_param,ensure_ascii=False,indent=2)
	try:
		resp= req.getResponse()
		if resp.get('alibaba_aliqin_fc_sms_num_send_response').get('result').get('success')==True:
			return True
		else:
			return False
	except Exception,e:
		return False
#----发手机短信
def postsms(mobile,username,userid):
	sqlp="select TIMESTAMPDIFF(SECOND,gmt_created,now()) as ltime from auth_forgot_password_log where company_id=%s and DATEDIFF(CURDATE(),gmt_created)<1 order by gmt_created desc"
	plist=dbc.fetchalldb(sqlp,[userid])
	pcount=len(plist)
	if (pcount<10):
		if plist:
			ltime=plist[0][0]
			if ltime<=60:
				return '验证码已经发送，一分钟内请不要重复提交！'
		tmp = random.randint(10000, 99999)
		#content="欢迎使用ZZ91再生网服务。验证码是："+str(tmp)+",输入验证码继续完成操作，该验证码10分钟内输入有效。"
		#url="http://mt.10690404.com/send.do?Account=astokf&Password=C@4k@33lsbe2lw^6&Mobile="+str(mobile)+"&Content="+content+"&Exno=0"
		#f = urllib.urlopen(url)
		#html = f.read()
		#o = json.loads(html)
		
		sms_template_code="SMS_12520535"
		sms_free_sign_name="ZZ91再生网"
		smscontent=r'验证是：(.*?)，请勿泄露'
		code=tmp
		sms_param={"code": str(code), "product": "ZZ91再生网"}
		returnsms=postsms_dayu(mobile[0:11],sms_template_code,sms_free_sign_name,sms_param)
		
		gmt_created=datetime.datetime.now()
		sql="insert into auth_forgot_password_log(company_id,type,gmt_created,gmt_modified) values(%s,%s,%s,%s)"
		dbc.updatetodb(sql,[userid,1,gmt_created,gmt_created]);
		sqlp="select id from auth_forgot_password where username=%s and userid=%s order by id desc"
		plist=dbc.fetchonedb(sqlp,[username,userid]);
		if not plist:
			sql="insert into auth_forgot_password(username,userid,auth_key,gmt_created) values(%s,%s,%s,%s)"
			dbc.updatetodb(sql,[username,userid,tmp,gmt_created]);
		else:
			sql="update auth_forgot_password set auth_key=%s,gmt_created=%s where id=%s"
			dbc.updatetodb(sql,[tmp,gmt_created,plist[0]]);
		return True
	else:
		return "您已经超过了每天发生10条短信的限制！"
#微信绑定抽奖 2015-12-7  2016-1-7
#端午抽奖  2016-6-2 2016-6-7
def choujiang(account="",company_id="",weixinid=""):
	format="%Y-%m-%d"
	gmt_created=getNow()
	beginDate="2016-6-2"
	endDate="2016-6-7"
	nowdate=date_to_int(getToday())
	endDate=date_to_int(strtodatetime(endDate,format))
	
	if nowdate>endDate:
		return None
	if nowdate<date_to_int(strtodatetime(beginDate,format)):
		return None
	
	bnum=1
	btype=1
	jiangpin=-1
	if account:
		sql="select company_id from company_account where account=%s"
		result=dbc.fetchonedb(sql,[account])
		if result:
			company_id=result[0]
	if weixinid:
		sqlc="select id from oauth_access where open_id=%s and open_type='weixin.qq.com' and gmt_created>'"+beginDate+"'"
		list=dbc.fetchonedb(sqlc,[str(weixinid)])
		if list:
			if company_id:
				sql="select id from subject_choujiang where company_id=%s and btype=1"
				result=dbc.fetchonedb(sql,[company_id])
				if not result:
					sql="insert into subject_choujiang(btype,gmt_created,bnum,company_id,jiangpin) values(%s,%s,%s,%s,%s)"
					dbc.updatetodb(sql,[btype,gmt_created,bnum,company_id,jiangpin])
					if weixinid[0:3]=="okX":
						wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
					else:
						wxc = Client(weixinconfig['zz91dingyue']['appid'], weixinconfig['zz91dingyue']['secret'])
					token=wxc.send_text_message(weixinid,"恭喜你获得一次抽奖机会，马上登录即可，即可获取iphone6s，<a href='http://m.zz91.com/choujiang/index.html?mid="+str(company_id)+">点此抽奖</a>")
					return company_id
#2016台州塑交会抽奖
def taizhou2016(weixinid=""):
	gmt_created=getNow()
	bnum=1
	jiangpin=-1
	btype=7
	if weixinid:
		sqlc="select id,target_account from oauth_access where open_id=%s and open_type='weixin.qq.com'"
		list=dbc.fetchonedb(sqlc,[str(weixinid)])
		if list:
			account=list[1]
			sql="select company_id from company_account where account=%s"
			result=dbc.fetchonedb(sql,[account])
			if result:
				company_id=result[0]
				sql="select id from subject_choujiang where company_id=%s and btype=7"
				result=dbc.fetchonedb(sql,[company_id])
				if not result:
					sql="insert into subject_choujiang(btype,gmt_created,bnum,company_id,jiangpin) values(%s,%s,%s,%s,%s)"
					dbc.updatetodb(sql,[btype,gmt_created,bnum,company_id,jiangpin])
					#token=wxc.send_text_message(weixinid,"恭喜你获得一次抽奖机会，马上登录抽奖，<a href='http://m.zz91.com/taizhou2016/index.html?mid="+str(company_id)+">点此抽奖</a>")
					return company_id
		else:
			#token=wxc.send_text_message(weixinid,"你还未绑定ZZ91再生网账号， <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(weixinid)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/register/?weixinid="+str(weixinid)+"'>木有帐号？用3秒钟注册一个</a>")
			return ''
	return None
def search_strong(search,title):
	search=search.replace(' ','')
	if re.findall('^[A-Z]+',search):
		title=re.sub(search,'<font color="red">'+search+'</font>',title)
		if '<font' not in title:
			losearch=search.lower()
			title=re.sub(losearch,'<font color="red">'+losearch+'</font>',title)
	elif re.findall('^[a-z]+',search):
		title=re.sub(search,'<font color="red">'+search+'</font>',title)
		if '<font' not in title:
			upsearch=search.upper()
			title=re.sub(upsearch,'<font color="red">'+upsearch+'</font>',title)
	else:
		searcht=split_str(search.decode('utf8'))
		title=title.decode('utf8')
		for s1 in searcht:
			title=title.replace(s1,u'<font color="red">'+s1+u'</font>')
	return title
def split_str(chinese):#传入的汉字分成一个一个的
	c=[]
	l=1
	len_c=range(0,len(chinese)/l)
	for lenn in len_c:
		ag=lenn*l
		ed=lenn*l+l
		c.append(chinese[ag:ed])
	return c 
	