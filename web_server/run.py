#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-10 16:18:20
# Filename        : run.py
# Description     : 
from tornado import options, ioloop, httpserver
from tornado.options import options, define

from app import MonitorApplication

define('port', type=int, default=1234, help="listen port")

if __name__ == "__main__":
    options.parse_command_line()
    application = MonitorApplication()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)

    ioloop.IOLoop.instance().start()

