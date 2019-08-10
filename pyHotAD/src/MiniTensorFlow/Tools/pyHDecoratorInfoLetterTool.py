#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 01/04/2017
@author: javi
"""

from MiniTensorFlow.Tools.pyHDecoratorTool import pyHDecoratorTool

from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure

class pyHDecoratorInfoLetterTool(pyHDecoratorTool):
    """
    Provides functions to show the content of nodes in different ways
    """
    def __init__(self, tool):
        pyHDecoratorTool.__init__(self, tool)

    # Solo letra
    def showInfoFunctionLetter(self):
        pass

    # Ventana creacion
    def showInfoFunctionType(self):
        for f in self.getDecoratedTool().getView().getDrawing().getFigures():
            if isinstance(f, NodeFigure) and not f.is_input():
                op = f.get_operation()
                f.set_text(op)

    # Letra de funcion + Tipo de funcion (subindice)
    def showInfoHybrid(self):
        for f in self.getDecoratedTool().getView().getDrawing().getFigures():
            if isinstance(f, NodeFigure) and not f.is_input():
                letter = f.get_function_letter()
                op = f.get_operation()
                text = letter + '_{_{' + op + '}}'
                f.set_text(text)