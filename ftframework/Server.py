#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from _thread import start_new_thread

from twisted.internet import reactor

from ftframework.communication.Server import Server as ComServer
from ftframework.config import getConfig, getServerConfig, getServerPeripheralConfig
from ftframework.peripherals.common.complex.RemoteCallDispatcher import RemoteCallDispatcher
from ftframework.peripherals.common.complex.RemoteClass import initializeRemoteClasses
from ftframework.peripherals.common.display import initializeRemoteDisplays


class Server:
    calldispatcher = RemoteCallDispatcher()
    datahandlers = []
    attributes = {}

    def __init__(self, config):
        # load config and get special parts
        self.config = getConfig(config)
        self.serverconfig = getServerConfig(self.config)
        self.peripheralsconfig = getServerPeripheralConfig(self.config, ['displays', 'complex'])
        # initialize server
        self.server = ComServer(self.datahandler, self.config)
        reactor.listenTCP(self.serverconfig['port'],  self.server)
        start_new_thread(reactor.run, (False,))
        print('Server ready!')
        print('Waiting for clients!')
        # wait for clients
        while not self.config['clients'].keys() == set(self.server.clients):
            pass
        print('All clients connected!')
        self.attributes.update(initializeRemoteClasses(self.peripheralsconfig['complex'], self.server.clients, self.calldispatcher))
        self.attributes.update(initializeRemoteDisplays(self.peripheralsconfig['displays'], self.config['clients'], self.server.clients))

    def registerDataHandler(self, call, data=None):
        self.datahandlers.append((call, data))

    def datahandler(self, data, client):
        # run datahandler -> if processed return
        for d, v in self.datahandlers:
            arg = []
            if v != None:
                arg.append(v)
            arg.append(client)
            arg.append(data)
            if d(*arg):
                return
        print(client.name, data.getJSON())

    def __getattr__(self, name):
        return(self.attributes[name])
