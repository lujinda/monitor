#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 18:05:19
# Filename        : weixin/unknow.py
# Description     : 
from __future__ import unicode_literals

from .base import CommandHandler

class UnknowCommand(CommandHandler):
    def handler(self):
        self.write_result('%s 命令不存在, 如需要帮助请回复"帮助"或"help"或"bz"' % self.command)

