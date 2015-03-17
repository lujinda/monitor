#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-16 18:33:10
# Filename        : run.py
# Description     : 
from __future__ import unicode_literals, absolute_import

from app import MonitorWebSocketApp
import websocket
from time import sleep

if __name__ == "__main__":
    websocket.enableTrace(True)
    while True:
        ws_app = MonitorWebSocketApp()
        ws_app.run_forever(ping_interval = 10, sslopt={"check_hostname": False})
        if ws_app.abort_exit:
            break
        sleep(1)

