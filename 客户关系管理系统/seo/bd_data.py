# -*- coding:utf-8 -*-
import re
import sys
import json
import urllib
import httplib
import pymongo
import datetime
import requests
from re import S
from lxml import etree
from get_time import GetTime

__author__ = 'fenghui'
reload(sys)
sys.setdefaultencoding('utf8')


def get_html(url):
    # 获取html，可用于正则表达式获取数据
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/58.0.3029.110 Safari/537.36'}
    html = requests.get(url, headers=header)
    html.encoding = "utf-8"
    result = html.content
    return result


def get_source_code(url):
    # 获取格式化过的html源代码，可以进行xpath获取对应的信息
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/58.0.3029.110 Safari/537.36'}
    html = requests.get(url, headers=header, timeout=5)
    # html.encoding = "utf-8"
    result = html.content
    rs_etree = etree.HTML(result)
    return rs_etree


def post_data(url, data):
    # 用于获取ajax数据
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/58.0.3029.110 Safari/537.36',
              }
    try:
        html = requests.post(url, headers=header, data=data, timeout=5)
        html.encoding = "utf-8"
        result = html.content
        return result
        # print result
    except Exception:
        result = {'index': '超时,未获取到'}
        return result


def get_bd_data(*args):
    """
    :param  包含site或domain
    :return: 返回收录数或反链数
    """
    # 获取百度收录数、反链数,数据格式为str，去除数字中的逗号
    url = "https://www.baidu.com/s?wd={}:{}".format(*args)
    rs_etree = get_source_code(url)
    # 获取site收录，两种形式的site收录数据
    # 形式1：https://www.baidu.com/s?wd=site:xiuhuali.zz91.com
    # 形式2：https://www.baidu.com/s?wd=site:linnan.zz91.com
    if 'site' in url:
        bd_sl = rs_etree.xpath('//div[@class="c-span21 c-span-last"]/p/b/text()')
        if bd_sl:
            bd_sl = bd_sl[0].encode('utf-8')
            try:
                bd_sl = re.search(r'找到相关结果数约(.*?)个', bd_sl).group(1)
                return bd_sl
            except Exception:
                return 0
        else:
            bd_sl = rs_etree.xpath('//div[@class="op_site_domain_right c-span24 c-span-last"]/p/span/b/text()')
            if bd_sl:
                bd_sl = ''.join(bd_sl[0].split(','))
                return bd_sl
            else:
                return 0

    # 获取domain相关域的数量
    # 形式：https://www.baidu.com/s?wd=domain:xiuhuali.zz91.coms
    if 'domain' in url:
        bd_fl = rs_etree.xpath('//div[@class="nums"]/text()')
        if bd_fl:
            bd_fl = bd_fl[0].encode('utf-8')  # 不加encode是unicode编码，加上变成str，可以直接处理
            # print type(bd_fl)
            try:
                bd_fl = re.search(r'百度为您找到相关结果约(.*?)个', bd_fl).group(1)
                bd_fl = ''.join(bd_fl.split(','))
                return bd_fl
            except Exception:
                return 0
        else:
            return 0
    else:
        return 0


