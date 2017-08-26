# -*- coding:utf-8 -*-
import sys
import json
import xlwt
import urllib
import datetime
from conn import *
from get_time import *
from paginator2 import Paginator2
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from bd_data import get_bd_data, get_bd_pm2, get_sl, get_title, save_to_mongodb2, check_ts_2, \
    get_ts_data2, get_ym_expire, get_ssl, bd_index

reload(sys)
sys.setdefaultencoding('utf8')


def get_page_data(paginator, page_num):
    # 获取分页数据
    try:
        pg_lt = paginator.page(page_num)
    except (PageNotAnInteger, InvalidPage):
        pg_lt = paginator.page(1)
    except EmptyPage:
        pg_lt = paginator.page(paginator.num_pages)
    return pg_lt


def seo_list(request):
    # 返回所有seo_list中的数据
    # 每页15条，按优化时间进行降序排序
    # 功能测试完成时间 2017.6.16 16:05

    # 从session中读取username与user_id
    user_name = request.session.get('username')
    user_id = request.session.get('user_id')
    # 参数等
    url_params = get_all_params(request)  # 拼接传递的参数
    sql_args = ''  # 拼接sql语句
    sql_params = []  # 参数
    sql_args2 = ''
    is_waste = request.GET.get('waste')  # 在线还是过期
    email = request.GET.get('email')  # 搜索邮箱
    keywords = request.GET.get('keywords')  # 搜索关键字
    comp_msb = request.GET.get('comp-msb')  # 搜索门市部链接
    db_qk = request.GET.get('db-qk')  # 搜索是否达标的单子
    yh_ry = request.GET.get('yh-ry')  # 搜索优化负责人对应的单子
    vap_sales = request.GET.get('vap')  # 搜索vap销售对应的单子
    gq_ks_sj = request.GET.get('gq-ks-time')  # 搜索过期开始时间
    gq_jz_sj = request.GET.get('gq-jz-time')  # 搜索过期截止时间
    if is_waste:
        sql_args = " and sk.isexpire=%s"
        sql_params.append(is_waste)
        sql_args2 = " and isexpire=%s"
        if is_waste == '0':
            waste_flag = 0
        elif is_waste == '1':
            waste_flag = 1
    else:
        waste_flag = 2
    if email:
        email = email.strip().encode('gbk', 'ignore')
        sql_args += " and sl.com_email=%s"
        sql_params.append(email)
    if keywords:
        keywords = keywords.strip()
        sql_args += " and sk.keywords like %s"
        sql_params.append('%' + keywords + '%')
    if comp_msb:
        if 'http://' in comp_msb:
            comp_msb = comp_msb.strip().split('http://')[-1]
        else:
            comp_msb = comp_msb.strip()
        sql_args += " and sl.com_msb like %s"
        sql_params.append('%' + comp_msb + '%')
    if db_qk and db_qk != 'default':
        db_qk = db_qk
        sql_args += " and sl.dbflag=%s"
        sql_params.append(db_qk)
    if yh_ry and yh_ry != 'default':
        yh_ry = yh_ry
        sql_args += " and sl.personid=%s"
        sql_params.append(yh_ry)
    if vap_sales and vap_sales != 'default':
        sql_args += " and k.user_id=%s"
        sql_params.append(vap_sales)
    if not user_name and not user_id:
        return HttpResponseRedirect('relogin.html')
    else:
        sql = "select id,realname,isadmin,user_category_code from user where id=%s and username=%s"
        result = fetch_one(sql, [user_id, user_name])
        # print result
        if result:
            is_admin = int(result['isadmin'])
            user_category_code = int(result['user_category_code'])
            # print is_admin, user_category_code
            if not is_admin and user_category_code == 4204:
                seo_name = result['realname']
                seo_id = result['id']
                sql_args += " and us.id=%s"
                sql_params.append(user_id)
            if not is_admin and user_category_code == 1315:
                sql_args += " and k.user_id=%s"
                sql_params.append(user_id)

    # print is_waste, email, keywords, comp_msb, db_qk, yh_ry

    # 获取seolist页面的所有信息
    sql = "select distinct sl.com_id,sl.id,sl.com_email,sl.target_assure,sl.seo_start,sl.baidu_sl," \
          "sl.baidu_fanlian,sl.price,sl.baidu_kuaizhao,sl.com_msb,u1.realname as seoperson,company.name," \
          "u.realname from seo_list as sl left join user as u1 on sl.personid=u1.id " \
          "left join company on sl.com_id=company.id " \
          "left join kh_assign_vap as k on sl.com_id=k.company_id left join user as u on k.user_id=u.id " \
          "left outer join seo_keywordslist as sk on sl.id=sk.sid " \
          "left outer join user as us on sl.personid=us.id " \
          "where sl.id>0" + sql_args
    sql_px = " order by sl.seo_start desc limit %s,%s"
    page_num = request.GET.get('page')
    row_count = get_count(sql, sql_params)
    # print row_count, type(row_count)
    paginator = Paginator2(row_count, page_num)
    sql_params_3 = sql_params
    limit_num = paginator.get_limit_list(page_num)
    # print limit_num, type(limit_num)
    # for each in limit_num:
    #     print each, type(each)
    sql_params_3.extend(limit_num)
    seo_ds = fetch_all(sql + sql_px, sql_params_3)
    # 获取所有客户的所有关键词信息
    for each in seo_ds:
        sql2 = "select keywords,id,sid,target_time,expire_time,target_require,baidu_ranking,isexpire from " \
               "seo_keywordslist where id>0" + sql_args2
        sql2 += " and sid=%s"
        if is_waste:
            all_keywords = fetch_all(sql2, [is_waste, each['id']])
        else:
            all_keywords = fetch_all(sql2, [each['id']])
        each['key_ws'] = all_keywords

    # 获取所有在职的优化人员
    sql3 = "select id,realname from user where closeflag=0 and user_category_code=4204"
    all_seo_ers = fetch_all(sql3)
    # 获取所有在职的vap销售人员
    sql4 = "select id,realname from user where closeflag=0 and user_category_code=1315"
    all_vap_sales = fetch_all(sql4)
    return render(request, "seolist.html", locals())


