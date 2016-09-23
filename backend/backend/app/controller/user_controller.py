# -*- coding:utf-8 -*-
"""
app.controller.user_controller
~~~~~~~~~~~~~~~
用户权限相关的controller
"""
from flask_restful import Resource, reqparse

from app.action.user_action import UserAction


class UserController(Resource):


    def get(self):
        """
        用户登陆
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location='args', trim=True)
        parser.add_argument('password', required=True, location='args', trim=True)
        args = parser.parse_args()

        jwt = UserAction.login(args.username, args.password)
        if jwt:
            return {'jwt': jwt, 'success': True}
        else:
            return {'jwt': '', 'success': False}
