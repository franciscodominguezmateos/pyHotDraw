#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
import math
from PyQt5.QtCore import QPointF

class pyHPoint(QPointF):
    def getX(self):
        return self.x()
    def getY(self):
        return self.y()
    def distance(self,p):
        dx=self.x()-p.getX()
        dy=self.y()-p.getY()
        return math.sqrt(dx*dx+dy*dy)
    def __sub__(self,p):
        return pyHPoint(self.getX()-p.getX(),self.getY()-p.getY())
    def __add__(self,p):
        return pyHPoint(self.getX()+p.getX(),self.getY()+p.getY())