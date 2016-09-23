# -*- coding:utf-8 -*-
"""
app.controller.feed_controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

对所有feed进行操作
"""
from flask_restful import reqparse
from flask import url_for

from base_controller import BaseController
from app.action.feed_action import FeedAction


class FeedListController(BaseController):

    method_decorators = [BaseController.authenticate]

    def post(self):
        """
        新建feed
        """
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True, location='json', trim=True)
        args = parser.parse_args()

        url = args.url
        resource = FeedAction.create(url)

        resource_url = url_for('feeds', feed_id=resource['id'], _external=True)
        resource['url'] = resource_url
        resource['entries_url'] = url_for('entry', feed_id=resource['id'], _external=True)

        response_header = {'Location': resource_url}

        return resource, 201, response_header

    def get(self):
        """
        获取全部feed的列表
        """
        feeds = FeedAction.get_feed_list()
        for feed in feeds:
            feed['feed_url'] = url_for('feeds', feed_id=feed['id'], _external=True)
        return feeds