def get_bd_pm(k_ws, msb_url):
    # 获取百度排名，默认获取前十页
    # bd_pm 最后获取的百度排名，flag 抓取10页，是否抓取到的标志，e_link 最后退出循环时获取到的链接
    bd_pm = 0
    flag = 0
    e_link = u''
    url_length = len(msb_url)
    k_ws = k_ws.encode('utf-8', 'ignore')

    # 百度url显示出来的为21位，超过的直接截断
    if url_length < 20:
        msb_url = msb_url
    else:
        msb_url = msb_url[:21]

    # 获取排名
    # 大部分可以准确显示
    # 有偏差的情况：
    # 1、包含百度图片的自然搜索结果，暂未获取到对应的url
    # 2、搜索关键词包含英文的时候，会在url里进行加粗，暂未获取到对应的url
    for i in xrange(0, 100, 10):
        # print u'>>>>>正在抓取第{}页……'.format(i // 10)
        url = "https://www.baidu.com/s?wd={}&pn={}&ie=gbk".format(k_ws, i)
        rs_etree = get_source_code(url)
        r_link_bd = rs_etree.xpath('//div[@class="result c-container "]')
        for each in r_link_bd:
            links = each.xpath('div[@class="c-row c-gap-top-small"]/div[@class="c-span18 c-span-last"]/'
                               'div[@class="f13"]/a[@class="c-showurl"]/text()')
            if links:
                # print type(links[0])
                bd_pm += 1
                e_link = links[0].encode('gbk', 'ignore')
                # print e_link
                if msb_url in e_link:
                    flag += 1
                    # print 1, e_link, flag
                    break
            else:
                links_2 = each.xpath('div[@class="f13"]/a[@class="c-showurl"]/text()')
                # print type(links_2[0])
                if links_2:
                    bd_pm += 1
                    e_link = links_2[0].encode('gbk', 'ignore')
                    # print e_link
                    if msb_url in e_link:
                        flag += 1
                        # print 2, e_link, flag
                        break
        # print e_link
        if msb_url in e_link:
            break
    # 返回排名
    if bd_pm and bd_pm < 101 and flag != 0:
        return bd_pm
    elif flag == 0:
        return 100
    else:
        return 0


def get_bd_pm2(k_ws, msb_url):
    # 优化后的百度排名
    # 时间：2017.6.10 16:34 author：fenghui
    # 存在的问题：测试发现有爱奇艺的暂时未获取到，百度图片、开放平台均已经获取到
    url_length = len(msb_url)
    bd_pm = 0
    flag = 0
    bd_pic = 0
    k_ws = k_ws.encode('utf-8', 'ignore')
    e_link = u''

    # 百度url显示出来的为21位，超过的直接截断
    if url_length < 20:
        msb_url = msb_url
    else:
        msb_url = msb_url[:18]

    for i in xrange(0, 100, 10):
        kws = urllib.quote(k_ws)
        url = "https://www.baidu.com/s?wd={}&pn={}&ie=gbk".format(kws, i)
        rs_etree = get_source_code(url)
        r_link_bd = rs_etree.xpath('//*[@class="c-showurl"]')
        for each_link in r_link_bd:
            e_link = each_link.xpath('string(.)')
            # print e_link.encode('gbk', 'ignore')
            if u'image.baidu.com' in e_link:  # 去除百度图片获取到的多余的链接
                if bd_pic == 0:
                    bd_pm += 1
                bd_pic += 1
            else:
                bd_pm += 1
                # print e_link.encode('gbk', 'ignore'), bd_pm
                if msb_url in e_link:
                    flag += 1
                    break
        if msb_url in e_link:
            break

    # 返回排名
    if bd_pm and bd_pm < 101 and flag != 0:
        return bd_pm
    elif flag == 0:
        return 100
    else:
        return 0


def get_bd_links(keywords):
    # 获取以关键词为基础的前三页的链接
    # 返回链接的list,判断是否有通往竞争
    # flag = 0
    key_ws = keywords.encode('utf-8', 'ignore')
    all_links = []

    for i in xrange(0, 30, 10):
        kws = urllib.quote(key_ws)
        url = "https://www.baidu.com/s?wd={}&pn={}&ie=gbk".format(kws, i)
        rs_etree = get_source_code(url)
        r_link_bd = rs_etree.xpath('//*[@class="c-showurl"]')
        for each_link in r_link_bd:
            # flag += 1
            e_link = each_link.xpath('string(.)').strip()
            if 'zz91.com' in e_link and 'www.zz91.com' not in e_link:
                all_links.append(e_link)
                break
            # print e_link, flag
    if all_links:
        # print all_links
        return 1
    else:
        return 0


