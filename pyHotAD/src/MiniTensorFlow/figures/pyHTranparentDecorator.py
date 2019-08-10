#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor, pyHAttributeFillColor, pyHAttributeWidth

BLACK = (0,0,0,255)
SEMI_BLACK = (75, 75, 75, 255)
class pyHTransparentDecorator(pyHDecoratorFigure):

    def __init__(self, figure):
        pyHDecoratorFigure.__init__(self, figure)


    def makeSemitransparent(self):
        #self.getDecoratedFigure().setAttribute('WIDTH', pyHAttributeWidth(1))
        if self.getDecoratedFigure().getColor():
            r, g, b, _ = self.getDecoratedFigure().getColor().values()
            self.getDecoratedFigure().setColor(pyHAttributeColor(r, g, b, 100))
        if self.getDecoratedFigure().getFillColor():
            r, g, b, _ = self.getDecoratedFigure().getFillColor()
            self.getDecoratedFigure().setFillColor(r, g, b, 100)


    def makeNormal(self):
        #self.getDecoratedFigure().setAttribute('WIDTH', pyHAttributeWidth(1))
        if self.getDecoratedFigure().getColor():
            r, g, b, _ = self.getDecoratedFigure().getColor().values()
            self.getDecoratedFigure().setColor(pyHAttributeColor(r, g, b, 255))
        if self.getDecoratedFigure().getFillColor():
            r, g, b, _ = self.getDecoratedFigure().getFillColor()
            self.getDecoratedFigure().setFillColor(r, g, b, 255)

    def makeEmphasis(self):
        self.makeNormal()
        #self.getDecoratedFigure().setAttribute('WIDTH', pyHAttributeWidth(3))

    @staticmethod
    def _normal(figure, attribs_dict):
        width = attribs_dict.get('WIDTH')
        color = attribs_dict.get('COLOR')
        fill = attribs_dict.get('FILL')
        if width: figure.setAttribute('WIDTH', pyHAttributeWidth(width))
        if color: figure.setAttribute('COLOR', pyHAttributeColor(*color))
        if fill:  figure.setAttribute('FILL', pyHAttributeFillColor(*fill))

    def _emphasis(self, figure, attribs_dict):
        self._normal(figure, attribs_dict)
        if attribs_dict.get('COLOR'):
            figure.setAttribute('COLOR', pyHAttributeColor(*SEMI_BLACK))

        width = attribs_dict.get('WIDTH') + 1
        if width: figure.setAttribute('WIDTH', pyHAttributeWidth(width))

    def _semitransparent(self, figure, attribs_dict):
        self._normal(figure, attribs_dict)
        width = attribs_dict.get('WIDTH') - 1
        color = attribs_dict.get('COLOR')
        fill = attribs_dict.get('FILL')
        if width:
            figure.setAttribute('WIDTH', pyHAttributeWidth(width))
        if color:
            r, g, b, _ = color
            figure.setAttribute('COLOR', pyHAttributeColor(r, g, b, 100))
        if fill:
            r, g, b, _ = fill
            figure.setAttribute('FILL', pyHAttributeFillColor(r, g, b, 100))

