#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-10 16:21:51
# Filename        : libs/monitor.py
# Description     : 

class MonitorManager():
    monitor_list  = {} # key是树莓派的编号
    client_list = {} # key是客户端ip，由session id(微信id) + 树莓派编号 来区分不同的用户请求

    def register_monitor(self, monitor):
        self.monitor_list[monitor.monitor_id] = monitor

    def unregister_monitor(self, monitor):
        self.monitor_list.pop(monitor.monitor_id, None)

    def register_client(self, client):
        self.client_list[client.client_id] = client

    def unregister_client(self, client):
        self.client_list.pop(client.client_id, None)

