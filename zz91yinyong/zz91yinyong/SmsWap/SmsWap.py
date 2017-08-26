#!-*- coding:utf-8 -*-
'''
Created on 2013-12-25
@author: shangwei
'''

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as pk
from hashlib import sha1
from rsa import key, common, encrypt
from urllib import urlencode
import Gl
import base64
import hmac
import json
import random
import time
import urllib
import urllib2
import webbrowser

class MerchantAPI:
    
    def doPost(self,url,values):
        '''
        post请求
        参数URL
        字典类型的参数
        '''
        req = urllib2.Request(url)
        data = urllib.urlencode(values)
        res = urllib2.urlopen(req, data)
        ret = res.read()
        return ret

    
    def doGet(self,url,values):
        '''
        get请求
        参数URL
        字典类型的参数
        '''
        REQUEST = url + "?" + urllib.urlencode(values)
        ret = urllib2.urlopen(REQUEST).read()  
        return ret
      
    @staticmethod
    def _pkcs7padding(data):
        """
        对齐块
        size 16
        999999999=>9999999997777777
        """
        size = AES.block_size
        count = size - len(data)%size
        if count:
            data+=(chr(count)*count)
        return data
    
    

    
    
    @staticmethod
    def _depkcs7padding(data):
        """
        反对齐
        """
        newdata = '' 
        for c in data:
            if ord(c) > AES.block_size:
                newdata+=c
        return newdata
    
    
    '''
    aes加密base64编码
    '''
    def aes_base64_encrypt(self,data,key):
        
        """
        @summary: 
            1. pkcs7padding
            2. aes encrypt
            3. base64 encrypt
        @return: 
            string
        """
        cipher = AES.new(key)
        return base64.b64encode(cipher.encrypt(self._pkcs7padding(data)))


    def base64_aes_decrypt(self,data,key):
        """
        1. base64 decode
        2. aes decode
        3. dpkcs7padding
        """
        cipher = AES.new(key)
        return self._depkcs7padding(cipher.decrypt(base64.b64decode(data)))        
        
    '''
    rsa加密
    '''
    def rsa_base64_encrypt(self,data,key):
        '''
        1. rsa encrypt
        2. base64 encrypt
        '''
        cipher = PKCS1_v1_5.new(key) 
        return base64.b64encode(cipher.encrypt(data))
    
    def rsa_base64_decrypt(self,data,key):
        '''
        1. base64 decrypt
        2. rsa decrypt
        示例代码
        
       key = RSA.importKey(open('privkey.der').read())
        >>>
        >>> dsize = SHA.digest_size
        >>> sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15
        >>>
        >>> cipher = PKCS1_v1_5.new(key)
        >>> message = cipher.decrypt(ciphertext, sentinel)
        >>>
        >>> digest = SHA.new(message[:-dsize]).digest()
        >>> if digest==message[-dsize:]:                # Note how we DO NOT look for the sentinel
        >>>     print "Encryption was correct."
        >>> else:
        >>>     print "Encryption was not correct."
        '''
        cipher = PKCS1_v1_5.new(key)
        return cipher.decrypt(base64.b64decode(data), Random.new().read(15+SHA.digest_size))
        
    '''
    RSA签名
    '''
    def sign(self,signdata):
        '''
        @param signdata: 需要签名的字符串
        '''
        
        h=SHA.new(signdata)
        signer = pk.new(Gl.privatekey)
        signn=signer.sign(h)
        signn=base64.b64encode(signn)
        return  signn
       
    '''
    RSA验签
    结果：如果验签通过，则返回The signature is authentic
         如果验签不通过，则返回"The signature is not authentic."
    '''
    def checksign(self,rdata):
        
        signn=base64.b64decode(rdata.pop('sign'))
        signdata=self.sort(rdata)
