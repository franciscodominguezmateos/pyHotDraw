#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure

class SocketList(pyHCompositeFigure):

    def setPositions(self, connectors):
        for f, c in zip(self.getFigures(), connectors):
            f.set_socket_position(c)

    def sockets(self):
        return self.getFigures()

    def getSocket(self, s):
        for f in self.getFigures():
            if f is s:
                return f

    def addChangedFigureObserver(self, fo):
        for f in self.getFigures():
            f.changedFigureObservers.append(fo)

    def notifyFigureChanged(self):
        for f in self.getFigures():
            f.notifyFigureChanged()

