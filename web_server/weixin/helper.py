#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 22:04:20
# Filename        : weixin/helper.py
# Description     : 

from .base import CommandHandler, weixin_authenticated

class HelperCommand(CommandHandler):
    """
    查看使用手册，指令: 帮助|help|bz
    """
    @weixin_authenticated
    def handler(self):
        _result_list = []
        for _, _handler in self.request.weixin_router.handlers:
            _result_list.append(_handler.__doc__.strip())

        self.write_result('\n\n'.join(_result_list))

