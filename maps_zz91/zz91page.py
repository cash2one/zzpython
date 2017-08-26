from math import ceil
class zz91page:
	def __init__ (self):
		self._limitNum          = 20
		self._nowpage           = 1
		self._frompageCount     = 0
		self._after_range_num   = 2
		self._before_range_num  = 9
		self._firstpage         = None
		self._lastpage          = None
		self._page_range        =[]
		self._listcount         =0
		self._page_listcount    =0
		self._nextpage          =0
		self._prvpage           =0
		
		
	def limitNum(self , Num):
		if(Num==None):
			return self._limitNum
		else:
			self._limitNum=Num
			return Num
	
	def nowpage(self , page):
		if(page==None):
			return self._nowpage
		else:
			self._nowpage=page
			return page
	
	def after_range_num(self , Num):
		if(Num==None):
			return self._after_range_num
		else:
			self._after_range_num=Num
			return Num
	def before_range_num(self , Num):
		if(Num==None):
			return self._before_range_num
		else:
			self._before_range_num=Num
			return Num
	
	def frompageCount(self):
		self._frompageCount=self._limitNum*(int(self._nowpage)-1)
		return self._limitNum*(int(self._nowpage)-1)
		
	def listcount(self , Num):
		if(Num==None):
			return self._listcount
		else:
			self._listcount=Num
			return Num
	def page_listcount(self):
		self._page_listcount=int(ceil(self._listcount / self._limitNum))+1
		return int(ceil(self._listcount / self._limitNum))+1
		
	
	def firstpage(self):
		if (self._page_listcount>1 and self._nowpage>1):
			self._firstpage=1
			return 1
		else:
			self._firstpage=None
			return None
	
	def lastpage(self):
		if (self._page_listcount > 1 and self._nowpage < self._page_listcount):
			self._lastpage=1
			return 1
		else:
			self._lastpage=None
			return None
	def page_range(self):
		page_rangep=[]
		i=1
		while (i<=self._page_listcount):
			pages={'number':'','nowpage':''}
			pages['number']=i
			if (i==self._nowpage):
				pages['nowpage']='1'
			else:
				pages['nowpage']=None
				
			page_rangep.append(pages)
			i+=1
		if self._nowpage >= self._after_range_num:
			return page_rangep[self._nowpage-self._after_range_num:self._nowpage + self._before_range_num]
		else:
			return page_rangep[0:int(self._nowpage) + self._before_range_num]
	
	def nextpage(self):
		self._nextpage=self._nowpage+1
		return self._nowpage+1
	def prvpage(self):
		self._prvpage=self._nowpage-1
		return self._nowpage-1
		
		