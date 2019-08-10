"""
Created on Jun 17, 2017

@author: Javier Martínez
"""

from MiniTensorFlow.microtensorflow.Node import Node


class SquareLoss(Node):
    def __init__(self, y, l):
        Node.__init__(self)
        self.input.append(y)
        self.input.append(l)
        y.output.append(self)
        l.output.append(self)

    def forward(self):
        yv = self.input[0].getValue()  # input value 0
        lv = self.input[1].getValue()  # input value 1 predictions
        dif = yv - lv
        loss = dif * dif.T
        self.value = loss / N
        return self.value

    def setPartialsLocal(self):
        yn = self.input[0]  # input Node 0
        ln = self.input[1]  # input Node 1
        yv = yn.getValue()  # input value 0
        lv = ln.getValue()  # input value 1
        dif = yv - lv
        self.partialsLocal[ln] = -2 * dif  # /N # should I use divide by N?
        L_y = 2 * dif  # partial with respect to y. Don't used
        self.partialsLocal[yn] = L_y
