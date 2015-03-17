#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-16 14:32:29
# Filename        : public/account.py
# Description     : 
from data.db import db

def try_login(username, password):
    """
    如果成功，登录则返回账号所属树莓派的id
    """
    account_obj = db.account.find_one({'username': username,
        'password': password})
    return account_obj and account_obj['monitor_id'] or None

