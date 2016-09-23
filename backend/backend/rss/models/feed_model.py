# -*- coding:utf-8 -*-
"""
rss.models.feed_model
~~~~~~~~~~~~~~~~~~

封装与feed有关的数据库操作
"""
from sqlalchemy.sql import text

from base_model import BaseModel
from rss.db import connection
from entry_model import EntryModel
from rss.utils import get_current_dt


class FeedModel(BaseModel):
    """
    与feed相关的逻辑
    """
    @classmethod
    def create(cls, title, link, updated, collect_dt):
        """
        新建一个feed

        Args:
            title: 标题
            link: 地址
            updated: 最近更新时间
            collect_dt: 最近抓取时间
        Return:
            这条feed的ID
        """
        with connection() as conn:
            sql = text('INSERT feed SET `title`=:title, `link`=:link, `updated`=:updated, `collect_dt`=:collect_dt '
                       'ON DUPLICATE KEY UPDATE `subscribed`=1, `collect_dt`=:collect_dt')
            result = conn.execute(sql, {'title': title, 'link': link, 'updated': updated, 'collect_dt': collect_dt})
            return result.lastrowid

    @classmethod
    def update(cls, feed_id, title, updated):
        """
        更新feed

        Args:
            feed_id: Feed ID
            title: 标题
            updated: 最近更新时间
            collect_dt: 最近抓取时间
        """
        with connection() as conn:
            sql = text('UPDATE feed SET `title`=:title, `updated`=:updated WHERE `id`=:feed_id')
            conn.execute(sql, {'feed_id': feed_id, 'title': title, 'updated': updated})


    @classmethod
    def update_entries(cls, feed_id, collect_dt, entries):
        """
        更新某个feed的多个entry

        Args:
            feed_id: feed id
            collect_dt: 采集时间
            entries (list): 每个元素是一个字典
        """
        for entry in entries:
            title = entry.title
            updated = entry.published
            link = entry.link
            hash_code = entry.hash

            EntryModel.update(title, updated, link, hash_code, feed_id, collect_dt)

    @classmethod
    def get_subscribed(cls):
        """
        获取订阅中的feed

        Return:
            list: 每个元素是tuple(feed_id, url, title)
        """
        with connection() as conn:
            sql = text('SELECT id, link, title FROM `feed` WHERE `subscribed`=1')
            result = conn.execute(sql)
            return [(item[0], item[1], item[2]) for item in result]

    @classmethod
    def mark_success(cls, feed_id):
        """
        记录抓取成功
        """
        now = get_current_dt()
        with connection() as conn:
            sql = text('UPDATE `feed` SET `collect_dt`=:collect_dt, `status`=1 WHERE `id`=:feed_id')
            conn.execute(sql, {'feed_id': feed_id, 'collect_dt': now})

    @classmethod
    def mark_fail(cls, feed_id):
        """
        记录抓取失败
        """
        now =get_current_dt()
        with connection() as conn:
            sql = text('UPDATE `feed` SET `collect_dt`=:collect_dt, `status`=0 WHERE `id`=:feed_id')
            conn.execute(sql, {'feed_id': feed_id, 'collect_dt': now})

    @classmethod
    def mark_start(cls, feed_id):
        """
        标记该feed开始抓取
        """
        with connection() as conn:
            sql = text('UPDATE `feed` SET `status`=0 WHERE `id`=:feed_id')
            conn.execute(sql, {'feed_id': feed_id})

    @classmethod
    def get(cls, feed_id):
        """
        根据id查询
        """
        with connection() as conn:
            sql = text('SELECT id, title, link, collect_dt FROM feed WHERE `id`=:feed_id AND `subscribed`=1')
            result = conn.execute(sql, {'feed_id': feed_id}).first()
            if result:
                return {
                    'id': result[0],
                    'title': result[1],
                    'link': result[2],
                    'collect_dt': result[3],
                }
            else:
                return None
