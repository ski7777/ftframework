#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from twisted.internet.protocol import Factory

from .ServerConnection import ServerConnection


class Server(Factory):
    def __init__(self, datahandler, config):
        # datahandler is a method (data, client instance) to handle incoming data
        # config is a serverconfig dict
        self.clients = {}
        self.datahandler = datahandler
        self.config = config

    def buildProtocol(self, addr):
        # build connection and return it
        return ServerConnection(self)

    def handledata(self, data, client):
        # call the datahandler
        self.datahandler(data, client)
