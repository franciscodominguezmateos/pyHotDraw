#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.pyHTranparentDecorator import pyHTransparentDecorator

BLACK = (0, 0, 0, 255)
BLUE = (187, 198, 221, 255)
GREEN = (189, 221, 187, 255)
GRAY = (220, 220, 220, 255)
DARK_BLUE = (127, 135, 151, 255)
DARK_GREEN = (136, 159, 135, 255)
DARK_GRAY = (170, 170, 170, 255)

NORMAL_INPUT = {'COLOR': DARK_GRAY, 'FILL': GRAY, 'WIDTH': 3}
NORMAL_WEIGHT = {'COLOR': DARK_GREEN, 'FILL': GREEN, 'WIDTH': 3}
NORMAL_NODE = {'COLOR': DARK_BLUE, 'FILL': BLUE, 'WIDTH': 3}
NORMAL_TEXT = {'COLOR': BLACK}

class pyHColorNodeDecorator(pyHTransparentDecorator):

    def makeNormal(self):
        f = self.getDecoratedFigure()
        if f.is_input():
            if f.isWeight():
                self._normal(f.getFigures()[0], NORMAL_WEIGHT)
            else:
                self._normal(f.getFigures()[0], NORMAL_INPUT)
        else:
            self._normal(f.getFigures()[0], NORMAL_NODE)
        f.getFigures()[1].setTextColor(*NORMAL_TEXT.get('COLOR'))


    def makeSemitransparent(self):
        f = self.getDecoratedFigure()
        if f.is_input():
            if f.isWeight():
                self._semitransparent(f.getFigures()[0], NORMAL_WEIGHT)
            else:
                self._semitransparent(f.getFigures()[0], NORMAL_INPUT)
        else:
            self._semitransparent(f.getFigures()[0], NORMAL_NODE)
        r, g, b, _ = NORMAL_TEXT.get('COLOR')
        f.getFigures()[1].setTextColor(r, g, b, 100)

    def makeEmphasis(self):
        f = self.getDecoratedFigure()
        if f.is_input():
            if f.isWeight():
                self._emphasis(f.getFigures()[0], NORMAL_WEIGHT)
            else:
                self._emphasis(f.getFigures()[0], NORMAL_INPUT)
        else:
            self._emphasis(f.getFigures()[0], NORMAL_NODE)
        f.getFigures()[1].setTextColor(*NORMAL_TEXT.get('COLOR'))


