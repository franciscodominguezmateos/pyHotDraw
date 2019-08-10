"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from MiniTensorFlow.microtensorflow.Node import Node


class ReLU(Node):
    def __init__(self, s0):
        Node.__init__(self)
        self.input.append(s0)
        s0.output.append(self)

    def forward(self):
        s0 = self.input[0].getValue()
        self.value = np.maximum(0, s0)
        return self.value

    def setPartialsLocal(self):
        n0 = self.input[0]
        s0 = n0.getValue()
        bmax = s0 > 0  # boolean matrix
        self.partialsLocal[n0] = bmax * 1.0  # trick to convert boolean to float

    def setPartials(self):
        for n in self.input:
            self.partials[n] = np.multiply(self.partialsLocal[n],
                                           self.partialGlobal)

