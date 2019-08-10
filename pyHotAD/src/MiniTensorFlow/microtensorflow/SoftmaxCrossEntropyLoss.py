"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from microtensorflow.MicroTensorFlow import Node


class SoftmaxCrossEntropyLoss(Node):
    def __init__(self, y, l):
        Node.__init__(self)
        self.input.append(y)  # one hot encoding binary target data
        self.input.append(l)  # logits  (linear ouput)
        y.output.append(self)
        l.output.append(self)

    def softmax(self, l):
        # trick to avoid numerical instability
        l -= np.max(l, axis=0)
        e = np.exp(l)
        s = np.sum(e, axis=0)
        p = e / s
        return p

    def forward(self):
        yv = self.input[0].getValue()  # input value 0
        lv = self.input[1].getValue()  # input value 1 (logit)
        N = yv.shape[1]  # column number
        p = self.softmax(lv)  # softmax probabilities/categorical distribution
        cross = np.multiply(yv, np.log(p))
        loss = -np.sum(cross) / N
        self.value = loss
        return self.value

    def setPartialsLocal(self):
        yn = self.input[0]  # input Node 0
        ln = self.input[1]  # input Node 1
        yv = yn.getValue()  # input value 0
        lv = ln.getValue()  # input value 1
        N = yv.shape[1]  # column number
        pv = self.softmax(lv)  # softmax probabilities/categorical distribution
        L_l = pv - yv  # partial with respect to the logits.
        self.partialsLocal[ln] = L_l / N  # should I use divide by N?
        L_y = -np.log(pv)  # partial with respect to y. Don't used
        self.partialsLocal[yn] = L_y / N

