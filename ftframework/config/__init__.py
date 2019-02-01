#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import hashlib
import json

# just some helper methods around the configuration file


def getConfig(path):
    with open(path) as f:
        data = json.load(f)
    data['checksum'] = hashlib.md5(json.dumps(
        data, sort_keys=True).encode('utf-8')).hexdigest()
    return (data)


def getServerConfig(config):
    default = {
        'host': '192.168.12.102',
        'port': 4711
    }
    if 'server' in config:
        default.update(config['server'])
    return(default)


def getConnectionConfig(config):
    def updaterecursive(value, nvalue):
        if not isinstance(value, dict) or not isinstance(nvalue, dict):
            return nvalue
        for k, v in nvalue.items():
            value.setdefault(k, dict())
            if isinstance(v, dict):
                v = updaterecursive(value[k], v)
            value[k] = v
        return value

    default = {
        "debug": False,
        "ping": {
            "startupwait": 5,
            "pinginterval": 15,
            "pongmaxage": 60,
            "runinterval": 15
        }
    }
    if 'connection' in config:
        default = updaterecursive(default, config['connection'])
    return(default)


def getClientConfig(config, name):
    return (config['clients'][name])


def getPeripheralsConfig(config):
    return (config['peripherals'])


def findDisplay(clients, name):
    for n, c in clients.items():
        p = getPeripheralsConfig(c)
        if name in p['displays']:
            return (n)


def mergeConfigs(client, general, configtype):
    try:
        client = client[configtype]
        general = general[configtype]
    except KeyError:
        return ({})
    for n in client.keys():
        client[n]['config'] = general[n]
    return (client)


def getIOConfig(config, controllers, name):
    io = config['ioconfig'][name]
    iocontroller = controllers[io['controller']]['controller']
    port = io['port']
    return (iocontroller, port)


def getServerPeripheralConfig(config, names):
    # function to find peripheral by name in all clients
    def findPeripheral(config, name):
        # iterate over clients
        for n, d in config.items():
            # return name of client if found
            if name in d:
                return n
        # else raise KeyError
        raise KeyError

    # create dict(name->{}) for all types of peripherals
    peripherals = dict([(n, {}) for n in names])
    # iterate over clients
    for n, d in config['clients'].items():
        # iterate over types
        for pn in names:
            try:
                # add list of names of peripherals of peripheral type of client
                peripherals[pn][n] = list(getPeripheralsConfig(d)[pn].keys())
            except KeyError:
                pass
    # get minimized peripheral configs for peripheral types
    config = dict([(n, d) for n, d in getPeripheralsConfig(
        config).items() if n in names])
    # iterate over peripheral types
    for cn, cd in config.items():
        # iterate over peripheral names
        for pn in cd.keys():
            # save client name in peripheral
            config[cn][pn]['client'] = findPeripheral(peripherals[cn], pn)
    return (config)
