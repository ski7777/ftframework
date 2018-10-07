#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json
import os


# just some helper methods around the configuration file


def getConfig(runfile, name):
    path = os.path.join(os.path.dirname(os.path.abspath(runfile)), name)
    with open(path) as f:
        data = json.load(f)
    return(data)


def getServerConfig(config):
    return(config['server'])


def getClientConfig(config, name):
    return(config['clients'][name])


def getPeripheralsConfig(config):
    return(config['peripherals'])


def getDisplayConfigs(client, general):
    client = client['displays']
    displays = general['displays']
    for n, d in client.items():
        client[n]['config'] = displays[n]
    return(client)


def findDisplay(config, name):
    clients = config['clients']
    for n, c in clients.items():
        p = getPeripheralsConfig(c)
        if name in p['displays']:
            return(n)