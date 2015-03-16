#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-11 18:37:52
# Filename        : public/e.py
# Description     : 
from requests import post
from config.config import remote_config

class MonitorException(Exception):
    def __init__(self, message, client_id):
        print message
        post(url = remote_config.post_url, data={
            'error': message,
            'client_id': client_id,
            })

