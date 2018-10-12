#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


def getClass(config):
    config = config['config']
    module = __import__(config['path'], fromlist=[config['name']])
    return(getattr(module, config['name']))


def getClasses(config):
    classes = {}
    for n, c in config.items():
        classes[n] = {
            'class': getClass(c),
            'config': c
        }
    return(classes)


def initializeClasses(complex, controllers):
    for n, d in complex.items():
        complex[n]['object'] = d['class'](d['config'], controllers)
    return(complex)
