import re
def getproductsinfo(pdtid,keywords):
	prolist=cache.get("zz91cp_pro"+str(pdtid))
	if prolist:
		return prolist
	if keywords:
		keywords=keywords.replace('\\','')
		keywords=keywords.replace('/','')
		keywords=keywords.replace('/','')
		keywords=keywords.replace('(','')
		keywords=keywords.replace(')','')
		keywords=keywords.replace('+','')
	sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%Y/%m/%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit,p.quantity,DATE_FORMAT(p.expire_time,'%Y-%m-%d'),DATEDIFF(p.expire_time,CURDATE()) as yxtime,p.quantity_unit,f.label,c.address,DATE_FORMAT(c.regtime,'%Y-%m-%d'),c.area_code,p.check_status,p.tags,p.source,p.specification,p.impurity,p.color,p.useful,p.appearance,p.manufacture,p.origin FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code left outer join category_products as f on p.category_products_main_code=f.code where p.id="+str(pdtid)+""
	#cursor.execute(sql)
	#productlist = cursor.fetchone()
	productlist=dbc.fetchonedb(sql)
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
		arrviptype={'vippic':'','vipname':'','vipclass':'','vipsubname':'','vipcheck':'','com_fqr':'','zstNum':'','ldb':''}
		if (viptype == '10051000'):
			arrviptype['vippic']=None
			arrviptype['vipname']='普通会员'
		if (viptype == '10051001'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/recycle.gif'
			arrviptype['vipname']='再生通'
			arrviptype['vipclass']='zst_logo'
		if (viptype == '100510021000'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptSilver.gif'
			arrviptype['vipname']='银牌品牌通'
			arrviptype['vipclass']='ypppt_logo'
		if (viptype == '100510021001'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptGold.gif'
			arrviptype['vipname']='金牌品牌通'
			arrviptype['vipclass']='jpppt_logo'
		if (viptype == '100510021002'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptDiamond.gif'
			arrviptype['vipname']='钻石品牌通'
			arrviptype['vipclass']='zsppt_logo'
		if (viptype == '10051003'):
			arrviptype['vippic']=''
			arrviptype['vipname']='来电宝客户'
			arrviptype['vipclass']='ldb_logo'
		if (viptype == '10051000'):
			arrviptype['vipcheck']=None
		else:
			arrviptype['vipcheck']=1
		#来电宝客户
		if (productlist[0]):
			sqll="select id from crm_company_service where company_id="+str(productlist[0])+" and crm_service_code in(1007,1008,1009,1010,1011) and apply_status=1"
			#cursor.execute(sqll)
			#ldbresult=cursor.fetchone()
			ldbresult=dbc.fetchonedb(sqll)
			if ldbresult:
				sqlg="select front_tel from phone where company_id="+str(productlist[0])+" and expire_flag=0"
				#cursor.execute(sqlg)
				#phoneresult=cursor.fetchone()
				phoneresult=dbc.fetchonedb(sqlg)
				if phoneresult:
					arrviptype['ldb']={'ldbphone':phoneresult[0]}
				else:
					arrviptype['ldb']=None
			else:
				arrviptype['ldb']=None
		arrviptype['vipsubname'] = productlist[7]
		arrviptype['com_fqr']=''
		com_province=productlist[10]
		if (com_province==None):
			com_province=''
		pdt_images=""
		area_code=productlist[21]
		#地区信息
		if (area_code):
			sqld="select label from category where code='"+str(area_code[:-4])+"'"
			#cursor.execute(sqld)
			#arealabel = cursor.fetchone()
			arealabel=dbc.fetchonedb(sqld)
			if arealabel:
				if arealabel[0]:
					com_province=arealabel[0]+' '+com_province
					
		arrcompinfo=None
		if (productlist[0]):
			sqld="select qq from company_account where company_id=%s"
			compqq=dbc.fetchonedb(sqld,[productlist[0]])
			if compqq:
				qq=compqq[0]
				if qq:
					qq=qq.strip()
				if (qq==""):
					qq=None
			
				if (qq):
					arrcompinfo={'qq':qq}
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
		#
		if (price_unit==None):
			price_unit=''
		else:
			if (allprice!=''):
				allprice=allprice+price_unit
				
		total_quantity=productlist[14]
		quantity_unit=productlist[17]
		if (quantity_unit==None):
			quantity_unit=''
		if (total_quantity=='' or total_quantity==' ' or total_quantity==None):
			total_quantity=None
		else:
			total_quantity=total_quantity+quantity_unit

		procatetype=productlist[18]
		if (procatetype!=None):
			procatetype=procatetype.replace('|',' ')
			procatetype=procatetype.replace('\\',' ')
			procatetype=procatetype.replace('/',' ')
			procatetype=procatetype.replace('(',' ')
			procatetype=procatetype.replace(')',' ')
		#----
		sql1="select pic_address from products_pic where product_id="+str(productlist[2])+" order by is_default desc,id desc"
		#cursor.execute(sql1)
		#productspic = cursor.fetchone()
		productspic=dbc.fetchonedb(sql1)
		if productspic:
			pdt_images=productspic[0]
		else:
			pdt_images=""
		if (pdt_images == '' or pdt_images == '0'):
			pdt_images='../cn/img/noimage.gif'
			ispropic=None
		else:
			pdt_images='http://img3.zz91.com/220x180/'+pdt_images+''
			ispropic=1
		#发起人标志
		company_id=productlist[0]
		zs=None
		cxcompany=None
		if (company_id!=None):
			sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001001' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
			fqrflag=dbc.fetchonedb(sql1)
			if fqrflag:
				fqr=1
			else:
				fqr=None
			
			#诚信会员
			sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001005' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
			cxflag=dbc.fetchonedb(sql1)
			if cxflag:
				cxcompany=1
			else:
				cxcompany=None

			#终生会员
			sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001003' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
			zsflag=dbc.fetchonedb(sql1)
			if zsflag:
				zs=1
			else:
				zs=None
			zst_year=0
			#年限
			sql2="select sum(zst_year) from crm_company_service where company_id="+str(company_id)+" and apply_status=1"
			zstNumvalue=dbc.fetchonedb(sql2)
			if zstNumvalue:
				zst_year=zstNumvalue[0]
			arrviptype['zstNum']=zst_year
		else:
			fqr=None
		#供求更多属性
		sqlm="select property,content from product_addproperties where pid=%s"
		resultmore=dbc.fetchalldb(sqlm,[productlist[2]])
		listmore=[]
		if resultmore:
			for ll in resultmore:
				if (ll[1]!=None):
					contentp=ll[1].strip()
					if (contentp==""):
						contentp=None
				else:
					contentp=None
				list={'property':ll[0],'content':contentp}
				listmore.append(list)
		source=productlist[24]
		listmore=getmoreproperty(listmore,'货源地',source)
		origin=productlist[31]
		listmore=getmoreproperty(listmore,'来源产品',origin)
		specification=productlist[25]
		listmore=getmoreproperty(listmore,'产品规格',specification)
		impurity=productlist[26]
		listmore=getmoreproperty(listmore,'杂质含量',impurity)
		color=productlist[27]
		listmore=getmoreproperty(listmore,'颜色',color)
		useful=productlist[28]
		listmore=getmoreproperty(listmore,'用途',useful)
		appearance=productlist[29]
		listmore=getmoreproperty(listmore,'外观',appearance)
		manufacture=productlist[30]
		
		#询盘量
		questioncount=None
		tagslist=[]
		pdt_name=productlist[4]
		list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
		,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5]
		,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype,'check_status':productlist[22]
		,'pdt_images':pdt_images,'pdt_price':allprice
		,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'fqr':fqr
		,'cxcompany':cxcompany,'total_quantity':total_quantity,'procatetype':procatetype
		,'zs':zs,'xianhuoid':'','questioncount':questioncount,'tagslist':tagslist
		,'arrcompinfo':arrcompinfo,'listmore':listmore,'ispropic':ispropic}
	else:
		list1=None

	#list1=getproid(pdtid)
	if (list1 == None):
		return None
	else:
		pdt_images=list1['pdt_images']
		if (pdt_images=='../cn/img/noimage.gif'):
			list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
		pdt_detail=filter_tags(list1['pdt_detail'])
		pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
		docs=[pdt_detail]
		list1['pdt_detail']=subString(pdt_detail,300)+'...'
		"""
		sqlxx="select id from products_spot where product_id=%s"
		cursor.execute(sqlxx,[pdtid])
		result=cursor.fetchone()
		if result:
			list1['xianhuoid']=result[0]
		else:
			list1['xianhuoid']=None
		"""
		pdt_name=list1['pdt_name']
		docs=[pdt_name]
		#for k in keywords:
			#pdt_name=pdt_name.replace(k,'<em>'+k+'</em>')
		list1['pdt_name']=pdt_name	
		cache.set("zz91cp_pro"+str(pdtid),list1,60*60)
	return list1
def getadlistkeywords(pkind,keywords):
	prolist=cache.get("zz91cp_adkeylist"+str(pkind)+str(keywords))
	if prolist:
		return prolist
	adid="0"
	adidlist="0"
	sqlp="select ad_id from ad_exact_type where ad_position_id=%s and anchor_point=%s"
	alist=dbads.fetchalldb(sqlp,[pkind,keywords])
	if alist:
		for aid in alist:
			ad_id=aid[0]
			adidlist+=","+str(ad_id)
			#adidlist.append(ad_id)
	#if adidlist:
		#adid=adidlist[0]
	#return adidlist	
	sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and id in ("+str(adidlist)+") and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
	alist=dbads.fetchalldb(sql,[pkind])
	listvalue=[]
	if alist:
		for list in alist:
			list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}
			listvalue.append(list1)
	cache.set("zz91cp_adkeylist"+str(pkind)+str(keywords),listvalue,60*30)
	return listvalue
def getmoreproperty(listmore,text,value):
	if (value!="" and value!=None):
		value=value.strip()
		listmore.append({'property':text,'content':value})
	return listmore
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
	if length >= len(string):   
		return string   
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
#mc = memcache.Client(['192.168.110.119:11211'],debug=0)

 
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
			nowhtml=cut2
			url=url.replace("img1.zz91.com/","")
			newpicurl="http://img3.zz91.com/600x600/"+url+""
			htmlstr=htmlstr.replace(url,newpicurl)
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

#获得远程图片宽和高
def getpicturewh(url):
	#url = 'http://img1.zz91.com/ads/1377964800000/f53cb9e8-8fc5-4bf1-ae3b-468f5f814da0.gif'
	file = urllib.urlopen(url)
	tmpIm = StringIO.StringIO(file.read())
	im = Image.open(tmpIm)
	isize={'width':im.size[0],'height':im.size[1]}
	return isize
#加密
def getjiami(strword):
	return strword.encode('utf8','ignore').encode("hex")
def getjiemi(strword):
	return strword.decode("hex").decode('utf8','ignore')