#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-17 22:03:31
# Filename        : handler/weixin_handler.py
# Description     : 
from __future__ import unicode_literals, absolute_import

from handler.public import RealTimeHandler
from tornado.web import asynchronous, HTTPError
import hashlib
from config.config import weixin_config
from lxml import etree
from weixin.router import WeiXinRouter
from libs.session import WeiXinSession


class WeiXinHandler(RealTimeHandler):
    """
    处理微信类
    """
    def get(self):
        """
        验证微信接口
        """
        self.interface_verfication()

    def interface_verfication(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')

        token = weixin_config['token']

        l = [token, timestamp, nonce]
        l.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, l)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            self.write(echostr)

    @asynchronous
    def post(self):
        print self.request.body
        msg_type, result_data = self.parse_xml(self.request.body) # 解析出xml
        self.session = self.get_weixin_session(result_data['from_user']) # 通过微信用户的id来获取session

        self.init_monitor() # 获取 session后就可以初始化监视器了 
        self.weixin_router = WeiXinRouter(result_data['content'])
        _handler = self.weixin_router.get_handler()
        self.weixin = _handler(self, from_user = result_data['from_user'],
                to_user = result_data['to_user'], command = self.weixin_router.command, 
                args = self.weixin_router.args, msg_type = msg_type) # 根据不同的事件，实例化不同的处理类，把自己传入，当服务器处理完后，把信息直接发给用户)


        self.weixin.handler()

    def get_weixin_session(self, from_user):
        session = WeiXinSession(self.application.session_manager, 
                from_user = from_user)
        return session

    def write_error(self, status_code, **kwargs):
        try:
            exc_info = kwargs['exc_info']
            error = exc_info[1].log_message
        except:
            error = '未知错误'

        self.set_status(status_code)
        self.weixin.write_error(error)

    def parse_xml(self, xml_string):
        """
        返回信息类型和数据
        """
        xml = etree.fromstring(xml_string)
        msg_type = xml.find('MsgType').text
        parse_func = getattr(self, '_parse_' + msg_type + '_xml', None)
        if not parse_func:
            return msg_type, _
        xml_data = parse_func(xml)

        return msg_type, xml_data

    def _parse_text_xml(self, xml):
        from_user = xml.find('FromUserName').text
        to_user = xml.find('ToUserName').text
        content = xml.find('Content').text

        return {'from_user': from_user,
                'to_user': to_user, 'content': content}

    def _parse_event_xml(self, xml):
        from_user = xml.find('FromUserName').text
        to_user = xml.find('ToUserName').text
        event = xml.find('Event').text

        return {'from_user': from_user,
                'to_user': to_user, 'event': event, 'content': ''}

    def _parse_voice_xml(self, xml):
        from_user = xml.find('FromUserName').text
        to_user = xml.find('ToUserName').text
        content = xml.find('Recognition').text # 如果是语音信息，则把解析结果给content

        return {'from_user': from_user,
                'to_user': to_user, 'content': content}

