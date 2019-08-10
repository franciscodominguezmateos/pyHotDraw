#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.AbstractBackwardStep import AbstractBackwardStep


class BackwardEndNodeStep(AbstractBackwardStep):
    def __init__(self, node, outLine, view):
        AbstractBackwardStep.__init__(self, node, view)
        self.out_line_figure = outLine


    def step0(self):
        """
        Vuelve opacos el nodo sobre el que se mostrará la información, así como sus
        nodos salida (y sus respectivos conectores)
        """
        self.makeNodeEnphasis(self.node)
        self.makeConnectorEnphasis(self.out_line_figure)

    def endStep(self):
        self.makeNodeOpaque(self.node)
        self.makeConnectorOpaque(self.out_line_figure)