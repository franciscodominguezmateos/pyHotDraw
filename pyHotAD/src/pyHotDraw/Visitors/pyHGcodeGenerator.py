#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 22/11/2013
Visitors all figures in order to create a string with its G-code

@author: paco
'''
class pyHGcodeGenerator:
    def __init__(self):
        self.safeZ=5
        self.workZ=-1
        self.tableZ=0
        self.feedRate=400
    def visitPolylineFigure(self,plf):
        points=plf.getPoints()
        p=points[0]
        s="G00 Z%.2f\n" % (self.safeZ)
        s+="G00 X%.2f Y%.2f\n" % (p.getX(),p.getY())
        for p in points[1:]:
            s+="G01 X%.2f Y%.2f Z%.2f F%d\n" % (p.getX(),p.getY(),self.workZ,self.feedRate)
        return s
    def visitSplineFigure(self,spf):
        return self.visitPolylineFigure(spf)
    def visitRectangleFigure(self,rf):
        return ""
    def visitEllipseFigure(self,ef):
        return ""
    def visitArcFigure(self,af):
        return ""
    def visitCompositeFigure(self,cf):
        s=''
        for f in cf.getFigures():
            s+=f.visit(self)
        return s
    def visitConnectionFigure(self,cf):
        return ""
    def visitDecoratorFigure(self,df):
        df.getDecoratedFigure().visit(self)