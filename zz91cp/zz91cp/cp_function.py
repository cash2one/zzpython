# -*- coding:utf-8 -*-
import time
import datetime
from django.core.cache import cache

INDUSTRY_LABEL = {
    '10001000': '废塑料',
    '10001001': '废金属',
    '10001002': '废纸',
    '10001003': '废旧轮胎与废橡胶',
    '10001004': '废纺织品与废皮革',
    '10001005': '废电子电器',
    '10001006': '废玻璃',
    '10001007': '废旧二手设备',
    '10001008': '其他废料',
    '10001009': '服务',
    '10001010': '塑料原料',
}


def get_time():
    # 获取当前时间的时间戳
    time_now = int(time.time())
    return time_now


def three_month_before():
    # 获取三个月以前的时间戳
    three_month = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
    bz_time = time.strptime(three_month, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(bz_time))
    return time_stamp


def get_month():
    # 获取当前月
    now_month = datetime.datetime.now().strftime("%m")
    return now_month


def get_hot_cp():
    # 按照类别获取热门产品词，读取tags表
    # 获得缓存
    hot_cp_list = cache.get("zz91cp_get_hot_cp_list")
    if hot_cp_list:
        return hot_cp_list


def re_sou_from_dh(num):
    # 从daohang表根据showcount获取对应的关键词
    re_sou_keywords_list = cache.get("zz91cp_get_re_sou_list" + str(num))
    if re_sou_keywords_list:
        return re_sou_keywords_list
    sql = "select id,label,pingyin,showcount from daohang order by showcount desc limit 0,%s"
    re_sou_list = dbc.fetchalldb(sql, [num])
    if re_sou_list:
        cache.set("zz91cp_get_re_sou_list" + str(num), re_sou_list, 60*10)
        return re_sou_list


def get_main_category(num):
    # 获取主类别
    # 前10条为主要类别,然后可以分别获取对应类别下的tags关键词
    sql = "select distinct tc.category_products_main_code,ct.label from tags_category as tc left join " \
          "ast.category_products as ct on tc.category_products_main_code=ct.code where ct.is_assist=0 " \
          "limit 0,%s"
    result = dbc.fetchalldb(sql, [num])
    if result:
        return result


def get_big_category():
    # 获取前10个大类
    # 分别为1000(废金属)、1001(废塑料)、1002(废橡胶)、1003(废纺织品)、1004(废纸)、1005(废电子电器)
    # 分别为1006(废玻璃)、1007(废旧二手设备)、1008(其他废料)、1009(服务)
    sql = "select cp.code,cp.label from category_products as cp limit 0,10"
    result = dbc.fetchalldb(sql)
    if result:
        return result
    else:
        return []


def get_one_product_pic(comp_id):
    # 根据公司id获取一张产品图片的地址与标题
    pro_pic_info = cache.get('zz91cp_get_one_product_pic{}'.format(str(comp_id)))
    if pro_pic_info:
        return pro_pic_info
    sql_pic = "select pp.pic_address,p.title,p.id from products_pic as pp left join products as p " \
              "on pp.product_id=p.id where p.company_id=%s and pp.check_status=1 and p.is_del=0 order by " \
              "pp.is_default limit 0,1"
    result_pro_pic = dbc.fetchonedb(sql_pic, [comp_id])
    if result_pro_pic:
        pdt_img_url = "http://img3.zz91.com/220x165/" + result_pro_pic[0]
        pdt_img_title = result_pro_pic[1]
        pdt_id = result_pro_pic[2]
    else:
        pdt_img_url = "http://img0.zz91.com/front/images/global/noimage.gif"
        pdt_img_title = ''
        pdt_id = 0
    pdt_img_info = {'pdt_img_url': pdt_img_url, 'pdt_img_title': pdt_img_title, 'pdt_id': pdt_id}
    cache.set('zz91cp_get_one_product_pic{}'.format(str(comp_id)), pdt_img_info, 60 * 10)
    return pdt_img_info


