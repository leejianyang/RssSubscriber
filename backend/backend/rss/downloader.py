# -*- coding:utf-8 -*-
"""
    downloader
    ~~~~~~~~~~~~~~~~~~~~~~

    下载rss资源
"""
import requests

from exceptions import HttpException


class Downloader(object):

    @classmethod
    def get(cls, url):
        """
        HTTP GET请求

        Args:
            url (str): 请求的url
        Return:
            str: Http Response的内容
        """
        try:
            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=30)
        except requests.RequestException:
            raise HttpException('HTTP Exception: %s', url)
        else:
            return response.content
