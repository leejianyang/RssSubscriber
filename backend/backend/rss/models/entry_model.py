# -*- coding:utf-8 -*-
"""
rss.models.entry_model
~~~~~~~~~~~~~~~~~~~~~~~~~~

与Entry有关的model
"""
import logging
import datetime
import uuid

from sqlalchemy.sql import text

from base_model import BaseModel
from rss.db import connection


class EntryModel(BaseModel):

    @classmethod
    def update(cls, title, updated, link, hash_code, feed_id, collect_dt):
        """更新一条entry记录

        如果entry的相关记录已存在于数据库中则更新记录，否则插入新纪录

        Args:
            title: 标题
            updated: 最后更新时间
            link: 原文连接
            hash_code: 哈希值，用于校验唯一性
            feed_id: 该entry所属的feed的ID
            collect_dt: 收集时间
        """
        with connection() as conn:
            unique_id = cls._generate_unique_id()
            sql = text("INSERT IGNORE entry SET `id`=:id, `title`=:title, `link`=:link, `hcode`=:hash_code, `updated`=:updated, `feed_id`=:feed_id, `collect_dt`=:collect_dt")
            result = conn.execute(sql, {"title": title, "link": link, "hash_code": hash_code,
                               "updated": updated, "feed_id": feed_id, "collect_dt": collect_dt, "id": unique_id})

            if result == 0:
                # 该entry已存在，看是否需要更新
                sql = text("UPDATE entry "
                           "SET `title`=:title, `updated`=:updated, `link`=:link, `collect_dt`=:collect_dt, `hash_code`=:hash_code"
                           "WHERE `link`=:link AND `hash_code`<>:hash_code")
                conn.execute(sql, {"title": title, "link": link, "hash_code": hash_code, "updated": updated, "collect_dt": collect_dt})

    @classmethod
    def get_unread_count_by_feed(cls, feed_id):
        """
        获取某个feed所有未读的entry的数量
        """
        with connection() as conn:
            sql = text("SELECT count(1) AS `cnt` FROM entry WHERE `feed_id`=:feed_id AND `unread`=1")
            result = conn.execute(sql, {'feed_id': feed_id}).fetchone()
            if result:
                return result[0]
            else:
                return 0

    @classmethod
    def get_unread_entries_by_feed(cls, feed_id):
        """
        根据feed获取未读entry的列表
        """
        with connection() as conn:
            sql = text("SELECT id, title, updated, link "
                       "FROM entry "
                       "WHERE `feed_id`=:feed_id AND `unread`=1 "
                       "ORDER BY updated DESC")
            result = conn.execute(sql, {'feed_id': feed_id}).fetchall()
            if result:
                return [{'id': item[0], 'title': item[1], 'updated': item[2], 'link': item[3]} for item in result]
            else:
                return None

    @classmethod
    def read(cls, entry_id):
        """
        标记为已读
        """
        with connection() as conn:
            sql = text("UPDATE entry "
                       "SET `unread`=0 "
                       "WHERE `id`=:entry_id")
            conn.execute(sql, {'entry_id': entry_id})

    @staticmethod
    def _generate_unique_id():
        """
        生成一个随机字符串作为entry的ID
        """
        return uuid.uuid4().hex[:6] + str(datetime.datetime.now().second)
