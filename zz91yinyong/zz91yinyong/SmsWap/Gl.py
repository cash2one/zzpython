#!-*- coding:utf-8 -*-
'''
Created on 2013-6-15

@author: shangwei
'''
'''
全局变量
'''
from Crypto.PublicKey import RSA
import os
'''
publickey为易宝的公钥
privatekey为商户自己的私钥
'''
publickey = RSA.importKey(open(os.path.dirname(__file__)+'/rsa_public_key144.pem','r').read())
privatekey=RSA.importKey(open(os.path.dirname(__file__)+'/pkcs8_rsa_private_key144.pem','r').read())
merchantaccount='10012427758'
URL='ok.yeepay.com'