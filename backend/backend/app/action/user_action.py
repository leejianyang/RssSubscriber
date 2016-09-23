# -*- coding:utf-8 -*-
"""
app.action.user_action
~~~~~~~~~~~~~~~~~~~~~~~~~

用户相关逻辑
"""
import time

import jwt
from jwt.exceptions import DecodeError

from rss.settings import USER_USERNAME, USER_PASSWORD, JWT_SECRET


class UserAction(object):

    @classmethod
    def login(cls, username, password):
        """
        用户登陆
        """
        # 用户名和密码正确则返回jwt，否则返回None
        if cls._check(username, password):
            return cls._generate_jwt(username)
        else:
            return None

    @staticmethod
    def _check(username, password):
        """
        鉴别用户名和密码是否正确
        """
        return username == USER_USERNAME and password == USER_PASSWORD

    @staticmethod
    def _generate_jwt(username):
        """
        生成JWT
        """
        payload = {
            'exp': int(time.time()) + 60 * 60 * 24 * 7,     # 表示该JWT只在7天内有效
            'aud': username
        }
        return jwt.encode(payload=payload, key=JWT_SECRET, algorithm='HS256')

    @classmethod
    def check_jwt(cls, token):
        """
        检测jwt的合法性
        """
        try:
            payload = jwt.decode(token, key=JWT_SECRET, algorithms='HS256', verify=False)
        except DecodeError:
            return False
        else:
            if 'exp' not in payload or 'aud' not in payload:
                return False
            if payload['aud'] != USER_USERNAME:
                return False
            if int(payload['exp']) < int(time.time()):
                return False
            return True
