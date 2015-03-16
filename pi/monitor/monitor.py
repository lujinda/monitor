#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-13 15:57:25
# Filename        : monitor/monitor.py
# Description     : 监控的主类，用来解析命令，并发送结果，细节并不实现
from __future__ import unicode_literals

from .capture import CaptureMonitor
from public.e import MonitorException

class MonitorManager(): 
    """
    监控的主类，用来解析命令，并发送结果，细节并不实现
    """
    def __init__(self):
        self.capture_map = {
                'capture': CaptureMonitor(),
                } # 存放各种命令与监控器的对应映射关系

    def parse_response(self, response):
        assert isinstance(response, dict), 'response 不是字典'

        command = response.get('command')
        client_id = response.get('client_id')

        if not (command and client_id):
            raise MonitorException('未知错误', client_id)

        capture = self.capture_map.get(command)
        if not capture:
            raise MonitorException('命令错误', client_id)

        try:
            capture.exec_monitor(client_id) # 由它完成后期工作
        except Exception, e:
            print e.args
            raise MonitorException('监控器出现异常', client_id)


