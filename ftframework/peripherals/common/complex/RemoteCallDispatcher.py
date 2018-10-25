#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from threading import Lock
from ftframework.communication.Messages import msgCallResponse
from uuid import uuid4


class RemoteCallDispatcher:
    data = {}
    datalock = Lock()

    def registerCall(self, id):
        # add empty dict for id
        self.datalock.acquire()
        self.data[id] = {}
        self.datalock.release()

    def waitOnResponse(self, id):
        ret = False
        # run until response
        while not ret:
            self.datalock.acquire()
            # check value available
            if 'value' in self.data[id]:
                # get value
                val = self.data[id]['value']
                # delete reference
                del self.data[id]
                # set status
                ret = True
            self.datalock.release()
        # return value
        return(val)

    def datahandler(self, server, data):
        # process packages
        if data.isSimilar(msgCallResponse):
            try:
                self.datalock.acquire()
                # save value
                self.data[data.data['id']]['value'] = data.data['value']
                self.datalock.release()
            except KeyError:
                pass
            return(True)
        else:
            return(False)

    def getCall(self):
        # return RemoteCall with dispatcher
        return(RemoteCall(self))


class RemoteCall:
    def __init__(self, dispatcher):
        # generate id
        self.id = uuid4().hex
        self.dispatcher = dispatcher
        # register
        self.dispatcher.registerCall(self.id)

    def waitOnResponse(self):
        # call parent
        return(self.dispatcher.waitOnResponse(self.id))
