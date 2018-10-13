#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json
import os
import hashlib


# just some helper methods around the configuration file


def getConfig(runfile, name):
    path = os.path.join(os.path.dirname(os.path.abspath(runfile)), name)
    with open(path) as f:
        data = json.load(f)
    data['checksum'] = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
    return(data)


def getServerConfig(config):
    return(config['server'])


def getClientConfig(config, name):
    return(config['clients'][name])


def getPeripheralsConfig(config):
    return(config['peripherals'])


def findDisplay(config, name):
    clients = config['clients']
    for n, c in clients.items():
        p = getPeripheralsConfig(c)
        if name in p['displays']:
            return(n)


def mergeConfigs(client, general, configtype):
    try:
        client = client[configtype]
        general = general[configtype]
    except KeyError:
        return({})
    for n in client.keys():
        client[n]['config'] = general[n]
    return(client)


def getIOConfig(config, controllers, name):
    io = config['ioconfig'][name]
    iocontroller = controllers[io['controller']]['controller']
    port = io['port']
    return(iocontroller, port)