def get_many_products_info(comp_id, num):
    # 根据公司id获取多张产品图片的地址与标题
    # 一条供求只获取一张图片
    pro_pic_info = cache.get('zz91cp_get_one_product_pic{}_{}'.format(str(comp_id), str(num)))
    if pro_pic_info:
        return pro_pic_info
    sql_pic = "select pp.pic_address,p.title,p.id from products_pic as pp left join products as p " \
              "on pp.product_id=p.id where p.company_id=%s and pp.check_status=1 and p.is_del=0 " \
              "group by pp.product_id order by pp.is_default limit 0,%s"
    result_pro_pic = dbc.fetchalldb(sql_pic, [comp_id, num])
    if result_pro_pic:
        pdt_img_info = result_pro_pic
    else:
        pdt_img_info = []
    cache.set('zz91cp_get_one_product_pic{}_{}'.format(str(comp_id), str(num)), pdt_img_info, 60 * 10)
    return pdt_img_info


def get_comp_info(comp_id):
    # 根据产品id获取公司名称、公司地区等
    sql = "select c.name,ca.label,cy.label as parent_address from company as c left join category as ca " \
          "on c.area_code=ca.code left join category as cy on ca.parent_code=cy.code where c.id=%s"
    result = dbc.fetchonedb(sql, [comp_id])

    # 获取高会domain
    sql_domain = "select domain_zz91 from company where id=%s"
    domain_zz91 = dbc.fetchonedb(sql_domain, [comp_id])

    # 判断是否为来电宝
    sql_ldb = "select * from crm_company_service where crm_service_code in (1007,1008,1009,1010," \
              "1011) and apply_status=1 and company_id=%s"
    ldb_result = dbc.fetchonedb(sql_ldb, [comp_id])
    if domain_zz91:
        domain_zz91 = domain_zz91[0].strip()
        comp_url = "http://" + str(domain_zz91) + ".zz91.com"
        contact_url = "http://" + str(domain_zz91) + ".zz91.com/lxfs.htm"
    elif ldb_result:
        comp_url = "http://www.zz91.com/ppc/index{}.htm".format(str(comp_id))
        contact_url = "http://www.zz91.com/ppc/contact{}.htm".format(str(comp_id))
    else:
        comp_url = "http://company.zz91.com/compinfo{}.html".format(str(comp_id))
        contact_url = "http://company.zz91.com/compinfo{}.html".format(str(comp_id))

    # 获取询价
    sql_inquiry = "select qcount from inquiry_count where company_id=%s"
    result_inquiry = dbc.fetchonedb(sql_inquiry, [comp_id])
    if result_inquiry:
        q_count = result_inquiry[0]
    else:
        q_count = 0
    result = {'comp_name': result[0], 'comp_p_area': result[2], 'comp_area': result[1], 'comp_url': comp_url,
              'contact_url': contact_url, 'q_count': q_count}
    return result


def get_pro_property(property_list, text, content):
    # 获取属性字典
    if content and content.strip():
        pro_attr = {'property': text, 'content': content}
        property_list.append(pro_attr)
    return property_list


