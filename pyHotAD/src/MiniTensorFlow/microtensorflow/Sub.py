"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

from MiniTensorFlow.microtensorflow.Node import Node


class Sub(Node):
    def __init__(self, s0, s1):
        Node.__init__(self)
        self.input.append(s0)
        self.input.append(s1)
        s0.output.append(self)
        s1.output.append(self)

    def forward(self):
        s0 = self.input[0].getValue()
        s1 = self.input[1].getValue()
        self.value = s0 - s1
        return self.value

    def setPartialsLocal(self):
        n0 = self.input[0]
        n1 = self.input[1]
        self.partialsLocal[n0] = 1
        self.partialsLocal[n1] = -1
