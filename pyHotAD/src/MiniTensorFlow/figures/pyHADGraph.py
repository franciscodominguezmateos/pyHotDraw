#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.pyHADOutputNodeFigure import pyHADOutputNodeFigure
from pyBackPropNets.scalar import scalar


class pyHADGraph:
    def __init__(self):
        self.net = []
        self.n_fn = {}     # n_fn -> k: node / v: nodeFigure (owner of node)
        self.inputs = []
        self.endNodes = [] # y    -> end nodes (nodes without outputs)
        self.outputs = []

        self.f = False
        self.function = None


    def _initValues(self, nodes):
        self.n_fn = {}
        self.endNodes = []
        self.inputs = []
        for nf in nodes:
            n = nf.get_node()
            self.n_fn[n] = nf
            if isinstance(n, scalar):
                self.inputs.append(nf)

            elif not n.getOutputs():
                self.endNodes.append(nf)

    # Genera el grafo (self.net) para recorrer los nodos en orden topologico (para realizar Forward y Backward)
    # Al mismo tiempo, genera la función f() que se se esta evaluando en el grafo dibujado
    def generateGraph(self, nodes):
        if nodes is not (None or []):
            self._initValues(nodes)
            initNode = self.endNodes[0]
            n = {None} # Nodes viewed

            net = self._generateNet(initNode, n)
            if len(net) == len(nodes):
                self.net = net
                self._generateGeneralFunction()
                self._assingFunctionLetter()

    def _assingFunctionLetter(self):
        abc = self._createNewABC(0)
        d = 1
        for n in self.net:
            if not abc:
                abc = self._createNewABC(d)
                d += 1
            l = abc.pop()
            n.assign_function_letter(l)

    def _createNewABC(self, i):
        abc = ['f', 'g', 'h', 't', 's', 'q', 'r', 'j', 'k', 'l', 'v', 'n', 'm',
               '\\alpha ', '\\beta ', '\chi ', '\epsilon', '\eta', '\gamma', '\mu',
               '\\nu ', '\omega ', '\phi ', '\psi', '\sigma', '\\tau', '\\theta']
        prime = '\prime '
        if i <= 0:
            return abc
        else:
            abcAux = []
            for l in abc:
                abcAux.append(l + '^{\ ' + i * prime + '}')
            return abcAux

    def _generateNet(self, nodeFigure, nodesViewed):
        node = nodeFigure.get_node()
        miniNet = [nodeFigure]
        if not node in nodesViewed:
            nodesViewed.add(node)

            for o in node.getOutputs():
                if not o in nodesViewed:
                    miniNet += self._generateNet(self.n_fn.get(o), nodesViewed)

            for i in node.getInputs():
                if i not in nodesViewed:
                    miniNet = self._generateNet(self.n_fn.get(i), nodesViewed) + miniNet

        return miniNet

    #  Genera la función f() que se se esta evaluando en el grafo dibujado
    def _generateGeneralFunction(self):
        if len(self.endNodes) is 1:  # 1 sola salida, cuando sepa mostrar varias funciones habrá que modificarlo
            function = '$f('

            for i in self.inputs[:-1]:
                function+= i.get_expression()[0] + ","
            function += self.inputs[-1].get_expression()[0] + ") = "

            function += self._gfRecursive(self.endNodes[0]) + "$"

            self.function = function


    def _gfRecursive(self, n):
        exp = n.get_expression()
        node = n.get_node()
        if len(exp) is 1:
            return exp[0]

        f = ""
        for i in range(len(exp[:-1])):
            f += exp[i]
            f +=self._gfRecursive(self.n_fn.get(node.getInputs()[i])) + " "
        f+= exp[-1]
        return f





    def forward(self):
        for n in self.net:
            n.setForwardPrintable(True)
            node = n.get_node()
            node.forward()
            n.notifyFigureChanged()

        for n in self.endNodes:
            self.outLine(n)

        self.f = True

    def backward(self):
        if self.f:
            for n in reversed(self.net):
                n.setBackwardPrintable(True)
                node = n.get_node()
                node.backward()
                n.notifyFigureChanged()
        self.f = False




    def outLine(self, n):
        cStart = n.getRightConnectors()
        Y = pyHADOutputNodeFigure(cStart)

        self.outputs.append(Y)

    def getY(self):
        return self.outputs


    def getFunction(self):
        return self.function









    def generateGraphn(self):
        d = self.n_fn
        y = self.endNodes
        net = []
        if y is not None:
            queue = [[y[0].get_node()]]
            u = {y[0].get_node()}

            while queue:
                auxQ = queue[-1]
                n = auxQ[0]

                aux = []
                for no in n.getOutputs():
                    if not no in u:
                        u.add(no)
                        aux.append(no)

                if aux:
                    queue.append(aux)

                else:
                    auxQ.pop(0)
                    net.append(d.get(n))

                    aux = []
                    for ni in n.getInputs():
                        if not ni in u:
                            if ni is not n:  # scalar tiene input a si mismo
                                u.add(ni)
                                aux.append(ni)

                    if aux:
                        auxQ += aux

                    elif not auxQ:
                        queue.pop()

        self.net = net[::-1]

    def generateGraph2(self, nodes):
        d = self.n_fn
        y = self.endNodes
        net = []
        if y is not None:
            queue = [y[0]]
            while queue:
                n = queue.pop()
                net.append(d.get(n))
                for ni in n.getInputs():
                    if ni is not n:  # scalar tiene input a si mismo
                        queue.append(ni)

        self.net = net[::-1]

