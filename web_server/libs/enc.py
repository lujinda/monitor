#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-10 15:56:36
# Filename        : libs/enc.py
# Description     : 
from hashlib import md5

def enc_string(string):
    return md5(string).hexdigest()

