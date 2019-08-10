"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from microtensorflow.Node import Node


class Tanh(Node):
    def __init__(self, n0):
        Node.__init__(self)
        self.input.append(n0)
        n0.output.append(self)

    def forward(self):
        n0 = self.input[0]
        v0 = n0.getValue()
        self.value = np.tanh(v0)
        return self.value

    def setPartialsLocal(self):
        n0 = self.input[0]
        v0 = self.getValue()  # v0 = tanh(n0)
        self.partialsLocal[n0] = 1.0 - np.multiply(v0, v0)

    def setPartials(self):
        for n in self.input:
            self.partials[n] = np.multiply(self.partialsLocal[n],
                                           self.partialGlobal)