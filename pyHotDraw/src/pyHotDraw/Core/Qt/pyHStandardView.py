#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 25/03/2013

@author: paco
'''              
import math
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtCore import Qt
from pyHotDraw.Core.pyHAbstractView import pyHAbstractView
from pyHotDraw.Core.pyHStandardEvent import pyHStandardEvent
from pyHStandardGraphic import pyHStandardGraphic

class pyHStandardView(pyHAbstractView,QtWidgets.QWidget):
    def __init__(self,e):      
        parent=None
        QtWidgets.QWidget.__init__(self)
        pyHAbstractView.__init__(self,e)
        #self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #self.setMouseTracking(True)
        self.initUI()
    def initUI(self):      
        self.setMinimumSize(1, 30)     
    def paintEvent(self, e):     
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        g=pyHStandardGraphic(qp,self)
        pyHAbstractView.draw(self,g)
        qp.end()
    def update(self):
        super(pyHStandardView, self).update()

#Platform specific mouse and key manipulation see any pyHStandardGraphic.py  
    def getPyHButton(self,event):  
        if event.button() == QtCore.Qt.LeftButton:
            return pyHStandardEvent.LeftButton
        if event.button() == QtCore.Qt.RightButton:
            return pyHStandardEvent.RightButton
        if event.button() == QtCore.Qt.MiddleButton:
            return pyHStandardEvent.MiddleButton
    def mousePressEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        #x=math.floor(x/1)*1
        #y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y,self.getPyHButton(event))
        self.editor.getCurrentTool().onMouseDown(e)
        self.editor.sb.setText("[x%0.2f] %0.0f,%0.0f - %0.2f,%0.2f" % (t.sx,event.x(),event.y(),e.getX(),e.getY()))
        self.update()
        
    def mouseReleaseEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        #x=math.floor(x/1)*1
        #y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y,self.getPyHButton(event))
        self.editor.getCurrentTool().onMouseUp(e)
        self.update()
             
    # this seem to be drag    
    def mouseMoveEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        #x=math.floor(x/1)*1
        #y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y,self.getPyHButton(event))
        self.editor.getCurrentTool().onMouseMove(e)
        self.editor.sb.setText("[x%0.2f] %0.0f,%0.0f - %0.2f,%0.2f" % (t.sx,event.x(),event.y(),e.getX(),e.getY()))
        self.update()
        
    def mouseDoubleClickEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        #x=math.floor(x/1)*1
        #y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y,self.getPyHButton(event))
        self.editor.getCurrentTool().onMouseDobleClick(e)
        self.editor.sb.setText("[x%0.2f] %0.0f,%0.0f - %0.2f,%0.2f" % (t.sx,event.x(),event.y(),e.getX(),e.getY()))
        self.update()

    def wheelEvent(self,event):
        h=self.height()
        t=self.getTransform()
        ex,ey=event.x(),h-event.y()
        x,y=t.itransform(event.x(),h-event.y())
        e=pyHStandardEvent(x,y)
        #.delta() is -120 or 120
        d=event.delta()/1200.0
        #mag=int(math.log10(t.sx))
        #t.sx+=d*10**mag
        #t.sy+=d*10**mag
        t.sx+=d*t.sx
        t.sy+=d*t.sy
        xm,ym=t.transform(x,y)
        t.tx-=xm-ex
        t.ty-=ym-ey
        print "ts",t.sx,t.sy,t.tx,t.ty,event.delta()
        self.editor.sb.setText("[x%0.2f] %0.0f,%0.0f - %0.2f,%0.2f" % (t.sx,event.x(),event.y(),e.getX(),e.getY()))
        self.update()
        
    def keyPressEvent(self,event):
        e=pyHStandardEvent(0,0,0,event.key())
        self.editor.getCurrentTool().onKeyPressed(e)
        self.update()

       
  



        