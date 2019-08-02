#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23/05/2015

@author: Francisco Dominguez
'''
from pyHRectangleFigure import pyHRectangleFigure
class pyHTextFigure(pyHRectangleFigure):
    def __init__(self,x0,y0,w,h,text="pyHotDraw",border=True):
        super(pyHTextFigure,self).__init__(x0,y0,w,h)
        self.text=text
        self.border=border
    def setText(self,text):
        self.text=text
        self.notifyFigureChanged()
    def getText(self):
        return self.text
    def draw(self,g):
        if self.border: super(pyHTextFigure,self).draw(g)
        g.drawText(self.x0,self.y0,self.w,self.h,self.text)
    #visitor method
    def visit(self,visitor):
        return visitor.visitTextFigure(self)
    