# -*- coding:utf-8 -*-
"""
    feed
    ~~~~~~~~~~~

    该模块提供对feed进行封装的类
"""
import hashlib
from collections import namedtuple

from utils import parse_dt


Entry = namedtuple('Entry', ['title', 'published', 'link', 'hash'])


class Feed(object):
    """
    对feed进行封装，只封装了目前用到的内容
    """
    def __init__(self):
        self._items = []

    @property
    def feed_id(self):
        return self._feed_id

    @feed_id.setter
    def feed_id(self, feed_id):
        self._feed_id = feed_id

    @property
    def title(self):
        """
        获取feed的标题
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        设置feed的标题
        """
        self._title = title

    @property
    def updated(self):
        """
        获取最后更新时间
        """
        return self._last_updated

    @updated.setter
    def updated(self, time_str):
        """
        设置最后更新时间
        """
        self._last_updated = parse_dt(time_str)

    @property
    def href(self):
        """
        该feed的地址
        """
        return self._href

    @href.setter
    def href(self, url):
        """
        设置该feed的地址
        """
        self._href = url

    @property
    def version(self):
        """
        该feed的版本
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        设置feed版本
        """
        self._version = version

    @property
    def items(self):
        return self._items

    def add_item(self, title, published, link):
        """
        新增一个item

        Args:
            title (str): 标题
            published (str): 最后更新时间
            link (str)：原文连接
        """
        published = parse_dt(published)
        hash_code = hashlib.md5((title + link + published).encode('utf-8')).hexdigest()
        item = Entry(title, published, link, hash_code)
        self._items.append(item)


if __name__ == '__main__':
    obj = Feed()
    obj.updated = 'Thu, 01 Sep 2016 06:53:27 +0000'
    print obj.updated