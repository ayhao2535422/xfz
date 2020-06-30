from django import template
from datetime import datetime
from django.utils.timezone import now as now_func, localtime


register = template.Library()


@register.filter
def time_since(value):
    if not isinstance(value, datetime):
        return value
    else:
        now = now_func()
        timestamp = (now - value).total_seconds()
        if timestamp < 60:
            return '刚刚'
        elif timestamp >= 60 and timestamp < 60*60:
            return f'{int(timestamp/60)}分钟前'
        elif timestamp >= 60*60 and timestamp < 60*60*24:
            return f'{int(timestamp/60/60)}小时前'
        elif timestamp >= 60*60*24 and timestamp < 60*60*24*30:
            return f'{int(timestamp/60/60/24)}天前'
        else:
            return value.strftime('%Y/%m/%d %H:%M')


@register.filter
def time_format(value):
    if not isinstance(value, datetime):
        return value
    else:
        return localtime(value).strftime('%Y/%m/%d %H:%M:%S')