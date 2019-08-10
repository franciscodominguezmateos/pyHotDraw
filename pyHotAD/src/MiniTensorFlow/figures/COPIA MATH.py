#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @autor: javi
    09/03/2017
"""


import numpy as np
import matplotlib as mpl
from matplotlib import figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Figures.pyHImageFigure import pyHImageFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeFillColor

class pyHMathTextFigure(pyHImageFigure):

    def __init__(self, x0, y0):
        pyHImageFigure.__init__(self, x0, y0, 0, 0)
        self.text = None
        self.imgText = None
        self.fontSize = 40
        #self.fillColor = (1, 1, 1, 0)

    def setText(self, mathTex, fontSize = 30):
        self.text = r'$' + str(mathTex) + '$'
        self.fontSize = float(fontSize)
        self.img = pyHImage()
        """
        if color:
            if len(color) is 3:
                r, g, b = color
                a = 0
            else:
                r, g, b, a = color
            self.fillColor = (float(r)/255, float(g)/255, float(b)/255, float(a)/255)

        """
        self.updateFigure()

    def getText(self):
        return self.text[1:-1]


    def setFillColor(self, r,g,b,a):
        self.setAttribute('FILL', pyHAttributeFillColor(r, g, b, a))

    # return rgb color
    def getFillColor(self):
        return self.attributes.get('FILL')


    def updateFigure(self):
        imgMT, w, h = self._createFigure()
        self.img.setData(imgMT)
        self.setImage(self.img)
        self.w = w*2
        self.h = h*2

    def _createFigure(self):

        fig = mpl.figure.Figure(edgecolor = (0,0,0,1), facecolor=(0,0,0,0)) #  color fondo
        fig.set_canvas(FigureCanvasAgg(fig))
        fig.clear()

        text = fig.suptitle(self.text, fontsize=self.fontSize)
        # text.set_color('k'/(1,1,1,1))  # text color

        # obtenemos el tamaño del texto
        dpi = fig.get_dpi()

        text_bbox = text.get_window_extent(fig.canvas.get_renderer())  # in pixels
        text_widht = text_bbox.getWidth / dpi
        text_height = text_bbox.getHeight / dpi

        w_figure = text_widht + (float(20) / dpi) # + (float(20) / dpi) -> margenes
        h_figure = text_height + (float(20) / dpi)

        # New figure size
        fig.set_size_inches(w_figure, h_figure)

        # The position of the elements in the figure are normalized
        # 1: top - 0: bottom
        dif_height = (h_figure - text_height)
        dif_height_norm = dif_height / h_figure

        text.set_y(1 - dif_height_norm / 2)

        fig.canvas.draw()

        w, h = fig.canvas.get_width_height()
        data = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8).reshape(h, w, 4)
        data = np.roll(data, 3, axis=2) # rgb to bgr (necesario por lo metodos de PyImage)
        return data, w, h