def fp_kh(request):
    # 分配客户、把客户拉入到过期库或取消拉入到过期库
    # 完成，完成时间2017.6.15 14:16，测试正常
    select_cb = request.POST.get('selectcb')
    do_stay = request.POST.get('dostay')
    to_person_id = request.POST.get('to-person-id')
    if do_stay == 'waste':
        # 放入丢单库
        sql = "update seo_list set waste=1 where id=%s"
        if ',' in select_cb:
            sid = select_cb.split(',')
            for each_sid in sid:
                update_db(sql, [each_sid])
        else:
            update_db(sql, [select_cb])
    if do_stay == 'nowaste':
        # 取消放入丢单库
        sql = "update seo_list set waste=0 where id=%s"
        if ',' in select_cb:
            sid = select_cb.split(',')
            for each_sid in sid:
                update_db(sql, [each_sid])
        else:
            update_db(sql, [select_cb])
    if do_stay == 'assignto':
        # 分配客户
        sql = "update seo_list set personid=%s where id=%s"
        if ',' in select_cb:
            sid = select_cb.split(',')
            for each_sid in sid:
                update_db(sql, [to_person_id, each_sid])
        else:
            update_db(sql, [to_person_id, select_cb])
    referer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer)


def seo_dolist(request):
    # 获取小计
    # 完成，完成时间：2017.6.13 16:00
    try:
        if request.method == 'GET':
            sid = request.GET.get('sid')
            com_id = request.GET.get('com_id')
            # 获取所有的小计
            if sid and com_id:
                sql = "select * from seo_dolist where sid=%s and com_id=%s order by gmt_time desc"
                do_list = fetch_all(sql, [sid, com_id])
                paginator = Paginator(do_list, 15)
                page_num = request.GET.get('page')
                if page_num:
                    do_ls = get_page_data(paginator, page_num)
                else:
                    do_ls = get_page_data(paginator, 1)
            return render(request, "seo_dolist.html", locals())
        elif request.method == 'POST':
            ta_xj = request.POST.get('ta-xj')
            sid = request.POST.get('sid')
            com_id = request.POST.get('com_id')
            if sid and com_id and ta_xj:
                create_time = datetime.datetime.now()
                sql2 = "insert into seo_dolist(sid,com_id,detail,gmt_time) values(%s,%s,%s,%s)"
                update_db(sql2, [sid, com_id, ta_xj, create_time])
                referrer = request.META.get('HTTP_REFERER', '/')
                return HttpResponseRedirect(referrer)
    except Exception:
        pass


def sl_gx(request):
    # 更新收录数
    # 测试完成时间 2017.6.15 21:00
    msb_url = request.GET.get('msb').strip()
    seo_id = request.GET.get('id')
    bd_sl = get_bd_data("site", msb_url)
    get_time = GetTime()
    kdate = get_time.get_strf_time2()
    # print create_time, kdate
    # print msb_url, seo_id, bd_sl
    if bd_sl and seo_id:
        sql = "update seo_list set baidu_sl=%s where id=%s"
        update_db(sql, [bd_sl, seo_id])
        # 收录更新，不录入到seo_keywords_history表中
        # sql2 = "insert into seo_keywords_history(kid,sid,ktype,kdate,baidu_sl,gmt_created) " \
        #        "values(%s,%s,%s,%s,%s,%s)"
        # last_id = update_db(sql2, [0, seo_id, 'baidu_sl', kdate, bd_sl, create_time])
        # print last_id, type(last_id), last_id[0]['id']
        # print r
    return render(request, "get_sl.html", locals())


def fl_gx(request):
    # 更新反链数量
    # 测试完成时间 2017.6.15 21:00
    msb_url = request.GET.get('msb').strip()
    seo_id = request.GET.get('id')
    bd_fl = get_bd_data("domain", msb_url)
    get_time = GetTime()
    kdate = get_time.get_strf_time2()
    if seo_id and bd_fl:
        sql = "update seo_list set baidu_fanlian=%s where id=%s"
        update_db(sql, [bd_fl, seo_id])
        # 反链更新，不录入到seo_keywords_history表中
        # sql2 = "insert into seo_keywords_history(kid,sid,ktype,kdate,baidu_fanlian,gmt_created) " \
        #        "values(%s,%s,%s,%s,%s,%s)"
        # update_db(sql2, [0, seo_id, 'baidu_fl', kdate, bd_fl, create_time])
    return render(request, "get_fl.html", locals())


