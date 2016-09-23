# -*- coding:utf-8 -*-
"""
app.controller.feed_controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

对单个feed进行操作
"""
from flask_restful import Resource, reqparse, abort
from flask import url_for

from app.action.feed_action import FeedAction


class FeedController(Resource):

    def get(self, feed_id):
        """
        根据ID获取feed
        """
        resource = FeedAction.get(feed_id)
        if not resource:
            abort(404, message="Feed {} doesn't exist".format(feed_id))
        resource['feed_url'] = url_for('feeds', feed_id=resource['id'], _external=True)

        for entry in resource['entries']:
            entry['entry_url'] = url_for('entry', entry_id=entry['id'], _external=True)

        return resource, 200
