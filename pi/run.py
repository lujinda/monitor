#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-11 12:34:59
# Filename        : run.py
# Description     : 
from __future__ import unicode_literals, absolute_import

from app import MonitorWebSocketApp
import websocket

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws_app = MonitorWebSocketApp()
    ws_app.run_forever()