def pm_gx(request):
    # 关键词排名更新
    # 测试完成时间 2017.6.15 21:00
    msb_url = request.GET.get('msb_url').strip()
    # print type(msb_url)
    k_id = request.GET.get('kid')
    k_ws = request.GET.get('q')
    s_id = request.GET.get('sid')
    get_time = GetTime()
    create_time = get_time.get_strf_time()
    kdate = get_time.get_strf_time2()
    if msb_url and k_id and k_ws and s_id:
        # print msb_url, k_ws, k_id
        bd_pm = get_bd_pm2(k_ws, msb_url)
        if bd_pm:
            sql = "update seo_keywordslist set baidu_ranking=%s where id=%s"
            update_db(sql, [bd_pm, k_id])
            sql2 = "insert into seo_keywords_history(baidu_ranking,ktype,kdate,gmt_created,kid,sid) " \
                   "values(%s,%s,%s,%s,%s,%s)"
            update_db(sql2, [bd_pm, 'check_pai', kdate, create_time, k_id, s_id])
    return render(request, "get_pm.html", locals())


def add_seokh(request):
    # 获取客户对应的邮箱
    # 测试完成时间 2017.6.15 21:00
    user_name = request.session.get('username')
    user_id = request.session.get('user_id')
    if not user_name and not user_id:
        return HttpResponseRedirect('relogin.html')
    else:
        sql = "select id,realname from user where id=%s"
        result = fetch_one(sql, [user_id])
        if result:
            user_name = result['realname']
    seo_email = request.POST.get('seo-zh')
    # print seo_email, type(seo_email)
    if seo_email:
        seo_email = seo_email.strip()
    else:
        seo_email = ""
    sql = "select c.name as comp_name,c.id as comp_id from company_account as ca  left join company as c " \
          "on ca.company_id=c.id WHERE ca.account=%s"
    comp = fetch_all(sql, [seo_email])
    # print comp
    if comp:
        comp_name = comp[0]['comp_name']
        com_id = comp[0]['comp_id']
        # print comp_name
    # 获取当前时间以及三个月后的时间
    get_time = GetTime()
    now_time = get_time.get_strf_time2()
    three_month_later = get_time.get_after_time()
    return render(request, "add_seokh.html", locals())


def save_seokh(request):
    # 提交录入的seo客户信息
    # seo_list表录入信息包括公司id：com_id、账号：seo_zh、开始优化时间：yh_start_time、保证达标时间：bz_db_time
    # 门市部链接：msb_link、优化单子接入价格：yg_jg
    # 测试完成时间 2017.6.15 21:00
    com_id = request.POST.get('com_id')
    seo_zh = request.POST.get('seo-zh')
    seo_zh_comp = request.POST.get('seo-zh-comp')
    seo_kews = request.POST.get('seo-kews')
    yh_start_time = request.POST.get('yh-start-time')
    bz_db_time = request.POST.get('bz-db-time')
    msb_link = request.POST.get('msb-link')
    yh_jg = request.POST.get('yh-jg')
    lr_ry = request.POST.get('lr-ry')
    if com_id:
        com_id = com_id
    else:
        com_id = '0'
    if seo_zh:
        seo_zh = seo_zh.strip()
    if seo_zh_comp:
        seo_zh_comp = seo_zh_comp.strip()
    if seo_kews:
        if '|' in seo_kews:
            kw_list = seo_kews.strip().split('|')
            seo_kews = kw_list
            # print u'有|，%s, %s' % (seo_kews, type(seo_kews))
        else:
            seo_kews = seo_kews.strip()
            # print u'无|，%s, %s' % (seo_kews, type(seo_kews))
    if msb_link:
        msb_link = msb_link.strip()
        if 'http://' in msb_link:
            msb_link = msb_link.split('http://')[-1]
    if lr_ry:
        lr_ry = lr_ry
    # 存入到数据库
    create_time = datetime.datetime.now()
    # print com_id, seo_zh, seo_zh_comp, seo_kews, yh_start_time, bz_db_time, msb_link, yh_jg, create_time
    sql = "insert into seo_list(com_id,com_email,seo_start,target_assure,com_msb,price,gmt_created,dbflag," \
          "waste,personid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    last_id = update_db(sql, [com_id, seo_zh, yh_start_time, bz_db_time, msb_link, yh_jg, create_time, 0, 0, lr_ry])
    # print last_id
    sql2 = "insert into seo_keywordslist(sid,keywords,com_msb,seo_start,target_assure,price,dbtype," \
           "gmt_created,personid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # 区分一个关键词还是多个关键词
    # if type(seo_kews) == type([]):
    if isinstance(seo_kews, list):
        for each_kw in seo_kews:
            each_kw = each_kw.encode('utf-8', 'ignore')
            # print each_kw, type(each_kw)
            update_db(sql2, [last_id['id'], each_kw, msb_link, yh_start_time, bz_db_time, 0, 0, create_time, lr_ry])
    else:
        # print seo_kews, type(seo_kews)
        seo_kews = seo_kews.encode('utf-8', 'ignore')
        update_db(sql2, [last_id['id'], seo_kews, msb_link, yh_start_time, bz_db_time, 0, 0, create_time, lr_ry])
    return render(request, "save_seokh.html", locals())


