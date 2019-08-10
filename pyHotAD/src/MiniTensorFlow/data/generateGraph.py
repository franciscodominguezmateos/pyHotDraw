#!/usr/bin/python
# -*- coding: utf-8 -*-



from MiniTensorFlow.figures.pyHADOutputNodeFigure import pyHADOutputNodeFigure

from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure


def _createNewABC(i):
    abc = ['f', 'g', 'h', 't', 's', 'q', 'r', 'j', 'k', 'l', 'v', 'm',
           r'\alpha', r'\beta', '\chi', '\eta', '\gamma', '\mu',
           r'\nu', '\omega', '\phi', '\psi', '\sigma', r'\tau', r'\theta']
    prime = '\prime '
    if i <= 0:
        return abc
    else:
        abcAux= []
        for l in abc:
            abcAux.append( l + '^{\ ' + i*prime + '}' )
        return abcAux


def lenMaxElem(listOfList):
    m = 0
    for l in listOfList:
        if len(l) > m:
            m = len(l)
    return m


class generateGraph:
    def __init__(self, nodeList):
        self.inputs = []
        self.weights = []
        self.net_ops = []
        self.outsFigures = []
        self.n_nf = {}     # n_nf -> k: node / v: nodeFigure (owner of node)
        self._initValues(nodeList)


    def _initValues(self, view):
        self.n_nf = {}
        nodeSet = set()
        for nf in view.getDrawing().getFigures():
            if isinstance(nf, NodeFigure):
                n = nf.get_node()
                nodeSet.add(nf)
                self.n_nf[n] = nf

        self._generateNet(nodeSet)
        self._createNet()
        self._assingFunctionLetter()
        self._addOutputsLines(view)
        self._createExpressionsList()
        # self._createBackwardInfo()
        """
        self.forward()
        self.backward()

        self._createBackwardInfo()
        """


    def forward(self):
        for n in self.inputs + self.weights + self.net_ops:
            n.setForwardPrintable(True)
            node = n.get_node()
            node.forward()
            n.notifyFigureChanged()


    def backward(self):
        for n in reversed(self.inputs + self.weights + self.net_ops):
            n.setBackwardPrintable(True)
            node = n.get_node()
            node.backward()
            n.notifyFigureChanged()

    def update(self, alpha):
        for n in self.weights:
            n.get_node().update(alpha)
            n.notifyFigureChanged()

    #  1- Topological sort
    def _generateNet(self, nodeList):
        stack = []
        nodesViewed = set()
        i = []
        w = []
        net = []
        while nodeList:
            if not stack:
                node = nodeList.pop()
                stack.append(node)
                nodesViewed.add(node)

            while stack:
                node = stack.pop()

                childsFounds = False
                childs = []
                for o in node.get_outputs_nodes():
                    if not o in nodesViewed:
                        childsFounds = True
                        childs.append(o)
                        nodeList.remove(o)
                        nodesViewed.add(o)

                if childsFounds:
                    stack.append(node)
                    stack += childs

                else:
                    if node.max_inputs_nodes == 0: # isInput()
                        if node.isWeight():
                            w.append(node)
                        else:
                            i.append(node)
                    else:
                        net.append(node)

        self.inputs = i
        self.weights = w
        self.net_ops = net[::-1]

    def _createNet(self):
        for n in self.inputs + self.weights + self.net_ops:
            n.create_node()

    def _addOutputsLines(self, view):
        for n in reversed(self.net_ops):
            if not n.get_outputs_nodes():
                cStart = n.getRightConnectors()
                out = pyHADOutputNodeFigure(cStart)
                self.outsFigures.append(out)
                view.getDrawing().addFigure(out)


    # 2- Asignar una letra a cada nodo (mas a delante unir con paso 3)
    def _assingFunctionLetter(self):
        abc = _createNewABC(0)
        d = 1
        for n in self.inputs + self.weights + self.net_ops:
            if not abc:
                abc = _createNewABC(d)
                d += 1
            if n.max_inputs_nodes is 0:
                n.assign_function_letter(n.get_text())
            else:
                l = abc.pop()
                n.assign_function_letter(l)


    # 3- Crear lista expresiones matematicas (forward) para cada nodo
    def _createExpressionsList(self):
        for node in self.inputs + self.weights + self.net_ops:
            if node.max_inputs_nodes is 0: # Nodo input
                l = node.get_function_letter()
                node.addForwardVar(l)
                node.addForwardOp(l)
                node.setForwardExp(['i = ' + l])

            else:  # nodo intermedio
                l = []
                v = []
                op = []
                for inputNode in node.get_inputs_nodes():
                    l.append(inputNode.get_function_letter())
                    v.append(inputNode.getForwardVar())
                    op.append(inputNode.getForwardOps())

                node.addForwardVar (_gExpresionVar(l))
                node.addForwardOp (_gExpresionOp(node, l))

                for pos in range(lenMaxElem(v)):
                    v_aux = []
                    op_aux = []
                    for i in range(len(op)):
                        if pos < len(op[i]):
                            v_aux.append(v[i][pos])
                            op_aux.append(op[i][pos])
                        else:
                            v_aux.append(v[i][-1])
                            op_aux.append(op[i][-1])

                    node.addForwardVar(_gExpresionVar(v_aux))
                    node.addForwardOp(_gExpresionOp(node, op_aux))

                node.setForwardExp(_gExpresion(node.get_function_letter(),
                                               node.getForwardVar(),
                                               node.getForwardOps()))



    # al hacer click en el handle (rapido y da mas informacion)
    def _createBackwardInfo(self):
        for node in reversed(self.inputs + self.weights + self.net_ops):
            l = node.get_function_letter()

            dif = '{\partial \ ' + l + ' }'

            if not node.get_outputs_nodes():
                node.addBackwardExp(r'\frac' + dif + dif +' = 1')  # ----
            else:
                back_exp = [r'', r'', r'']
                for o in node.get_outputs_nodes():
                    print (o.get_node().partialGlobal)
                    dotPG = '\cdot \ ' + str(o.get_node().partialGlobal) + '\ + \ '
                    o_dif = o.get_function_letter()      # 0
                    back_exp[0]+= r'\frac {\partial \ ' + o_dif + ' }' + dif + dotPG

                    o_operation = o.getForwardOps()[0] # 1
                    back_exp[1] += r'\frac {\partial \ ' + o_operation + ' }' + dif + dotPG

                    o_partial = o.get_partials(l) # 2 -----
                    back_exp[2] += str(o_partial) +'\ '+ dotPG

                for be in back_exp:
                    node.addBackwardExp(be[:-6])


    def getOutputsFigures(self):
        return self.outsFigures

    def getNet(self):
        return self.inputs + self.weights + self.net_ops