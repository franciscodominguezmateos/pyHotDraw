#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.MathTextFigure import MathTextFigure
from MiniTensorFlow.figures.MatrixFigure import MatrixFigure
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHAttributes import *
import numpy as np





class MathExpressionFigure(pyHCompositeFigure):

    def set_position(self, x, y):
        move_on_x = x - self.get_x()
        move_on_y = y - self.get_y()
        for figure in self.getFigures():
            figure.move(move_on_x, move_on_y)


    def get_x(self):
        box = self.getDisplayBox()
        return box.getX()

    def get_y(self):
        box = self.getDisplayBox()
        return box.getY()

    def get_w(self):
        box = self.getDisplayBox()
        return box.getWidth()

    def get_h(self):
        box = self.getDisplayBox()
        return box.getHeight()

    x = property(get_x)
    y = property(get_y)
    w = property(get_w)
    h = property(get_h)

def equal_expression(x,
                     y,
                     left_of_equal,
                     right_of_equal,
                     horizontal_margin=0,
                     vertical_margin=0):
    """
        Generate a matematical expression figure like this:
        left_of_equal = right_of_equal
    :param x:
    :param y:
    :param left_of_equal:
    :param right_of_equal:
    :param horizontal_margin:
    :param vertical_margin:
    :return:
    """
    if not isinstance(left_of_equal, (list, tuple)):
        left_of_equal = [left_of_equal]

    if not isinstance(right_of_equal, (list, tuple)):
        right_of_equal = [right_of_equal]


    fl_left, sw_left, mh_left = _create_figures(left_of_equal)
    fl_right, sw_right, mh_right = _create_figures(right_of_equal)
    equal = MathTextFigure(x, y, ' = ')

    figure_list = fl_left + [equal] + fl_right
    sum_width = sw_left + equal.w + sw_right
    max_height = max(mh_left, equal.h, mh_right)

    half_horizontal_margin = horizontal_margin / 2 if horizontal_margin > 0 else 0
    half_vertical_margin = vertical_margin / 2 if vertical_margin > 0 else 0
    expression_figure = _create_expresion_figure(x + half_horizontal_margin,
                                                 y + half_vertical_margin,
                                                 figure_list, max_height)

    conteiner = _create_conteiner_figure(x, y, sum_width, max_height,
                                         horizontal_margin, vertical_margin)
    expression_figure.figures.insert(0, conteiner)

    return expression_figure

def _create_figures(list_of_math_text):
    figure_list = []
    sum_widths = 0
    max_height = 0

    for text in list_of_math_text:
        matrix_types = (list, np.ndarray, np.matrix)
        if isinstance(text, matrix_types) and _size(text) > 1:
            figure = MatrixFigure(0, 0, text)
        else:
            figure = MathTextFigure(0, 0, text)
        print(figure.w, ' ', figure.h)
        figure_list.append(figure)
        max_height = max(max_height, figure.h)
        sum_widths += figure.w

    return figure_list, sum_widths, max_height


def _create_expresion_figure(start_x, start_y, figure_list, max_height):
    expression_figure = MathExpressionFigure()
    for figure in figure_list:
        figure.setX(start_x)
        start_x += figure.w
        figure.setY(start_y + (max_height - figure.h)/2)
        _set_border_and_background_transparent(figure)
        expression_figure.addFigure(figure)
    return expression_figure

def _create_conteiner_figure(x, y, w, h, hm, vm):
    rec = pyHRectangleFigure(x, y, w + hm, h + vm)
    rec.setAttribute('FILL', pyHAttributeFillColor(255, 255, 255, 255))
    return rec


def _set_border_and_background_transparent(figure):
    """
    Oculta el borde y el color de fondo de la figura.
    :param figure:
    :return:
    """
    figure.setAttribute('COLOR', pyHAttributeColor(0, 0, 0, 0))
    figure.setAttribute('FILL', pyHAttributeFillColor(0, 0, 0, 0))


def _size(matrix):
    if isinstance(matrix, list):
        return _size_of_list(list)
    elif isinstance(matrix, (np.matrix, np.ndarray)):
        return matrix.size
    else:
        return 0

def _size_of_list(l):
    if isinstance(l, list):
        return sum(_size_of_list(sub_list) for sub_list in l)
    else:
        return 1
