#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 22:40:48
# Filename        : handler/real.py
# Description     : 
from __future__ import unicode_literals, absolute_import

from .public import RealTimeHandler
from tornado.web import asynchronous, HTTPError
from libs.session import WeiXinSession
from weixin.base import ua_authenticated

from public.token import get_real_token

class RealCaptureHandler(RealTimeHandler):
    real_data_show_way = 'web'
    def prepare(self):
        from_user = self.get_query_argument('session_id')
        self.session = WeiXinSession(self.application.session_manager,
                from_user = from_user)

    @ua_authenticated
    @asynchronous
    def get(self):
        token = self.get_query_argument('token', None)
        session_id = self.get_query_argument('session_id', None)
        assert token and session_id # 这个处理器全是通过微信访问的，所以必须要检查token和session_id来判定用户的身份
    
        if token != get_real_token(session_id):
            raise HTTPError(403)

        if self.init_monitor(): # 如果初始化是没问题的话，才会去访问这个
            self.send_command('capture')

    def write_result(self, result):
        self.write(result)
        self.finish()

