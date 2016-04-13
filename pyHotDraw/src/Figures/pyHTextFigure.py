#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23/05/2015

@author: paco
'''
from pyHRectangleFigure import pyHRectangleFigure
class pyHTextFigure(pyHRectangleFigure):
    def __init__(self,x0,y0,w,h,text="pyHotDraw"):
        super(pyHTextFigure,self).__init__(x0,y0,w,h)
        self.text=text
    def setText(self,text):
        self.text=text
        self.notifyFigureChanged()
    def getText(self):
        return self.text
    def draw(self,g):
        super(pyHTextFigure,self).draw(g)
        #pyHAbstractFigure.draw(self,g)
        g.drawText(self.x0,self.y0,self.w,self.h,self.text)
    #visitor method
    def visit(self,visitor):
        return visitor.visitTextFigure(self)
    