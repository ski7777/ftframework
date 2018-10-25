#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from ftframework.communication.Server import Server
from ftframework.config import getConfig, getServerConfig, getServerPeripheralConfig
from ftframework.peripherals.common.display import initializeRemoteDisplays
from ftframework.peripherals.common.complex.RemoteClass import initializeRemoteClasses
from ftframework.peripherals.common.complex.RemoteCallDispatcher import RemoteCallDispatcher
from twisted.internet import reactor
from luma.core.render import canvas
from _thread import start_new_thread
import time
from datetime import datetime

# load config and get special parts
config = getConfig(__file__, 'config.json')
serverconfig = getServerConfig(config)
peripheralsconfig = getServerPeripheralConfig(config, ['displays', 'complex'])

calldispatcher = RemoteCallDispatcher()

# define datahandler
datahandlers = [(calldispatcher.datahandler, None)]


def datahandler(data, client):
    # run datahandler -> if processed return
    for d, v in datahandlers:
        arg = []
        if v != None:
            arg.append(v)
        arg.append(client)
        arg.append(data)
        if d(*arg):
            return
    print(client.name, data.getJSON())


# initialize server
server = Server(datahandler, config)
reactor.listenTCP(serverconfig['port'], server)
start_new_thread(reactor.run, (False,))
print('Server ready!')
print('Waiting for clients!')

# wait for clients
while not config['clients'].keys() == set(server.clients):
    pass
print('All clients connected!')

complex = initializeRemoteClasses(peripheralsconfig['complex'], server.clients, calldispatcher)
displays = initializeRemoteDisplays(peripheralsconfig['displays'], config['clients'], server.clients)

# draw some test stuff on display 1 and 2
display1 = displays['display1']
display2 = displays['display2']
cnt = 0
while True:
    cnt += 1
    with canvas(display1) as draw:
        draw.rectangle(display1.bounding_box, outline='white', fill='black')
        t = datetime.now()
        draw.text((10, 5), 'Hello World', fill='white')
        draw.text((10, 20), str(t.strftime('%Y-%m-%d')), fill='white')
        draw.text((10, 30), str(t.strftime('%H:%M:%S')), fill='white')
        if (int(t.strftime('%S')) % 2) == 0:
            draw.text((10, 40), 'X', fill='white')
        draw.text((10, 50), str(cnt), fill='white')
    with canvas(display2) as draw:
        draw.rectangle(display1.bounding_box, outline='white', fill='black')
        t = datetime.now()
        draw.text((10, 5), 'Hello World XXX', fill='white')
        draw.text((10, 20), str(t.strftime('%Y-%m-%d')), fill='white')
        draw.text((10, 30), str(t.strftime('%H:%M:%S')), fill='white')
        if (int(t.strftime('%S')) % 2) == 0:
            draw.text((10, 40), 'X', fill='white')
        draw.text((10, 50), str(cnt), fill='white')
    time.sleep(0.01)