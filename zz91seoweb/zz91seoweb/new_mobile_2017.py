# -*- coding:utf-8 -*-
import os
import sys
import settings
from datetime import date
from zz91page import zz91page
from sphinxapi import *
from django.core.cache import cache
from django.shortcuts import render


reload(sys)
sys.setdefaultencoding('UTF-8')
now_path=os.path.dirname(__file__)
execfile(now_path+"/conn.py")
execfile(now_path+"/function.py")


def index(request, company_id):
    """
    :param request: 请求
    :param company_id: 公司id
    :return: 手机站首页,返回公司简介、最新供求5条、公司动态5条
    """
    # 根据公司id,获取公司信息
    comp_info = getcompanydetail(company_id)
    if not comp_info:
        return render(request, 'html/404.html', locals(), status=500)
    # 根据公司id,获取产品信息
    all_products = getcompanyproductslist('', 0, 6, company_id)
    # 根据公司id,获取公司动态
    all_news = getcompanynewslist(0, 2, company_id)
    return render(request, "shops/index.html", locals())


def about(request, company_id):
    """
    :param request: 请求
    :param company_id: 公司id
    :return: 手机站公司简介页面,根据公司id返回对应公司的公司简介
    """
    # 获取所有公司信息
    comp_info = getcompanydetail(company_id)
    # 获取认证信息
    rz_info = getcredit_file(company_id)
    if not comp_info:
        return render(request, 'html/404.html', locals(), status=500)
    return render(request, "shops/about.html", locals())


def contact(request, company_id):
    """
    :param request: 请求
    :param company_id: 公司id
    :return: 手机站公司联系我们页面,根据公司id返回对应的联系我们信息
    """
    # 获取所有公司信息
    comp_info = getcompanydetail(company_id)
    if not comp_info:
        return render(request, 'html/404.html', locals(), status=500)
    return render(request, "shops/contact.html", locals())


def products(request, company_id, page,seriesid=""):
    """
    :param request: 请求
    :param company_id: 公司id
    :param page: 页码
    :return: 手机站公司供求页面,根据公司id返回对应的供求信息
    """
    keywords=request.GET.get("keywords")
    # 获取公司信息
    comp_info = getcompanydetail(company_id)
    if not comp_info:
        return render(request, 'html/404.html', locals(), status=500)
    
    if seriesid:
        if seriesid == '0':
            toseriesid = ''
        else:
            toseriesid = seriesid
    else:
        toseriesid = ''
    # 获取供求信息
    if not page:
        page_num = 1
    else:
        page_num = page
    page_info = zz91page()
    now_page = page_info.nowpage(int(page_num))
    limit_num = page_info.limitNum(5)
    from_page_count = page_info.frompageCount()
    products_list = getcompanyproductslist(kname=keywords, frompageCount=from_page_count, limitNum=limit_num,seriesid=toseriesid, company_id=company_id,fcflag=keywords)
    all_prods_num = products_list['count']
    list_count = page_info.listcount(all_prods_num)
    page_list_count = page_info.page_listcount()
    next_page = page_info.nextpage()
    prev_page = page_info.prvpage()
    page_range = page_info.page_range()
    first_page = page_info.firstpage()
    last_page = page_info.lastpage()
    return render(request, "shops/products.html", locals())


def products_detail(request, pid):
    """
    :param request: 请求
    :param pid: 供求信息id
    :return: 根据供求信息id,返回对应的供求信息的详细内容
    """
    company_id = getproductscompanyid(pid)
    if company_id:
        comp_info = getcompanydetail(company_id)
    else:
        return render(request, 'html/404.html', locals(), status=404)
    prod_detail = getproductdetail(pid)
    return render(request, "shops/products_details.html", locals())


def news(request, company_id, page):
    """
    :param request: 请求
    :param company_id: 公司id
    :param page: 页码
    :return: 手机站公司动态页面,根据公司id返回对应的公司动态
    """
    # 获取公司信息
    comp_info = getcompanydetail(company_id)
    # 获取公司动态信息
    if not page:
        page_num = 1
    else:
        page_num = page
    page_info = zz91page()
    now_page = page_info.nowpage(int(page_num))
    limit_num = page_info.limitNum(6)
    from_page_count = page_info.frompageCount()
    news_list = getcompanynewslist(from_page_count, limit_num, company_id)
    all_news_num = news_list['count']
    list_count = page_info.listcount(all_news_num)
    page_list_count = page_info.page_listcount()
    next_page = page_info.nextpage()
    prev_page = page_info.prvpage()
    page_range = page_info.page_range()
    first_page = page_info.firstpage()
    last_page = page_info.lastpage()
    return render(request, "shops/news.html", locals())


def news_detail(request, nid):
    """
    :param request: 请求
    :param nid 公司动态id
    :return: 根据公司动态id,返回对应的公司动态的内容
    """
    # 获取公司信息
    company_id = getnewscompanyid(nid)
    if company_id:
        comp_info = getcompanydetail(company_id)
    else:
        return render(request, 'html/404.html', locals(), status=404)
    # 获取公司动态详细信息
    news_detail = getcompanynewsdetails2(nid)
    return render(request, "shops/news_details.html", locals())


def address(request, company_id):
    """
    :param request: 请求
    :param company_id: 公司id
    :return: 根据公司id,返回对应的公司的地址信息,用于显示百度地图
    """
    comp_info = getcompanydetail(company_id)
    return render(request, "shops/address.html", locals())