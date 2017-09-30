# -*- coding:utf-8 -*-
import sys
import time
from sphinxapi import *
from django.core.cache import cache
from zz91settings import SPHINXCONFIG


reload(sys)
sys.setdefaultencoding('utf8')
dbc = companydb()


def get_timestamp(one_time):
    # 获取给定的时间的时间戳
    # 指定的时间格式为 2017-08-04
    bz_time = time.strptime(one_time, "%Y-%m-%d")
    time_stamp = int(time.mktime(bz_time))
    return time_stamp


def get_qf_info(from_page_count='', limit_num='', qf_id=''):
    # 获取所有购买群发的客户信息
    # if not qf_id:
    #     qf_info = cache.get('qunfa_info')
    #     if qf_info:
    #         return qf_info
    # else:
    #     qf_info = cache.get('qunfa_info' + str(qf_id))
    #     if qf_info:
    #         return qf_info
    if not qf_id:
        sql_qf = "select sq.id,sq.content,sq.company_id as cid,sq.gmt_created,sq.isqunfa,sq.qf_all_num," \
                 "sq.qf_success_num,sq.exec_time,sq.start_time,sq.start_hour,c.name as cname,ca.account " \
                 "from shop_qunfa as sq left join company as c on sq.company_id=c.id left join " \
                 "company_account as ca on sq.company_id=ca.company_id"
        if from_page_count and limit_num:
            sql_qf += " and limit %s,%s order by sq.gmt_created desc"
            all_qf_data = dbc.fetchalldb(sql_qf, [from_page_count, limit_num])
        else:
            sql_qf += " order by sq.gmt_created desc"
            all_qf_data = dbc.fetchalldb(sql_qf)
        # cache.set('qunfa_info', all_qf_data, 60 * 10)
    else:
        sql_qf = "select sq.id,sq.content,sq.company_id as cid,sq.gmt_created,sq.isqunfa,sq.qf_all_num," \
                 "sq.qf_success_num,sq.exec_time,sq.start_time,sq.start_hour,c.name as cname,ca.account " \
                 "from shop_qunfa as sq left join company as c on sq.company_id=c.id left join " \
                 "company_account as ca on sq.company_id=ca.company_id where sq.id=%s"
        all_qf_data = dbc.fetchonedb(sql_qf, [qf_id])
        # cache.set('qunfa_info' + str(qf_id), all_qf_data, 60 * 10)
    return all_qf_data


def member_style(company_id):
    # 根据公司id获取会员类型
    sql_memeber = "select ca.label from company as c left join category as ca on c.membership_code=ca.code " \
                  "where c.id=%s"
    result = dbc.fetchonedb(sql_memeber, [company_id])
    if result:
        return result[0]
    else:
        return 0


def get_all_products(start_num, end_num, limit_num, pdt_kind='', keywords='', start_time='', end_time='', area=''):
    # 获取供求信息
    list_all = []
    cl = SphinxClient()
    cl.SetServer(SPHINXCONFIG['serverid'], SPHINXCONFIG['port'])
    cl.SetMatchMode(SPH_MATCH_BOOLEAN)
    cl.SetLimits(start_num, end_num, limit_num)
    cl.SetGroupBy('company_id', SPH_GROUPBY_ATTR, "refresh_time desc")
    cl.SetSortMode(SPH_SORT_EXTENDED, 'refresh_time desc')
    # 限制供应还是求购
    if pdt_kind:
        cl.SetFilter('pdt_kind', [int(pdt_kind)])
    # 限制地区
    if area:
        keywords = area + keywords
    # 限制刷新时间
    if start_time and end_time:
        cl.SetFilterRange('refresh_time', get_timestamp(start_time), get_timestamp(end_time))
    # 限制关键词
    if keywords:
        query_result = cl.Query('@(title,label0,label1,label2,label3,label4,city,province,tags) ' + keywords,
                                'offersearch_new,offersearch_new_vip')
    else:
        query_result = cl.Query('', 'offersearch_new,offersearch_new_vip')
    if query_result and 'matches' in query_result:
        res_list = query_result['matches']
        for each_data in res_list:
            each_attr = each_data['attrs']
            pro_id = each_data['id']
            pro_title = each_attr['ptitle']
            pdt_kind = each_attr['pdt_kind']
            refresh_time = each_attr['refresh_time']
            company_id = each_attr['company_id']

            # 获取会员类型
            member_ship = member_style(company_id)
            # if member_ship == '10051001':
            #     vip_type = '再生通'
            # elif member_ship == '1725773192':
            #     vip_type = '银牌品牌通'
            # elif member_ship == '1725773193':
            #     vip_type = '金牌品牌通'
            # elif member_ship == '1725773194':
            #     vip_type = '钻石品牌通'
            # else:
            #     vip_type = '普通会员'

            # 过滤是否为来电宝

            # 默认过滤已添加
            sql_filter = "select id from shop_qunfa_record where pdt_id=%s"
            result_filter = dbc.fetchonedb(sql_filter, [pro_id])
            if result_filter:
                had_added = 1
            else:
                had_added = 0
            # 返回数据
            data_dict = {'pro_id': pro_id, 'pro_title': pro_title, 'pdt_kind': pdt_kind,
                         'refresh_time': refresh_time, 'company_id': company_id, 'had_added': had_added,
                         'vip_type': member_ship}
            list_all.append(data_dict)
        all_num = query_result['total_found']
        dict_all = {'list_all': list_all, 'all_num': all_num}
        return dict_all


def get_comp_account(comp_id):
    # 根据公司id获取account
    sql_account = "select account from company_account where company_id=%s"
    result = dbc.fetchonedb(sql_account, [comp_id])
    if result:
        comp_account = result[0]
    else:
        comp_account = ''
    return comp_account
