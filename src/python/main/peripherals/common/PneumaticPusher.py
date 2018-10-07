#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


class PneumaticPusher:
    # this class provides a simple pneumatic pusher
    def __init__(self, output, invert=False, maxlevel=512):
        # outer must be an output-like object
        # set invert if output is inverted
        # maxlevel is the maximum level ot the output
        self.outer = output
        self.invert = invert
        self.maxlevel = maxlevel
        # initialize position
        self.setPos(False)

    def setPos(self, pos):
        # set output according to new position, invertion and maxlevel
        # pos != self.invert returns True if it´s (non-inverting and pos is True)
        # (or inverting and pos False)
        # multiplying this by maxlevel returns the output level
        self.outer.setLevel((pos != self.invert) * self.maxlevel)
