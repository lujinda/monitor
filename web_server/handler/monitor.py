#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 19:57:03
# Filename        : handler/monitor.py
# Description     : 
from __future__ import unicode_literals

from tornado.websocket import WebSocketHandler
from .public import PublicHandler
import json 
class MonitorHandler(WebSocketHandler, PublicHandler):
    monitor_id = None
    def open(self):
        print self._made_mess('树莓派已连接')

    def _made_mess(self, mess):
        """
        生成信息日志, 并会记录到数据库中
        """
        return "{client_ip} {mess}".format(
                client_ip = self.client_ip, mess = mess)

    def on_close(self):
        print self._made_mess('树莓派已断开 编号为: {monitor_id}'.\
                format(monitor_id = self.monitor_id))
        self.monitor_manager.unregister_monitor(self)

    def on_message(self, message):
        """
        当websocket连接后，会发现一个代表自己标识符，这时候才将树莓派注册
        """
        self.monitor_id = message
        self.monitor_manager.register_monitor(self)

        print self._made_mess('树莓派已注册 编号为: {monitor_id}'.\
                format(monitor_id = message))
        
    def check_origin(self, origin):
        return True
    
    def post(self):
        """
        在这里会把信息写给客户
        """
        client_id = self.get_argument('client_id', None)
        client = self.monitor_manager.client_list.get(client_id, None)
        assert client

        result = self.get_result(client)

        if client.real_data_show_way == 'web':
            client.write_result(result)
        else:
            client.weixin.write_result(result)


    def get_result(self, client):
        """
        获得树莓派返回的结果
        """
        image_list = self.request.files.get('image', None)
        if image_list:
            image = image_list[0]
            client.set_header('Content-Type', image['content_type'])
            return image['body']

        error = self.get_argument('error', None)
        if error:
            return error

        result = self.get_argument('result', None)
        return result

    def send_command(self, command):
        """
        向树莓派发送command, 格式必须是字典的，包含客户端的标识和命令
        """
        assert isinstance(command, dict)
        json.dumps(command)
        self.write_message(command)

