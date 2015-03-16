#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-13 16:06:23
# Filename        : monitor/base.py
# Description     : 
from requests import post
from config.config import remote_config

from celery import Celery
from celery.contrib.methods import task_method

BROKER_URL = 'redis://127.0.0.1:6379/15'
celery = Celery('MonitorManager', broker = BROKER_URL)

class BaseMonitor():
    """
    各种监控器的基类, 定义了一些接口
    """
    def __init__(self):
        raise NotImplementedError

    def exec_monitor(self):
        raise NotImplementedError

    @celery.task(filter = task_method)
    def __send_result(self, data = {}, files = None):
        post(url = remote_config.post_url,
                data = data, files = files)

    def send_result(self, *args, **kwargs):
        self.__send_result.delay(*args, **kwargs)

