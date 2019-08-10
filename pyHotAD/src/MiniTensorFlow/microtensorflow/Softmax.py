"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from microtensorflow.MicroTensorFlow import Node


class Softmax(Node):
    def __init__(self, n0):
        Node.__init__(self)
        self.input.append(n0)
        n0.output.append(self)

    def softmax(self, l):
        # trick to avoid numerical instability
        l -= np.max(l, axis=0)
        e = np.exp(l)
        s = np.sum(e, axis=0)
        p = e / s
        return p

    # this operation is too expensive that is
    # because softmax is not used before a cross entropy Node
    # It is better use the next Node to train
    # this Node is use only to predict
    def dsoftmax(self, l):
        p = self.softmax(l)  # we could reuse self.getValue(). But...
        # Jacobian is a negated outer product of p except
        # diagonal. Diagonal in this case is similar to sigmoid
        p_l = -p * p.T
        pd = np.multiply(p, (1 - p))
        p_l[np.diag_indices_from(p_l)] = pd
        return p_l

    def forward(self):
        n0 = self.input[0]
        v0 = n0.getValue()
        self.value = self.softmax(v0)
        return self.value

    def setPartialsLocal(self):
        n0 = self.input[0]
        v0 = n0.getValue()
        # maybe it need to be np.multiply
        self.partialsLocal[n0] = self.dsoftmax(v0)

