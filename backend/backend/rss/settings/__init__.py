# -*- coding:utf-8 -*-
"""
rss.settings
~~~~~~~~~~~~~~~~~~~~
配置项
"""
import os

from rss.exceptions import ImproperlyConfiguredError


def get_env_variable(var_name, default=None):
    """
    封装读取环境变量的函数
    """
    try:
        return os.environ[var_name]
    except KeyError:
        if default or default == '':
            return default
        else:
            msg = "Set the environment variable {}".format(var_name)
            raise ImproperlyConfiguredError(msg)


# 从环境变量中读取以下配置
MYSQL_HOST = get_env_variable('RSS_MYSQL_HOST')
MYSQL_PASSWORD = get_env_variable('RSS_MYSQL_PASSWORD')
MYSQL_USER = get_env_variable('RSS_MYSQL_USER')
MYSQL_DB = get_env_variable('RSS_MYSQL_DB')
USER_USERNAME = get_env_variable('RSS_USERNAME')
USER_PASSWORD = get_env_variable('RSS_PASSWORD')
JWT_SECRET = get_env_variable('RSS_JWT_SECRET')
ENV = get_env_variable('RSS_ENV')