def modify_seokh(request):
    # 修改客户关键词等相关信息
    # 测试完成时间 2017.6.15 21:00
    # 获取当前时间以及三个月后的时间
    get_time = GetTime()
    now_time = get_time.get_strf_time2()
    three_month_later = get_time.get_after_time()
    sql_args = ''
    sql_params = []
    if request.method == 'GET':
        seo_list_id = request.GET.get('id')
        del_action = request.GET.get('action')
        is_waste = request.GET.get('waste')
        if is_waste:
            sql_args += ' and isexpire=%s'
        # print seo_list_id
        # 展示可以修改的百度优化单子信息
        if seo_list_id:
            sql = "select sl.id,sl.com_email,sl.com_msb,sl.price,sl.target_assure,sl.seo_start,user.realname " \
                  "from seo_list as sl " \
                  "left join user on sl.personid=user.id " \
                  "where sl.id=%s" % seo_list_id
            ms_info = fetch_all(sql)
            # print ms_info
            for each in ms_info:
                sql2 = "select keywords,price,id,target_time,expire_time,seo_start,target_require,isexpire " \
                       "from seo_keywordslist where sid=%s" + sql_args
                if is_waste:
                    ms_info2 = fetch_all(sql2, [each['id'], is_waste])
                else:
                    ms_info2 = fetch_all(sql2, [each['id']])
                each['ky_ws'] = ms_info2
                # print ms_info2
            # print ms_info
            if ms_info:
                com_email = ms_info[0]['com_email']
                msb = ms_info[0]['com_msb']
                price = ms_info[0]['price']
                yh_time = ms_info[0]['seo_start']
                db_time = ms_info[0]['target_assure']
                all_kys = ms_info[0]['ky_ws']
                yhr_name = ms_info[0]['realname']
                if 'www' in msb:
                    msb2 = msb.split('www.')[-1]
                    gq_time = get_ym_expire(msb2)
            return render(request, "modify_seokh.html", locals())
        # 删除关键词
        if del_action == 'del':
            kid = request.GET.get('kid')
            sql = "delete from seo_keywordslist where id=%s"
            update_db(sql, [kid])
            referer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer)
        else:
            referer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer)
    if request.method == 'POST':
        kid = request.POST.get('kid')
        add_ky = request.POST.get('add-ky')
        is_xg_dz = request.POST.get('xg-dz')
        # 修改关键词
        if kid:
            keywords = request.POST.get('xg-ky')
            price = request.POST.get('xg-ky-jg')
            db_yq = request.POST.get('db-yq-' + kid)
            ky_db_time = request.POST.get('xg-db-time')
            ky_gq_time = request.POST.get('xg-gq-time')
            is_expire = int(request.POST.get('isexpire-' + kid))
            # print kid, keywords, price, ky_db_time, ky_gq_time
            if keywords and price and ky_db_time and ky_gq_time:
                keywords = keywords.strip()
                # print kid, keywords, price, ky_db_time, ky_gq_time
                sql = "update seo_keywordslist set keywords=%s,price=%s,target_time=%s,expire_time=%s," \
                      "target_require=%s,isexpire=%s,dbtype=%s where id=%s"
                r = update_db(sql, [keywords, price, ky_db_time, ky_gq_time, db_yq, is_expire, 1, kid])
            referer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer)
        # 添加关键词
        if add_ky == 'add':
            msb = request.POST.get('msb')
            sid = request.POST.get('sid')
            keywords = request.POST.get('keywords')
            price = request.POST.get('keyws-price')
            db_yq = request.POST.get('ky-db-yq')
            yh_ks_time = request.POST.get('ky-db-time')
            yh_bz_time = request.POST.get('ky-gq-time')
            is_expire = request.POST.get('ky-isexpire')
            get_time = GetTime()
            gmt_time = get_time.time_now()
            # print msb, sid, keywords, price, db_yq, yh_ks_time, yh_bz_time, is_expire, gmt_time
            if keywords and price and db_yq:
                keywords = keywords.strip()
                sql = "insert into seo_keywordslist(sid,keywords,com_msb,price,target_require,seo_start," \
                      "target_assure,isexpire,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                update_db(sql, [sid, keywords, msb, price, db_yq, yh_ks_time, yh_bz_time, is_expire, gmt_time])
            referer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer)
        # 百度优化单子信息修改，可以修改优化时间、保证达标时间、门市部链接、单子接入价格
        if is_xg_dz == 'xg-dz':
            dz_yh_time = request.POST.get('yh-time')
            dz_db_time = request.POST.get('db-time')
            msb_link = request.POST.get('msb-link')
            dz_jg = request.POST.get('yh-jg')
            dz_id = request.POST.get('dz-id')
            # print dz_yh_time, dz_db_time, msb_link, dz_jg, dz_id
            if dz_yh_time and dz_db_time and msb_link and dz_jg:
                msb_link = msb_link.split('http://')[-1]
                sql = "update seo_list set seo_start=%s,target_assure=%s,com_msb=%s,price=%s where id=%s"
                update_db(sql, [dz_yh_time, dz_db_time, msb_link, dz_jg, dz_id])
            referer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer)
    else:
        return HttpResponse("信息录入有误")


