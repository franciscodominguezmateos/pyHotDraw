#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.pyHADNodeConnectionFigure import pyHADNodeConnectionFigure

from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure

class pyHRemoveFiguresDecorator(pyHDecoratorFigure):

    def __init__(self, drawing, selectedFigures = None):
        pyHDecoratorFigure.__init__(self, drawing)
        self.selected_figures = selectedFigures


    def removeFigures(self):
        for f in self.selected_figures[:]:
            if self._isNode(f):
                self._removeNode(f)
            elif self._isConnector(f):
                self._removeConnector(f)
            else:
                self.getDecoratedFigure().removeFigure(f)
        self.selected_figures = []

    def _removeNode(self, node):
        inputs_connectors = node.get_inputs_links()
        outputs_connectors = node.get_outputs_links()
        for ic in inputs_connectors[:]:
            self._removeConnector(ic)

        for oc in outputs_connectors[:]:
            self._removeConnector(oc)

        self.getDecoratedFigure().removeFigure(node)
        self.getDecoratedFigure().view.unSelectFigure(node)

    def _removeConnector(self, connector):
        start_node = connector.get_start_node()
        end_node = connector.get_end_node()
        start_node.remove_output_link(connector)
        end_node.remove_input_link(connector)

        self.getDecoratedFigure().removeFigure(connector)
        v = self.getDecoratedFigure().view
        v.unSelectFigure(connector)

    def _isNode(self, f):
        return isinstance(f, NodeFigure)

    def _isConnector(self, f):
        return isinstance(f, pyHADNodeConnectionFigure)