def get_sl(url):
    url = url.strip()
    check_url = "http://www.baidu.com/s?wd={}&ie=gbk".format(url)
    rs_etree = get_source_code(check_url)
    # print wz_title
    r_link_bd = rs_etree.xpath('//div[@class=" c-gap-bottom-small f13"]/span')  # 未收录页面返回的数据
    r_link_bd2 = rs_etree.xpath('//div[@class="nors"]/p')
    # r_link_bd_2 = rs_etree.xpath('//h3[@class="t"]/a/@href')  # 收录页面返回的数据

    # 获取是否收录
    if r_link_bd:
        for each_link in r_link_bd:
            text = each_link.xpath('string(.)')
            # print text
            if '没有找到该URL' in text:
                sl_flag = 0
                return sl_flag
    if r_link_bd2:
        text = r_link_bd2[0].xpath('string(.)')
        # print text
        if '很抱歉，没有找到与' in text:
            sl_flag = 0
            return sl_flag
    else:
        sl_flag = 1
        return sl_flag


def get_ssl(keywords):
    # 获取某个关键词的搜索量
    # 返回结果格式为:1,230,000
    if isinstance(keywords, str):
        keywords = keywords.decode('utf-8').encode('utf-8')
    if isinstance(keywords, unicode):
        # print keywords
        keywords = keywords.encode('utf-8')
    kw_s = urllib.quote(keywords)
    # print kw_s
    url_link = "http://www.baidu.com/s?ie=utf-8&wd={}".format(kw_s)
    # print url_link
    html = get_html(url_link)
    # print html
    result = re.search(ur'百度为您找到相关结果约(.*?)个', html, S)
    if result:
        ssl_num = result.group(1)
        ssl_num = ''.join(ssl_num.split(','))
    else:
        ssl_num = 0
    return ssl_num


def get_bd_index(keywords):
    # 从百度指数页面,返回百度指数
    # 备注:未做完
    kw_s = urllib.quote(keywords)
    url_link = "http://index.baidu.com/?tpl=trend&word={}".format(kw_s)
    html = get_html(url_link).decode('gbk', 'ignore')
    return html


def bd_index(keywords):
    # 从站长工具获取
    # 获取百度指数,包含百度pc指数、移动指数、360指数以及神马指数
    # 指数数据仅供参考
    if isinstance(keywords, str):
        keywords = keywords.decode('gb18030', 'ignore').encode('utf-8').replace('"', '')
    if isinstance(keywords, unicode):
        keywords = keywords.encode('utf-8')
    kw_s = urllib.quote(keywords)
    get_time = GetTime()
    time_stamp = ''.join(str(get_time.get_time_stamp()).split('.'))
    url_link = "http://rank.chinaz.com/ajaxsync.aspx?at=index&" \
               "callback=jQuery111307865518439714061_{}".format(time_stamp)
    # print kw_s
    data2 = {
        'kw': kw_s
    }
    html = post_data(url_link, data2)
    try:
        ls = re.findall(r'(\w+)(?=:)', html)  # 获取冒号左边的字符串
        rs = re.findall(r'(?<=\')(\d+|\W+)(?=\')', html)  # 获取冒号右边的数字或文字或其他字符
        if ls and rs:
            result = dict(zip(ls, rs))
            return result
    except TypeError:
        # 错误原因:expected string or buffer
        return html

    # demjson库的使用,对于()会报错
    # if html:
    #     result = re.search(r'.*?\((.*?)\)', html).group(1)
    #     result = demjson.decode(result)
    #     return result
    # else:
    #     return {}


def get_xl_kws(keywords):
    # 获取百度下拉框相关关键词
    if isinstance(keywords, str):
        keywords = keywords.decode('gb18030', 'ignore').encode('utf-8')
    if isinstance(keywords, unicode):
        keywords = keywords.encode('utf-8')
    keywords = urllib.quote(keywords)
    url_link = "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd={}".format(keywords)
    html = get_html(url_link)
    xl_kws = re.search(r's:\[(.*?)\]', html).group(1)
    # print xl_kws.decode('gbk'), type(xl_kws.decode('gbk'))
    # xl_kws = re.findall(r'(?<=\")()(?=\")', html)
    if xl_kws:
        xl_kws_list = xl_kws.split(',')
        return xl_kws_list
    else:
        return []


