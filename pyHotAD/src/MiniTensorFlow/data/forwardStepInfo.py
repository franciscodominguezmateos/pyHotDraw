#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.MathTextFigure import MathTextFigure

from MiniTensorFlow.figures.pyHTranparentDecorator import pyHTransparentDecorator


class forwardStepInfo:

    def __init__(self, node, index, view):
        self.node = node
        self.index = index
        self.view = view

        self.step = 0
        self.steps_list = [self.step0, self.step1, self.step2, self.step3, self.step4]

        self.infoFigure = MathTextFigure(0, 0)
        self.infoFigure.setFillColor(255, 255, 255, 255)





    def nextStep(self):
        self.steps_list[self.step]()
        self.step += 1

    def hasNextStep(self):
        return self.step < len(self.steps_list)

    def step0(self):
        self._makeFigureOpaque(self.node)
        for input_conector in self.node.get_inputs_links():
            self._makeFigureOpaque(input_conector)
            self._makeFigureOpaque(input_conector.get_start_node())

    def step1(self):
        self.infoFigure.set_math_text(self.node.getForwardOps()[0])
        self.moveFigureText()
        self.view.getDrawing().addFigure(self.infoFigure)
        self.view.update()

    def step2(self):
        inputs_values = []
        for input in self.node.get_inputs_nodes():
            inputs_values.append(input.get_node().getValue())
        self.infoFigure.set_math_text(self.node.get_expression(*inputs_values))
        self.moveFigureText()

    def step3(self):
        self.node.get_node().forward()
        v = self.node.get_node().getValue()
        self.infoFigure.set_math_text(v)
        self.moveFigureText()

    def step4(self):
        self.node.setForwardPrintable(True)
        self.view.getDrawing().removeFigure(self.infoFigure)

        for input_conector in self.node.get_inputs_links():
            self._makeFigureTransparent(input_conector)
            self._makeFigureTransparent(input_conector.get_start_node())

        for out_contector in self.node.get_outputs_links():
            self._makeFigureOpaque(out_contector)

        self.view.update()
    def moveFigureText(self):
        x = (2 * self.node.getX() + self.node.getWidth() - self.infoFigure.w) / 2
        y = self.node.getY() + self.node.getHeight() + 20
        self.infoFigure.x0 = x
        self.infoFigure.y0 = y

    def nextIndex(self):
        return self.index + 1

    def _makeFigureTransparent(self, f):
        f_decorated = pyHTransparentDecorator(f)
        f_decorated.makeSemitransparent()

    def _makeFigureOpaque(self, f):
        f_decorated = pyHTransparentDecorator(f)
        f_decorated.makeNormal()