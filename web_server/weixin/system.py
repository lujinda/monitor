#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 19:33:08
# Filename        : weixin/system.py
# Description     : 
from .base import CommandHandler, weixin_authenticated
from libs.wrap import monitor_exist

class SystemCommand(CommandHandler):
    """
    查看系统状态，指令: 系统|系统状态|system|zt
    """
    @weixin_authenticated
    @monitor_exist
    def handler(self):
        self.request.send_command('system')