def del_seokh(request):
    # 删除指定的seo客户
    # 测试完成时间2017.6.16 10:00
    kh_id = request.GET.get('id')
    if kh_id:
        # 删除单子
        sql = "delete from seo_list where id=%s"
        update_db(sql, [kh_id])
        # 删除单子里的所有关键词
        sql2 = "select k.id from seo_keywordslist as k left outer join seo_list as s on k.sid=s.id where " \
               "k.sid=%s"
        result = fetch_all(sql2, [kh_id])
        for each in result:
            sql3 = "delete from seo_keywordslist where id=%s"
            update_db(sql3, [each['id']])
    refer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(refer)


def k_history(request):
    # 关键词排名更新历史
    sid = request.GET.get('sid')
    kid = request.GET.get('kid')
    page_num = request.GET.get('page')
    url_params = get_all_params(request)
    if sid and kid:
        sql = "select baidu_ranking,gmt_created from seo_keywords_history where sid=%s and kid=%s " \
              "order by gmt_created desc"
        # k_hs = fetch_all(sql, [sid, kid])
        # if page_num:
        #     k_hs = get_page_data(k_hs, 15)
        sql_params = [sid, kid]
        sql_lmt = " limit %s,%s"
        row_count = get_count(sql, sql_params)
        paginator = Paginator2(row_count, page_num)
        limit_num = paginator.get_limit_list(page_num)
        sql_params.extend(limit_num)
        # print sql_params
        k_hs = fetch_all(sql + sql_lmt, sql_params)
    return render(request, "k_history.html", locals())


def get_all_params(request):
    # 获取翻页前所有的url参数，传递到下一页
    get_paras = request.GET.items()
    url_params = {}
    for key, value in get_paras:
        if key != 'page':
            url_params[key] = value
    url_params = urllib.urlencode(url_params)
    return url_params


def get_index_link(request):
    # 获取每次进来的首页的url
    index_link = request.get_full_path().split('/')[1].encode('utf-8')
    return index_link


def pl_sl(request):
    # 批量收录
    bd_url = request.GET.get('url')
    if bd_url:
        bd_url = bd_url.strip()
        bd_sl = get_sl(bd_url)
        return render(request, "get_sl.html", locals())
    return render(request, "pl_sl.html", locals())


def pl_sl2(request):
    # 批量收录改进版
    bd_url_list = request.POST.get('bdurls')
    bd_url_list2 = []
    bd_url_list3 = []
    if bd_url_list:
        bd_url_list2 = bd_url_list.split('\r\n')
        for each_url in bd_url_list2:
            if each_url != '':
                bd_url_list3.append(each_url)
        bd_url_list = enumerate(bd_url_list3)
        return render(request, "pl_sl2.html", locals())
    return HttpResponse("没有任何数据", status=500)


def get_plsl(request):
    # 获取批量收录数据
    bd_url = request.GET.get('url')
    bt_sl = {}
    if bd_url:
        bd_url = bd_url.strip()
        wz_title = get_title(bd_url)
        bt_sl["title"] = wz_title
        sl_status = get_sl(bd_url)
        bt_sl["sl-status"] = str(sl_status)
        js_data = json.dumps(bt_sl)
        # print js_data, type(js_data)
        # print bd_url, wz_title, sl_status
    return render(request, "get_plsl.html", locals())


def file_iterator(file_name, chunk_size=512):
    # 把文件存到本地
    # ie导出时文件名中文会出现乱码，有待解决
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def export_excel(request):
    # 导出到excel
    wz_title = request.POST.getlist('cx-title')
    wz_url = request.POST.getlist('cx-url')
    sl_status = request.POST.getlist('cx-slstatus')
    all_num = request.POST.get('tj-all-num')
    sl_num = request.POST.get('tj-sl-num')
    wsl_num = request.POST.get('tj-wsl-num')
    sl_rate = request.POST.get('sl-rate')
    if wz_title and wz_url and sl_status:
        length = len(wz_title)
        wb = xlwt.Workbook()
        font_family = xlwt.easyxf('font:name Microsoft YaHei')
        bt_style = xlwt.easyxf('font:name Microsoft YaHei;alignment:horz center;')
        sl_style = xlwt.easyxf('font:name Microsoft YaHei,color green,bold 1;alignment:horz center;')
        wsl_style = xlwt.easyxf('font:name Microsoft YaHei,color red,bold 1;alignment:horz center;')
        tj_style = xlwt.easyxf('font:name Microsoft YaHei,color light_orange,bold 1;')
        # font_align = xlwt.XFStyle()
        # font_align.alignment.horz = 2
        # font_align.font.name = 'simSun'
        ws = wb.add_sheet(u'批量收录查询报表')
        ws.write(0, 0, u'标题', bt_style)
        ws.write(0, 1, u'链接', bt_style)
        ws.write(0, 2, u'收录状态', bt_style)
        ws.write(0, 3, u'统计信息', bt_style)
        ws.col(0).width = 0x0d00 + 15000
        ws.col(1).width = 0x0d00 + 12000
        ws.col(2).width = 0x0d00  # 3328
        ws.col(3).width = 0x0d00 + 5000
        for each_index in range(length):
            ws.write(each_index + 1, 0, wz_title[each_index], font_family)
            ws.write(each_index + 1, 1, wz_url[each_index], font_family)
            if sl_status[each_index] == u'收录':
                ws.write(each_index + 1, 2, sl_status[each_index], sl_style)
            else:
                ws.write(each_index + 1, 2, sl_status[each_index], wsl_style)
        if all_num and sl_num and wsl_num and sl_rate:
            ws.write(1, 3, u'总数:' + all_num, tj_style)
            ws.write(2, 3, u'百度pc收录数:' + sl_num, tj_style)
            ws.write(3, 3, u'百度pc未收录数:' + wsl_num, tj_style)
            ws.write(4, 3, u'百度pc收录率:' + sl_rate, tj_style)
            ws.write(5, 3, u'zz91再生网-seo小组为您整理生成', tj_style)
            ws.write(6, 3, u'生成时间:' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tj_style)
        file_name = '批量收录查询_' + datetime.datetime.now().strftime("%Y-%m-%d") + '.xls'.encode('gb2312')
        wb.save(file_name)
        response = StreamingHttpResponse(file_iterator(file_name))
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    return HttpResponse("无数据可导出", status=500)


