"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from MiniTensorFlow.microtensorflow.Node import Node


class Weights(Node):
    def __init__(self, sr, sc):
        Node.__init__(self)
        self.value = np.matrix(np.random.randn(sr, sc) / np.sqrt(sc))
        self.input.append(self)

    def setPartialsLocal(self):
        self.partialsLocal[self] = 1  # np.ones_like(self.value)

    def setValue(self, v):
        self.value = v

    def update(self, alpha):
        partial = self.getPartial(self)
        iValue = -partial  # Want the opposite direction of the gradient
        self.value += alpha * iValue
