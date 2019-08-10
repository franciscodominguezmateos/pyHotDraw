#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.MatrixFigure import MatrixFigure
from pyHEllipseFigure import pyHEllipseFigure

class ButtonForMatrix(pyHEllipseFigure):

    def __init__(self, data=None):
        pyHEllipseFigure.__init__(self, 0, 0, 50, 30)
        self._data = data
        self._open = False
        self._matrix_figure = None


    def are_opened(self):
        return self._open


    def check_data(self, data):
        return data == self._data


    def open(self):
        self._open = True


    def close(self):
        self._open = False


    def set_position(self, x, y):
        move_on_x = x - self._matrix_figure.x
        move_on_y = y - self._matrix_figure.y
        self._matrix_figure.move(move_on_x, move_on_y)


    def draw(self,g):
        pyHEllipseFigure.draw(self, g)
        if self._open:
            self._check_matrix()
            self._matrix_figure.draw(g)


    def _check_matrix(self):
        if self._matrix_figure:
            data = self._matrix_figure.get_data()
            if data != self._data:
                x = self._matrix_figure.x
                y = self._matrix_figure.y
                self._matrix_figure = MatrixFigure(x, y, self._data)
        else:
            self._matrix_figure = MatrixFigure(0, 0, self._data)