# def pl_ts(request):
#     # 批量推送
#     bd_token = ''
#     bd_url_list2 = []
#     all_ts_info = []
#     ts_sp = request.POST.get('ts-sp')
#     ts_dl = request.POST.get('ts-dl')
#     bd_url = request.POST.get('bdurls')
#
#     # 判断推送的是独立网站还是zz91商铺
#     if ts_sp and ts_sp == '0':
#         bd_token += 'b35gLljevCgUJrj5'
#     if ts_dl and ts_dl == '1':
#         bd_token += 'Z29qxdD99L2JKKaH'
#
#     # 处理空格
#     if bd_url:
#         bd_url_list = bd_url.strip().split('\r\n')
#         for each_url in bd_url_list:
#             if each_url != '':
#                 bd_url_list2.append(each_url)
#         connect('richangts', host='192.168.2.178', port=27017)
#         for each_url in bd_url_list2:
#             domain = each_url.split('/')[2]
#             # print domain, bd_token
#             r = threading.Thread(target=save_to_mongodb2, args=(each_url, domain, bd_token))
#             r.start()
#             ts_info = Tuisong.objects(ts_link=each_url)
#             all_ts_info.append(ts_info)
#         return render(request, "pl_ts.html", locals())
#     return HttpResponse("无数据可推送", status=500)


def pl_ts2(request):
    # 批量收录改进版
    bd_url_list = request.POST.get('bdurls')
    ts_wz = request.POST.get('ts-wz')
    # if not ts_wz:
    #     ts_wz = request.POST.get('ts-wz-2')
    bd_url_list2 = []
    bd_url_list3 = []
    if bd_url_list:
        bd_url_list2 = bd_url_list.split('\r\n')
        for each_url in bd_url_list2:
            if each_url != '':
                bd_url_list3.append(each_url)
        bd_url_list = enumerate(bd_url_list3)
        return render(request, "pl_ts2.html", locals())
    return HttpResponse("没有任何数据", status=500)


def ts_json_data(bd_url):
    # 根据url获取推送过的信息
    pl_ts = {}
    ts_info = get_ts_data2(bd_url)
    for each_info in ts_info:
        pl_ts['ts_time'] = str(each_info['ts_time'].strftime("%Y-%m-%d %H:%M:%S"))
        pl_ts['ts_status'] = str(each_info['ts_message_info'])
        pl_ts['ts_return'] = str(each_info['ts_message_remain'])
    js_data = json.dumps(pl_ts)
    # print js_data
    return js_data


def get_plts(request):
    # 批量获取推送的信息
    bd_url = request.GET.get('url')
    ts_wz = request.GET.get('tswz')
    if bd_url and ts_wz:
        ts_status1 = check_ts_2(bd_url)
        if ts_status1 == 0:
            js_data = ts_json_data(bd_url)
        else:
            domain = bd_url.strip().split('/')[2]
            bd_token = 'b35gLljevCgUJrj5'
            result = save_to_mongodb2(bd_url, domain, bd_token)
            if result == 1:
                js_data = ts_json_data(bd_url)
    return render(request, "get_plts.html", locals())


def xz_mb(request):
    # 在线选择模板
    return render(request, "moban.html", locals())


def ci_ku(request):
    # 批量查询关键词
    user_name = request.session.get('username')
    user_id = request.session.get('user_id')
    if not user_name and not user_id:
        return HttpResponseRedirect('relogin.html')
    return render(request, "ciku.html", locals())


def ci_ku_tj(request):
    # 批量查询关键词统计页面
    keywords_list = request.POST.get('keywords')
    cx_xz = request.POST.get('cx-xz')
    cx_person = request.POST.get('person')
    sql = "select realname from user where username=%s"
    real_name = fetch_one(sql, [cx_person])
    if real_name:
        cx_person = real_name['realname']
    k_list2 = []
    if keywords_list:
        k_list = keywords_list.strip().split('\r\n')
        for each_ky in k_list:
            if each_ky != u'':
                # print each_ky
                k_list2.append(each_ky)
        k_list = enumerate(k_list2)
        # print k_list, type(k_list)
        return render(request, "pl_ciku.html", locals())
    return HttpResponse("无任何关键词信息", status=500)


