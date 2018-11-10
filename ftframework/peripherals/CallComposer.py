#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


def composeCalls(cls):
    # initialize fresh dict
    calls = {}
    # iterate over all parents and the class itself
    for c in list(cls.__bases__) + [cls]:
        # check whether attribute is available
        if hasattr(c, 'calls'):
            # update calls
            calls.update(c.calls)
    # set calls in class
    cls.calls = calls
    # return class
    return (cls)
