#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure

class pyHDecoratorUndoRedo(pyHDecoratorFigure):
    """ Adornar la clase drawing para que implemente las operacion redo y undo"""

    def __init__(self, draw):
        pyHDecoratorFigure.__init__(self, draw)


    def addFigure(self, f):
        """ Sobreescribe el metodo addFigure de la clase Drawing"""
        draw = self.getDecoratedFigure()
        #editor = draw.view.getEditor()
        #editor.addDrawChange(draw)
        draw.addFigure(f)