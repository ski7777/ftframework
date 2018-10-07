#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from twisted.protocols.basic import LineReceiver
from .Package import Package
from .Messages import msgPing, msgPong
from .PingThread import PingThread

# this class represents the connection between two parties


class Connection(LineReceiver):
    # this varaiable defines the state of the connection
    # depending on the side it can have various states
    # 'ok' is the state when the connectin has been established and data can be tranfered safely
    # this is after the login procedure
    state = ''

    def __init__(self, transporter):
        # transporter can be either Server or Client
        self.transporter = transporter
        self.config = self.transporter.config['connection']
        self.debug = self.config['debug']
        self.pingthread = PingThread(self)
        self.pingthread.start()

    def lineReceived(self, data):
        # this method is called when a new line is recieved
        # data is the raw line
        # create new Package
        package = Package()
        # load decoded data
        package.loadJSON(data.decode('utf-8'))
        # print if debug prints are enabled
        if self.debug:
            print("IN:", package.getJSON())
        # now the package needs to be handled somewhere
        # if it is type system, systemLineRecieved will do this
        if package.type == 'system':
            self.systemLineRecieved(package)
        # if it is ping we answer with pong
        elif package == msgPing:
            self.sendData(msgPong)
        # if it is pong we need to deliver this to the ping/pong thread
        elif package == msgPong:
            self.pingthread.pong()
        # if it none of the above it must be data, so we call the handledata method of the transporter
        else:
            self.transporter.handledata(package, self)

    def sendData(self, package):
        # check whether state is either 'ok' or it is a system message
        if self.state == 'ok' or package.type in ['system', 'ping', 'pong']:
            # print if debug prints are enabled
            if self.debug:
                print("OUT:", package.getJSON())
            # send data
            self.sendLine(package.getJSON().encode('utf-8'))
            return(True)
        else:
            # if send was not allowed return False
            return(False)

    def systemLineRecieved(self, package):
        # dummy method for system packages
        # this will be overwritten by ClientConnection/ServerConnection
        pass

    def close(self):
        # dummy method for system packages
        # this will be overwritten by ClientConnection/ServerConnection if needed
        pass