def get_pro_info(pro_id):
    # 获取产品信息
    zz91cp_pro_info = cache.get('zz91cp_pro_info' + str(pro_id))
    if zz91cp_pro_info:
        return zz91cp_pro_info

    all_pro_properties = []
    # pro_num = ''
    pro_attr = {}
    price_range = ''
    # 获取产品各种属性
    sql_pro_info = "select p.title,p.details,p.total_quantity,p.price_unit,p.price,p.quantity_unit," \
                   "p.quantity,source,p.specification,p.origin,p.impurity,p.color,p.useful,p.appearance," \
                   "p.min_price,p.max_price,c.label from products as p left join category as c " \
                   "on p.products_type_code=c.code where p.check_status=1 and p.is_del=0 and p.id=%s"
    pro_detail = dbc.fetchonedb(sql_pro_info, [pro_id])
    if pro_detail:
        # total_quantity = pro_detail[2]
        price_unit = pro_detail[3]  # 价格单位
        # pro_price = pro_detail[4]  # 价格
        quantity_unit = pro_detail[5]  # 数量单位
        pro_quantity = pro_detail[6]  # 数量
        pro_source = pro_detail[7]
        pro_specification = pro_detail[8]
        pro_origin = pro_detail[9]
        pro_impurity = pro_detail[10]
        pro_color = pro_detail[11]
        pro_useful = pro_detail[12]
        pro_apperance = pro_detail[13]
        pro_min_price = pro_detail[14]
        pro_max_price = pro_detail[15]
        # pro_style = pro_detail[16]
        if pro_quantity and pro_quantity != '':
            if quantity_unit:
                content = pro_quantity + quantity_unit
            else:
                content = pro_quantity
            all_pro_properties = get_pro_property(all_pro_properties, '数量', content)
            pro_attr['pro_num'] = content
            # pro_num = pro_style + '量: ' + content
        if pro_source and pro_source.strip():
            all_pro_properties = get_pro_property(all_pro_properties, '货源地', pro_source)
            pro_attr['pro_source'] = pro_source
        if pro_specification and pro_specification.strip():
            all_pro_properties = get_pro_property(all_pro_properties, '产品规格', pro_specification)
            pro_attr['pro_specification'] = pro_specification
        if pro_origin and pro_origin.strip():
            all_pro_properties = get_pro_property(all_pro_properties, '来源产品', pro_origin)
            pro_attr['pro_origin'] = pro_origin
        if pro_impurity and pro_impurity.strip():
            all_pro_properties = get_pro_property(all_pro_properties, '杂质含量', pro_impurity)
        if pro_color and pro_color.strip():
            all_pro_properties = get_pro_property(all_pro_properties, '颜色', pro_color)
        if pro_useful and pro_useful.strip():
            all_pro_properties = get_pro_property(all_pro_properties, '用途', pro_useful)
        if pro_apperance and pro_apperance.strip():
            all_pro_properties = get_pro_property(all_pro_properties, '外观', pro_apperance)
        if pro_min_price and pro_min_price != '0.0':
            if price_unit:
                price_range += str(pro_min_price) + price_unit
            else:
                price_range += str(pro_min_price)
            if pro_max_price and pro_max_price != pro_min_price and pro_max_price != '0.0':
                if price_unit:
                    price_range += '-' + str(pro_max_price) + price_unit
                else:
                    price_range += '-' + str(pro_max_price)
        else:
            price_range = '面议或电议'
        if price_range and price_range != '':
            # price_range = '价格：' + price_range
            all_pro_properties = get_pro_property(all_pro_properties, '价格', price_range)
            pro_attr['price_range'] = price_range

    # 获取更多产品属性信息
    sql_pro_property = "select property,content from product_addproperties where pid=%s"
    pro_properties = dbc.fetchalldb(sql_pro_property, [pro_id])
    if pro_properties:
        for each_add_pps in pro_properties:
            if each_add_pps[1]:
                all_pro_properties = get_pro_property(all_pro_properties, each_add_pps[0], each_add_pps[1])
    # pro_properties_dict = {'all_properties': all_pro_properties, 'pro_num': pro_num, 'price_range': price_range}
    # cache.set('zz91cp_pro_info' + str(pro_id), all_pro_properties, 60 * 10) # 获取全部属性
    all_pro_properties.append(pro_attr)
    cache.set('zz91cp_pro_info' + str(pro_id), all_pro_properties, 60 * 10)  # 获取部分属性
    return all_pro_properties


