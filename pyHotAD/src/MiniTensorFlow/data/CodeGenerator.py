
from MiniTensorFlow.Visitors.TensorflowCodeVisitor import TensorflowCodeVisitor
from MiniTensorFlow.data.nbcreator import NotebookDocument, markdown_cell, \
    code_cell
import numpy as np


class TensorFlowCode:
    @staticmethod
    def jupyter_notebook(graph, alpha=0.1):
        visitor = TensorflowCodeVisitor()
        notebook = NotebookDocument()
        # Intro
        TensorFlowCode._intro_1(notebook)
        # imports
        TensorFlowCode._imports_2(notebook)
        # inputs values
        feed_dict, input_op = TensorFlowCode._inputs_values_3(alpha, graph,
                                                              notebook, visitor,
                                                              _is_loss(graph.hiddenNodes()[-1]))
        # inputs declaration
        TensorFlowCode._inputs_declaration_4(graph, input_op, notebook, visitor)
        # Graph declaration
        name_last = TensorFlowCode._grpah_declaration_5(graph, notebook,
                                                        visitor)
        # Optimizador: Descenso de gradiente
        TensorFlowCode._optimizator_6(name_last, notebook)

        # Evaluation
        if _is_loss(graph.hiddenNodes()[-1]):
            TensorFlowCode._evaluation_7(feed_dict, name_last, notebook)
        else:
            TensorFlowCode._evaluation_7_cg(feed_dict, name_last, notebook)

        return notebook

    @staticmethod
    def _evaluation_7_cg(feed_dict, name_last, notebook):
        notebook.add_cell(markdown_cell('### Evaluation of the Graph\n'
                                        'This contain the code to evaluate one time'
                                        ' the graph.'))
        evaluation_cell = code_cell()
        evaluation_cell.add_line('with tf.Session() as sess:')
        evaluation_cell.add_line('    sess.run(init)  # init variables')
        evaluation_cell.add_line('    v = sess.run(%s, feed_dict={%s})' % (name_last, feed_dict))
        evaluation_cell.add_line('    print("Value:\\n", v)')

        notebook.add_cell(evaluation_cell)

    @staticmethod
    def _evaluation_7(feed_dict, name_last, notebook):
        notebook.add_cell(markdown_cell('### Evaluation of the Graph\n'
                                        'This contain the code to evaluate num_steps times'
                                        ' the graph. After evaluation, the variation of error'
                                        'is shown on a plot.'))
        evaluation_cell = code_cell()
        evaluation_cell.add_line('error = np.zeros(num_steps)  # used for plot')
        evaluation_cell.add_line('')
        evaluation_cell.add_line('with tf.Session() as sess:')
        evaluation_cell.add_line('    sess.run(init)  # init variables')
        evaluation_cell.add_line('    for step in range(num_steps):')
        evaluation_cell.add_line(
            '        v, _ = sess.run([%s, train], feed_dict={%s})' % (
            name_last, feed_dict))
        evaluation_cell.add_line('        error[step] = v')
        evaluation_cell.add_line('')
        evaluation_cell.add_line('# show plot')
        evaluation_cell.add_line('plt.title("Optimization")')
        evaluation_cell.add_line('plt.xlabel("Steps")')
        evaluation_cell.add_line('plt.ylabel("Error")')
        evaluation_cell.add_line('')
        evaluation_cell.add_line('plt.plot(range(num_steps), error)')
        evaluation_cell.add_line('plt.show()')
        notebook.add_cell(evaluation_cell)

    @staticmethod
    def _optimizator_6(name_last, notebook):
        notebook.add_cell(markdown_cell('### Optimizator: Gradient descent\n'
                                        'The gradient descent optimizator implements '
                                        'the following operation for each $w$ input variable'
                                        '(tf.Variable):'
                                        '$ w\' = w- \\alpha \\nabla \\varepsilon $'))
        optimizator_cell = code_cell()
        optimizator_cell.add_line(
            'optimizer = tf.train.GradientDescentOptimizer(alpha)')
        optimizator_cell.add_line('train = optimizer.minimize(%s)' % name_last)
        notebook.add_cell(optimizator_cell)

    @staticmethod
    def _grpah_declaration_5(graph, notebook, visitor):
        notebook.add_cell(markdown_cell('### Graph declaration\n'
                                        'Then, all nodes in the graph are declarated.'))
        notebook.add_cell(code_cell("def create_mul(v0, v1, name=''):\n"
                                    "    try:\n"
                                    "        return tf.matmul(v0, v1, name=name)\n"
                                    "    except(ValueError, TypeError):\n"
                                    "        return tf.multiply(v0, v1, name)\n"))
        graph_cell = code_cell()
        hidden_node_list = graph.hiddenNodes()
        for node in hidden_node_list[:-1]:
            name, op = node.visit(visitor)
            graph_cell.add_line('%s = %s' % (name, op))
        name_last, op_last = hidden_node_list[-1].visit(visitor)
        graph_cell.add_line('%s = %s' % (name_last, op_last))
        graph_cell.add_line('')
        graph_cell.add_line('init = tf.global_variables_initializer()  '
                            '# variables should be inicializate')
        notebook.add_cell(graph_cell)
        return name_last

    @staticmethod
    def _inputs_declaration_4(graph, input_op, notebook, visitor):
        notebook.add_cell(markdown_cell('### Input nodes\n'
                                        'In tis cell, the entries nodes to the graph are defined'))
        inputs_cell = code_cell()
        for i_n in input_op:
            inputs_cell.add_line(i_n)
        inputs_cell.add_line('')
        for weigth_node in graph.weights():
            name, op = weigth_node.visit(visitor)
            inputs_cell.add_line('%s = %s' % (name, op))
        notebook.add_cell(inputs_cell)

    @staticmethod
    def _inputs_values_3(alpha, graph, notebook, visitor, is_neural_net):
        notebook.add_cell(markdown_cell('### Inputs Values\n'
                                        'This cell contain the '
                                        'basic configuration for the graph and the '
                                        'values for the input nodes.'))
        inputs_values_cell = code_cell()
        inputs_values_cell.add_line('# graph configuration')
        inputs_values_cell.add_line('alpha = {}'.format(alpha))
        inputs_values_cell.add_line('num_steps = 1000')
        inputs_values_cell.add_line(
            '\n# input values for placeholders (input nodes)')
        input_op = []
        feed_dict = ''
        for input_node in graph.inputs():
            value = input_node.get_node().getValue()
            name, op = input_node.visit(visitor)
            feed_dict += '%s: %s_value, ' % (name, name)
            input_op.append('%s = %s' % (name, op))
            inputs_values_cell.add_line(
                '{}_value = {}'.format(name, _format_input_value(value, is_neural_net)))
        feed_dict = feed_dict[:-2]
        notebook.add_cell(inputs_values_cell)
        return feed_dict, input_op

    @staticmethod
    def _imports_2(notebook):
        imports = code_cell()
        imports.add_line('import numpy as np')
        imports.add_line('import tensorflow as tf')
        imports.add_line('import matplotlib.pyplot as plt')
        notebook.add_cell(imports)

    @staticmethod
    def _intro_1(notebook):
        notebook.add_cell(markdown_cell('# PYHOTAD \n'
                                        'This document represent the '
                                        'tensorflow code of the graph created in'
                                        'the PyHotAD application.'))


def _format_input_value(value, is_neural_net=False):
    """
    if isinstance(value, np.matrix) and value.size is not 1:
        return 'np.matrix({})'.format(value.tolist())
    elif isinstance(value, np.matrix) and value.size is 1:
        return float(value)
    return value
    """

    v = 'np.' + repr(value)
    return v + '.T' if is_neural_net else v

from MiniTensorFlow.figures.Nodes.SquareLossNodeFigure import SquareLossNodeFigure as se
from MiniTensorFlow.figures.Nodes.MeanSquareLossNodeFigure import MeanSquareLossNodeFigure \
    as mse

def _is_loss(node):
    return isinstance(node, se) or isinstance(node, mse)
