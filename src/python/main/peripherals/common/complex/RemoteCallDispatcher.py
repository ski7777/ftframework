#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from threading import Lock


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
