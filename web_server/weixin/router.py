#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-16 12:30:52
# Filename        : weixin/router.py
# Description     : 
from .login import LoginCommand

class WeiXinRouter():
    delimiter = None
    def __init__(self, command_line, handlers = None):
        self.command, self.args = self.parse_command_line(command_line)
        self.handlers = handlers or {'ld': LoginCommand}

    def parse_command_line(self, command_line):
        _parts = command_line.split(delimiter)
        return _parts[0], _parts[1:]

    def get_handler(self):
        handler = self.handlers.get(self.command)
        return handler