def get_some_pro_info(pro_id):
    # 获取部分产品信息
    zz91cp_pro_info = cache.get('zz91cp_pro_info' + str(pro_id))
    if zz91cp_pro_info:
        return zz91cp_pro_info
    pro_attr = {}
    price_range = ''
    # 获取产品各种属性
    sql_pro_info = "select p.title,p.details,p.total_quantity,p.price_unit,p.price,p.quantity_unit," \
                   "p.quantity,source,p.specification,p.origin,p.impurity,p.color,p.useful,p.appearance," \
                   "p.min_price,p.max_price,c.label from products as p left join category as c " \
                   "on p.products_type_code=c.code where p.check_status=1 and p.is_del=0 and p.id=%s"
    pro_detail = dbc.fetchonedb(sql_pro_info, [pro_id])
    if pro_detail:
        price_unit = pro_detail[3]  # 价格单位
        quantity_unit = pro_detail[5]  # 数量单位
        pro_quantity = pro_detail[6]  # 数量
        pro_source = pro_detail[7]
        pro_specification = pro_detail[8]
        pro_origin = pro_detail[9]
        pro_min_price = pro_detail[14]
        pro_max_price = pro_detail[15]
        if pro_quantity and str(pro_quantity).strip() != '':
            if quantity_unit:
                content = pro_quantity + quantity_unit
            else:
                content = pro_quantity
            pro_attr['pro_num'] = content
        if pro_source and pro_source.strip():
            pro_attr['pro_source'] = pro_source
        if pro_specification and pro_specification.strip():
            pro_attr['pro_specification'] = pro_specification
        if pro_origin and pro_origin.strip():
            pro_attr['pro_origin'] = pro_origin
        if pro_min_price and pro_min_price != '0.0':
            if price_unit:
                price_range += str(pro_min_price) + price_unit
            else:
                price_range += str(pro_min_price)
            if pro_max_price and pro_max_price != pro_min_price and pro_max_price != '0.0':
                if price_unit:
                    price_range += '-' + str(pro_max_price) + price_unit
                else:
                    price_range += '-' + str(pro_max_price)
        else:
            price_range = '面议或电议'
        if price_range and price_range != '':
            pro_attr['price_range'] = price_range

    pro_attr_more = []
    # 获取更多产品属性信息
    sql_pro_property = "select property,content from product_addproperties where pid=%s"
    pro_properties = dbc.fetchalldb(sql_pro_property, [pro_id])
    if pro_properties:
        for each_add_pps in pro_properties:
            if each_add_pps[1] and str(each_add_pps[1]).strip():
                    pro_attr_more = get_pro_property(pro_attr_more, each_add_pps[0], each_add_pps[1])
        pro_attr['attr_more'] = pro_attr_more
    cache.set('zz91cp_pro_info' + str(pro_id), pro_attr, 60 * 10)
    return pro_attr


def hot_cp_keywords(code, start_num, end_num, num):
    # 从tags获取所有类别的关键词,每个类别24个
    cl = SphinxClient()
    cl.SetServer(SPHINXCONFIG['serverid'], SPHINXCONFIG['port'])
    cl.SetMatchMode(SPH_MATCH_ANY)
    cl.SetSortMode(SPH_SORT_ATTR_DESC, 'search_count')
    cl.SetLimits(start_num, end_num, num)
    result = cl.Query(str(code), 'tagslist')
    list_all = []
    if result.has_key('matches'):
        res_list = result['matches']
        for each_data in res_list:
            each_attr = each_data['attrs']
            tags_name = each_attr['tags']
            tags_id = each_attr['tid']
            tags_py = each_attr['pingyin']
            res_dict = {'tags_name': tags_name, 'tags_id': tags_id, 'tags_py': tags_py}
            list_all.append(res_dict)
    total_count = result['total_found']
    return {'all_list': list_all, 'total': total_count}


def get_company_list(start_num, end_num, num):
    # 获取信誉商家
    cl = SphinxClient()
    cl.SetServer(SPHINXCONFIG['serverid'], SPHINXCONFIG['port'])
    cl.SetMatchMode(SPH_MATCH_BOOLEAN)
    cl.SetSortMode(SPH_SORT_ATTR_DESC, 'membership_code')
    cl.SetFilter('membership_code', [10051001, 1725773192, 1725773193, 1725773194])
    cl.SetLimits(start_num, end_num, num)
    result = cl.Query('', 'company')
    list_all = []
    if 'matches' in result:
        res_list = result['matches']
        for each_data in res_list:
            each_attr = each_data['attrs']
            comp_name = each_attr['compname']
            comp_business = each_attr['pbusiness']
            domain_zz91 = each_attr['domain_zz91']
            comp_id = each_data['id']
            area_province = each_attr['parea_province']

            # 获取综合指数
            comp_all_score = ''
            sql = "select all_score from company_pro_orderscore where company_id=%s"
            get_all_score = dbc.fetchonedb(sql, [comp_id])
            if get_all_score:
                comp_all_score = get_all_score[0]
            # 判断客户的属性,返回对应的地址
            if domain_zz91:
                domain_zz91 = domain_zz91.strip()
                comp_url = "http://" + str(domain_zz91) + ".zz91.com"
            else:
                comp_url = "http://company.zz91.com/compinfo{}.html".format(str(comp_id))

            # 获取产品图片信息
            pdt_img_info = get_one_product_pic(comp_id)

            # 判断是否为来电宝
            sql_ldb = "select * from crm_company_service where crm_service_code in (1007,1008,1009,1010," \
                      "1011) and apply_status=1 and company_id=%s"
            ldb_result = dbc.fetchonedb(sql_ldb, [comp_id])
            if ldb_result:
                comp_url = "http://www.zz91.com/ppc/index{}.htm".format(str(comp_id))

            # 获取公司地区
            comp_info = get_comp_info(comp_id)

            data_dict = {'comp_name': comp_name, 'comp_business': comp_business, 'domain_zz91': domain_zz91,
                         'comp_all_score': comp_all_score, 'comp_url': comp_url, 'area_province': area_province,
                         'pdt_img_info': pdt_img_info, 'comp_info': comp_info}
            list_all.append(data_dict)
        return list_all


