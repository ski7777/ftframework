#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from communication.Client import Client
from config import getConfig, getServerConfig, getClientConfig, getPeripheralsConfig, getDisplayConfigs
from peripherals.common.display import getDisplays, datahandlerdisplays
from twisted.internet import reactor
from _thread import start_new_thread
import argparse
import socket

args = argparse.ArgumentParser(description='ftFramework client')
args.add_argument('--name', default=socket.gethostname(), help='The name of the client')
args.add_argument('--disable-displays', action='store_false', default=True, dest='displays', help='Set  this if displays should be disabled')
args = args.parse_args()

# load config and get special parts
config = getConfig(__file__, 'config.json')
serverconfig = getServerConfig(config)
clientconfig = getClientConfig(config, args.name)
displayconfigs = getDisplayConfigs(getPeripheralsConfig(clientconfig), getPeripheralsConfig(config))


# initialize displays
if args.displays:
    displays = getDisplays(displayconfigs)
else:
    displays = {}

# define datahandler


def datahandler(data, server):
    # run datahandler -> if processed return
    if datahandlerdisplays(displays, data):
        return
    print(data.getJSON())


# initialize client
client = Client(args.name, datahandler, config)
reactor.connectTCP(serverconfig['host'], serverconfig['port'], client)
start_new_thread(reactor.run, (False,))

while True:
    pass
