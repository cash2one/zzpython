# -*- coding:utf-8 -*-
import time
from django import template

register = template.Library()


@register.filter
def timestamp_to_date(value):
    return time.strftime('%Y-%m-%d %X', time.localtime(value))