def get_gjc_ck(cx_xz, pc_index, in_ssl):
    # 判断关键词是否能做
    if pc_index == '--' or pc_index == '0':
        # 没有百度指数或百度指数为0
        if cx_xz == '0':
            # 查询的为zz91商铺
            if int(in_ssl) < 10000:
                cx_jy = 1
            else:
                cx_jy = 0
            return cx_jy
        if cx_xz == '1':
            # 查询的为独立网站
            if int(in_ssl) < 100000:
                cx_jy = 1
            else:
                cx_jy = 0
            return cx_jy
    else:
        # 有百度指数，不能做
        cx_jy = 0
        return cx_jy


def check_jz(keyword, cx_xz):
    # 判断目前crm里在线的词的完全匹配度
    sql = 'select * from seo_keywordslist where keywords=%s'
    result = fetch_all(sql, [keyword])
    # print result
    if result:
        return 1
    else:
        return 0


def save_gjc(js_data):
    # 保存搜索的关键词到mongodb
    db = conn_mongodb()
    collection = db.seo_gjc
    get_time = GetTime()
    now_time = get_time.time_now()
    post_info = {'create_time': now_time, 'keywords': js_data['keywords'], 'bd_index': js_data['zt_index'],
                 'bd_ssl': js_data['gjc_ssl'], 'bd_intitle_ssl': js_data['gjc_intitle_ssl'],
                 'cx_xz': js_data['cx_xz'], 'cx_jy': js_data['cx_jy'], 'reason': js_data['ck_jy'],
                 'person': js_data['person'], 'ck_jg': js_data['ck_jg']
                 }
    collection.insert_one(post_info)


