# -*- coding:utf-8 -*-
"""
backend.webserver
~~~~~~~~~~~~~~~~~~~~~~~

运行WebServer的入口
"""
from app import app

app.run(debug=True, port=9999)

