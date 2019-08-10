from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
import numpy as np
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure
from pyHotDraw.Figures.pyHRectangleRoundedFigure import pyHRectangleRoundedFigure
from pyHotDraw.Figures.pyHAttributes import *
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure
from MiniTensorFlow.qt.AssignValuesDialog import AssignValuesDialog
from microtensorflow.Variable import Variable


class VNode(NodeFigure):
    def __init__(self, x, y, w, h, num_inputs, op='op', fl='f'):
        # super
        NodeFigure.__init__(self, x, y, w, h, num_inputs, op, fl)
        self._variables = {}

    def create_node(self):
        raise NotImplementedError

    def get_expression(self, *values):
        raise NotImplementedError

    def get_partial_expressions(self, *values):
        raise NotImplementedError



    def add_variable(self, name, value=None):
        self._variables[name] = value

    def get_variable(self, name):
        return self._variables.get(name)

    def _create_variables_handles(self):
        width_margin = 20
        height_margin_between_figures = 5
        w = 80
        h_cte = 30
        figures = []
        for var_name in self._variables.keys():
            representation_figure = pyHRectangleRoundedFigure(0,
                                           h_cte + height_margin_between_figures,
                                           w,
                                           h_cte)
            text_figure = MathTextFigure(0, 0, var_name, 12, non_math_text=True)
            text_figure.move(representation_figure.w/2 - text_figure.w/2, - 20)
            composite_figure = pyHCompositeFigure()
            composite_figure.addFigure(representation_figure)
            composite_figure.addFigure(text_figure)
            self._set_style_handles_of_variables(composite_figure)
            figures.append(composite_figure)

        occupied_space = len(self._variables) * w + \
                      width_margin * (len(self._variables) - 1)

        x = self.getX() + ((self.getWidth() - occupied_space) / 2)
        y = self.getY() - 100
        handles = []
        for fig in figures:
            fig.move(x, y)
            new_handdle = VariableHandle(self, fig)
            handles.append(new_handdle)
            x += w + width_margin
        return handles

    @staticmethod
    def _set_style_handles_of_variables(composite_figure):
        representation = composite_figure.figures[0]
        text = composite_figure.figures[1]

        representation.setAttribute('COLOR', pyHAttributeColor(136, 159, 135, 255))
        representation.setAttribute('FILL', pyHAttributeFillColor(189, 221, 187, 255))
        representation.setAttribute('WIDTH', pyHAttributeWidth(2))
        text.setAttribute('COLOR', pyHAttributeColor(0, 0, 0, 0))
        text.setAttribute('FILL', pyHAttributeFillColor(0, 0, 0, 0))

    def getHandles(self):
        h = []
        if self.node is not None:
            h = NodeFigure.getHandles(self)
        return h + self._create_variables_handles()

    def are_all_inputs_occupied(self):
        inputs_occupied = NodeFigure.are_all_inputs_occupied(self)
        variables_assigned = all(v is not None
                                 for v in self._variables.values())
        return inputs_occupied and variables_assigned

    def notifyFigureChanged(self):
        NodeFigure.notifyFigureChanged(self)


class VariableHandle(object):
    def __init__(self, owner, figure):
        self.handle_figure = figure
        self.owner = owner

    # Figure methods
    def containPoint(self, p):
        return self.handle_figure.containPoint(p)

    def draw(self, g):
        self.handle_figure.draw(g)

    # Tool methods
    def onMouseDown(self, e):
        pass

    def onMouseUp(self, e):
        pass

    def onMouseMove(self, e):
        pass

    def onMouseDobleClick(self, e):
        name = self.handle_figure.figures[1].get_text()
        old_value = self.owner.get_variable(name)
        old_value = old_value.getValue() if old_value is not None else ''
        dialog = AssignValuesDialog(actual_name=name,
                                    actual_value=old_value,
                                    name_editabe=False)
        # dialog.move()
        if dialog.exec():
            new_value = dialog.get_value()
            if new_value:
                matrix_value = Variable(new_value)
                self.owner.add_variable(name, matrix_value)



