#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 20:33:06
# Filename        : weixin/handlers.py
# Description     : 
from __future__ import unicode_literals

from .login import LoginCommand, LogoutCommand
from .unknow import UnknowCommand
from .capture import CaptureCommand
from .system import SystemCommand
from .helper import HelperCommand

__all__ = ['weixin_handlers', 'weixin_default_handler']
weixin_handlers = [
                (r'(查看|最新)?监控', CaptureCommand),
                (r'(系统|系统状态|状态|system|zt)', SystemCommand),
                (r'(登陆|登录|dl)', LoginCommand),
                (r'(注销|退出登录|zx)', LogoutCommand),
                (r'(帮助|help|bz)', HelperCommand),
            ]

weixin_default_handler = UnknowCommand

