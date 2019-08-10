#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from PyQt5 import QtGui, QtCore, QtWidgets
from pyHotDraw.Core.Qt.pyHStandardView import pyHStandardView
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure
from collections import deque
from copy import deepcopy

_MAX_STATES = 10
class StandardView(pyHStandardView):

    def __init__(self, e):
        pyHStandardView.__init__(self, e)
        self._undo = deque(maxlen=_MAX_STATES)
        self._redo = deque(maxlen=_MAX_STATES)


    def selectFigure(self,figure, show_handles=True, show_displaybox=True):
        self.selectedFigures.addFigure(figure)


    def draw(self,g):
        self.drawGrid(g)
        self.drawing.draw(g)
        for f in self.getSelectedFigures():
            for h in f.getHandles():
                h.draw(g)


        # if selectedForShowHanddles(): draw handdles

    def actual_state(self):
        """
        Realiza una copia del draw actual
        :return:
        """
        draw = self.getDrawing()
        draw.view = None
        draw.changedDrawingObservers.clear()

        draw_copy = deepcopy(draw)

        draw.view = self
        draw.addChangedDrawingObserver(self)

        draw_copy.view = self
        return draw_copy

    def save_actual_state(self):
        """
        Guarda una copia del estado actual para poder volver a ella
        en un futuro.
        :return:
        """
        self.save_state( self.actual_state() )

    def save_state(self, state):
        """ Guarda un estado obtenido mediante el método actual_state"""
        self._undo.append(state)
        self._redo.clear()

    def undo(self):
        """
        Cambia el dibujo por un dibujo de un estado anterior
        :return:
        """
        if self._undo:
            self.clearSelectedFigures()
            actual_state = self.actual_state()
            self._redo.append(actual_state)
            old_state = self._undo.pop()
            self.setDrawing(old_state)

    def redo(self):
        """
        Cambia el dibujo por un dibujo que había estado presente antes.
        :return:
        """
        if self._redo:
            self.clearSelectedFigures()
            actual_state = self.actual_state()
            new_state = self._redo.pop()
            self._undo.append(actual_state)
            self.setDrawing(new_state)


