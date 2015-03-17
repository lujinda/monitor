#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com # Last modified   : 2015-03-16 20:00:42
# Filename        : monitor/capture.py
from __future__ import unicode_literals

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import cv2
from PIL import Image
from .base import BaseMonitor 
CAPTURE_NO = 1

class CaptureMonitor(BaseMonitor):
    """
    负责视频监控类的
    """
    def __init__(self):
        pass
    def get_image(self): 
        capture = cv2.VideoCapture(CAPTURE_NO)

        ret, img = capture.read()
        capture.release()

        assert ret

        return img

    def exec_monitor(self, client_id):
        img = self.get_image()
        img_raw_data = self.process_image(img)

        post_data = {'client_id': client_id}
        post_file = {'image': ('a.jpeg', img_raw_data, 'image/jpeg')}
        self.send_result(post_data, post_file)

    def process_image(self, img): 
        """
        处理图片，并获取图片的原始数据
        """
        img = cv2.resize(img, (680, 480))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img, 'RGB')
        s_io = StringIO()
        img.save(s_io, format = 'JPEG')

        return s_io.getvalue()

