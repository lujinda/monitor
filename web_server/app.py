#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-16 20:37:29
# Filename        : app.py
# Description     : 
from tornado.web import Application
from handler.monitor import MonitorHandler
from libs.monitor import MonitorManager
from libs.session import SessionManager
from handler.test import TestHandler
from handler.weixin_handler import WeiXinHandler
from handler.real import RealCaptureHandler
from handler.wrap import WrapCaptureHandler
from data.db import session_db
from os import path

class MonitorApplication(Application):
    def __init__(self):
        handlers = [
                (r'/monitor', MonitorHandler), # 用来处理树莓派，这是打洞的关键
                (r'/real/capture', RealCaptureHandler), # 实时处理类
                (r'/wrap/capture', WrapCaptureHandler), # 显示实时照片的载体
                (r'/weixin', WeiXinHandler), # 只是拿来做测试
                ]

        settings = {
                'debug': True,
                'cookie_secret': '534f404d488048e38c8c882c47b8f5a8',
                'template_path': path.join(path.dirname(__file__), 'template'),
                'static_path': path.join(path.dirname(__file__), 'static'),
                }
        session_settings = {
                'session_timeout': 86400,
                'session_db': session_db,
                'session_secret': '534f404d488048e38c8c882c47b8f5a8',
                }

        self.monitor_manager = MonitorManager() # 用来管理与树莓派的连接
        self.session_manager = SessionManager(**session_settings)

        super(MonitorApplication, self).__init__(handlers, **settings)

