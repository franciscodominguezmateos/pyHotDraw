#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
import math
#from PyQt4.QtCore import QPointF

class pyHPoint(object): #QPointF):
    def __init__(self,x,y):
        self.setX(x)
        self.setY(y)
    def setX(self,x): self.x=float(x)
    def setY(self,y): self.y=float(y)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def distance(self,p):
        dx=self.getX()-p.getX()
        dy=self.getY()-p.getY()
        return math.sqrt(dx*dx+dy*dy)
    def __sub__(self,p):
        return pyHPoint(self.getX()-p.getX(),self.getY()-p.getY())
    def __add__(self,p):
        return pyHPoint(self.getX()+p.getX(),self.getY()+p.getY())