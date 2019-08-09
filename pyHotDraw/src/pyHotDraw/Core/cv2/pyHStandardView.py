#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 25/03/2013

@author: paco
'''              
import math
from pyHotDraw.Core.pyHAbstractView import pyHAbstractView
from pyHotDraw.Core.pyHStandardEvent import pyHStandardEvent
from pyHotDraw.Core.cv2.pyHStandardGraphic import pyHStandardGraphic

class pyHStandardView(pyHAbstractView):
    def __init__(self,e):      
        pyHAbstractView.__init__(self,e)
        self.initUI()
    def setImg(self,img):
        self.img=img
        self.graphics=pyHStandardGraphic(self,self.img)
    def width(self):
        return self.img.shape[1]
    def height(self):
        return self.img.shape[0]
    def initUI(self):      
        pass     
    def update(self):
        self.img[:]=255  
        self.draw(self.graphics)
        
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
        d=event.angleDelta().y()/1200.0
        #mag=int(math.log10(t.sx))
        #t.sx+=d*10**mag
        #t.sy+=d*10**mag
        t.sx+=d*t.sx
        t.sy+=d*t.sy
        xm,ym=t.transform(x,y)
        t.tx-=xm-ex
        t.ty-=ym-ey
        print "ts",t.sx,t.sy,t.tx,t.ty,event.angleDelta().y()
        self.editor.sb.setText("[x%0.2f] %0.0f,%0.0f - %0.2f,%0.2f" % (t.sx,event.x(),event.y(),e.getX(),e.getY()))
        self.update()
        
    def keyPressEvent(self,event):
        e=pyHStandardEvent(0,0,0,event.key())
        self.editor.getCurrentTool().onKeyPressed(e)
        self.update()

       
  



        