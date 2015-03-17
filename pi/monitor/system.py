#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 17:56:23
# Filename        : monitor/system.py
# Description     : 
from __future__ import unicode_literals

from .base import BaseMonitor
from os import path

class SystemMonitor(BaseMonitor):
    def __init__(self):
        self.mem_file = '/proc/meminfo'
        self.uptime_file = '/proc/uptime'
        assert path.isfile(self.mem_file)
        assert path.isfile(self.uptime_file)

    def exec_monitor(self, client_id):
        memory_stat = self.get_memory_stat()
        uptime_stat = self.get_uptime_stat()
        result = "树莓派已开机: {uptime_stat}\n内存已使用: {memory_stat:.2f}%".format(uptime_stat = uptime_stat, 
                memory_stat = memory_stat * 100)

        post_data = {'client_id': client_id,
                'result': result}

        self.send_result(post_data)

    # 返回内存使用的百分比
    def get_memory_stat(self):
        mem = {}
        f = open(self.mem_file, 'r')

        for line in f:
            name, val = map(lambda x: x.strip().split()[0], line.split(':')[:2])
            mem[name] = long(val) * 1024.0
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        f.close()

        return (mem['MemUsed'] or 1) / mem['MemTotal']

    # 返回信息已开机的时间，会转换成可读模式
    def get_uptime_stat(self):
        f = open(self.uptime_file, 'r')
        uptime = float(f.readline().split()[0])
        f.close()

        return "%s天%s小时%s分%s秒" % (self.seconds_to_time(uptime))

    # 根据传入的秒数，返回(天，时，分，秒)
    def seconds_to_time(self, seconds):
        days = int(seconds / 86400)
        hours = int(seconds % 86400 / 3600)
        minutes = int(seconds % 3600 / 60)
        seconds = int(seconds % 60)

        return days, hours, minutes, seconds

