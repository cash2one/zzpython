# -*- coding:utf-8 -*-
from math import ceil


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator2(object):

    def __init__(self, row_count, page_num, orphans=0, per_page=15):
        # object_list 查询到的list， per_page 每页的条数, row_count 是mysql返回的总记录数， page_num 页码
        # number_pages 总页数
        # self.object_list = object_list
        self.per_page = int(per_page)
        self.row_count = int(row_count)
        self.orphans = int(orphans)
        self.number_pages = self.get_pages()
        self.page_num = self.validate_num_2(page_num)

    def validate_num(self, number):
        try:
            number = int(number)
        except (ValueError, TypeError):
            raise PageNotAnInteger('this page number is not an integer')
        if number < 1:
            raise EmptyPage('this page is an empty page')
        if number > self.number_pages:
            raise EmptyPage('that page contains no results')
        return number

    def validate_num_2(self, number):
        # 如果输入的页数小于1，返回第一页的页码
        # 如果输入的页数大于最大的页码，返回最后一页的页码
        # 如果输入的不是整数或其他非数字的字符，默认返回第一页的页码
        try:
            number = int(number)
        except (ValueError, TypeError):
            number = 1
        if number < 1:
            number = 1
        if number > self.number_pages:
            number = self.number_pages
        # print number, type(number)
        return number

    def get_limit(self, page_num):
        # 显示限制的条数
        number = self.validate_num_2(page_num)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans > self.number_pages:
            top = self.number_pages
        return [bottom, top]

    def get_limit_list(self, page_num):
        # 返回限制的条数
        # bottom 根据当前页码乘以页数获取当前的最小索引号，每页的最大条数为per_page
        number = self.validate_num_2(page_num)
        bottom = (number - 1) * self.per_page
        if bottom < 0:
            bottom = 0
        return [bottom, self.per_page]

    def has_next(self):
        # 是否有下一页
        return self.page_num < self.number_pages

    def has_previous(self):
        # 是否有上一页
        return self.page_num > 1

    def has_other_pages(self):
        # 是否有其他页面
        return self.page_num < self.number_pages or self.page_num > 1

    def previous_page_num(self):
        # 返回上一页的页码
        return self.page_num - 1

    def next_page_num(self):
        # 返回下一页的页码
        return self.page_num + 1

    def get_pages(self):
        # 返回总页数
        # ceil返回获得的浮点数对应的最小整数
        self.number_pages = int(ceil(self.row_count / float(self.per_page)))
        return self.number_pages
