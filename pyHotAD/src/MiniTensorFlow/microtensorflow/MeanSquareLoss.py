"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

from MiniTensorFlow.microtensorflow.Node import Node


class MeanSquareLoss(Node):
    def __init__(self, y, l):
        Node.__init__(self)
        self.input.append(y)
        self.input.append(l)
        y.output.append(self)
        l.output.append(self)

    def forward(self):
        yv = self.input[0].getValue()  # input value 0
        lv = self.input[1].getValue()  # input value 1 predictions
        N = yv.shape[1]  # column number = number of data
        dif = yv - lv
        loss = dif * dif.T  # /N
        self.value = loss / N
        return self.value

    def setPartialsLocal(self):
        yn = self.input[0]  # input Node 0
        ln = self.input[1]  # input Node 1
        yv = yn.getValue()  # input value 0
        lv = ln.getValue()  # input value 1
        N = yv.shape[1]  # column number
        dif = yv - lv
        self.partialsLocal[ln] = (-2 * dif) / N # /N # should I use divide by N?
        L_y = 2 * dif / N  # partial with respect to y. Don't used
        self.partialsLocal[yn] = L_y / N
