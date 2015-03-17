#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 21:32:58
# Filename        : public/token.py
# Description     : 
from data.db import redis_db
from uuid import uuid4

TOKEN_EXPIRED = 60

def made_real_token(session_id):
    """
    用来生成为微信用户来获取实时信息的token, 用于web方式的
    """
    token = uuid4().hex
    redis_db.setex('w_token_' + session_id, token, TOKEN_EXPIRED)

    return token

def get_real_token(session_id):
    return redis_db.get('w_token_' + session_id) or None

