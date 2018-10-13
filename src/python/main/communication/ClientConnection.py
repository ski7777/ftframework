#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from .Connection import Connection
from .Messages import msgConnected, msgLogin, msgAccepted, msgRejected, msgClose
from .Package import Package

# this class represents the connection between two parties on the client side


class ClientConnection(Connection):
    def __init__(self, client):
        Connection.__init__(self, client)
        self.name = client.name

    def connectionMade(self):
        # set state to 'open' right after connection has been made
        self.state = 'open'

    def systemLineRecieved(self, package):
        # handle recieved system packages
        if self.state == 'open' and package == msgConnected:
            # state 'open' and package msgConnected
            # this is the request by the server to login
            # load package and fill in name
            login = msgLogin
            login.data['name'] = self.name
            login.data['checksum'] = self.checksum
            # send data and set new state
            self.sendData(login)
            self.state = 'login'  # 'login' means that the login process is pending
        elif self.state == 'login':
            # if state is login we have two possible packages
            if package == msgAccepted:
                # either the connection is accepted -> set state 'ok'
                self.state = 'ok'
            elif package.isSimilar(msgRejected):
                # or not -> close connection
                self.transporter.close()
                print("Connection rejected")
                print("Reason:", package.data['reason'])
        if package == msgClose:
            self.transporter.close()
