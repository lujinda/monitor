#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 22:37:59
# Filename        : handler/wrap.py
# Description     : 
from __future__ import  absolute_import
from .public import PublicHandler
from weixin.base import ua_authenticated
from public.token import get_real_token

class WrapCaptureHandler(PublicHandler):
    @ua_authenticated
    def get(self):
        token = self.get_query_argument('token', None)
        session_id = self.get_query_argument('session_id', None)
        assert token and session_id

        if token != get_real_token(session_id):
            error = '指令已过期，请在微信上重新获取'
        else:
            error = None

        self.render('wrap/capture.html',
                img_url = '/real/capture?' + self.request.uri.split('?', 1)[1],
                error = error)

