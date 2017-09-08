# -*- coding:utf-8 -*-
import os
import sys
import json
import urllib
from zz91page import zz91page
from get_time import GetTime
from zz91db_ast import companydb
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

reload(sys)
sys.setdefaultencoding('utf8')
dbc = companydb()
now_path = os.path.dirname(__file__)
execfile(now_path + "/func/qunfa_function.py")


def qunfa_list(request):
    # 购买群发客户列表
    all_qf_data = get_qf_info()
    rowcount = len(all_qf_data)
    page_info = zz91page()
    page_num = request.GET.get('page')
    if not page_num:
        page_num = 1
    limit_num = page_info.limitNum(15)
    now_page = page_info.nowpage(int(page_num))
    from_page = page_info.frompageCount()
    list_count = page_info.listcount(int(rowcount))
    page_list_count = page_info.page_listcount()
    all_qf_data = get_qf_info(from_page, limit_num)
    first_page = page_info.firstpage()
    last_page = page_info.lastpage()
    next_page = page_info.nextpage()
    prev_page = page_info.prvpage()
    return render(request, "qunfa/quanfa_list.html", locals())


def qunfa_record(request):
    # 群发速配管理

    # 获取购买速配的客户的群发内容
    qf_id = request.GET.get('qf_id')  # 购买群发的id
    if qf_id:
        qf_sql = "select content from shop_qunfa where id=%s"
        qf_result = dbc.fetchonedb(qf_sql, [qf_id])
        if qf_result:
            qf_content = qf_result[0]
        # 修改群发内容
        xg_qf_content = request.POST.get('qf-content')
        if xg_qf_content:
            sql_gx = "update shop_qunfa set content=%s where id=%s"
            dbc.updatetodb(sql_gx, [xg_qf_content, qf_id])
            refer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(refer)
        return render(request, "qunfa/qunfa_record.html", locals())
    return HttpResponse(u'无任何群发内容', status=500)


def qunfa_manage(request):
    # 群发任务管理
    all_qf_data = get_qf_info()
    rowcount = len(all_qf_data)
    page_info = zz91page()
    page_num = request.GET.get('page')
    if not page_num:
        page_num = 1
    limit_num = page_info.limitNum(15)
    now_page = page_info.nowpage(int(page_num))
    from_page = page_info.frompageCount()
    list_count = page_info.listcount(int(rowcount))
    page_list_count = page_info.page_listcount()
    all_qf_data = get_qf_info(from_page, limit_num)
    first_page = page_info.firstpage()
    last_page = page_info.lastpage()
    next_page = page_info.nextpage()
    prev_page = page_info.prvpage()
    return render(request, "qunfa/qunfa_manage.html", locals())


def match_keywords(request):
    # 根据关键词与过滤条件,匹配供求客户
    url_params = get_all_params(request)  # 拼接传递的参数
    qf_id = request.GET.get('qf-id')  # 购买群发的id
    pdt_kind = request.GET.get('prod-style')  # 供应或求购
    pdt_area = request.GET.get('province')  # 地区,选择对应的额省份
    refresh_start_time = request.GET.get('refresh-start-time')  # 刷新起始时间
    refresh_end_time = request.GET.get('refresh-end-time')  # 刷新结束时间
    search_keyword = request.GET.get('search-keyword')  # 需要搜索的关键词
    is_had_sent = request.GET.get('filter-account')  # 默认是过滤已发送客户,为空的时候不过滤
    page_num = request.GET.get('page')
    page_info = zz91page()
    if not page_num:
        page_num = 1
    page_info.nowpage(int(page_num))
    limit_num = page_info.limitNum(10)
    from_page = page_info.frompageCount()
    all_products = get_all_products(int(from_page), limit_num, 100000, pdt_kind, search_keyword, refresh_start_time,
                                    refresh_end_time, pdt_area)
    next_page = page_info.nextpage()
    prev_page = page_info.prvpage()
    all_num = all_products['all_num']
    if all_num > 100000:
        all_num = 100000
    list_count = page_info.listcount(int(all_num))
    page_list_count = page_info.page_listcount()
    first_page = page_info.firstpage()
    last_page = page_info.lastpage()
    return render(request, "qunfa/qunfa_match_keywords.html", locals())


