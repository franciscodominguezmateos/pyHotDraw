
import numpy as np
from MiniTensorFlow.microtensorflow.Node import Node
from MiniTensorFlow.microtensorflow.Weight import Weights


class FullyConnectedLinear(Node):
    def __init__(self, s0, nOutput, weight=None, bias=None):
        Node.__init__(self)
          # n should be forwarded/evaluated
        self.w = weight
        self.b = bias
        self.input.append(self.w)
        self.input.append(s0)
        self.input.append(self.b)
        s0.output.append(self)
        if self.w: self.w.output.append(self)
        if self.b: self.b.output.append(self)


        self._neurons = nOutput
        #self._D = s0.value.shape[0]

    def forward(self):

        D = self.input[1].value.shape[0]
        if self.w is None:
            self.w = Weights(self._neurons, D)
            self.input[0] = self.w
            self.w.output.append(self)

        if self.b is None:
            self.b = Weights(self._neurons, 1)
            self.input[2] = self.b
            self.b.output.append(self)

        print('Neuronas:', self._neurons, ', examples:', D)
        w = self.input[0].getValue()
        x = self.input[1].getValue()
        b = self.input[2].getValue()

        self.value = w * x + b
        print(self.value.shape)
        return self.value

    def backward(self):
        Node.backward(self)
        self.w.backward()
        self.b.backward()

    def setPartials(self):
        n0 = self.input[0]
        n1 = self.input[1]
        n2 = self.input[2]
        self.partials[n0] = self.partialGlobal * self.partialsLocal[n0]
        self.partials[n1] = self.partialsLocal[n1] * self.partialGlobal
        self.partials[n2] = self.partialGlobal

    def setPartialsLocal(self):
        n0 = self.input[0]
        n1 = self.input[1]
        n2 = self.input[2]
        self.partialsLocal[n0] = n1.getValue().T
        self.partialsLocal[n1] = n0.getValue().T
        self.partialsLocal[n2] = 1
