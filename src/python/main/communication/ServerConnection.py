#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from .Connection import Connection
from .Messages import msgConnected, msgAccepted, msgRejected, msgLogin, msgClose
from .Package import Package

# this class represents the connection between two parties on the server side


class ServerConnection(Connection):
    def __init__(self, server):
        Connection.__init__(self, server)

    def connectionMade(self):
        # send msgConnected
        self.sendData(msgConnected)
        # set state to 'open' right after connection has been made
        self.state = 'open'
        self.name = ''

    def systemLineRecieved(self, package):
        # handle recieved system packages
        if self.state == 'open' and package.isSimilar(msgLogin):
            # state 'open' and package msgLogin
            # get name
            self.name = package.data['name']
            # check whether name is already legged in
            if self.name in self.transporter.clients:
                # already logged in -> reject
                self.sendData(msgRejected)
                return
            # else add client and accept
            self.transporter.clients[self.name] = self
            self.sendData(msgAccepted)
            # set state 'ok'
            self.state = 'ok'
        if package == msgClose:
            del self.transporter.clients[self.name]
