# -*- coding:utf-8 -*-
"""
"""
from flask import request
from flask_restful import Resource, reqparse

from rss.settings import ENV
from app.action.user_action import UserAction


class BaseController(Resource):

    @staticmethod
    def authenticate(func):
        """
        用于用户权限验证的装饰器
        """
        def wrapped(*args, **kwargs):
            parser = reqparse.RequestParser()
            parser.add_argument('debug', required=False, location='args', trim=True)
            parser.add_argument('Authorization', required=False, location='headers', trim=True)
            http_args = parser.parse_args()
            if not (ENV == 'dev' and http_args.debug == '1'):
                try:
                    schema, token = http_args.Authorization.split(' ')
                except (AttributeError, ValueError):
                    return {'msg': 'please login in.'}, 401
                else:
                    if schema != 'Bearer':
                        return {'msg': 'please login in.'}, 401
                    if not UserAction.check_jwt(token):
                        return {'msg': 'please login in.'}, 401

            return func(*args, **kwargs)
        return wrapped
