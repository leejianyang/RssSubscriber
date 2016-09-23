# -*- coding:utf-8 -*-
"""
utils
~~~~~~~~~~~~

工具函数
"""
import arrow
import dateutil.tz

from exceptions import ParseDatetimeException


def parse_dt(dt):
    """
    解析日期时间字符串

    已知的格式有：
        - ddd, YY MMM YYYY HH:mm:ss Z    例如：Thu, 01 Sep 2016 07:37:45 +0000
        - YYYY-MM-DDTHH:mm:ss.SSSZ    例如：2016-03-22T06:30:57.008Z
        - YYYY-MM-DDTHH:mm:ssZ    例如：

    Args:
        dt (str): 表示日期时间的字符串
    Return:
        str: 日期字符串，格式是YYYY-MM-DD HH:mm:ss
    """
    try:
        try:
            return arrow.get(dt).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        except:
            try:
                return arrow.get(dt, 'YYYY-MM-DDTHH:mm:ss.SSSZ').to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
            except:
                return arrow.get(dt, 'ddd, DD MMM YYYY HH:mm:ss Z').to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
    except:
        raise ParseDatetimeException()


def get_current_dt():
    """
    获取表示当前时间的字符串
    """
    return arrow.now().format('YYYY-MM-DD HH:mm:ss')


def to_utc(dt, format='YYYY-MM-DD HH:mm:ss', tzinfo='Asia/Shanghai'):
    """
    将日期字符串转换成ISO8601格式的UTC字符串
    """
    return arrow.get(dt, format).replace(tzinfo=dateutil.tz.gettz(tzinfo)).isoformat()


def datetime_to_string(dt):
    """
    将标准库datetime对象转换成字符串
    """
    return arrow.Arrow.fromdatetime(dt, tzinfo='Asia/Shanghai').format('YYYY-MM-DDTHH:mm:ssZ')
