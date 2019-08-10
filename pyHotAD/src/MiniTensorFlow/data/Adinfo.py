#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.BackwardEndNodeStep import BackwardEndNodeStep
from MiniTensorFlow.data.BackwardStep import BackwardStep
from MiniTensorFlow.data.ForwardEndNodeStep import ForwardEndNodeStep
from MiniTensorFlow.data.ForwardStep import ForwardStep
from MiniTensorFlow.data.WeightUpdateStep import WeightUpdateStep
from MiniTensorFlow.figures.pyHColorConnectorDecorator import pyHColorConnectorDecorator
from MiniTensorFlow.figures.pyHColorNodeDecorator import pyHColorNodeDecorator


class Adinfo:
    def __init__(self,
                 inputs_nodes,
                 weights_nodes,
                 hidden_nodes,
                 outputes_figures,
                 view):

        self.view = view
        self._alpha = 0.1

        self._inputs = inputs_nodes
        self._weights = weights_nodes
        self._hidden_nodes = hidden_nodes
        self._outputs_figures = outputes_figures

        self.node_position = 0
        self.step_info = None


    """ Operaciones sobre todos los nodos: """

    def forward(self, makeTransparent = False):
        """
        Realiza la operación 'forward' sobre cada uno de los nodos de la red
        """
        if makeTransparent:
            self.makeEverythingSemitransparent()

        for node_figure in self.neuralNet():
            node_figure.setForwardPrintable(True)
            node_figure.get_node().forward()
            node_figure.notifyFigureChanged()

    def backward(self, makeTransparent = False):
        """
        Realiza la operación 'backward' sobre cada uno de los nodos de la red
        """
        if makeTransparent:
            self.makeEverythingOpaqueLessWeights() if self._weights else self.makeEverythingOpaque()

        for node_figure in reversed(self.neuralNet()):
            node_figure.setBackwardPrintable(True)
            node_figure.get_node().backward()
            node_figure.notifyFigureChanged()


    def updateWeight(self, alpha=0.1, makeOpaque = False):
        """
        Actualiza el valor de todos los pesos de la red
        """
        if makeOpaque:
            self.makeEverythingOpaque()

        for n in self._weights:
            n.get_node().update(float(alpha))
            n.notifyFigureChanged()

    def run(self, alpha=0.1):
        """
        Realiza la operación 'forward' y 'backward' sobre cada uno de los nodos de la red,
        y actualiza el valor de todos los pesos de la red
        """
        self.forward()
        self.backward()
        self.updateWeight(alpha)

    """ Operaciones paso a paso """

    def hasForwardInfo(self):
        """
        Informa si quedan nodos/pasos que realizar.
        :return: Bool
        """
        return self.step_info.hasNextStep() or self.node_position < len(self._hidden_nodes)

    def hasForwardStep(self):
        """
        Informa si quedan pasos de un nodo que realizar.
        :return: Bool
        """
        return self.step_info.hasNextStep()

    def forwardStep(self):
        """
        Realiza un
        :return:
        """
        if not self.step_info.hasNextStep():
            self.step_info.endStep()
            self._newForwardNodeInfo()
        self.step_info.nextStep()

    def hasBackwardInfo(self):
        """
        Informa si quedan nodos/pasos que realizar.
        :return: Bool
        """
        return self.step_info.hasNextStep() or self.node_position >= 0

    def hasBackwardStep(self):
        """
        Informa si quedan pasos de un nodo que realizar.
        :return: Bool
        """
        return self.step_info.hasNextStep()

    def backwardStep(self):
        """
        Realiza un
        :return:
        """
        if not self.step_info.hasNextStep():
            self.step_info.endStep()
            self._newBackwardNodeInfo()
        self.step_info.nextStep()

    def hasUpdateWeightInfo(self):
        """
        Informa si quedan nodos/pasos que realizar.
        :return: Bool
        """
        return self.step_info.hasNextStep() or self.node_position < len(self._weights)

    def hasUpdateWeightStep(self):
        """
        Informa si quedan pasos de un nodo que realizar.
        :return: Bool
        """
        return self.step_info.hasNextStep()

    def updateWeightStep(self):
        """
        Realiza un
        :return:
        """
        if not self.step_info.hasNextStep():
            self.step_info.endStep()
            self._newUpdateNodeInfo()
        self.step_info.nextStep()

    """ Others operations """

    def beginForwardSteps(self):
        self.node_position = 0
        self._newForwardNodeInfo()

    def _newForwardNodeInfo(self):
        node = self._hidden_nodes[self.node_position]
        if self._outputs_figures.get(node):
            self.step_info =  ForwardEndNodeStep(node, self._outputs_figures.get(node), self.view)
        else:
            self.step_info = ForwardStep(node, self.view)
        self.node_position += 1


    def beginBackwardSteps(self):
        self.node_position = len(self.neuralNet()) - 1
        self._newBackwardNodeInfo()

    def _newBackwardNodeInfo(self):
        node = self.neuralNet()[self.node_position]
        if self._outputs_figures.get(node):
            self.step_info =  BackwardEndNodeStep(node, self._outputs_figures.get(node), self.view)
        else:
            self.step_info = BackwardStep(node, self.view)
        self.node_position -= 1

    def beginUpdateSteps(self):
        self.node_position = 0
        self._newUpdateNodeInfo()

    def _newUpdateNodeInfo(self):
        node = self._weights[self.node_position]
        self.step_info = WeightUpdateStep(node, self._alpha, self.view)
        self.node_position += 1


    def makeEverythingOpaque(self):
        if self.step_info:
            info_fig = self.step_info.get_info_figure()
            self.view.getDrawing().removeFigure(info_fig)

        for figure in self.neuralNet():
            decorated = pyHColorNodeDecorator(figure)
            decorated.makeNormal()
            for o in figure.get_outputs_links():
                o_decorated = pyHColorConnectorDecorator(o)
                o_decorated.makeNormal()
        for o in self.outsFigures().values():
            o_decorated = pyHColorConnectorDecorator(o)
            o_decorated.makeNormal()

    def makeEverythingOpaqueLessWeights(self):
        if self.step_info:
            info_fig = self.step_info.get_info_figure()
            self.view.getDrawing().removeFigure(info_fig)

        for figure in self.inputs() + self.hiddenNodes():
            decorated = pyHColorNodeDecorator(figure)
            decorated.makeNormal()
            for o in figure.get_outputs_links():
                o_decorated = pyHColorConnectorDecorator(o)
                o_decorated.makeNormal()

        for figure in self.weights():
            decorated2 = pyHColorNodeDecorator(figure)
            decorated2.makeSemitransparent()
            for o in figure.get_outputs_links():
                o_decorated = pyHColorConnectorDecorator(o)
                o_decorated.makeNormal()

        for o in self.outsFigures().values():
            o_decorated = pyHColorConnectorDecorator(o)
            o_decorated.makeNormal()

    def makeEverythingSemitransparent(self):
        if self.step_info:
            info_fig = self.step_info.get_info_figure()
            self.view.getDrawing().removeFigure(info_fig)

        for figure in self.neuralNet():
            decorated = pyHColorNodeDecorator(figure)
            decorated.makeSemitransparent()
            for o in figure.get_outputs_links():
                o_decorated = pyHColorConnectorDecorator(o)
                o_decorated.makeSemitransparent()

        for o in self.outsFigures().values():
            o_decorated = pyHColorConnectorDecorator(o)
            o_decorated.makeSemitransparent()

    """ Attributes setters """
    def setAlpha(self, a):
        self._alpha = float(a)


    """ Attributes getters """
    def alpha(self):
        return self._alpha

    def inputs(self):
        return self._inputs

    def weights(self):
        return self._weights

    def hiddenNodes(self):
        return self._hidden_nodes

    def outsFigures(self):
        return self._outputs_figures

    def neuralNet(self):
        return self._inputs + self._weights + self._hidden_nodes

