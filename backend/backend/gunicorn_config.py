# -*- coding:utf-8 -*-
"""
gunicorn的配置文件
"""
bind = '127.0.0.1:5001'
workers = 1
workers_class = 'sync'
max_requests = 1000
