#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-16 15:40:32
# Filename        : libs/session.py
# Description     : 使用redis来实现tornado的session 模块

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle

import hashlib
from uuid import uuid4
import hmac

class InvalidSessionException(Exception):
    pass

class SessionData(dict):
    def __init__(self, session_id, hmac_key = None):
        self.session_id = session_id
        self.hmac_key = hmac_key

class Session(SessionData):
    def __init__(self, session_manager, request):
        self.session_manager = session_manager
        self.request = request

        try:
            current_session = session_manager.get(request)
        except InvalidSessionException: # 如果session出错了，就认定为无session信息，则新建一个session
            current_session = session_manager.get()

        for _key, _value in current_session.iteritems():
            self[_key] = _value

        self.session_id = current_session.session_id
        self.hmac_key = current_session.hmac_key

        if 'session_id' not in current_session:
            # 如果在当前session中还没有session_id，则把它添加进去，并保存到session
            self['session_id'] = current_session.session_id
            self.save()

    def save(self):
        self.session_manager.set(self.request, self)

    def logout(self):
        self.session_manager.delete(self.request, self)

class WeiXinSession(SessionData):
    def __init__(self, session_manager, from_user):
        self.session_manager = session_manager
        self.from_user = from_user
        current_session = session_manager.get_weixin(from_user)

        for _key, _value in current_session.iteritems():
            self[_key] = _value

        if 'session_id' not in current_session:
            # 如果在当前session中还没有session_id，则把它添加进去，并保存到session
            self['session_id'] = current_session.session_id

    def save(self):
        self.session_manager.set_weixin(self)

    def logout(self):
        self.session_manager.delete_weixin(self)

class SessionManager(object):
    def __init__(self, session_secret, session_timeout, session_db):
        self.session_secret = session_secret
        self.session_timeout = session_timeout
        self.session_db = session_db

    def get(self, request = None):
        session_id = (request and request.get_secure_cookie('session_id')) or self._gen_session_id()
        hmac_key = (request and request.get_secure_cookie('verification')) or self._gen_hmac_key(session_id)

        if hmac_key != self._gen_hmac_key(session_id):
            raise InvalidSessionException

        session = SessionData(session_id, hmac_key)
        session_data = self._fetch(session_id) # 从redis获取session的内容
        session.update(session_data)

        return session

    def get_weixin(self, from_user):
        session_id = from_user
        session = SessionData(session_id)
        session_data = self._fetch(session_id)
        session.update(session_data)

        return session

    def set_weixin(self, session):
        self.session_db.setex(session.from_user, pickle.dumps(dict(session.items())),
                self.session_timeout)

    def set(self, request, session):
        request.set_secure_cookie('session_id', session.session_id)
        request.set_secure_cookie('verification', session.hmac_key)

        self.session_db.setex(session.session_id, pickle.dumps(dict(session.items())),
                self.session_timeout)

    def delete(self, request, session):
        request.clear_cookie('session_id')
        request.clear_cookie('verification')

        self.session_db.delete(session.session_id)

    def delete_weixin(self, session):
        self.session_db.delete(session.from_user)

    def _fetch(self, session_id):
        try:
            raw_data = self.session_db.get(session_id)
            if raw_data:
                session_data = pickle.loads(raw_data)
                self.session_db.setex(session_id, raw_data, self.session_timeout) # 每次访问，就重新设置过期时间
            else:
                session_data = {}

            return isinstance(session_data, dict) and session_data or {}
        except IOError, e:
            return {}

    def _gen_session_id(self):
        _id = hashlib.sha256(self.session_secret + str(uuid4()))
        return _id.hexdigest()

    def _gen_hmac_key(self, session_id):
        return hmac.new(session_id, self.session_secret, 
                hashlib.sha256).hexdigest()

