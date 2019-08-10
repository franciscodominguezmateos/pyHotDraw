#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.pyHTranparentDecorator import pyHTransparentDecorator

GRAY = 150, 150, 150, 255

BASE_CONNECTOR = {'COLOR': GRAY,
                    'WIDTH': 2,
                    'FILL': None}

class pyHColorConnectorDecorator(pyHTransparentDecorator):

    def makeNormal(self):
        self._normal(self.getDecoratedFigure(), BASE_CONNECTOR)

    def makeSemitransparent(self):
        self._semitransparent(self.getDecoratedFigure(), BASE_CONNECTOR)

    def makeEmphasis(self):
        self._emphasis(self.getDecoratedFigure(), BASE_CONNECTOR)

