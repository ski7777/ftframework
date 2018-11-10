#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import threading
import time

from .Messages import msgPing


# this thread handles periodic ping requests


class PingThread(threading.Thread):
    lastping = 0
    lastpong = 0

    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent
        self.config = self.parent.config['ping']
        self.startupwait = self.config['startupwait']
        self.pinginterval = self.config['pinginterval']
        self.pongmaxage = self.config['pongmaxage']
        self.runinterval = self.config['runinterval']

    def run(self):
        # wait on startup and initialize pong time
        time.sleep(self.startupwait)
        self.pong()
        # now the endless loop begins...
        while True:
            # check whether we need to send a ping and do so if needed
            if self.lastping + self.pinginterval < time.time():
                self.ping()
            # check whether the last pong was too long ago
            if self.lastpong + self.pongmaxage < time.time():
                # close thread and return
                self.close()
                return
            # wait for next cycle
            time.sleep(self.runinterval)

    def ping(self):
        # send a ping and reset time
        self.parent.sendData(msgPing)
        self.lastping = time.time()

    def pong(self):
        # set pong time
        self.lastpong = time.time()

    def close(self):
        # call parent close call
        self.parent.close()
