#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-10 17:08:52
# Filename        : data/db.py
# Description     : 

from redis import Redis
from config.config import redis_config

session_db = Redis(**redis_config)


