#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 19:32:39
# Filename        : weixin/login.py
# Description     : 
from .base import CommandHandler, weixin_authenticated
from public.account import try_login

class LogoutCommand(CommandHandler):
    """
    注册账号，指令: 注销|退出登录|zx
    """
    @weixin_authenticated
    def handler(self):
        self.session.logout()
        self.write_result('注销成功')

class LoginCommand(CommandHandler):
    """
    登录账号，指令: 登录|dl + 用户名 + 密码
    """
    def handler(self):
        if len(self.args) != 2:
            self.write_error('登录格式有误，请回复格式如ld 用户名 密码的语句')
            return

        username, password = self.args
        
        monitor_id = try_login(username, password)
        if monitor_id == None:
            self.write_error('登录失败，请检查用户名和密码是否正常')
        else:
            self.session['monitor_id'] = monitor_id
            self.session.save()
            self.write_result('登录成功，请尽情使用本系统')
        
