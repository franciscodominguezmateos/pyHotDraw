#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 25/03/2013

@author: paco
'''              
import math
from PyQt4 import QtGui,QtCore
from pyHotDraw.Core.pyHAbstractView import pyHAbstractView
from pyHotDraw.Core.pyHStandardEvent import pyHStandardEvent
from pyHStandardGraphic import pyHStandardGraphic

class pyHStandardView(QtGui.QWidget,pyHAbstractView):
    def __init__(self,e):      
        super(pyHStandardView, self).__init__()
        pyHAbstractView.__init__(self,e)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
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
    def mousePressEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        x=math.floor(x/1)*1
        y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y)
        self.editor.getCurrentTool().onMouseDown(e)
        self.editor.sb.setText("%0.2f,%0.2f - %0.2f,%0.2f" % (event.x(),event.y(),e.getX(),e.getY()))
        self.update()
        
    def mouseReleaseEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        x=math.floor(x/1)*1
        y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y)
        self.editor.getCurrentTool().onMouseUp(e)
        self.update()
             
    # this seem to be drag    
    def mouseMoveEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        x=math.floor(x/1)*1
        y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y)
        self.editor.getCurrentTool().onMouseMove(e)
        self.editor.sb.setText("%0.2f,%0.2f - %0.2f,%0.2f" % (event.x(),event.y(),e.getX(),e.getY()))
        self.update()
        
    def mouseDoubleClickEvent(self,event):
        h=self.height()
        t=self.getTransform()
        x,y=t.itransform(event.x(),h-event.y())
        x=math.floor(x/1)*1
        y=math.ceil(y/1)*1
        e=pyHStandardEvent(x,y)
        self.editor.getCurrentTool().onMouseDobleClick(e)
        self.update()

    def wheelEvent(self,event):
        h=self.height()
        t=self.getTransform()
        ex,ey=event.x(),h-event.y()
        x,y=t.itransform(event.x(),h-event.y())
        d=event.delta()/1200.0
        mag=int(math.log10(t.sx))
        t.sx+=d*10**mag
        t.sy+=d*10**mag
        xm,ym=t.transform(x,y)
        t.tx-=xm-ex
        t.ty-=ym-ey
        print "ts",t.sx,t.sy,t.tx,t.ty
        self.update()
        
    def keyPressEvent(self,event):
        e=pyHStandardEvent(0,0,0,event.key())
        self.editor.getCurrentTool().onKeyPressed(e)
        self.update()

       
  



        