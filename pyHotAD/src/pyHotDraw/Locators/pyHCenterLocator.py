#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 30/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHCenterLocator(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def locate(self,figure):
        r=figure.getDisplayBox()
        return pyHPoint(r.getX()+r.getWidth()/2,r.getY()+r.getHeight()/2)