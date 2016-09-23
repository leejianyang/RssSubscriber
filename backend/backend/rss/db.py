# -*- coding:utf-8 -*-
"""
rss.db
~~~~~~~~
管理数据库连接
"""
from sqlalchemy import create_engine

from settings import MYSQL_HOST, MYSQL_DB, MYSQL_PASSWORD, MYSQL_USER


class _MySQLConnectionPool(object):
    """
    MySQL连接池
    """
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB),
                                    pool_recycle=60*5)

    def get_connection(self):
        return self.engine.connect()


_connection_pool = _MySQLConnectionPool()


class _DBConnection(object):
    """
    数据库连接
    """
    def __enter__(self):
        self._conn = _connection_pool.get_connection()
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()


def connection():
    return _DBConnection()
