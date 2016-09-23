# -*- coding:utf-8 -*-
"""
app.action.feed
~~~~~~~~~~~~~~~~~~~~~~~

与feed有关的业务逻辑
"""
from rss import Downloader, RssParser, FeedModel, EntryModel
from rss.utils import get_current_dt, to_utc, datetime_to_string


class FeedAction(object):

    @classmethod
    def create(cls, url):
        """
        创建该feed
        """
        document = Downloader.get(url)
        feed = RssParser(document).parse()
        title = feed.title
        updated = feed.updated
        now = get_current_dt()
        feed_id = FeedModel.create(title, url, updated, now)
        FeedModel.update_entries(feed_id, now, feed.items)
        return {
            'url': url,
            'title': title,
            'id': feed_id,
            'updated': to_utc(updated),
            'subscribed': 1,
            'collect_dt': to_utc(now)
        }

    @classmethod
    def get_feed_list(cls):
        """
        获取全部订阅中的feed的列表
        """
        feeds_info = FeedModel.get_subscribed()     # 获取当前订阅中的所有feed的信息
        feeds = []
        for info in feeds_info:
            feed_id = info[0]
            feed_title = info[2]
            unread_count = EntryModel.get_unread_count_by_feed(feed_id)
            feed = {
                'id': feed_id,
                'title': feed_title,
                'unread_count': unread_count,
            }
            feeds.append(feed)
        return feeds

    @classmethod
    def get(cls, feed_id):
        """
        获取单个feed
        """
        feed = FeedModel.get(feed_id)
        if feed is None:
            return None
        else:
            feed_id = feed['id']
            entries = EntryModel.get_unread_entries_by_feed(feed_id)
            for entry in entries:
                entry['updated'] = datetime_to_string(entry['updated'])
            return {
                'id': feed_id,
                'title': feed['title'],
                'link': feed['link'],
                'collect_dt': datetime_to_string(feed['collect_dt']),
                'entries': entries
            }