#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from twisted.internet.protocol import ClientFactory

from .ClientConnection import ClientConnection


# This is the client class. It handles the client itself but not the connection


class Client(ClientFactory):

    def __init__(self, name, datahandler, config, closehandler=None):
        # name is the name of the client
        # datahandler is a method (data, client instance) to handle incoming data
        # config is a clientconfig dict
        # closehandler is a fucntion which is called when the connection is being closed
        self.name = name
        self.datahandler = datahandler
        self.config = config
        self.closehandler = closehandler

    def buildProtocol(self, addr):
        # build connection and return it
        self.client = ClientConnection(self)
        return self.client

    def handledata(self, data, server):
        # call the datahandler
        self.datahandler(data, self.client)

    def close(self):
        # call the close handler if possible
        try:
            self.closehandler()
        except:
            pass
