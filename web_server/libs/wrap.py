#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-14 17:45:40
# Filename        : libs/wrap.py
# Description     : 
from __future__ import unicode_literals

from functools import wraps

def monitor_exist(func):
    """
    检测实时操作时，树莓派是否在线
    """
    @wraps(func)
    def wrap(self, *args, **kwargs):
        if not self.monitor:
            self.write_error('编号为%s 的树莓派暂不在线' % self.monitor_id)
            return
        return func(self, *args, **kwargs)
    return wrap
