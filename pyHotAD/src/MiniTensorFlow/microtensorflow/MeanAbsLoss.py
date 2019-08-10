"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from microtensorflow.MicroTensorFlow import Node


class MeanAbsLoss(Node):
    def __init__(self, y, l):
        Node.__init__(self)
        self.input.append(y)
        self.input.append(l)
        y.output.append(self)
        l.output.append(self)

    def forward(self):
        y = self.input[0].getValue()  # input value 0
        l = self.input[1].getValue()  # input value 1 predictions
        N = y.shape[1]  # column number = number of data
        dif = y - l
        loss = np.sum(np.abs(dif)) / N
        self.value = loss
        return self.value

    def setPartialsLocal(self):
        yn = self.input[0]  # input Node 0
        ln = self.input[1]  # input Node 1
        yv = yn.getValue()  # input value 0
        lv = ln.getValue()  # input value 1
        N = yv.shape[1]  # column number
        dif = yv - lv
        print("dif=", dif.shape)
        dLoss = np.sign(dif)  # should I use divide by N?
        self.partialsLocal[ln] = -dLoss
        self.partialsLocal[yn] = dLoss

