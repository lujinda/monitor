#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 18:33:54
# Filename        : weixin/router.py
# Description     : 
from __future__ import unicode_literals
from .handlers import weixin_handlers, weixin_default_handler

import re

class WeiXinRouter():
    delimiter = None
    def __init__(self, command_line, handlers = None):
        self.command, self.args = self.parse_command_line(command_line)
        self.handlers = handlers or weixin_handlers
        self.default_hanadler = weixin_default_handler

    def parse_command_line(self, command_line):
        _parts = command_line.split(self.delimiter)
        return _parts[0], _parts[1:] or ['help', '']

    def get_handler(self):
        for _re_string, _handler in self.handlers: # 采用类似tornado的路由处理方法
            if re.match(r'^%s$' % _re_string, self.command):
                return _handler

        return self.default_hanadler

