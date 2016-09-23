# -*- coding:utf-8 -*-
"""
    rss解析器
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import logging

import feedparser

from feed import Feed
import exceptions

logger = logging.getLogger(__name__)


class RssParser(object):

    def __init__(self, resource):
        """
        Args:
            resource (str): xml格式的字符串
        """
        self._resource = resource

    def parse(self):
        """
        进行解析

        Return:
            Feed: 封装好的Feed对象
        """
        try:
            data = feedparser.parse(self._resource)

            feed = Feed()
            # 设置基本属性
            feed.title = data.feed.title
            feed.updated = data.feed.updated
            feed.version = data.version
            # 遍历item
            for item in data.entries:
                title = item.title
                published = item.published
                link = item.link
                feed.add_item(title, published, link)
        except Exception as e:
            logging.exception(e)
            raise exceptions.ParserException()
        else:
            return feed
