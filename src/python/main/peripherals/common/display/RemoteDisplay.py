#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from communication.Messages import msgSetDisplay

# this class represents a remote display
# It has the same API as a luma.core.device object to allow easier usage


class RemoteDisplay:
    def __init__(self, config, name, remote):
        self.config = config
        self.name = name
        self.remote = remote
        # the following variables are for the canvas wrapper
        self.rotate = config['rotate']
        width = self.config['size']['width']
        height = self.config['size']['height']
        self.width = width if self.rotate % 2 == 0 else height
        self.height = height if self.rotate % 2 == 0 else width
        self.size = (self.width, self.height)
        self.bounding_box = (0, 0, self.width - 1, self.height - 1)
        self.mode = self.config['mode']

    def display(self, image):
        # image is a PIL.Image object
        # convert it to bytes, base64 encode it convert it to a string
        from base64 import b64encode
        data = b64encode(image.tobytes()).decode('utf-8')
        # create a package
        package = msgSetDisplay
        package.data['display'] = self.name
        package.data['image'] = data
        # send data
        self.remote.sendData(package)
