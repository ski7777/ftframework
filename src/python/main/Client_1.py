#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from communication.Client import Client
from config import getConfig, getServerConfig, getClientConfig, getPeripheralsConfig, getDisplayConfigs
from peripherals.common.display import getDisplays, datahandlerdisplays
from twisted.internet import reactor
from _thread import start_new_thread

NAME = 'client1'
# load config and get special parts
config = getConfig(__file__, 'config.json')
serverconfig = getServerConfig(config)
clientconfig = getClientConfig(config, NAME)
displayconfigs = getDisplayConfigs(getPeripheralsConfig(clientconfig), getPeripheralsConfig(config))

# initialize displays
displays = getDisplays(displayconfigs)


# define datahandler
def datahandler(data, server):
    # run datahandler -> if processed return
    if datahandlerdisplays(displays, data):
        return
    print(data.getJSON())


# initialize client
client = Client(NAME, datahandler, config)
reactor.connectTCP(serverconfig['host'], serverconfig['port'], client)
start_new_thread(reactor.run, (False,))

while True:
    pass