def get_pl_cc(request):
    # 获取批量查询关键词的json
    user_name = request.session.get('username')
    user_id = request.session.get('user_id')
    if not user_name and not user_id:
        return HttpResponseRedirect('relogin.html')
    else:
        sql = "select realname from user where username=%s and id=%s"
        real_name = fetch_one(sql, [user_name, user_id])
        # print real_name
        if real_name:
            user_name = real_name['realname']
    key_word = request.GET.get('keyword')
    cx_xz = request.GET.get('cx-xz')
    if cx_xz == '0':
        cx_wz = 'zz91商铺'
    else:
        cx_wz = '独立网站'
    reason = {
        '0': '原因:有百度指数',
        '1': '原因:百度指数过高',
        '2': '原因:已经有客户做过这个词',
        '3': '原因:做的客户较多,建议咨询:吴凌峰,QQ:1727828907',
        '4': '原因:关键词字数较短,建议咨询:吴凌峰,QQ:1727828907',
        '5': '原因:intitle搜索量过高',
        '6': '原因:获取百度指数超时,建议您稍后再进行查询',
        '7': '原因:搜索量大于1000w,一般情况难度都比较大,建议不接'
    }
    keyword_price = {
        '0': '￥1500-￥2500',
        '1': '￥2500-￥3500',
        '2': '￥3500-￥5500',
        '3': '大于￥6000'
    }
    limit_keywords = ['电表', '编织袋']
    bd_zs = bd_index(key_word)
    flag = 0
    timeout_flag = 1
    # 判断是否为限制词
    if limit_keywords[0] in key_word or limit_keywords[1] in key_word:
        flag = 1
    # 判断是否抓取超时
    if limit_keywords[0] not in key_word and limit_keywords[1] not in key_word:
        flag = 0
    if bd_zs['index'] != '超时,未获取到':
        timeout_flag = 1
    else:
        timeout_flag = 0
    if key_word and flag == 0 and timeout_flag:
        length = len(key_word)
        bd_zs['keywords'] = key_word
        if bd_zs['keywords'] != bd_zs['kw']:
            pc_index = bd_zs['kw']
        else:
            pc_index = bd_zs['index']
        bd_zs['zt_index'] = pc_index
        gjc_ssl = get_ssl(key_word)
        gjc_intitle_ssl = get_ssl('intitle:' + key_word)
        bd_zs['gjc_ssl'] = gjc_ssl
        bd_zs['gjc_intitle_ssl'] = gjc_intitle_ssl
        bd_zs['cx_xz'] = cx_wz
        bd_zs['ck_jy'] = '--'
        bd_zs['ck_jg'] = '--'
        # 测试是否有客户已经做过此关键词
        jz_result = check_jz(key_word, cx_xz)
        if jz_result:
            # 已经做过,不能做
            bd_zs['ck_jy'] = reason['2']
            bd_zs['cx_jy'] = 0
        else:
            cx_jy = get_gjc_ck(cx_xz, pc_index, gjc_intitle_ssl)
            bd_zs['cx_jy'] = cx_jy
            if length < 4:
                # 字数为1-3个字,做过的不能做,未做过的建议咨询
                # 如果没有其他原因,会显示过短,建议咨询
                bd_zs['cx_jy'] = 0
                bd_zs['ck_jy'] = reason['4']
                # 不能做的,指数原因
                if pc_index != '--' and pc_index != '0' and not cx_jy:
                    if (int(pc_index) > 0) and (int(pc_index) < 50):
                        bd_zs['ck_jy'] = reason['0']
                    if int(pc_index) > 50:
                        bd_zs['ck_jy'] = reason['1']
            else:
                # 字数大于4个字的
                if cx_jy:
                    # 可以做的,报参考价格
                    if (int(gjc_ssl) >= 0) and (int(gjc_ssl) <= 2000000):
                        bd_zs['ck_jg'] = keyword_price['0']
                    if (int(gjc_ssl) > 2000000) and (int(gjc_ssl) <= 5000000):
                        bd_zs['ck_jg'] = keyword_price['1']
                    if (int(gjc_ssl) > 5000000) and (int(gjc_ssl) <= 8000000):
                        bd_zs['ck_jg'] = keyword_price['2']
                    if (int(gjc_ssl) > 8000000) and (int(gjc_ssl) <= 10000000):
                        bd_zs['ck_jg'] = keyword_price['3']
                    if int(gjc_ssl) > 10000000:
                        # 超过1000w的均不能做
                        bd_zs['cx_jy'] = 0
                        bd_zs['ck_jy'] = reason['7']
                else:
                    # 不能做的,指数原因
                    if pc_index != '--' and pc_index != '0':
                        if (int(pc_index) > 0) and (int(pc_index) < 50):
                            bd_zs['ck_jy'] = reason['0']
                        if int(pc_index) > 50:
                            bd_zs['ck_jy'] = reason['1']
                    # 不能做的,intitle搜索量原因
                    if pc_index == '--' or pc_index == '0':
                        bd_zs['ck_jy'] = reason['5']
        bd_zs['person'] = user_name
        save_gjc(bd_zs)
        js_data = json.dumps(bd_zs)
        return render(request, "get_pl_cc.html", locals())
    if key_word and flag == 1 and timeout_flag:
        bd_zs = bd_index(key_word)
        bd_zs['keywords'] = key_word
        if bd_zs['keywords'] != bd_zs['kw']:
            pc_index = bd_zs['kw']
        else:
            pc_index = bd_zs['index']
        bd_zs = {'index': '--', 'gjc_ssl': '--', 'gjc_intitle_ssl': '--', 'cx_xz': cx_wz, 'cx_jy': 0,
                 'ck_jy': reason['3'], 'keywords': key_word, 'person': user_name, 'zt_index': pc_index,
                 'ck_jg': '--'}
        jz_result = check_jz(key_word, cx_xz)
        if jz_result:
            bd_zs['ck_jy'] = reason['2']
        else:
            if pc_index != '--':
                if (int(pc_index) > 0) and (int(pc_index) < 50):
                    bd_zs['ck_jy'] = reason['0']
                if int(pc_index) > 50:
                    bd_zs['ck_jy'] = reason['1']
        save_gjc(bd_zs)
        js_data = json.dumps(bd_zs)
        return render(request, "get_pl_cc.html", locals())
    if not timeout_flag:
        pc_index = bd_zs['index']
        bd_zs = {'index': '--', 'gjc_ssl': '--', 'gjc_intitle_ssl': '--', 'cx_xz': cx_wz, 'cx_jy': 0,
                 'ck_jy': reason['6'], 'keywords': key_word, 'person': user_name, 'zt_index': pc_index,
                 'ck_jg': '--'}
        jz_result = check_jz(key_word, cx_xz)
        save_gjc(bd_zs)
        js_data = json.dumps(bd_zs)
        return render(request, "get_pl_cc.html", locals())
    return HttpResponse("未获取到任何关键词信息", status=500)


def gjc_cx_jl(request):
    # 关键词查询记录
    db = conn_mongodb()
    row_count = db.seo_gjc.find().count()
    page_num = request.GET.get('page')
    paginator = Paginator2(row_count, page_num)
    limit_num = paginator.get_limit_list(page_num)
    all_keywords = db.seo_gjc.find().sort("create_time", pymongo.DESCENDING).skip(limit_num[0]).limit(limit_num[1])
    return render(request, "cx_jl.html", locals())


def yue_bao(request):
    # 客户月报函数
    s_id = request.GET.get('id')
    get_time = GetTime()
    now_month = get_time.get_month()
    now_time = get_time.get_strf_time2()
    # 获取公司名称
    sql = "select c.name,sl.com_msb from seo_list as sl left join company as c on sl.com_id=c.id " \
          "where sl.id=%s"
    result = fetch_one(sql, [s_id])
    if result:
        com_name = result['name']
        com_msb = result['com_msb']
    # 获取该id对应的客户的所有已经上线的关键词和排名
    sql2 = "select sk.keywords,sk.baidu_ranking from seo_keywordslist as sk left join seo_list as sl " \
           "on sk.sid=sl.id where sl.id=%s and sk.isexpire=0 and sk.dbtype=1"
    result2 = fetch_all(sql2, [s_id])
    if result2:
        result2 = enumerate(result2)
        return render(request, "yuebao.html", locals())
    return HttpResponse('没有达标的关键词', status=500)