def get_hot_company_list(start_num, end_num, num):
    # 获取人气商铺
    cl = SphinxClient()
    cl.SetServer(SPHINXCONFIG['serverid'], SPHINXCONFIG['port'])
    cl.SetMatchMode(SPH_MATCH_BOOLEAN)
    cl.SetSortMode(SPH_SORT_ATTR_ASC, 'gmt_start')
    cl.SetFilter('membership_code', [10051001, 1725773192, 1725773193, 1725773194])
    cl.SetLimits(start_num, end_num, num)
    result = cl.Query('', 'company')
    list_all = []
    if 'matches' in result:
        res_list = result['matches']
        for each_data in res_list:
            each_attr = each_data['attrs']
            comp_name = each_attr['compname']
            comp_business = each_attr['pbusiness']
            domain_zz91 = each_attr['domain_zz91']
            comp_id = each_data['id']
            area_province = each_attr['parea_province']

            # 获取综合指数
            comp_all_score = ''
            sql = "select all_score from company_pro_orderscore where company_id=%s"
            get_all_score = dbc.fetchonedb(sql, [comp_id])
            if get_all_score:
                comp_all_score = get_all_score[0]
            # 判断客户的属性,返回对应的地址
            if domain_zz91:
                domain_zz91 = domain_zz91.strip()
                comp_url = "http://" + str(domain_zz91) + ".zz91.com"
            else:
                comp_url = "http://company.zz91.com/compinfo{}.htm".format(str(comp_id))

            # 获取产品图片信息
            pdt_img_info = get_one_product_pic(comp_id)

            # 判断是否为来电宝
            sql_ldb = "select * from crm_company_service where crm_service_code in (1007,1008,1009,1010," \
                      "1011) and apply_status=1 and company_id=%s"
            ldb_result = dbc.fetchonedb(sql_ldb, [comp_id])
            if ldb_result:
                comp_url = "http://www.zz91.com/ppc/index{}.htm".format(str(comp_id))

            # 获取浏览量
            sql_visit = "select visit_count from analysis_esite_visit where company_id=%s"
            visit_reuslt = dbc.fetchonedb(sql_visit, [comp_id])
            if visit_reuslt:
                visit_count = visit_reuslt[0]
            else:
                visit_count = 0

            # 获取公司地区
            comp_info = get_comp_info(comp_id)

            data_dict = {'comp_name': comp_name, 'comp_business': comp_business, 'domain_zz91': domain_zz91,
                         'comp_all_score': comp_all_score, 'comp_url': comp_url, 'visit_count': visit_count,
                         'area_province': area_province, 'pdt_img_info': pdt_img_info, 'comp_info': comp_info}
            list_all.append(data_dict)
        return list_all


