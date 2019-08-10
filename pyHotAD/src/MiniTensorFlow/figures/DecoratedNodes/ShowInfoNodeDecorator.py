from figures.Nodes.NodeFigure import NodeFigure
from figures.DecoratedNodes.NodeDecorator import DecoratedNode
from format_values import *
from pyHPoint import pyHPoint
from handles.InfoHandle import InfoHandle
from format_values import *

class ShowInfoNodeDecorator(DecoratedNode):

    def __init__(self, node):
        DecoratedNode.__init__(self, node)
        self.info = {'forward_value': None,
                'backward_value': None,
                'forward_expression': None,
                'backward_expression': None}

    def get_info_dic(self, key):
        """ Devuelve la variable info.
            Key: string
            Value: mathFigure (si existe)
        """
        return self.info.get(key)

    def set_info_dic(self, key, info):
        if key in self.info.keys():
            self.info[key] = info
        else:
            raise ValueError('Key %s not in dictionary' % key)

    def generate_info(self, key):
        """
            Genera el texto de información para
            una de las keys de la variable info.
        """
        node = self.getDecoratedFigure()
        if key == 'forward_value':
            v = node.get_value()
            return v if is_matrix(v) else None

        elif key == 'backward_value':
            v = node.get_partial_global()
            return v if is_matrix(v) else None
        elif key == 'forward_expression':
            node_letter = self.get_function_letter()
            i_letts = [i.get_function_letter() for i in self.get_inputs_nodes()]
            return node_letter + ' = ' + node.get_expression(*i_letts)
        elif key == 'backward_expression':
            return self._create_backward_figure()


    def _create_backward_figure(self):
        node_letter = self.get_function_letter()
        expression = self._partial_frac(r'\varepsilon', node_letter) + ' = '
        separator = ' \ + \ '
        dot = ' \cdot '
        for p in self.get_outputs_nodes():
            parent_letter = p.get_function_letter()
            target = self._partial_frac(r'\varepsilon', parent_letter)
            partial_local = str(p.get_partial_expressions().get(self.getDecoratedFigure()))
            invert_order = p.invert_dot_to_calculate_partial().get(self.getDecoratedFigure())
            if invert_order:
                expression += partial_local + dot + target + separator
            else:
                expression += target + dot + partial_local + separator
        return expression[:-6]

    @staticmethod
    def _partial_frac(numerator, denominator):
        return r' \dfrac{\partial \/ %s}{\partial \/ %s}' % \
               (numerator, denominator)


    def getHandles(self):
        handles = []

        if is_matrix(self.get_value()):
            f = InfoHandle(self, 'noroeste', 'forward_value', 'gray')
            handles.append(f)
        if is_matrix(self.get_partial_global()):
            b = InfoHandle(self, 'suroeste', 'backward_value', 'gray')
            handles.append(b)
        if not self.is_input():
            fe = InfoHandle(self, 'noreste', 'forward_expression', 'blue')
            handles.append(fe)

        be = InfoHandle(self, 'sureste', 'backward_expression', 'red')
        handles.append(be)
        return handles

    def draw(self, g):
        self.getDecoratedFigure().draw(g)

        for k in ['forward_value', 'backward_value']:
            if self.info.get(k) is not None:
                info = self.generate_info(k)
                actual_info = self.info[k].get_text()
                if not actual_info == info and (actual_info is not None) and (info is not None):
                    self.info[k].set_math_text(format_value(info))

        for k in self.info.keys():
            fig = self.info.get(k)
            if fig is not None:
                  fig.draw(g)

