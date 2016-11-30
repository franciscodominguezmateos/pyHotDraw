#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 22/11/2013
Visit all figures in order to create a string with its PLT file format

@author: paco
'''
class pyHPLTGenerator:
    def __init__(self):
        self.pointsUnit=40
    def visitPolylineFigure(self,plf):
        points=plf.getPoints()
        p=points[0]
        s="PU%.2f,%.2f;\n" % (p.getX()*self.pointsUnit,p.getY()*self.pointsUnit)
        for p in points[1:]:
            s+="PD%.2f,%.2f;\n" % (p.getX()*self.pointsUnit,p.getY()*self.pointsUnit)
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