#        print "signdata="+signdata
        verifier = pk.new(Gl.publickey)
        if verifier.verify(SHA.new(signdata), signn):
            print "The signature is authentic."
        else:
            print "The signature is not authentic."
         
    
        
        
    
    def sort(self,mes):
        '''
        作用类似与java的treemap,
        取出key值,按照字母排序后将value拼接起来
        返回字符串
        '''
        _par = []
       
        keys=mes.keys()
        keys.sort()
        for v in keys:
            _par.append(str(mes[v]))
        sep=''
        message=sep.join(_par)
        return message
    
    '''
    请求接口前的加密过程
    '''
    def requestprocess(self,mesdata):
        '''
        加密过程：
        1、将需要的参数mes取出key排序后取出value拼成字符串signdata
        2、用signdata对商户私钥进行rsa签名，生成签名signn，并转base64格式
        3、将签名signn插入到mesdata的最后生成新的data
        4、用encryptkey16位常量对data进行AES加密后转BASE64,生成机密后的data
        5、用易宝公钥publickey对encryptkey16位常量进行RSA加密BASE64编码，生成加密后的encryptkey
        '''
        signdata=self.sort(mesdata)
        print '需要签名的排序后的字符串为：'+signdata       
        signn=self.sign(signdata)

          
        mesdata['sign']=signn
        print mesdata
        encryptkey = '1234567890123456'
        data=self.aes_base64_encrypt(json.dumps(mesdata),encryptkey)
    
        print '加密后的data='+data
        values={}
        values['merchantaccount']=Gl.merchantaccount
        values['data']=data
        values['encryptkey']=self.rsa_base64_encrypt(encryptkey,Gl.publickey)
        return values


    
    
    '''
    对返回结果进行解密后输出
    '''
    def result_decrypt(self,result):
        '''
        1、返回的结果json传给data和encryptkey两部分，都为加密后的
        2、用商户私钥对encryptkey进行RSA解密，生成解密后的encryptkey。参考方法：rsa_base64_decrypt
        3、用解密后的encryptkey对data进行AES解密。参考方法：base64_aes_decrypt
        '''
        result=json.loads(result)
        kdata=result['data']
        kencryptkey=result['encryptkey']
        print '返回的加密后的data='+kdata
        print '返回的加密后的encryptkey='+kencryptkey
        cryptkey=self.rsa_base64_decrypt(kencryptkey,Gl.privatekey)
        print '解密后的encryptkey='+cryptkey
        rdata=self.base64_aes_decrypt(kdata,cryptkey)
        print '解密后的data='+rdata
        return rdata
    def result_decrypt1(self,result):
        '''
        1、返回的结果json传给data和encryptkey两部分，都为加密后的
        2、用商户私钥对encryptkey进行RSA解密，生成解密后的encryptkey。参考方法：rsa_base64_decrypt
        3、用解密后的encryptkey对data进行AES解密。参考方法：base64_aes_decrypt
        '''
        #result=json.loads(result)
        kdata=result['data']
        kencryptkey=result['encryptkey']
        print '返回的加密后的data='+kdata
        print '返回的加密后的encryptkey='+kencryptkey
        cryptkey=self.rsa_base64_decrypt(kencryptkey,Gl.privatekey)
        print '解密后的encryptkey='+cryptkey
        rdata=self.base64_aes_decrypt(kdata,cryptkey)
        print '解密后的data='+rdata
        return rdata
    
    '''
   	PC网页收银台
    '''
    def testwap_credit(self,merchantaccount,orderid,orderexpdate,transtime,currency,amount,productcatalog,userua,productname,productdesc,userip,identityid,identitytype,terminalid,terminaltype,other,callbackurl,fcallbackurl,paytypes):
        mesdata={"merchantaccount":merchantaccount,"orderid":orderid,"orderexpdate":orderexpdate,"transtime":transtime,"currency":currency,"amount":amount,"productcatalog":productcatalog,"userua":userua,"productname":productname,"productdesc":productdesc,"userip":userip,"identityid":identityid,"identitytype":identitytype,"terminalid":terminalid,"teminaltype":terminaltype,"other":other,"callbackurl":callbackurl,"fcallbackurl":fcallbackurl,"paytypes":paytypes}
        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/payweb/api/pay/request'

        REQUEST = url + "?" + urllib.urlencode(values)
        return REQUEST
        #print urllib.urlencode(values)
        #webbrowser.open_new_tab(REQUEST)   
    
    '''
    移动终端网页收银台
    '''
    def testwap_credit(self,merchantaccount="",orderid="",orderexpdate="",transtime="",currency="",amount="",productcatalog="",userua="",productname="",productdesc="",userip="",identityid="",identitytype="",callbackurl="",fcallbackurl="",paytypes="",terminaltype="",terminalid=""):
        mesdata={"merchantaccount":merchantaccount,"orderid":orderid,"orderexpdate":orderexpdate,"transtime":transtime,"currency":currency,"amount":amount,"productcatalog":productcatalog,"userua":userua,"productname":productname,"productdesc":productdesc,"userip":userip,"identityid":identityid,"identitytype":identitytype,"callbackurl":callbackurl,"fcallbackurl":fcallbackurl,"paytypes":paytypes,"terminaltype":terminaltype,"terminalid":terminalid}
        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/paymobile/api/pay/request'
        REQUEST = url + "?" + urllib.urlencode(values)
        return REQUEST
        #print urllib.urlencode(values)
        #webbrowser.open_new_tab(REQUEST)   

    '''
    绑卡支付异步接口
    '''
    def testBindPaysignAsync(self,merchantaccount,bindid,orderid,transtime,currency,amount,productcatalog,productname,productdesc,userip,identityid,identitytype,terminaltype,terminalid,callbackurl,fcallbackurl):
        mesdata={"merchantaccount":merchantaccount,"bindid":bindid,"orderid":orderid,"transtime":transtime,"currency":currency,"amount":amount,"productcatalog":productcatalog,"productname":productname,"productdesc":productdesc,"userip":userip,"identityid":identityid,"identitytype":identitytype,"terminaltype":terminaltype,"terminalid":terminalid,"callbackurl":callbackurl,"fcallbackurl":fcallbackurl}

        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/testpayapi/api/bankcard/bind/pay/request'


        print url
        result=self.doPost(url, values)    
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)

        
        
    '''
    发送验证码
    '''
    def testvalidatecode(self,merchantaccount,orderid):
        mesdata={"merchantaccount":merchantaccount,"orderid":orderid}

        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/testpayapi/api/validatecode/send'


        print url
        result=self.doPost(url, values)    
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)
        
    '''
    发起支付请求
    '''
    def testpayvalidatecode(self,merchantaccount,orderid,validatecode):
        mesdata={"merchantaccount":merchantaccount,"orderid":orderid,"validatecode":validatecode}

        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/testpayapi/api/async/bankcard/pay/confirm/validatecode'


        print url
        result=self.doPost(url, values)    
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)     
        
    def testUnbindCardsign(self,merchantaccount,bindid,identityid,identitytype):
        '''
        解绑接口
        RSA签名方式
        '''  
        
        mesdata={"merchantaccount":Gl.merchantaccount,'bindid':'940',"identityid":"ee","identitytype":6}
        values=self.requestprocess(mesdata)
        print values
        url='http://'+Gl.URL+'/testpayapi/api/bankcard/unbind'
        result=self.doPost(url, values)
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)
    
    
    
    def testQueryOrderSign(self,merchantaccount,orderid):
        '''
        支付结果查询
        RSA签名方式
        '''  

        mesdata={"merchantaccount":merchantaccount,"orderid":orderid}
        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/testpayapi/api/query/order'
        result=self.doGet(url, values)
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)

    
    def testQueryPay(self,merchantaccount,orderid,yborderid):
        '''
        商户自用交易记录查询
        RSA签名方式
        '''  

        
        mesdata={"merchantaccount":merchantaccount,"orderid":orderid,"yborderid":yborderid}
        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/merchant/query_server/pay_single'
        result=self.doGet(url, values)
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)
    
    
    def testQueryRefund(self,merchantaccount,orderid):
        '''
        商户自用退款记录查询
        RSA签名方式
        '''  

        
        mesdata={"merchantaccount":merchantaccount,"orderid":orderid}
        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/merchant/query_server/refund_single'
        result=self.doGet(url, values)
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)
    
    
    def testDirectRefund(self,merchantaccount,orderid,origyborderid,amount,currency,cause):
        '''
        商户自用接口退款
        RSA签名方式
        '''  
          
        mesdata={"merchantaccount":merchantaccount,"orderid":orderid,"origyborderid":origyborderid,"amount":amount,"currency":currency,"cause":cause}
        values=self.requestprocess(mesdata)
        url='http://'+Gl.URL+'/merchant/query_server/direct_refund'
        result=self.doPost(url, values)
        rdata=json.loads(self.result_decrypt(result))
        self.checksign(rdata)
 

