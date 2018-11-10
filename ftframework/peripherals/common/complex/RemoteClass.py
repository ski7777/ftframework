#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from ftframework.communication.Messages import msgCall
from .LocalClass import getClass


class RemoteClass:
    def __init__(self, name, config, client, calldispatcher):
        self.name = name
        self.cls = getClass(config)
        self.client = client
        self.calls = self.cls.calls
        self.calldispatcher = calldispatcher

    def __getattr__(self, name):
        # define universal method
        def method(*args, **kwarg):
            # check method
            if name not in self.calls:
                raise NameError
            arguments = {}
            # process arguments if needed
            if 'arguments' in self.calls[name]:
                argumentsspec = self.calls[name]['arguments']
                # load arguments
                for n in range(len(args)):
                    arguments[argumentsspec[n][0]] = args[n]
                # load keyword arguments
                for n, v in kwarg.items():
                    arguments[n] = v
                # cleanup arguments
                arguments = dict([(k, v) for k, v in arguments.items() if k in [n for n, t, r in argumentsspec]])
                # check all arguments
                for n, t, r in argumentsspec:
                    if t and n not in arguments:
                        # fail if required argument missing
                        raise ValueError('Argument ' + n + ' missing!')
                    if n not in arguments:
                        # continue if optional argument not available
                        continue
                    # get value of argument
                    v = arguments[n]
                    if not isinstance(v, t):
                        # fail if type mismatch
                        raise TypeError(
                            'Argument ' + n + 'is type ' + type(v).__name__ + ', expected ' + t.__name__ + '!')
            else:
                if len(args) != 0 or len(kwarg) != 0:
                    # raise error if args given but not needed
                    raise ValueError
            # build package
            pkg = msgCall
            msgCall.data['peripheral'] = self.name
            msgCall.data['call'] = name
            msgCall.data['arguments'] = arguments
            # check whether function returns value
            retval = 'return' in self.calls[name]
            if retval:
                # initialize RemoteCall
                call = self.calldispatcher.getCall()
                # set id in package
                msgCall.data['id'] = call.id
            # send data
            self.client.sendData(pkg)
            if retval:
                # return return value
                return (call.waitOnResponse())
            # no return value -> no return

        return (method)


def initializeRemoteClasses(config, clients, calldispatcher):
    classes = {}
    # iterate over complex
    for n, d in config.items():
        # initialize RemoteClass for each complex with name, config and client
        classes[n] = RemoteClass(n, d, clients[d['client']], calldispatcher)
    return (classes)
