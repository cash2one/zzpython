# -*- coding:utf-8 -*-
import sys
from get_time import GetTime

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('/mnt/pythoncode/zz91public/')
from zz91db_ast import companydb
dbc = companydb()


def get_comp_account(comp_id):
    # 根据公司id获取account
    sql_account = "select account from company_account where company_id=%s"
    result = dbc.fetchonedb(sql_account, [comp_id])
    if result:
        comp_account = result[0]
    else:
        comp_account = ''
    return comp_account


def qun_fa_task():
    # 定时任务,执行时间为每天上午9点
    get_time = GetTime()
    time_now = get_time.get_strf_time2()
    sql = "select id from shop_qunfa where start_time=%s and isqunfa=0 and start_hour=9"
    all_task = dbc.fetchalldb(sql, [time_now])
    # return all_task
    for each_task_id in all_task:
        sql_qf = "select pdt_id,company_id,comp_id_buy,pdt_title,sq_id,id from shop_qunfa_record " \
                 "where sq_id=%s and isqunfa=0"
        df_result = dbc.fetchalldb(sql_qf, [each_task_id[0]])
        # return len(df_result)
        if df_result:
            for each_df_data in df_result:
                pdt_id = each_df_data[0]
                company_id = each_df_data[1]
                comp_id_buy = each_df_data[2]
                pdt_title = each_df_data[3]
                sq_id = each_df_data[4]
                qf_record_id = each_df_data[5]
                # 获取公司账户有conversation_group,根据公司id前大后小,并获取公司对应的账号
                receiver_account = get_comp_account(company_id)
                sender_account = get_comp_account(comp_id_buy)
                if int(company_id) > int(comp_id_buy):
                    conversation_group = '{}-{}'.format(company_id, comp_id_buy)
                else:
                    conversation_group = '{}-{}'.format(comp_id_buy, company_id)
                # 获取群发内容
                sql_qf_content = "select content from shop_qunfa where id=%s"
                qf_content = dbc.fetchonedb(sql_qf_content, [sq_id])
                if qf_content:
                    content = qf_content[0]
                else:
                    content = ''
                get_time = GetTime()
                time_now = get_time.time_now()
                # 判断插入到询盘表里的信息是否重复,通过判断conversation_group字段,获取最近3天内是否插入的为同一条
                sql_inquiry_duplicate = "select conversation_group from inquiry where conversation_group=%s " \
                                        "and datediff(curdate(),send_time)<=3"
                duplicate_result = dbc.fetchonedb(sql_inquiry_duplicate, [conversation_group])
                if not duplicate_result:
                    # 插入数据到询盘表
                    sql_inquiry = "insert into inquiry(title,content,conversation_group,be_inquired_type," \
                                  "be_inquired_id,inquired_type,sender_account,receiver_account,send_time," \
                                  "gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    last_insert_id = dbc.updatetodb(sql_inquiry, [pdt_title, content, conversation_group, '0', pdt_id,
                                                                  '1', sender_account, receiver_account, time_now,
                                                                  time_now, time_now])
                    # 更新群发记录表里的isqunfa、inquiry_id、modified_time两个字段
                    time_now = get_time.time_now()
                    sql_update_record = "update shop_qunfa_record set inquiry_id=%s,isqunfa=%s,modified_time=%s" \
                                        " where id=%s"
                    dbc.updatetodb(sql_update_record, [last_insert_id[0], '1', time_now, qf_record_id])

        # 更新群发购买表里的群发总数,发送成功总数,是否完成、执行时间等多条记录
        # 获取群发总数
        sql_update_qf = "select count(1) as all_num from shop_qunfa_record where sq_id=%s"
        all_num = dbc.fetchonedb(sql_update_qf, [each_task_id[0]])
        # 获取发送成功总数
        sql_update_qf2 = "select count(1) as all_num from shop_qunfa_record where sq_id=%s and isqunfa=1"
        success_num = dbc.fetchonedb(sql_update_qf2, [each_task_id[0]])
        # 更新群发总数、发送成功总数到shop_qunfa表里
        sql_update_qf3 = "update shop_qunfa set qf_all_num=%s,qf_success_num=%s where id=%s"
        dbc.updatetodb(sql_update_qf3, [all_num[0], success_num[0], each_task_id[0]])
        # 群发完成之后,设置群发状态为完成并添加完成时间
        time_now = get_time.time_now()
        sql_update_qf4 = "update shop_qunfa set isqunfa=%s,exec_time=%s where id=%s"
        dbc.updatetodb(sql_update_qf4, ['2', time_now, each_task_id[0]])


if __name__ == '__main__':
    qun_fa_task()
