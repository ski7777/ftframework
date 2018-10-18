#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from communication.Messages import msgCall


def getClass(config):
    module = __import__(config['path'], fromlist=[config['name']])
    return(getattr(module, config['name']))


def getClasses(config):
    classes = {}
    for n, c in config.items():
        classes[n] = {
            'class': getClass(c['config']),
            'config': c
        }
    return(classes)


def initializeClasses(complex, controllers):
    for n, d in complex.items():
        complex[n]['object'] = d['class'](d['config'], controllers)
    return(complex)


def datahandlercomplex(complex, data):
    if data.isSimilar(msgCall):
        try:
            # get complex
            complex = complex[data.data['peripheral']]
            # get method by object and name, call it with arguments
            getattr(complex['object'], data.data['call'])(**data.data['arguments'])
        except KeyError:
            pass
        return(True)
    else:
        return(False)
