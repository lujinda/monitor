#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-16 19:58:13
# Filename        : app.py
# Description     : 
from __future__ import unicode_literals

from websocket import WebSocketApp
from config.config import remote_config
from requests import post
import json

from monitor import MonitorManager

class MonitorWebSocketApp(WebSocketApp):
    abort_exit = False
    def __init__(self):
        super(MonitorWebSocketApp, self).__init__(remote_config.ws_url,
                on_open = self.on_open,
                on_message = self.on_message,
                on_error = self.on_error,
                on_close = self.on_close)


        self.monitor_manager = MonitorManager()

    def on_message(self, ws, message):
        response = json.loads(message)
        print response
        self.monitor_manager.parse_response(response)  # 交给monitor去处理这个回复

    def on_error(self, ws, error):
        """
        如果不是因为自动断开的话，就把abort_exit设定成True
        """
        self.abort_exit = True
        print error

    def on_close(self, wx):
        print 'close'

    def on_open(self, ws):
        self.send('2#213')

