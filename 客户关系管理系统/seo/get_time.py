# -*- coding:utf-8 -*-
import sys
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'fenghui'


class GetTime(object):
    """
    获取各种标准化时间
    """

    def time_now(self):
        # 返回datetime.datetime格式的时间,例如:datetime.datetime(2017, 7, 6, 11, 52, 32, 853000)
        now_time = datetime.datetime.now()
        return now_time

    def get_time_stamp(self):
        # 获取当前时间的时间戳
        time_stamp = time.time()
        return time_stamp

    def get_timestamp(self, strf_time):
        # 获取任意标准化时间的时间戳
        mk_time = time.mktime(strf_time)
        return mk_time

    def get_strf_time(self):
        # 获取标准化格式的日期,格式为2017-07-01 17:38:09
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return now_time

    def get_strf_time2(self):
        # 获取标准化格式的日期,格式为2017-07-01
        now_time = datetime.datetime.now().strftime("%Y-%m-%d")
        return now_time

    def get_year(self):
        # 获取当前年
        now_year = datetime.datetime.now().strftime("%Y")
        return now_year

    def get_month(self):
        # 获取当前月
        now_month = datetime.datetime.now().strftime("%m")
        return now_month

    def get_day(self):
        # 获取当前天
        now_day = datetime.datetime.now().strftime("%d")
        return now_day

    def is_leap_year(self, year):
        # 根据年份来判断是平年还是闰年
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 1
        else:
            return 0

    def get_month_days(self, year):
        # 根据平年还是闰年,修改2月份的天数
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        is_leap = self.is_leap_year(year)
        if is_leap:
            month_days[1] = 29
        return month_days

    def get_after_time(self):
        # 获取基于当前年月日之后的三个月的日期
        # 格式为:2017-07-03
        now_year = int(self.get_year())
        now_month = int(self.get_month())
        now_day = int(self.get_day())
        # now_month = 11
        # now_day = 31
        month_days = self.get_month_days(now_year)
        next_three_month = now_month + 3
        if next_three_month > 12:
            now_year += 1
            next_three_month = next_three_month - 12
        month_days = self.get_month_days(now_year)
        this_month_day = month_days[next_three_month - 1]
        # print u'3个月后的月份的天数为:{}'.format(str(this_month_day))
        if now_day > this_month_day:
            delta_day = now_day - this_month_day
            next_three_month += 1
            now_day = delta_day
        next_three_month = ''.join(['0', str(next_three_month)]) if (next_three_month < 10) else str(next_three_month)
        now_day = ''.join(['0', str(now_day)]) if (now_day < 10) else str(now_day)
        three_month_later = '-'.join([str(now_year), str(next_three_month), str(now_day)])
        return three_month_later