#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json

# A package is a block of data tranfered between two end points


class Package:
    type = ''
    status = ''
    data = {}

    def __init__(self, data={}):
        # normally a package is empty but it is possible to load a dict directly
        if data != {}:
            self.type = data['type']
            self.status = data['status']
            self.data = data['data']

    def getJSON(self):
        # this method returns a JSON to send to the other party
        # validate the data
        assert((
            self.type in ['system', 'data'] and self.status in ['ok', 'error'] and self.data != {}
        ) or (
            self.type in ['ping', 'pong'] and self.status == 'ok' and self.data == {}
        ))
        # build package
        data = {'type': self.type, 'status': self.status, 'data': self.data}
        # return JSON
        return(json.dumps(data, sort_keys=True))

    def loadJSON(self, data):
        # load the given JSON
        data = json.loads(data)
        self.type = data['type']
        self.status = data['status']
        self.data = data['data']

    def __eq__(self, other):
        # this method is called when rich comparisson equal is called
        # it checks whether the two objects are both Package and have the same data
        if isinstance(other, Package):
            return self.getJSON() == other.getJSON()
        return False

    def isSimilar(self, other):
        # this method checks whether the two packages are similar to each other
        if isinstance(other, Package):
            return self.type == other.type and self.status == other.status and sorted(list(self.data.keys())) == sorted(list(other.data.keys()))
        return False
