"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from MiniTensorFlow.microtensorflow.Node import Node


class Maximum(Node):
    def __init__(self, s0, s1):
        Node.__init__(self)
        self.input.append(s0)
        self.input.append(s1)
        s0.output.append(self)
        s1.output.append(self)

    def forward(self):
        s0 = self.input[0].getValue()
        s1 = self.input[1].getValue()
        self.value = np.maximum(s0, s1)
        return self.value

    def setPartialsLocal(self):
        n0 = self.input[0]
        n1 = self.input[1]
        s0 = n0.getValue()
        s1 = n1.getValue()
        bmax = s0 > s1
        bmaxn = not bmax
        self.partialsLocal[n0] = np.int(bmax)
        self.partialsLocal[n1] = np.int(bmaxn)

    def setPartials(self):
        for n in self.input:
            self.partials[n] = np.multiply(self.partialsLocal[n],
                                           self.partialGlobal)

