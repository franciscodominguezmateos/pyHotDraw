#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/07/2019

@author: Francisco Dominguez
'''
from math import cos,sin,pi
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Figures.pyHPolylineFigure import pyHPolylineFigure

class pyHStarFigure(pyHPolylineFigure):
    '''
    classdocs
    '''
    def __init__(self,x,y,ri,ro,n=5):
        '''
        x,y= star center position
        ri= inner radious
        r0= outter radius
        n = number of tips
        '''
        pyHPolylineFigure.__init__(self)
        self.ri=ri
        self.ro=ro
        self.n=n
        self.x=x
        self.y=y
        self.fill()
        
    def fill(self):
        for i in range(2*self.n+1):
            a=pi/self.n*i
            xs=cos(a+pi/2)# first tip start at 90 degrees i mean poining up
            ys=sin(a+pi/2)
            if i%2==0:
                xs*=self.ro
                ys*=self.ro
            else:
                xs*=self.ri
                ys*=self.ri
            p=pyHPoint(self.x+xs,self.y+ys)
            self.addPoint(p)
            
    def containPoint(self,p):
        return self.getDisplayBox().contains(p)
        
