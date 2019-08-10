#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.pyHADOutputNodeFigure import pyHADOutputNodeFigure


from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from NodeOperations import topological_sort


class GraphCreator(pyHDecoratorFigure):

    def __init__(self, drawing):
        pyHDecoratorFigure.__init__(self, drawing)

        net = self._generateNet()
        self._inputs = net['inputs nodes']
        self._weights = net['weights nodes']
        self._hidden = net['hidden nodes']
        self._outputs_figures = {}

    def buildNet(self):
        self._createNet()
        self._assingFunctionLetter()
        self._addOutputsLines()

    def searchErrors(self):
        errors = []
        if not self._inputs and not self._weights:
            errors.append('- Debe existir por lo menos un nodo entrada, ya se un input o un weight.\n')
        inputs_error = ''
        for i in self._inputs + self._weights:
            if not i.get_node():
                node_type = 'Weight' if i.isWeight() else 'Input'
                inputs_error += '\t - {} named: {}\n'.format(node_type, i.get_text())

        if inputs_error:
            e = '- Todas las variables de entrada deben estar inicializadas. Faltan:\n' + inputs_error
            errors.append(e)

        if not self._hidden:
            errors.append('- Debe existir por lo menos una operación a realizar.\n')

        for n in self._hidden:
            if not n.are_all_inputs_occupied():
                errors.append('- Todos los nodos deben tener sus entradas ocupadas.\n')
                break

        return errors



    def _get_nodes_from_drawing(self):
        def is_node(figure):
            return isinstance(figure, NodeFigure)

        figures = self.decorated.getFigures()
        return set(f for f in figures if is_node(f))


    def _generateNet(self):
        sort = topological_sort(self._get_nodes_from_drawing())
        net = {'inputs nodes': [],
               'weights nodes': [],
               'hidden nodes': []}
        for node in sort:
            if node.is_input():
                if node.isWeight():
                    net['weights nodes'].append(node)
                else:
                    net['inputs nodes'].append(node)
            else:
                net['hidden nodes'].append(node)

        return net

    #  1- Topological sort
    def _generateNet_mysort(self):
        """ sin usar """
        stack = []
        node_list = self._get_nodes_from_drawing()
        nodes_viewed = set()
        net = {'inputs nodes': [],
               'weights nodes': [],
               'hidden nodes': []}
        while node_list:
            if not stack:
                node = node_list.pop()
                stack.append(node)
                nodes_viewed.add(node)

            while stack:
                node = stack.pop()
                childs_founds = []
                for output_node in node.get_outputs_nodes():
                    if not output_node in nodes_viewed:
                        childs_founds.append(output_node)
                        node_list.remove(output_node)
                        nodes_viewed.add(output_node)

                if childs_founds:
                    stack.append(node)
                    stack += childs_founds

                else:
                    if node.is_input(): # isInput()
                        if node.isWeight():
                            net['weights nodes'].append(node)
                        else:
                            net['inputs nodes'].append(node)
                    else:
                        net['hidden nodes'].append(node)

        net['hidden nodes'] = net['hidden nodes'][::-1]
        return net


    # 2- Asignar una letra a cada nodo (mas a delante unir con paso 3)
    def _assingFunctionLetter(self):
        abc = _createNewABC(0)
        d = 1
        for n in self._inputs + self._weights + self._hidden:
            if not abc:
                abc = _createNewABC(d)
                d += 1
            if n.is_input():
                n.assign_function_letter(n.get_text())
            else:
                l = abc.pop()
                n.assign_function_letter(l)

    def _createNet(self):
        for n in self._inputs + self._weights + self._hidden:
            n.show_sockets(False)
            n.create_node()

    def _addOutputsLines(self):
        for n in reversed(self._hidden):
            if not n.get_outputs_nodes():
                print(n.get_outputs_sockets()[0])
                cStart = n.getRightConnectors()
                out = pyHADOutputNodeFigure(cStart)
                self._outputs_figures[n] = out
                self.decorated.addFigure(out)

    def inputs(self):
        return self._inputs

    def weights(self):
        return self._weights

    def net_ops(self):
        return self._hidden

    def outputsFigures(self):
        return self._outputs_figures

    def getFullNet(self):
        return self._inputs + self._weights + self._hidden


def _createNewABC(i):
    abc = ['f', 'g', 'h', 't', 's', 'q', 'r', 'j', 'k', 'l', 'v', 'n', 'm',
           r'\alpha', r'\beta', '\kappa', '\phi', '\epsilon', '\eta', r'\tau','\mu',
           '\gamma', r'\nu', '\omega', r'\theta', r'\varphi', '\psi', '\sigma']
    prime = '\prime '

    if i <= 0:
        return abc
    else:
        abcAux = []
        for l in abc:
            abcAux.append(l + '^{\ ' + i * prime + '}')
        return abcAux


