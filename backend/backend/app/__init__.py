# -*- coding:utf-8 -*-
"""
初始化WebApp
"""
from flask import Flask
from flask_restful import Api

import controller


app = Flask(__name__)

api = Api(app, prefix='/api')

# 注册resource
api.add_resource(controller.FeedListController, '/feeds')
api.add_resource(controller.FeedController, '/feeds/<int:feed_id>', endpoint='feeds')
api.add_resource(controller.EntryController, '/entries/<entry_id>', endpoint='entry')
api.add_resource(controller.UserController, '/user/login')