def get_company_list_2(start_num, end_num, num):
    # 获取信誉商家,带翻页信息
    cl = SphinxClient()
    cl.SetServer(SPHINXCONFIG['serverid'], SPHINXCONFIG['port'])
    cl.SetMatchMode(SPH_MATCH_BOOLEAN)
    cl.SetSortMode(SPH_SORT_EXTENDED, 'membership_code desc,gmt_start desc')
    cl.SetFilter('membership_code', [10051001, 1725773192, 1725773193, 1725773194])
    cl.SetLimits(start_num, end_num, num)
    result = cl.Query('', 'company')
    list_all = []
    if 'matches' in result:
        res_list = result['matches']
        for each_data in res_list:
            each_attr = each_data['attrs']
            comp_name = each_attr['compname']
            comp_business = each_attr['pbusiness']
            domain_zz91 = each_attr['domain_zz91']
            comp_id = each_data['id']
            area_province = each_attr['parea_province']
            industry_name = INDUSTRY_LABEL[str(each_attr['industry_code'])]

            # 获取会员类型
            member_style = str(each_attr['membership_code'])
            if member_style == '10051001':
                member_name = '再生通'
            elif member_style == '1725773192':
                member_name = '银牌品牌通'
            elif member_style == '1725773193':
                member_name = '金牌品牌通'
            elif member_style == '1725773194':
                member_name = '钻石品牌通'
            else:
                member_name = '普通会员'

            # 获取会员再生通年限
            sql_zst = "select zst_year from company where id=%s"
            result_zst = dbc.fetchonedb(sql_zst, [comp_id])
            if result_zst:
                zst_year = result_zst[0]
            else:
                zst_year = 0

            # 获取联系人
            sql_contact = "select contact from company_account where company_id=%s"
            result_contact = dbc.fetchonedb(sql_contact, [int(comp_id)])
            if result_contact:
                contact_man = result_contact[0]
            else:
                contact_man = ''

            # 获取综合指数
            comp_all_score = ''
            sql = "select all_score from company_pro_orderscore where company_id=%s"
            get_all_score = dbc.fetchonedb(sql, [comp_id])
            if get_all_score:
                comp_all_score = get_all_score[0]

            # 获取客户所在市场
            sql_market = "select m.name from market_company as mc left join market as m " \
                         "on mc.market_id=m.id where mc.company_id=%s"
            result_market = dbc.fetchonedb(sql_market, [comp_id])
            if result_market:
                market = result_market[0]
            else:
                market = ''

            # 判断客户的属性,返回对应的地址

            # 判断是否为来电宝
            sql_ldb = "select * from crm_company_service where crm_service_code in (1007,1008,1009,1010," \
                      "1011) and apply_status=1 and company_id=%s"
            ldb_result = dbc.fetchonedb(sql_ldb, [comp_id])
            if domain_zz91:
                domain_zz91 = domain_zz91.strip()
                comp_url = "http://" + str(domain_zz91) + ".zz91.com"
                contact_url = "http://" + str(domain_zz91) + ".zz91.com/lxfs.htm"
            elif ldb_result:
                comp_url = "http://www.zz91.com/ppc/index{}.htm".format(str(comp_id))
                contact_url = "http://www.zz91.com/ppc/contact{}.htm".format(str(comp_id))
            else:
                comp_url = "http://company.zz91.com/compinfo{}.html".format(str(comp_id))
                contact_url = "http://company.zz91.com/compinfo{}.html".format(str(comp_id))

            # 获取三条产品信息
            pro_info = get_many_products_info(comp_id, 3)

            # 获取公司地区
            comp_info = get_comp_info(comp_id)

            # 返回数据
            data_dict = {'comp_name': comp_name, 'comp_business': comp_business, 'domain_zz91': domain_zz91,
                         'comp_all_score': comp_all_score, 'comp_url': comp_url, 'area_province': area_province,
                         'zst_year': zst_year, 'member_name': member_name, 'contact_url': contact_url,
                         'industry_name': industry_name, 'contact_man': contact_man, 'market': market,
                         'pro_info': pro_info, 'comp_info': comp_info}
            list_all.append(data_dict)
        all_num = result['total_found']
        dict_all = {'list_all': list_all, 'all_num': all_num}
        return dict_all


