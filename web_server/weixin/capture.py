#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 21:43:29
# Filename        : weixin/capture.py
# Description     : 
from .base import CommandHandler, weixin_authenticated
from libs.wrap import monitor_exist
from public.token import made_real_token

class CaptureCommand(CommandHandler):
    """
    实时获取监控信息，指令: 监控|最新监控
    """
    @weixin_authenticated
    @monitor_exist
    def handler(self):
        url_root = self.request.request.protocol + '://' + self.request.request.host # 第一个request,是handler_request,第二个request是handler中的request
        real_capture_url = '{url_root}/wrap/capture?session_id={session_id}&token={token}'.format(url_root = url_root,
                session_id = self.session['session_id'],
                token = made_real_token(self.session['session_id']))
        
        self.write_result("""<a href="{url}">点击查看最新监控照片(该链接在60秒内有效)</a>""".format(
            url = real_capture_url))

