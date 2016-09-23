# -*- coding:utf-8 -*-
import logging

import arrow
from celery import Celery, chain

from rss import Downloader, RssParser, FeedModel, RssException
import celery_config

app = Celery('rss')
app.config_from_object(celery_config)


@app.task(bind=True, max_retries=3)
def collect_task(self, url):
    """采集任务

    根据url把rss格式的文档下载回来

    Args:
        url: feed的url
    Return:
        str: rss格式的文本
    """
    try:
        document = Downloader.get(url)
    except RssException as e:
        logging.exception(e)
        raise self.retry(countdown=30)
    else:
        return document


@app.task()
def parse_task(document, feed_id, url):
    """解析任务

    将rss格式的文本解析成rss对象

    Args:
        feed_id: 该feed的ID
        url: document的url
        document: rss格式的文本
    Return:
        rss.feed.Feed对象
    """
    feed = RssParser(document).parse()
    feed.feed_id = feed_id
    feed.href = url
    return feed


@app.task()
def persistence_task(feed):
    """持久化任务

    将feed入库

    Args:
        feed: Feed对象
    """
    feed_id = feed.feed_id
    entries = feed.items
    title = feed.title
    updated = feed.updated
    # 更新feed
    FeedModel.update(feed_id, title, updated)
    # 更新entry
    now = arrow.now().to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
    FeedModel.update_entries(feed_id, now, entries)
    return feed_id


@app.task
def mark_success(feed_id):
    """标记一次抓取任务完成
    """
    FeedModel.mark_success(feed_id)


@app.task
def main_task():
    """更新全部feed的入口函数
    """
    jobs = []
    for feed_id, feed_url, _ in FeedModel.get_subscribed():
        jobs.append((feed_id, chain(collect_task.s(feed_url), parse_task.s(feed_id, feed_url), persistence_task.s(), mark_success.s())))

    # 提交全部job
    for item in jobs:
        feed_id, job = item
        FeedModel.mark_start(feed_id)
        job()
