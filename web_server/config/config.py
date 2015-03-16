#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-13 17:28:38
# Filename        : config/config.py
# Description     : 

from ConfigParser import ConfigParser

CFG_PATH = 'config/config.cfg'

class Config():
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read(CFG_PATH)

    def __get_config(self, section, int_list = None):
        _config = {}
        int_list = int_list or []
        for k, v in self.cfg.items(section):
            if k in int_list:
                v = int(v)
            _config[k] = v

        return _config

    @property
    def redis_config(self):
        return self.__get_config('redis', ['db', 'port'])

    @property
    def weixin_config(self):
        return self.__get_config('weixin')

config = Config()
redis_config = config.redis_config
weixin_config = config.weixin_config

