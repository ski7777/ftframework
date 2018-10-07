#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
from .Package import Package

msgConnected = Package({
    'type': 'system',
    'status': 'ok',
    'data': {
        'message': 'connected'
    }
})

msgRejected = Package({
    'type': 'system',
    'status': 'ok',
    'data': {
        'message': 'rejected'
    }
})

msgAccepted = Package({
    'type': 'system',
    'status': 'ok',
    'data': {
        'message': 'accepted'
    }
})

msgLogin = Package({
    'type': 'system',
    'status': 'ok',
    'data': {
        'message': 'login',
        'name': ''
    }
})

msgClose = Package({
    'type': 'system',
    'status': 'ok',
    'data': {
        'message': 'close'
    }
})

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
