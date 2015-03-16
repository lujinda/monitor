#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-14 18:57:12
# Filename        : handler/public.py
# Description     : 
from __future__ import unicode_literals

from tornado.web import RequestHandler
from libs.session import Session
from libs.enc import enc_string
from tornado.web import HTTPError

class PublicHandler(RequestHandler):
    """
    所有路由请求的基类
    """
    @property
    def client_ip(self):
        return self.request.remote_ip

    def initialize(self):
        self.init_data()

    def init_data(self):
        pass

    @property
    def monitor_manager(self):
        return self.application.monitor_manager

class BaseHandler(PublicHandler):
    """
    不需要实时获取信息的基类
    """
    def init_data(self):
        self.session = Session(self.application.session_manager, 
                self)
        self.client_id = enc_string(self.session['session_id'] + self.monitor_id)

class RealTimeHandler(BaseHandler):
    """
    用来处理实时信息的基类，同时也是微信的基类
    """
    def init_data(self):
        pass

    @property
    def monitor_id(self):
        return self.session.get('monitor_id', None)

    @property
    def valid_user(self):
        """
        用来验证用户是否合法的接口
        """
        return bool(self.monitor_id)

    def init_monitor(self):
        """
        为会话设定特定的monitor
        """
        if not self.monitor_id :
            self.monitor = None
            return False # 如果没有monitor_id则表示未登录，此时就要关闭
        self.client_id = enc_string(self.session['session_id'] + self.monitor_id)

        self.monitor = self.monitor_manager.monitor_list.get(self.monitor_id, None)
        self.monitor_manager.register_client(self)

    def on_finish(self):
        if self.monitor_id:
            self.monitor_manager.unregister_client(self)

    def send_response(self, response):
        self.monitor.send_command(response)

    def __made_response(self, command):
        _response = {'command': command,
                'client_id': self.client_id}
        return _response
    
    def send_command(self, command):
        """
        根据传入的命令，生成相应的response，并发送
        """
        response = self.__made_response(command)
        self.send_response(response)