def add_task(request):
    # 选择客户产品进行速配服务
    # 添加测试数据
    # sql_test = "select id,company_id,products_type_code,title,refresh_time from products where " \
    #            "company_id=718590 and is_del=0 limit 0,20"
    # test_product = dbc.fetchalldb(sql_test)
    # for each_prod in test_product:
    #     sql_record = "insert into shop_qunfa_record(pdt_id,company_id,comp_id_buy,sq_id,pdt_kind," \
    #                  "pdt_title,pdt_refresh_time,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    #     get_time = GetTime()
    #     time_now = get_time.time_now()
    #     refresh_time = each_prod[4]
    #     pro_id = each_prod[0]
    #     pdt_kind = each_prod[2]
    #     if pdt_kind == '10331000':
    #         pdt_kind = '0'
    #     else:
    #         pdt_kind = '1'
    #     pdt_title = each_prod[3]
    #     company_id = each_prod[1]
    #     comp_id_buy = '123572238'
    #     qf_id = '4'
    #     dbc.updatetodb(sql_record, [pro_id, company_id, comp_id_buy, qf_id, pdt_kind, pdt_title, refresh_time,
    #                                 time_now])
    prod_list = []
    default_tr_num = xrange(20)
    pdt_list = request.POST.getlist('cbb')
    qf_id = request.POST.get('qf_id')
    qf_id_2 = request.GET.get('qf_id')
    if qf_id:
        qf_id = qf_id
    elif qf_id_2:
        qf_id = qf_id_2
    else:
        qf_id = ''

    # 获取某个群发id对应的公司id
    sql_comp_id = "select company_id from shop_qunfa where id=%s"
    comp_id_buy = ''
    if qf_id:
        result_comp = dbc.fetchonedb(sql_comp_id, [qf_id])
        if result_comp:
            comp_id_buy = result_comp[0]
    if pdt_list:
        for each_pdt in pdt_list:
            each_pdt = json.loads(each_pdt)
            prod_list.append(each_pdt)
    if prod_list:
        for each_prod in prod_list:
            sql_record = "insert into shop_qunfa_record(pdt_id,company_id,comp_id_buy,sq_id,pdt_kind," \
                         "pdt_title,pdt_refresh_time,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            get_time = GetTime()
            time_now = get_time.time_now()
            refresh_time = get_time.str_to_datetime(each_prod['refresh_time'])
            pro_id = each_prod['pro_id']
            pdt_kind = each_prod['pdt_kind']
            pdt_title = each_prod['pdt_title']
            company_id = each_prod['company_id']
            # 过滤已经添加过的
            sql_filter = "select id from shop_qunfa_record where pdt_id=%s"
            result_filter = dbc.fetchonedb(sql_filter, [pro_id])
            if result_filter:
                had_added = 1
            else:
                had_added = 0
            if had_added == 0:
                dbc.updatetodb(sql_record, [pro_id, company_id, comp_id_buy, qf_id, pdt_kind, pdt_title, refresh_time,
                                            time_now])
    # 获取qunfa_record表里的内容
    # 添加到待发任务里
    sql_qf_record = "select * from shop_qunfa_record where sq_id=%s"
    rowcount = len(dbc.fetchalldb(sql_qf_record, [qf_id]))
    sql_qf_record += ' limit %s,%s'
    page_info = zz91page()
    page_num = request.GET.get('page')
    if not page_num:
        page_num = 1
    page_info.nowpage(int(page_num))
    limit_num = page_info.limitNum(20)
    from_page = page_info.frompageCount()
    pt_list = dbc.fetchalldb(sql_qf_record, [qf_id, int(from_page), int(limit_num)])
    next_page = page_info.nextpage()
    prev_page = page_info.prvpage()
    list_count = page_info.listcount(int(rowcount))
    page_list_count = page_info.page_listcount()
    first_page = page_info.firstpage()
    last_page = page_info.lastpage()

    # 表格栏里的删除待发任务里已经添加的任务
    del_id = request.GET.get('del_id')
    if del_id:
        sql_del = "delete from shop_qunfa_record where id=%s"
        dbc.updatetodb(sql_del, [del_id])
        refer = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(refer)

    # 全选框右侧的删除和添加到群发任务
    del_task_id = request.POST.getlist('cbb-task')
    do_what = request.POST.get('do-what')
    if del_task_id and do_what == 'del-checked':
        for each_task_id in del_task_id:
            sql_del_task = "delete from shop_qunfa_record where id=%s"
            dbc.updatetodb(sql_del_task, [int(each_task_id)])
        refer = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(refer)
    # # 添加到群发任务
    # if del_task_id and do_what == 'add-task':
    #     for each_task_id in del_task_id:
    #         sql_qf = "select pdt_id,company_id,comp_id_buy,pdt_title,sq_id,id from shop_qunfa_record " \
    #                  "where id=%s"
    #         result = dbc.fetchonedb(sql_qf, [each_task_id])
    #         if result:
    #             pdt_id = result[0]
    #             company_id = result[1]
    #             company_id_buy = result[2]
    #             pdt_title = result[3]
    #             sq_id = result[4]
    #             qf_record_id = result[5]
    #             # 获取公司账户有conversation_group,根据公司id前大后小,并获取公司对应的账号
    #             receiver_account = get_comp_account(company_id)
    #             sender_account = get_comp_account(company_id_buy)
    #             if int(company_id) > int(comp_id_buy):
    #                 conversation_group = '{}-{}'.format(company_id, comp_id_buy)
    #             else:
    #                 conversation_group = '{}-{}'.format(comp_id_buy, company_id)
    #             # 获取群发内容
    #             sql_qf_content = "select content from shop_qunfa where id=%s"
    #             qf_content = dbc.fetchonedb(sql_qf_content, [sq_id])
    #             if qf_content:
    #                 content = qf_content[0]
    #             else:
    #                 content = ''
    #             get_time = GetTime()
    #             time_now = get_time.time_now()
    #             # 插入数据到询盘表
    #             sql_inquiry = "insert into inquiry(title,content,conversation_group,be_inquired_type," \
    #                           "be_inquired_id,inquired_type,sender_account,receiver_account,send_time," \
    #                           "gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #             last_insert_id = dbc.updatetodb(sql_inquiry, [pdt_title, content, conversation_group, '0', pdt_id,
    #                                                           '1', sender_account, receiver_account, time_now,
    #                                                           time_now, time_now])
    #             # 插入开始执行时间到群发购买表里
    #             sql_exec_time = "update shop_qunfa set exec_time=%s where id=%s"
    #             dbc.updatetodb(sql_exec_time, [time_now, sq_id])
    #             # 更新群发记录表里的isqunfa、inquiry_id两个字段
    #             sql_update_record = "update shop_qunfa_record set inquiry_id=%s,isqunfa=%s where id=%s"
    #             dbc.updatetodb(sql_update_record, [last_insert_id[0], '1', qf_record_id])
    #     sql_update_qf = "select count(1) as all_num from shop_qunfa_record where sq_id=%s"
    #     all_num = dbc.fetchonedb(sql_update_qf, [qf_id])
    #     sql_update_qf2 = "select count(1) as all_num from shop_qunfa_record where sq_id=%s and isqunfa=1"
    #     success_num = dbc.fetchonedb(sql_update_qf2, [qf_id])
    #     sql_update_qf3 = "update shop_qunfa set qf_all_num=%s,qf_success_num=%s where id=%s"
    #     dbc.updatetodb(sql_update_qf3, [all_num[0], success_num[0], qf_id])
    #     if int(all_num[0]) == 5 and int(success_num[0] == 5):
    #         sql_update_qf4 = "update shop_qunfa set isqunfa=%s where id=%s"
    #         dbc.updatetodb(sql_update_qf4, ['1', qf_id])
    #     refer = request.META.get('HTTP_REFERER', '/')
    #     return HttpResponseRedirect(refer)

    # 页面右上的清空按钮的效果,清空所有已经添加的客户
    sq_id = request.POST.get('sq-id')
    if sq_id:
        sql_del_all = "delete from shop_qunfa_record where sq_id=%s"
        dbc.updatetodb(sql_del_all, [sq_id])
        refer = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(refer)
    return render(request, "qunfa/qunfa_add_task.html", locals())


def fix_task(request):
    # 修改群发任务
    sq_id = request.GET.get('sq_id')
    content = request.POST.get('qf-content')
    start_date = request.POST.get('start-date')
    exec_time = request.POST.get('exec-time')
    task_status = request.POST.get('task-status')
    if sq_id:
        qun_fa_content = get_qf_info('', '', sq_id)
        get_time = GetTime()
        time_now = get_time.time_now()
        time_now2 = get_time.get_strf_time2()
        if content and start_date and exec_time and task_status:
            sql_modify = "update shop_qunfa set content=%s,start_time=%s,start_hour=%s,isqunfa=%s," \
                         "gmt_modified=%s where id=%s"
            dbc.updatetodb(sql_modify, [content, start_date, exec_time, task_status, time_now, sq_id])
            refer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(refer)
        return render(request, "qunfa/qunfa_fix_task.html", locals())
    else:
        return HttpResponse('没有该群发任务', status=500)


def get_all_params(request):
    # 获取翻页前所有的url参数，传递到下一页
    get_paras = request.GET.items()
    url_params = {}
    for key, value in get_paras:
        if key != 'page':
            url_params[key] = value
    url_params = urllib.urlencode(url_params)
    return url_params