def get_all_products(start_num, end_num, limit_num, sort_mode):
    # 获取供求信息
    list_all = []
    cl = SphinxClient()
    cl.SetServer(SPHINXCONFIG['serverid'], SPHINXCONFIG['port'])
    cl.SetMatchMode(SPH_MATCH_BOOLEAN)
    cl.SetLimits(start_num, end_num, limit_num)

    if sort_mode == 1:
        # 排序1
        cl.SetSortMode(SPH_SORT_EXTENDED, 'havepic desc')
    if sort_mode == 2:
        # 排序2
        cl.SetSortMode(SPH_SORT_EXTENDED, 'viptype desc')
    # cl.SetGroupBy('company_id', SPH_GROUPBY_ATTR)
    query_result = cl.Query('', 'offersearch_new_vip')
    if query_result and 'matches' in query_result:
        res_list = query_result['matches']
        for each_data in res_list:
            each_attr = each_data['attrs']
            pro_id = each_data['id']
            comp_id = each_attr['company_id']
            pro_title = each_attr['ptitle']
            pdt_kind = each_attr['pdt_kind']

            # 获取客户所在市场
            sql_market = "select m.name from market_company as mc left join market as m " \
                         "on mc.market_id=m.id where mc.company_id=%s"
            result_market = dbc.fetchonedb(sql_market, [comp_id])
            if result_market:
                market = result_market[0]
            else:
                market = ''

            # 获取产品图片信息
            sql_img = "select pic_address from products_pic where product_id=%s and check_status=1"
            result_img = dbc.fetchonedb(sql_img, [pro_id])
            if result_img:
                pdt_img_info = "http://img3.zz91.com/220x165/{}".format(result_img[0])
            else:
                pdt_img_info = "http://img0.zz91.com/front/images/global/noimage.gif"

            # 根据产品id获取公司对应的地区
            comp_info = get_comp_info(comp_id)

            # 获取产品详细信息
            sql_pro_detail = "select details from products where id=%s"
            pro_detail = dbc.fetchonedb(sql_pro_detail, [pro_id])
            if pro_detail:
                pro_detail = pro_detail[0]
            else:
                pro_detail = ''

            # 获取产品属性信息
            pro_attr = get_some_pro_info(pro_id)

            # 返回数据
            data_dict = {'pro_id': pro_id, 'market': market, 'pdt_img_info': pdt_img_info, 'pro_title': pro_title,
                         'comp_info': comp_info, 'pro_detail': pro_detail, 'pdt_kind': pdt_kind,
                         'pro_attr': pro_attr}
            list_all.append(data_dict)
        all_num = query_result['total_found']
        dict_all = {'list_all': list_all, 'all_num': all_num}
        return dict_all


def get_hot_huzhu_info(start_num, end_num, limit_num, sort_mode):
    # 获取最热商圈,可以按照回复数和浏览量进行排序
    bbs_list = []
    cl = SphinxClient()
    cl.SetServer(SPHINXCONFIG['serverid'], SPHINXCONFIG['port'])
    cl.SetMatchMode(SPH_MATCH_BOOLEAN)
    cl.SetFilter('bbs_post_assist_id', [107])
    cl.SetFilterRange('post_time', three_month_before(), get_time())
    cl.SetLimits(start_num, end_num, limit_num)
    if sort_mode == 1:
        # 按照回复数进行排序
        cl.SetSortMode(SPH_SORT_EXTENDED, 'reply_count desc,post_time desc')
    if sort_mode == 2:
        # 按照浏览量进行排序
        cl.SetSortMode(SPH_SORT_EXTENDED, 'visited_count desc,post_time desc')
    query_result = cl.Query('', 'huzhu')
    if query_result and 'matches' in query_result:
        res_list = query_result['matches']
        for each_res in res_list:
            each_attr = each_res['attrs']
            bbs_id = each_attr['pid']
            reply_count = each_attr['reply_count']
            visited_count = each_attr['visited_count']
            post_time = each_attr['ppost_time']
            bbs_title = each_attr['ptitle']
            # 获取对应帖子的内容
            sql_bbs_content = "select content,post_time,content_query from bbs_post where id=%s"
            bbs_result = dbc.fetchonedb(sql_bbs_content, [bbs_id])
            if bbs_result:
                bbs_content = bbs_result[0]
                post_time_2 = bbs_result[1]
                content_query = bbs_result[2]
            else:
                bbs_content = ''
                post_time_2 = ''
                content_query = ''
            bbs_dict = {'bbs_id': bbs_id, 'reply_count': reply_count, 'visited_count': visited_count,
                        'post_time': post_time, 'bbs_title': bbs_title, 'bbs_content': bbs_content,
                        'post_time_2': post_time_2}
            if str(bbs_title) == '我发布了一条供求' or not bbs_title:
                bbs_dict['bbs_title'] = content_query
            bbs_list.append(bbs_dict)
    return bbs_list

