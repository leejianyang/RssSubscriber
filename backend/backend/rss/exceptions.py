# -*- coding:utf-8 -*-
"""
自定义的Exception类
"""
class RssException(Exception):
    """
    自定义Exception的基类
    """
    pass


class ParserException(RssException):
    """
    解析Rss时异常
    """
    pass


class HttpException(RssException):
    """
    HTTP错误
    """
    pass


class ParseDatetimeException(RssException):
    """
    解析日期时间字符串错误
    """
    pass


class ImproperlyConfiguredError(Exception):
    """
    环境变量配置错误
    """
    pass