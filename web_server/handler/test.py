#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-11 14:52:57
# Filename        : handler/test.py
# Description     : 
from __future__ import unicode_literals

from .public import RealTimeHandler
from tornado.web import asynchronous, HTTPError

class TestHandler(RealTimeHandler):
    @asynchronous
    def get(self):
        command = self.get_argument('command')
        assert command
        self.send_command(command)

