#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from ftframework.communication.Messages import msgCall, msgCallException, msgCallResponse


def getClass(config):
    if config['builtin']:
        prefix = 'ftframework.peripherals.common'
    else:
        prefix = ''
    module = __import__(prefix + config['path'], fromlist=[config['name']])
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


def datahandlercomplex(complex, server, data):
    if data.isSimilar(msgCall):
        try:
            # get complex
            complex = complex[data.data['peripheral']]
            # Prepare variable for return package
            ret = None
            # get method by object and name, call it with arguments
            try:
                retval = getattr(complex['object'], data.data['call'])(**data.data['arguments'])
                if 'return' in complex['object'].calls[data.data['call']]:
                    ret = msgCallResponse
                    ret.data['value'] = retval
            # catch exception and load data in package
            except Exception as e:
                ret = msgCallException
                ret.data['name'] = e.__class__.__name__
                ret.data['text'] = e.__str__()
            # send back all collected data if available and id given
            if ret is not None and data.data['id'] != '':
                ret.data['id'] = data.data['id']
                server.sendData(ret)
        # catch KeyError here. If peripheral is unknown we will catch it here
        except KeyError:
            pass
        return(True)
    else:
        return(False)
