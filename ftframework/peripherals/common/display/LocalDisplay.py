#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from .UpdateThread import UpdateThread
from ftframework.communication.Messages import msgSetDisplay


def getDisplay(config, name):
    if config['type'] == 'i2c':
        from luma.core.interface.serial import i2c
        serial = i2c(port=config['bus'], address=config['address'])
    # TODO: Add SPI/BB support
    if config['config']['type'] == 'ssd1306':
        from luma.oled.device import ssd1306
        reference = ssd1306
        display = reference(serial, rotate=config['config']['rotate'])
    # add support for other displays
    else:
        return(None)

    # save reference and name in display
    display.reference = reference
    display.name = name

    # overwrite the display method
    def display_(self, data):
        # dont write the data to the display. First save it in the thread
        self.thread.setData(data, self.name)

    display.display = display_
    return(display)


def setDisplay(display, data):
    # decode data and write it to display
    from PIL import Image
    from base64 import b64decode
    image = Image.frombytes(display.mode, display.size, b64decode(data.encode('utf-8')))
    display.display(display, image)


def getDisplays(displayconfigs):
    displays = {}
    for n, d in displayconfigs.items():
        # some crude logic to generate a name for the display interface
        if d['type'] == 'i2c':
            t = 'i2c-' + d['bus']
        elif d['type'] == 'spi':
            if d['bus'] != 'bb':
                t = 'spi-' + d['bus']
        else:
            t = 'single'
        if t not in displays:
            displays[t] = {}
        # save display object
        displays[t][n] = getDisplay(d, n)

    # create threads for each interface

    # 'single' is sprecial. Here we need one thread per interface
    if 'single' in displays:
        # create on thread per display, start it and save it in the display
        for n in displays['single']:
            thread = UpdateThread(displays['single'])
            thread.start()
            displays['single'][n].thread = thread

    # iterate over all other interfaces
    for c in [c for c in displays if c != 'single']:
        # start one thread each
        thread = UpdateThread(displays[c])
        thread.start()
        for n in displays[c]:
            # save it in all displays
            displays[c][n].thread = thread

    # create a dict with all displays
    alldisplays = {}
    for d in displays.values():
        for n, dd in d.items():
            alldisplays[n] = dd
    # return it
    return(alldisplays)


def datahandlerdisplays(displays, server, data):
    if data.isSimilar(msgSetDisplay):
        try:
            display = displays[data.data['display']]
            setDisplay(display, data.data['image'])
        except KeyError:
            pass
        return(True)
    else:
        return(False)
