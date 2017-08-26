import requests
a=requests.post("http://m.zz91.com/zz91payverify_notify.html")
print a

<notify><payment_type>1</payment_type><subject>手机钱包充值</subject><trade_no>2014082515619967</trade_no><buyer_email>kangxianyue@sina.com</buyer_email><gmt_create>2014-08-25 19:43:58</gmt_create><notify_type>trade_status_sync</notify_type><quantity>1</quantity><out_trade_no>20140825668366</out_trade_no><notify_time>2014-08-25 19:44:23</notify_time><seller_id>2088511051388426</seller_id><trade_status>TRADE_FINISHED</trade_status><is_total_fee_adjust>N</is_total_fee_adjust><total_fee>0.01</total_fee><gmt_payment>2014-08-25 19:44:23</gmt_payment><seller_email>zhifu@asto-inc.com</seller_email><gmt_close>2014-08-25 19:44:23</gmt_close><price>0.01</price><buyer_id>2088002519567678</buyer_id><notify_id>7e6b70600306188ffd8599ebb0f1ba045q</notify_id><use_coupon>N</use_coupon></notify>

<WSGIRequest
GET:<QueryDict: {}>,
POST:<QueryDict: {u'sec_id': [u'MD5'], u'v': [u'1.0'], u'notify_data': [u'<notify><payment_type>1</payment_type><subject>\u624b\u673a\u94b1\u5305\u5145\u503c</subject><trade_no>2014082515588667</trade_no><buyer_email>kangxianyue@sina.com</buyer_email><gmt_create>2014-08-25 19:36:57</gmt_create><notify_type>trade_status_sync</notify_type><quantity>1</quantity><out_trade_no>20140825859067</out_trade_no><notify_time>2014-08-25 19:37:13</notify_time><seller_id>2088511051388426</seller_id><trade_status>TRADE_FINISHED</trade_status><is_total_fee_adjust>N</is_total_fee_adjust><total_fee>0.01</total_fee><gmt_payment>2014-08-25 19:37:13</gmt_payment><seller_email>zhifu@asto-inc.com</seller_email><gmt_close>2014-08-25 19:37:13</gmt_close><price>0.01</price><buyer_id>2088002519567678</buyer_id><notify_id>23ec1e4641412ed7c09518b831499af05q</notify_id><use_coupon>N</use_coupon></notify>'], u'service': [u'alipay.wap.trade.create.direct'], u'sign': [u'd822d9e40170bfaa15fdb82b7686101b']}>,
COOKIES:{},
META:{'CONTENT_LENGTH': '1166',
 'CONTENT_TYPE': 'application/x-www-form-urlencoded; text/html; charset=utf-8',
 'HTTP_CONNECTION': 'close',
 'HTTP_CONTENT_LENGTH': '1166',
 'HTTP_CONTENT_TYPE': 'application/x-www-form-urlencoded; text/html; charset=utf-8',
 'HTTP_HOST': 'm.zz91.com',
 'HTTP_USER_AGENT': 'Mozilla/4.0',
 'HTTP_X_FORWARDED_FOR': '110.75.152.2',
 'HTTP_X_REAL_IP': '110.75.152.2',
 'PATH_INFO': u'/zz91payverify_notify.html',
 'QUERY_STRING': '',
 'REMOTE_ADDR': '192.168.110.120',
 'REQUEST_METHOD': 'POST',
 'SCRIPT_NAME': u'',
 'SERVER_NAME': 'chinazz91',
 'SERVER_PORT': '8019',
 'SERVER_PROTOCOL': 'HTTP/1.0',
 'wsgi.errors': <flup.server.fcgi_base.TeeOutputStream object at 0x385e9d0>,
 'wsgi.input': <flup.server.fcgi_base.InputStream object at 0x385eb10>,
 'wsgi.multiprocess': True,
 'wsgi.multithread': False,
 'wsgi.run_once': False,
 'wsgi.url_scheme': 'http',
 'wsgi.version': (1, 0)}>