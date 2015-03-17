#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-16 18:46:58
# Filename        : data/db.py
# Description     : 

from redis import Redis
from config.config import redis_config
from pymongo import Connection

redis_db = session_db = Redis(**redis_config)
db = Connection().monitor

