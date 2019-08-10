#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: javi
"""
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor, pyHAttributeFillColor
from figures.MathTextFigure import MathTextFigure
from format_values import *
from pyHPoint import pyHPoint


class InfoHandle(object):

    def __init__(self, owner, position, info, color):
        self.owner=owner
        self._position = position
        self.handle_point = pyHPoint(*self._position_handle())
        self.handle_figure = pyHRectangleFigure(self.handle_point.getX() - 1,
                                                self.handle_point.getY() - 1,
                                                20, 20)
        self._set_color(color)
        self._info = info



    #Figure methods
    def containPoint(self,p):
        return self.handle_figure.containPoint(p)

    def draw(self,g):
        self.handle_figure.draw(g)



    #Tool methods
    def onMouseDown(self, e):
        print(self)
        if self.owner.get_info_dic(self._info) is None:
            info = self.owner.generate_info(self._info)
            if info is not None:
                info_fig = MathTextFigure(0, 0, format_value(info), 18, True)
                info_fig.set_position(*self._position_info(info_fig))
                info_fig.setFillColor(255,255,255,255)
                self.owner.set_info_dic(self._info, info_fig)
        else:
            self.owner.set_info_dic(self._info, None)

    def onMouseUp(self,e):
        pass

    def onMouseMove(self,e):
        pass

    def onMouseDobleClick(self,e):
        pass

    def onMouseWheel(self,e):
        pass

    def onKeyPressed(self,e):
        pass


    def _set_color(self, c):
        if c == 'red':
            color = pyHAttributeColor(141, 38, 38, 255)
            fill = pyHAttributeFillColor(232, 61, 61, 255)
        elif c == 'blue':
            color = pyHAttributeColor(0, 76, 153, 255)
            fill = pyHAttributeFillColor(0, 128, 255, 255)
        elif c == 'gray':
            color = pyHAttributeColor(170, 170, 170, 255)
            fill = pyHAttributeFillColor(220, 220, 220, 255)
        else:
            raise ValueError('bad color selected')

        self.handle_figure.setAttribute('COLOR', color)
        self.handle_figure.setAttribute('FILL', fill)

    def _position_handle(self):
        r = self.owner.getDisplayBox()
        x = r.getX()
        y = r.getY()
        w = r.getWidth()
        h = r.getHeight()

        if self._position == 'noroeste':
            return x-20, y + h
        elif self._position == 'noreste':
            return x + w, y + h
        elif self._position == 'suroeste':
            return x - 20, y - 20
        elif self._position == 'sureste':
            return x + w, y - 20

    def _position_info(self, info):
        x, y = self._position_handle()
        w = info.w
        h = info.h

        if self._position == 'noroeste':
            return x - 20 -w , y + 20
        elif self._position == 'noreste':
            return x + 40, y + 40
        elif self._position == 'suroeste':
            return x - 20 - w, y - 20 - h
        elif self._position == 'sureste':
            return x + 40, y - 20 - h

    def __repr__(self):
        return 'InfoHandle {}, {}, {}'.format(self._position, self._info,
                                              self.owner.getDecoratedFigure())