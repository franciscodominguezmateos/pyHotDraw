from MiniTensorFlow.figures.Nodes_Expanded.ComplexVNode import VNode
from MiniTensorFlow.microtensorflow.MeanSquareLoss import MeanSquareLoss
import numpy as np
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure, format_matrix


class MeanSquareLossFigure(VNode):
    def __init__(self, x, y, w, h):
        VNode.__init__(self, x, y, w, h, 1)
        self.set_text(self.get_operation())
        self.add_variable('Y')

    def create_node(self):
        input_node = self.get_inputs_nodes()[0].get_node()
        y = self.get_variable('Y')
        self.node = MeanSquareLoss(y, input_node)

    def get_partials(self):
        inputs_nodes = self.get_inputs_nodes()
        input0_letter = 'Ŷ'
        input1_letter = inputs_nodes[0].get_function_letter()
        input0_dvalue = self.get_node().partialsLocal.get(inputs_nodes[0].get_node())
        input1_dvalue = self.get_node().partialsLocal.get(inputs_nodes[1].get_node())
        return {input0_letter : (input1_letter, input0_dvalue),
                input1_letter : (input0_letter, input1_dvalue)}

    def get_expression(self, prediction, obteined='Y'):
        loss = '({}_i - {}_i)^2 '.format(prediction, obteined)
        exp = r'\frac{1}{n} \sum_{i=1}^{n} ' + loss
        return exp

    def get_figure_expression(self, prediction, obteined='Y'):
        expression = '{} \/ = \/ '.format(self.get_function_letter())
        accepted_list = (list, np.ndarray, np.matrix)
        if isinstance(prediction, accepted_list):
            matrix_0 = format_matrix(prediction)
            expression += r'\frac{1}{n} \sum \left(' + matrix_0 + ' - ' + obteined + r' \right)^2'
            return MathTextFigure(0, 0, expression, use_latex=True)
        else:
            expression += self.get_expression(prediction, obteined)
            return MathTextFigure(0, 0, expression)

    def get_operation(self):
        return '\mathrm{\mathsf{MSE}}'

    def visit(self,visitor):
        return visitor.visitMulFigure(self)