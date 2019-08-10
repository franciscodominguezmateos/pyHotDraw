#!/usr/bin/python

from MiniTensorFlow.figures.Nodes_Expanded.nodeExpandedDecorator import nodeExpandedDecorator
from MiniTensorFlow.figures.Nodes_Simples.pyHSumFigure import pyHADSumFigure
from MiniTensorFlow.figures.Nodes_Simples.pyHWeightFigure import pyHADWeightFigure

from MiniTensorFlow.figures.Nodes.mulNodeFigure import mulNodeFigure


class abstractComplexNodeFigure(nodeExpandedDecorator):

    def createInternalNet(self):
        W = pyHADWeightFigure(0, 0, 130, 130)
        Mul = mulNodeFigure(0, 0, 130, 130)
        b = pyHADWeightFigure(0, 0, 130, 130)
        Sum = pyHADSumFigure(0, 0, 130, 130)

        self.createConnection(W, Mul, 0)
        self.createConnection(Mul, Sum, 0)
        self.createConnection(b, Sum, 1)

        input_figures_connectors = self.get_inputs_links()
        if input_figures_connectors:
            # eliminar input_figures_connectors del dibujo
            start_node = input_figures_connectors.getConnectorStart().owner()
            self.createConnection(start_node, Mul, 1)

        self._internal_net['weight'].extend([W, b])
        self._internal_net['net'].extend([Mul, Sum])

    def assignNetPosition(self):
        W = self._internal_net.get('weight')[0]
        Mul = self._internal_net.get('net')[0]
        b = self._internal_net.get('weight')[1]
        Sum = self._internal_net.get('net')[1]

        self.setNodePosition(W, 0, 1)
        self.setNodePosition(Mul, 2, 2)
        self.setNodePosition(b, 2, 0)
        self.setNodePosition(Sum, 4, 5)