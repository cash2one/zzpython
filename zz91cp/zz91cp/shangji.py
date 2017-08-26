# -*- coding:utf-8 -*-
import os
import sys
import random
import settings
from sphinxapi import *
from zz91db_ast import companydb
from zz91settings import SPHINXCONFIG, limitpath
from django.core.cache import cache
from django.shortcuts import render
from zz91page import *

reload(sys)
sys.setdefaultencoding('utf-8')
nowpath = os.path.dirname(__file__)
execfile(nowpath + "/conn.py")
execfile(nowpath + "/commfunction.py")
execfile(nowpath + "/function.py")
execfile(nowpath + "/cp_function.py")
dbc = companydb()
wmh = weimenhu()


def index(request):
    # 商机排行榜首页
    hidfloat=1
    # 随机获取微门户热搜词,获取前200条随机显示前16条
    re_sou_200 = re_sou_from_dh(200)
    hot_cp_list = [random.choice(re_sou_200) for _ in range(16)]
    # 获取微门户飙升词,获取前400条随机显示16条
    re_sou_400 = re_sou_from_dh(400)
    inc_keywords_list = [random.choice(re_sou_400) for _ in range(16)]
    # 最新加入高会的客户前6个
    new_member = enumerate(get_company_list(0, 6, 6))
    # 获取人气商铺前6个
    hot_website = enumerate(get_hot_company_list(0, 6, 6))
    # 获取供求列表-精品商机
    pro_dict = get_all_products(0, 5, 5, 1)
    pro_list = pro_dict['list_all']
    # 获取供求列表-人气商机
    pro_dict_2 = get_all_products(0, 5, 5, 2)
    pro_list_2 = pro_dict_2['list_all']
    # 获取互助信息
    bbs_list = get_hot_huzhu_info(0, 6, 6, 1)
    bbs_list_2 = get_hot_huzhu_info(0, 6, 6, 2)

    return render(request, "paihang/index.html", locals())


def hot_cp(request):
    hidfloat=1
    # 商机排行榜热门产品词
    # 获取大类
    big_category = get_big_category()
    hot_cp_dt = {}
    list_all = []
    # 根据大类,获取对应类别下的前24个关键词
    if big_category:
        for each_code in big_category:
            hot_cp_dict = hot_cp_keywords(int(each_code[0]), 0, 24, 24)
            if hot_cp_dict:
                count = hot_cp_dict['total']
                hot_cp_dict['count'] = count
                hot_cp_dict['code'] = each_code[0]
                hot_cp_dict['label'] = each_code[1]
                list_all.append(hot_cp_dict)
    if list_all:
        list_all_1 = list_all[:5]
        list_all_2 = list_all[5:]
    return render(request, "paihang/hot.html", locals())


def sj_billboard(request):
    hidfloat=1
    # 商机榜单
    now_month = get_month()
    # 获取供求列表-精品商机
    pro_dict = get_all_products(0, 5, 5, 1)
    pro_list = pro_dict['list_all']
    all_pro_nums = pro_dict['all_num']
    # 获取供求列表-人气商机
    pro_dict_2 = get_all_products(0, 5, 5, 2)
    pro_list_2 = pro_dict_2['list_all']
    all_pro_nums2 = pro_dict_2['all_num']
    return render(request, "paihang/opportunity.html", locals())


def sj_bd_more(request):
    hidfloat=1
    # 更多商机榜单
    now_month = get_month()
    page_info = zz91page()
    now_page = page_info.nowpage(1)
    limit_num = page_info.limitNum(6)
    next_page = page_info.nextpage()
    before_page = page_info.prvpage()
    pro_list = get_all_products(0, limit_num, limit_num, 1)
    if pro_list:
        list_all = pro_list['list_all']
        all_num = pro_list['all_num']
        list_count = page_info.listcount(int(all_num))
        page_info.page_listcount()
        page_info.before_range_num(3)
        page_info.after_range_num(4)
        page_range = page_info.page_range()
    return render(request, "paihang/opportunityMore.html", locals())


def sj_bd_more_2(request, page):
    hidfloat=1
    # 更多商机榜单
    now_month = get_month()
    page_info = zz91page()
    if not page:
        page = 1
    page_info.nowpage(int(page))
    limit_num = page_info.limitNum(6)
    from_page = page_info.frompageCount()
    next_page = page_info.nextpage()
    before_page = page_info.prvpage()
    pro_list = get_all_products(int(from_page), int(limit_num), 30000, 1)
    if pro_list:
        list_all = pro_list['list_all']
        all_num = pro_list['all_num']
        list_count = page_info.listcount(int(all_num))
        page_info.page_listcount()
        page_info.before_range_num(3)
        page_info.after_range_num(4)
        page_range = page_info.page_range()
    return render(request, "paihang/opportunityMore.html", locals())


def esite_billboard(request):
    hidfloat=1
    # 商铺榜单
    now_month = get_month()
    new_member = enumerate(get_company_list(0, 7, 7))
    hot_member = enumerate(get_hot_company_list(0, 7, 7))
    return render(request, "paihang/seller.html", locals())


def sp_bd_more(request):
    hidfloat=1
    # 更多商铺榜单
    now_month = get_month()
    page_info = zz91page()
    now_page = page_info.nowpage(1)
    # list_count = page_info.listcount(int(all_num))
    limit_num = page_info.limitNum(15)
    next_page = page_info.nextpage()
    before_page = page_info.prvpage()
    member_list = get_company_list_2(0, limit_num, limit_num)
    if member_list:
        list_all = enumerate(member_list['list_all'])
        all_num = member_list['all_num']
        list_count = page_info.listcount(int(all_num))
        page_info.page_listcount()
        page_info.before_range_num(3)
        page_info.after_range_num(4)
        page_range = page_info.page_range()
    return render(request, "paihang/sellerMore.html", locals())


def sp_bd_more_2(request, page):
    hidfloat=1
    # 更多商铺榜单
    now_month = get_month()
    page_info = zz91page()
    if not page:
        page = 1
    page_info.nowpage(int(page))
    limit_num = page_info.limitNum(6)
    from_page = page_info.frompageCount()
    next_page = page_info.nextpage()
    before_page = page_info.prvpage()
    member_list = get_company_list_2(int(from_page), int(limit_num), 30000)
    if member_list:
        list_all = enumerate(member_list['list_all'])
        all_num = member_list['all_num']
        list_count = page_info.listcount(int(all_num))
        page_info.page_listcount()
        page_info.before_range_num(3)
        page_info.after_range_num(4)
        page_range = page_info.page_range()
    return render(request, "paihang/sellerMore.html", locals())
