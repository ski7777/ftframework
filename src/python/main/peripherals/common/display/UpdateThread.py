#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import threading
import time

# this thread manages the update of all displays of one interface
# (It´s not needed that all displays of this thread are on the same interface
# but it´s recommended for higher frame rates)


class UpdateThread(threading.Thread):
    def __init__(self, displays):
        # displays is the dict with all displays for this thread
        threading.Thread.__init__(self)
        self.daemon = True
        self.displays = displays
        # data will be the place to save pending frames
        self.data = {}
        # for every access on the data dict the lock needs to be set/unset
        self.datalock = threading.Lock()

    def run(self):
        while True:
            # acquire lock
            self.datalock.acquire()
            # copy data
            data = self.data.copy()
            # wipe original dict
            self.data = {}
            # release lock
            self.datalock.release()
            # iterate over displays
            for n, d in data.items():
                # get display and reference
                display = self.displays[n]
                reference = display.reference
                # set display
                reference.display(display, d)
            # wait a moment
            time.sleep(0.1)

    def setData(self, data, name):
        # this is to save a new image for a display
        # check display name is available
        assert(name in self.displays)
        # acquire lock
        self.datalock.acquire()
        # save data
        self.data[name] = data
        # release lock
        self.datalock.release()
