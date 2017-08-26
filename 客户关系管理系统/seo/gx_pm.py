# -*- coding:utf-8 -*-
import sys
import time
from conn import *
from bd_data import get_bd_pm2,get_bd_data
from get_time import GetTime

reload(sys)
sys.setdefaultencoding('utf8')


def update_ranking():
    # 定时更新排名、每天凌晨1点、16点
    sql = "select id,sid,keywords,com_msb from seo_keywordslist where isexpire=0"
    all_keywords = fetch_all(sql)
    #print len(all_keywords), all_keywords[0]
    i = 1
    for each_keyword in all_keywords:
        print u'正在获取第{}条'.format(str(i))
        try:
            kid = each_keyword['id']
            sid = each_keyword['sid']
            keywords = each_keyword['keywords']
            com_msb = each_keyword['com_msb']
            bd_ranking = get_bd_pm2(keywords, com_msb)
            print keywords, com_msb, bd_ranking
            # 更新seo_keywordslist中的关键词排名
            sql_gx = "update seo_keywordslist set baidu_ranking=%s where id=%s"
            update_db(sql_gx, [bd_ranking, kid])
            get_time = GetTime()
            now_time = get_time.time_now()
            k_date = get_time.get_strf_time2()
            # 更新排名到seo_keywords_historyd中
            sql_history = "insert into seo_keywords_history(kid,sid,ktype,baidu_ranking,kdate,gmt_created) " \
                          "values(%s,%s,%s,%s,%s,%s)"
            update_db(sql_history, [kid, sid, 'check_pai', bd_ranking, k_date, now_time])
            i += 1
        except Exception:
            continue


def update_site_sl():
    # 更新site收录数
    # 每天更新1次,更新时间凌晨1点
    sql_seo_list = "select id,com_msb from seo_list where waste=0"
    result_all_msb = fetch_all(sql_seo_list)
    i = 1
    for each_msb in result_all_msb:
        try:
            msb_link = each_msb['com_msb']
            sid = each_msb['id']
            print u'>>>>>>正在抓取第{}条门市部链接,链接为{}'.format(str(i), msb_link)
            #  更新seo_list中的百度收录数
            sql_sl_gx = "update seo_list set baidu_sl=%s where id=%s and waste=0"
            bd_sl = get_bd_data("site", msb_link)
            update_db(sql_sl_gx, [bd_sl, sid])
            # 把更新的数据插入到seo_keywords_history中
            get_time = GetTime()
            now_time = get_time.time_now()
            k_date = get_time.get_strf_time2()
            sql2 = "insert into seo_keywords_history(kid,sid,ktype,kdate,baidu_sl,gmt_created) " \
                   "values(%s,%s,%s,%s,%s,%s)"
            update_db(sql2, [0, sid, 'baidu_sl', k_date, bd_sl, now_time])
            i += 1
        except Exception:
            continue


update_site_sl()
update_ranking()
