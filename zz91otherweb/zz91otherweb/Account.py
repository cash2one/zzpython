#-*- coding: UTF-8 -*-
#！/usr/bin/python

class Account:
	id = ''
	name = ''
	contact =''
	mobile = ''
	address= ''
	
	
	
	def __init__(self,id,name,contact,mobile,address):
		self.id = id
		self.name = name
		self.contact = contact
		self.mobile = mobile
		self.address= address
		
		
	
	def printComany(self):
			print 'id',id,'name',name,'contact',contact,'mobile',mobile,'address',address

