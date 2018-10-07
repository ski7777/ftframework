#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
from .Package import Package

msgPing = Package({
    'type': 'ping',
    'status': 'ok',
    'data': {}
})

msgPong = Package({
    'type': 'pong',
    'status': 'ok',
    'data': {}
})
