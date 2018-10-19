#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from communication.Client import Client
from config import getConfig, getServerConfig, getClientConfig, getPeripheralsConfig, mergeConfigs
from peripherals.common.display import getDisplays, datahandlerdisplays
from peripherals.common.controller import getControllers
from peripherals.common.complex.LocalClass import getClasses, initializeClasses, datahandlercomplex
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
displayconfigs = mergeConfigs(getPeripheralsConfig(clientconfig), getPeripheralsConfig(config), 'displays')
controllerconfigs = mergeConfigs(getPeripheralsConfig(clientconfig), getPeripheralsConfig(config), 'controllers')
complexperipheralsconfigs = mergeConfigs(getPeripheralsConfig(clientconfig), getPeripheralsConfig(config), 'complex')

# initialize displays
if args.displays:
    displays = getDisplays(displayconfigs)
else:
    displays = {}

# initialize controllers
controllers = getControllers(controllerconfigs)

# initialie complex peripherals
# load classes
complex = initializeClasses(getClasses(complexperipheralsconfigs), controllers)

# define datahandler
datahandlers = [(datahandlerdisplays, displays), (datahandlercomplex, complex)]


def datahandler(data, server):
    # run datahandler -> if processed return
    for d, v in datahandlers:
        arg = []
        if v != None:
            arg.append(v)
        arg.append(server)
        arg.append(data)
        if d(*arg):
            return
    print(data.getJSON())


# initialize client
client = Client(args.name, datahandler, config)
reactor.connectTCP(serverconfig['host'], serverconfig['port'], client)
start_new_thread(reactor.run, (False,))
print('Client ready!')

while True:
    pass
