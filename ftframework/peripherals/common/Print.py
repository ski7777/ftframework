#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


class Print:
    calls = {
        'show': {
            'arguments': [
                ('data', str, True)
            ]
        }
    }

    def __init__(self, config, controllers):
        pass

    def show(self, data):
        print(data)
