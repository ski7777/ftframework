#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse
import socket
import sys
from _thread import start_new_thread

from twisted.internet import reactor

from ftframework.communication.Client import Client
from ftframework.config import getClientConfig, getConfig, getPeripheralsConfig, getServerConfig, mergeConfigs
from ftframework.peripherals.common.complex.LocalClass import datahandlercomplex, getClasses, initializeClasses
from ftframework.peripherals.common.controller import getControllers
from ftframework.peripherals.common.display import datahandlerdisplays, getDisplays

sys.path.append('.')

args = argparse.ArgumentParser(description='ftFramework client')
args.add_argument('--name', default=socket.gethostname(), help='The name of the client')
args.add_argument('--disable-displays', action='store_false', default=True, dest='displays',
                  help='Set  this if displays should be disabled')
args.add_argument('config', help='Path to global config.json')
args = args.parse_args()

# load config and get special parts
config = getConfig(args.config)
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
