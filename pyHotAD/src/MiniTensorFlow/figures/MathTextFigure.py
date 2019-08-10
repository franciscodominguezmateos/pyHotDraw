#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @autor: javi
    09/03/2017
"""


import numpy as np
from math import isnan
import matplotlib as mpl
from matplotlib import figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Figures.pyHImageFigure import pyHImageFigure
from pyHotDraw.Figures.pyHAttributes import *
from MiniTensorFlow.data.operations import is_float
from matplotlib.text import Text
import numpy as np

mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
# mpl.rcParams['text.usetex'] = False

class MathTextFigure(pyHImageFigure):

    def __init__(self,
                 x0,
                 y0,
                 math_text=r'\ ',
                 font_size = 20,
                 use_latex= False,
                 non_math_text=False):

        pyHImageFigure.__init__(self, x0, y0, 0, 0)
        if bool(use_latex):
            mpl.rcParams['text.usetex'] = use_latex
            mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

        self.text = math_text
        self.imgText = None
        self._textColor = (0,0,0,255)
        self.fontSize = font_size
        self.non_math_text = non_math_text
        self.set_math_text(math_text)


    def set_math_text(self, math_text, font_size=None):
        if self.non_math_text:
            self.text = r'$\mathrm{\mathsf{' + math_text + '}}$'
        else:
            if is_float(math_text):
                self.text = r'$ {:g} $'.format(float(math_text))
            else:
                self.text = r'$ {} $'.format(math_text)

        if font_size:
            self.fontSize = float(font_size)

        self.img = pyHImage()
        self.updateFigure()

    def get_text(self):
        if self.non_math_text:
            return self.text[17:-3]
        else:
            return self.text[2:-2]


    def updateFigure(self):
        imgMT = self._createFigure()
        h, w, _ = imgMT.shape
        self.img.setData(imgMT)
        self.setImage(self.img)
        self.w = w*2
        self.h = h*2
        self.notifyFigureChanged()

    def _createFigure(self):

        fig = mpl.figure.Figure(facecolor=(0,0,0,0))
        fig.set_canvas(FigureCanvasAgg(fig))
        fig.clear()

        text = fig.suptitle(self.text, fontsize=self.fontSize)
        text.set_color(self.getTextColorNormalized())
        # obtenemos el tamaño del texto
        dpi = fig.get_dpi()

        text_bbox = text.get_window_extent(fig.canvas.get_renderer())  # in pixels
        text_widht = text_bbox.width / dpi
        text_height = text_bbox.height / dpi

        w_figure = text_widht + (float(20) / dpi) # + (float(20) / dpi) -> margenes
        h_figure = text_height + (float(20) / dpi)

        # New figure size
        fig.set_size_inches(w_figure, h_figure)

        # The position of the elements in the figure are normalized
        # 1: top - 0: bottom
        dif_height = (h_figure - text_height)
        dif_height_norm = dif_height / h_figure

        if isnan(dif_height_norm):
            text.set_y(0.1)
        else:
            text.set_y(1 - dif_height_norm / 2)


        fig.canvas.draw()

        w, h = fig.canvas.get_width_height()
        data = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8).reshape(h, w, 4)
        data = np.roll(data, 3, axis=2) # rgb to bgr (necesario por lo metodos de PyImage)
        return data


    def setFillColor(self, r, g, b, a):
        self.setAttribute('FILL', pyHAttributeFillColor(r,g,b,a))

    def getFillColor(self):
        return self.getAttribute('FILL')

    def setTextColor(self, r, g, b, a=255):
        self._textColor = (r, g, b, a)
        if self.text:
            self.updateFigure()

    def getTextColor(self):
        return self._textColor


    def getTextColorNormalized(self):
        r, g, b, a = self._textColor
        rn = round(r / 255.0, 2)
        gn = round(g / 255.0, 2)
        bn = round(b / 255.0, 2)
        an = round(a / 255.0, 2)
        return rn, gn, bn, an

    def getColor(self):
        return self.getAttribute('COLOR')


    def set_position(self, x, y):
        move_on_x = x - self.x
        move_on_y = y - self.y
        self.move(move_on_x, move_on_y)

    def setX(self, x):
        move_on_x = int(x) - self.x
        self.move(move_on_x, 0)

    def setY(self, y):
        move_on_y = int(y) - self.y
        self.move(0, move_on_y)

    def getX(self):
        return self.x0

    def getY(self):
        return self.y0

    x = property(getX, setX)
    y = property(getY, setY)



def is_math_text(text, usetex=False):
    """
    Comprueba si un texto es aceptado por la figura o no.
    :param text: String. Texto matemático (Sin usar $)
    :param usetex: Bool. Usar o no el compilador de Latex.
    :return: Bool
    """

    _, is_acceptable = Text.is_math_text(str(text), bool(usetex))
    return is_acceptable


def matrix_to_latex(matrix):
    h, w = matrix.shape
    text = ''
    for row in range(h):
        for column in range(w):
            value = matrix[row][column]
            if is_float(value):
                if int(value) - value == 0:
                    text += ' {} &'.format(int(value))
                else:
                    text += ' {:.2f} &'.format(value)
            else:
                text += ' {} &'.format(value)
        text = text[:-1] + r'\\ '
    return text[:-3]

def format_matrix(matrix):
    if isinstance(matrix, np.matrix):
        matrix = matrix_to_latex(matrix.A)
    elif isinstance(matrix, list):
        matrix = matrix_to_latex(np.array(matrix))
    elif isinstance(matrix, np.ndarray):
        matrix = matrix_to_latex(matrix)
    elif not isinstance(matrix, str):
        ValueError('Error de tipo')

    intro = r'\left( \begin{matrix} '
    end   = r' \end{matrix} \right)'
    return intro + matrix + end


def format_small_matrix(matrix):
    if isinstance(matrix, np.matrix):
        matrix = matrix_to_latex(matrix.A)
    elif isinstance(matrix, list):
        matrix = matrix_to_latex(np.array(matrix))
    elif isinstance(matrix, np.ndarray):
        matrix = matrix_to_latex(matrix)
    elif not isinstance(matrix, str):
        ValueError('Error de tipo')

    intro = r'\left( \begin{smallmatrix} '
    end = r' \end{smallmatrix} \right)'
    return intro + matrix + end
