#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-10 16:12:44
# Filename        : config/config.py
# Description     : 

from ConfigParser import ConfigParser

CFG_PATH = 'config/config.cfg'

class ConfigData(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

class Config():
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read(CFG_PATH)

    def __get_config(self, section, int_list = None):
        _config = ConfigData()
        int_list = int_list or []
        for k, v in self.cfg.items(section):
            if k in int_list:
                v = int(v)
            _config[k] = v

        return _config

    @property
    def remote_config(self):
        return self.__get_config('remote')

config = Config()
remote_config = config.remote_config

