#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 01/04/2017
@author: javi
"""

class pyHDecoratorTool(object):
    """
    Design Patter Decorator for Tools
    """
    def __init__(self, decorated):
        """
        Constructor
        """
        self.decorated=decorated

    def getDecoratedTool(self):
        return self.decorated

    def setDecoratedTool(self,f):
        self.decorated=f

    def onMouseDown(self, e):
        self.decorated.onMouseDown(e)

    def onMouseUp(self, e):
        self.decorated.onMouseUp(e)

    def onMouseMove(self, e):
        self.decorated.onMouseMove(e)

    def onMouseDobleClick(self, e):
        self.decorated.onMouseDobleClick(e)

    def onMouseWheel(self, e):
        self.decorated.onMouseWheel(e)

    def onKeyPressed(self, e):
        self.decorated.onKeyPressed(e)
