#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


class BeltBidirectional:
    # this class provides a basic two-way belt
    def __init__(self, motor):
        # motor must be a motor-like object
        self.outer = motor
        # stop Belt
        self.stop()

    def setSpeed(self, speed):
        # this function set the speed of the belt
        # values for speed are in range -512 to 512
        self.outer.setSpeed(speed)

    def stop(self):
        # this function stops the belt
        self.outer.stop()


class BeltUnidirectional:
    # this class provides a basic one-way belt
    def __init__(self, output):
        # output must be an output-like object
        self.outer = output
        # stop Belt
        self.stop()

    def setSpeed(self, speed):
        # this function set the speed of the belt
        # values for speed are in range 0 to 512
        self.outer.setLevel(speed)

    def stop(self):
        # this function stops the belt
        self.outer.setLevel(0)


class BeltStopSensor:
    # this class is an addition to BeltBidirectional and BeltUnidirectional
    # it provides a stop sensor and function for easy integration
    def __init__(self, input, invert=False):
        # input must be an input-like object
        # set invert if the state of input is normally True
        self.stopsensor = input
        self.invert = invert

    def getStopsensor(self):
        # this function returns the state of the input
        return(self.invert != self.stopsensor.state())

    def moveToSensor(self, speed):
        # this function starts the belt at the given speed and
        # stops when the sensor gets triggered
        # allowed values for speed depend on the belt type

        # start belt
        self.setSpeed(speed)
        # check sensor
        while not getStopsensor():
            # stay in loop
            pass
        # now the sensor was triggered
        # stop belt
        self.stop()


class BeltImpulseSensor(BeltBidirectional):
    # this class is an addition to BeltBidirectional
    # it provides an impulse sensor and function for easy integration
    def __init__(self, motor):
        # motor must be a motor-like object
        # initialize BeltBidirectional
        BeltBidirectional.__init__(self, motor)

    def getMoveFinished(self):
        # this function returns whether the move is finished
        return(self.outer.finished())

    def getCurrentDistance(self):
        # this function returns the current distance
        return(self.outer.getCurrentDistance())

    def moveDistance(self, speed, distance, wait=False):
        # this function moves the belt for a given distance
        # values for speed are in range -512 to 512
        # distance is the distance in encoder steps
        # if wait is True the funtion will wait until the belt stopped
        # in this case the function will clean up the motor
        # if wait is False (default) you need to clean up after the move

        # set motor distance
        self.outer.setDistance(distance)
        # set motor speed
        self.setSpeed(speed)
        # check whether wait is set
        if wait:
            # wait is set
            # check move finished
            while not self.getMoveFinished():
                # stay in loop
                pass
            # stop implies that we stop the belt here. This is done automatically
            # this is just to it up
            self.stop()
        # either wait is unset or we are done. So we can just leave
