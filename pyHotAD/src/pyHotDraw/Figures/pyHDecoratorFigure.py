#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 29/03/2013

@author: paco
'''

class pyHDecoratorFigure(object):
    '''
    Design Patter Decorator for figures
    '''
    def __init__(self,decorated):
        '''
        Constructor
        '''
        self.decorated=decorated
    def getDecoratedFigure(self):
        return self.decorated
    def setDecoratedFigure(self,f):
        self.decorated=f
    def draw(self,g):
        self.decorated.draw(g)
    def move(self,x, y):
        self.decorated.move(x, y)
    def containPoint(self,p):
        self.decorated.containPoint(p)
    def getDisplayBox(self):
        return self.decorated.getDisplayBox()
    def setDisplayBox(self,r):
        self.decorated.setDisplayBox(r)
    #visitor method
    def visit(self,visitor):
        return visitor.visitDecoratorFigure(self)
    
class pyHArrowDecoratorFigure(pyHDecoratorFigure):
    def __init__(self,decorated):
        #Must be a Polyline or have a getLastPoint method
        pyHDecoratorFigure.__init__(self,decorated)
    def draw(self,g):
        pyHDecoratorFigure.draw(self, g)
        #Draw a arrow
        p=self.decorated.getLastPoint()
        g.drawEllipse(p.getX(),p.getY(),10,10)
        
