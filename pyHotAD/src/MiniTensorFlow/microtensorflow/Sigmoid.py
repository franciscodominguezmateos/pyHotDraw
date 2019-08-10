"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from MiniTensorFlow.microtensorflow.Node import Node



class Sigmoid(Node):
    def __init__(self, n0):
        Node.__init__(self)
        self.input.append(n0)
        n0.output.append(self)

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def dsigmoid(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

    def forward(self):
        n0 = self.input[0]
        v0 = n0.getValue()
        self.value = self.sigmoid(v0)
        return self.value

    def setPartialsLocal(self):
        n0 = self.input[0]
        v0 = self.getValue()
        # maybe it need to be np.multiply
        self.partialsLocal[n0] = np.multiply(v0, (1 - v0))

    def setPartials(self):
        for n in self.input:
            self.partials[n] = np.multiply(self.partialsLocal[n],
                                           self.partialGlobal)

