# -*- coding:utf-8 -*-
import urllib
from django import template

register = template.Library()


@register.filter
def spl_str(value):
    # 字符串分割过滤器
    try:
        if type(value):
            str_to_list = value.split(',')
            return str_to_list
        else:
            return value
    except:
        pass


@register.filter
def url_encode(value):
    if isinstance(value, unicode):
        value = urllib.quote(value.decode('utf-8').encode('utf-8'))
        return value
    # print value
    # return value


@register.filter
def trim(value):
    # 字符串去除空格
    # from：https://stackoverflow.com/questions/10361240/template-filter-to-trim-any-leading-or-trailing-whitespace
    return value.strip()


@register.filter
def encode_url(value):
    if isinstance(value, unicode):
        value = value.encode('gb2312')
    value = urllib.quote_plus(value)
    return value