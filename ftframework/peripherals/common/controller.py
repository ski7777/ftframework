#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


def getControllers(controllerconfigs):
    # initialize new dict for the controllers
    controllers = {}
    while True:
        # get dict of uninitialized controllers
        pending = dict([(n, c) for n, c in controllerconfigs.items() if n not in controllers])
        # if this is empty -> leave the loop
        if len(pending) == 0:
            break
        # iterate over pending controllers
        for n, c in pending.items():
            # jump to next if master not initialized yet
            if 'master' in c:
                if c['master'] not in controllers:
                    continue

            # get controller type
            controllertype = c['config']['type']
            # write controller config in new dict
            controllers[n] = c

            # choose between controller types
            if controllertype == 'txt':
                # TXT: just initialize
                from ftrobopy import ftrobopy
                controllers[n]['controller'] = ftrobopy(c['host'])

            elif controllertype == 'robointerface':
                # Robo Interface
                from ftifpy import ftifpy
                # initialize master controller
                controllers[n]['mastercontroller'] = ftifpy()
                # get master
                controllers[n]['controller'] = controllers[n]['mastercontroller'].roboif()
            elif controllertype == 'roboextension':
                # Robo Entension
                # get the extension from the master
                controllers[n]['controller'] = controllers[c['master']]['mastercontroller'].roboif(c['id'])

            elif controllertype == 'tx':
                # Robo TX Controller
                from fttxpy import fttxpy
                # initialize master controller
                controllers[n]['mastercontroller'] = fttxpy()
                # get master
                controllers[n]['controller'] = controllers[n]['mastercontroller'].robotx()
            elif controllertype == 'txextsion':
                # Robo TX Controller Extension
                # get the extension from the master
                controllers[n]['controller'] = controllers[c['master']]['mastercontroller'].robotx(c['id'])
    # return controllers
    return (controllers)
