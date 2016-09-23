# -*- coding:utf-8 -*-
"""
app.controller.entry_controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

操作entry的controller
"""
from flask_restful import Resource, reqparse
from flask import request

from app.action.entry_action import EntryAction


class EntryController(Resource):

    def post(self, entry_id):
        """
        修改entry
        """
        parser = reqparse.RequestParser()
        parser.add_argument('unread', type=int, choices=(0, 1), required=False, location='json', trim=True)
        args = parser.parse_args()

        EntryAction.update(entry_id, unread=args.unread)
        return '', 204