def get_title(url):
    # 获取对应URL的页面标题
    try:
        wz_html = get_source_code(url)
        wz_title = wz_html.xpath('//title/text()')[0]
        length = len(wz_title)
        if length > 25:
            wz_title = wz_title[0:25] + '...'
    except Exception:
        wz_title = '页面加载异常'
    return wz_title


def conn_mongodb():
    # 连接pymongo
    client = pymongo.MongoClient(host='192.168.2.4', port=27017)
    db = client.richangts
    collection = db.tuisong
    return collection


def check_ts_2(url_link):
    # pymongo 检测是否推送
    collection = conn_mongodb()
    single_data = collection.find({'ts_link': url_link})
    for each_data in single_data:
        if each_data['ts_link'] and each_data['ts_message_info'] == 1:
            return 0
        elif each_data['ts_link'] and each_data['ts_message_info'] == 401:
            return 1
    else:
        return 2


def tui_song(url_link, domain, token):
    # 主动推送
    # 推送到百度接口
    conn = httplib.HTTPConnection('data.zz.baidu.com')
    api = '/urls?site={}&token={}'.format(domain, token)
    conn.request(method='POST', url=api, body=url_link, headers={'Content-Type': 'text/plain'})
    response = conn.getresponse().read()
    conn.close()
    message = json.loads(response)
    return message


def save_to_mongodb2(url_link, domain, token):
    # pymongo 保存数据到mongodb
    # 修改测试完成,失败可重新推送,测试时间2017.7.6 10:20
    message_info = 0
    ts_flag = 0
    ts_status = check_ts_2(url_link)
    # print ts_status
    if ts_status == 2 or ts_status == 1:
        # 未推送过或者是推送过,状态码为401
        message = tui_song(url_link, domain, token)
        # print message, type(message)
        for key, value in message.items():
            if key == 'success':
                message_info = message['success']
                ts_flag += message['remain']
            elif key == 'error':
                message_info = message['error']
                ts_flag += 0
        collection = conn_mongodb()
        if ts_status == 2:
            # print u'未推送过'
            post_info = {'ts_link': url_link, 'ts_time': datetime.datetime.now(), 'ts_domain': domain,
                         'ts_message_info': message_info, 'ts_message_remain': ts_flag
                         }
            collection.insert_one(post_info)
        else:
            # print u'已推送过,状态码为401'
            collection.update({'ts_link': url_link}, {'$set': {'ts_time': datetime.datetime.now(),
                                                               'ts_message_info': message_info,
                                                               'ts_message_remain': ts_flag}})
        return 1
    else:
        # print u'已推送过'
        return 0


def get_ts_data2(url_link):
    # 获取单条数据
    collection = conn_mongodb()
    single_data = collection.find({'ts_link': url_link})
    return single_data


def get_ts_data3():
    start_time = datetime.datetime(2017, 6, 1)
    # end_time = datetime.datetime(2017, 6, 30)
    # print start_time, end_time, type(start_time)
    collection = conn_mongodb()
    all_failure_data = collection.find({'ts_message_info': 401, 'ts_time': {'$gte': start_time}})
    return all_failure_data


def get_ym_expire(url_link):
    # 获取域名的过期时间
    def_url = 'http://whois.chinaz.com/{}'.format(url_link)
    html = get_html(def_url)
    expire_time = re.search(ur'过期时间</div><div class="fr WhLeList-right"><span>(.*?)</span></div>',
                            html, S)
    if expire_time:
        expire_time = expire_time.group(1)
    else:
        expire_time = '未获取到'
    return expire_time