#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 07/03/2017

@author: Javi
"""


class nodeInfo:

    def __init__(self, nodeF, nf_d):
        self.node = nodeF
        self.n_fn = nf_d

        self.forward_expression = None
        self.forward_nodes = {None}
        self.forward_inputs = []

        self.backward_expression = None
        self.backward_nodes = {None}

        self.initValues()


    def initValues(self):
        self.generateNodeForwardValues(self.node)
        self.generateNodeBackwardValues(self.node)


    def generateNodeForwardValues(self, node):

        exp = self._gnFRecursive(node)

        function = "$Forward("
        for i in self.forward_inputs[:-1]:
            function += i.get_expression()[0] + ","
        function += self.forward_inputs[-1].get_expression()[0] + ") = "

        self.forward_expression = function + exp + "$"


    def _gnFRecursive(self, n):
        self.forward_nodes.add(n)

        exp = n.get_expression()
        node = n.get_node()

        if len(exp) is 1:
            if n not in self.forward_inputs:
                self.forward_inputs.append(n)
            return exp[0]

        f = ""
        for i in range(len(exp[:-1])):
            f += exp[i] + self._gnFRecursive(self.n_fn.get(node.getInputs()[i]))
        f+= exp[-1]
        return f


    def generateNodeBackwardValues(self, node):
        pass


    def getForwardExpresion(self):
        return self.forward_expression

    def getForwardNodes(self):
        return self.forward_nodes
