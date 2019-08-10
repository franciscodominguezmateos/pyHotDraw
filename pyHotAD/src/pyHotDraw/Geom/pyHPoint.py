#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco, edited by Javi
'''
import math

class pyHPoint:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def distance(self, p):
        dx=self._x-p.getX()
        dy=self._y-p.getY()
        return math.sqrt(dx*dx+dy*dy)

    x = property(getX, setX)
    y = property(getY, setY)

    def __repr__(self):
        return '({}, {})'.format(self._x, self._y)