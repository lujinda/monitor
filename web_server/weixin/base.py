#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 22:29:46
# Filename        : weixin/base.py
# Description     : 
from functools import wraps
from time import time
from libs.wrap import monitor_exist
from tornado.web import HTTPError

def ua_authenticated(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        if 'MicroMessenger' not in self.UA:
            raise HTTPError(403)

        return func(self, *args, **kwargs)

    return wrap


def weixin_authenticated(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        if not self.valid_user:
            self.write_error('您还未登录，请回复"dl 用户名 密码(三者用空格隔开)来登录"')
        else:
            return func(self, *args, **kwargs)
    return wrap

class CommandHandler():
    def __init__(self, request, from_user, to_user, command, args, msg_type):
        self.msg_type = msg_type # 基本上没用到.
        self.request = request
        self.session = request.session
        self.monitor = request.monitor
        self.monitor_id = request.monitor_id
        self.from_user = from_user
        self.to_user = to_user
        self.args = args
        self.command = command

    def handler(self):
        raise NotImplementedError
        #self.request.send_command(self.request_data['content'])

    def write_result(self, result, result_type = 'text'):
        self.request.render('reply_text.html', content = result,
                **self.public_result())

    def write_error(self, error):
        return self.write_result(error)

    @property
    def create_time(self):
        return int(time())

    def public_result(self):
        """
        所有回复信息中，共有的一些属于参数
        """
        return {'to_user': self.from_user, 'from_user': self.to_user, 'create_time': self.create_time,}

    @property
    def valid_user(self):
        return self.request.valid_user

