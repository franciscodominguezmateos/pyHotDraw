#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import sys
from MiniTensorFlow.data import operations as ops
from MiniTensorFlow.data.Adinfo import Adinfo
from images import IMG_DIR
from PyQt5 import QtCore, QtGui, QtWidgets
from pyHotDraw.Core.Qt.pyHStandardEditor import pyHStandardEditor

from MiniTensorFlow.figures.GraphCreator \
    import GraphCreator
from MiniTensorFlow.figures.pyHTranparentDecorator \
    import pyHTransparentDecorator
from MiniTensorFlow.Tools.pyHDecoratorInfoLetterTool \
    import pyHDecoratorInfoLetterTool
from MiniTensorFlow.Visitors.TensorflowCodeVisitor import TensorflowCodeVisitor
from MiniTensorFlow.Visitors.pyHTensorflowVisitor import pyHTensorflowVisitor
from pyHQTError import pyHQTError
from MiniTensorFlow.core.StandardView import StandardView

from MiniTensorFlow.figures.Nodes.NodeFigure \
    import NodeFigure
from MiniTensorFlow.figures.pyHADOutputNodeFigure import pyHADOutputNodeFigure
from MiniTensorFlow.figures.Conexion.NodeLinkFigure import NodeLinkFigure
from pyHotDraw.Tools.pyHViewTranslationTool import pyHViewTranslationTool

from PyQt5.QtCore import Qt
from MiniTensorFlow.data.CodeGenerator import TensorFlowCode
from NodeOperations import *
from MiniTensorFlow.Tools.EvaluateGenericTool import EvaluateGenericTool
from format_values import *

class StandardEditor(pyHStandardEditor):

    def __init__(self):
        pyHStandardEditor.__init__(self)
        self.graph = None
        self.setGeometry(300, 30, 1330, 1000)


    def initUI(self):

        ops.addSheetStyle(self)

        self.setGeometry(300, 30, 1550, 900)
        self.setWindowTitle('PyHotAD')
        self.sb = QtWidgets.QLabel(self)
        self.sb.setText("x=0,y=0")
        self.statusBar().addPermanentWidget(self.sb)

        self.setView(StandardView(self))

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(self.getView())

        self.setCentralWidget(self.getView())
        action = self.get_action('&CreateGraph', 'Select')
        action.setChecked(True)
        action.activate(QtWidgets.QAction.Trigger)

        self.show()

        d = self.getView().getDrawing()



    def setCurrentTool(self, t):
        try:
            self.getCurrentTool().exit()
        except:
            print('La herramienta no tiene método exit()')
        pyHStandardEditor.setCurrentTool(self, t)

    def get_action(self, group, action_name):
        for action in self.actionGroup[group].actions():
            if action.text() == action_name:
                return action
        return

    def metodoBurro(self):
        for f in self.view.getDrawing().figures[:]:
            not_remove = (NodeFigure,
                          pyHADOutputNodeFigure,
                          NodeLinkFigure)
            if not isinstance(f, not_remove):
                self.view.getDrawing().removeFigure(f)





    def add_toolbar(self,
                    name,
                    movable=False,
                    orientation=Qt.TopToolBarArea,
                    text_icon=Qt.ToolButtonTextUnderIcon):
        self.toolBar[name] = self.addToolBar(name)
        self.addToolBar(orientation, self.toolBar[name])
        self.actionGroup[name] = QtWidgets.QActionGroup(self)
        #self.toolBar[name].setToolButtonStyle(QtCore.qt.ToolButtonTextUnderIcon)
        self.toolBar[name].setToolButtonStyle(text_icon)
        self.toolBar[name].setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.toolBar[name].setMovable(bool(movable))

    def add_menu(self, name):
        self.menu[name] = self.menuBar.addMenu(name)
        self.actionGroup[name] = QtWidgets.QActionGroup(self)

    def initActionMenuToolBars(self):
        self._createToolbar_CreateGraph()
        text = self._createToolbar_ADTool()
        self._createToolbar_S2S(text)



    def undo(self):
        self.view.undo()
        self.view.update()

    def redo(self):
        self.view.redo()
        self.view.update()

    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseSheet
        file_name, ext = file_dialog.getOpenFileName(
            self, 'Open PYHAD project', QtCore.QDir.currentPath(), 'PYHAD (*.pyad)', options=options)

        if file_name:
            print(file_name)
            self.open_pyad(file_name)

    def save_file_dialog(self):
        #file_dialog = QtWidgets.QFileDialog()
        #options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseSheet
        #file_name, ext = file_dialog.getSaveFileName(
        #    None, 'Save PYHAD project', '', 'PYHAD (*.pyad)') #, options=options)
        file_name="perceptron.pyad"
        if file_name:
            print(file_name)
            self.save_pyad(file_name)
        #file_dialog.close()

    def save_nb_dialog(self):
        file_dialog = QtWidgets.QFileDialog()
        #options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseSheet
        file_name, ext = file_dialog.getSaveFileName(
            None, 'Export PYHAD project', '', 'Jupyter Notebook (*.ipynb)') #,options=options)

        if file_name:
            print(file_name)
            self.TF_code(file_name)
        file_dialog.close()

    def save_pyad(self, path, ext='.pyad'):
        d = self.getView().clearSelectedFigures()
        d = self.getView().getDrawing()
        d_co = d.changedDrawingObservers
        v = d.view

        d.changedDrawingObservers = []
        d.view = None
        if path[-5:] != ext: path += ext
        try:
            with open(path , 'wb') as f:
                pickle.dump(d, f, protocol=3)
        except IOError:
            print ('error al guardar el archivo')

        d.changedDrawingObservers = d_co
        d.view = v

    def TF_code(self, path):
        nb = TensorFlowCode.jupyter_notebook(self.graph)
        add_ext = path[-5:] != '.ipynb'
        nb.save_notebook(path, add_ext=add_ext)
        print('ipynb creado')


    def open_pyad(self, path, ext='.pyad'):
        try:
            with open(path, 'rb') as f:
                d_load = pickle.load(f)
            view = self.getView()
            d_load.view = view
            view.setDrawing(d_load)
            view.update()
        except IOError:
            print('error al abrir el archivo')




    def design_graph_view(self):
        self.view.clearSelectedFigures()

        for f in self.graph.outsFigures().values():
            self.getView().getDrawing().removeFigure(f)
        for node in self.graph.inputs() + self.graph.weights():
            node.setBackwardPrintable(False)
            node.show_sockets(True)
        for node in self.graph.hiddenNodes():
            node.setForwardPrintable(False)
            node.setBackwardPrintable(False)
            node.show_sockets(True)

        showInfoFunctionType(self.graph.neuralNet())
        self.graph = None

        self.toolBar['&CreateGraph'].setVisible(True)
        self.toolBar["&ADTool"].setVisible(False)
        self.test()

    def evaluateNetworkView(self):
        self.view.clearSelectedFigures()

        nn = GraphCreator(self.getView().getDrawing())
        errors = nn.searchErrors()
        if errors:
            e = pyHQTError('Se produjo un error al generar la información del grafo.')
            e.detailed_mensagge = ''.join(map(str, errors))
            e.showDialog()
        else:
            nn.buildNet()
            self.graph = Adinfo(nn.inputs(), nn.weights(),
                                nn.net_ops(), nn.outputsFigures(), self.getView())



            #pyHDecoratorInfoLetterTool(self.getCurrentTool()).showInfoHybrid()
            showInfoHybrid(self.graph.neuralNet())
            self.toolBar['&CreateGraph'].setVisible(False)
            self.toolBar["&ADTool"].setVisible(True)
            self.toolBar['&S2S'].setVisible(False)
            # self.setCurrentTool(pyHInfoNodeTool(self.getView(), graph.n_fn))
            #self.selectingADNodes
            self.setCurrentTool(EvaluateGenericTool(self.getView()))
            self.getView().update()

            # self._TEST_TENSORFLOW_CODE()



    def stepToStepView(self):
        self.view.clearSelectedFigures()

        if self.graph.hiddenNodes():
            # UI
            self.toolBar['&S2S'].setVisible(True)
            self.toolBar['&ADTool'].setVisible(False)
            self.get_action("&S2S", 'For. Step').setEnabled(True)
            self.get_action("&S2S", 'Back. Step').setEnabled(False)
            self.get_action("&S2S", 'Upd. Step').setEnabled(False)
            self.get_action("&S2S", 'Forward').setEnabled(True)
            self.get_action("&S2S", 'Backward').setEnabled(False)
            self.get_action("&S2S", 'Update').setEnabled(False)

            alpha = u'\u03B1'
            alpha_value = self.toolBar["&ADTool"].actions()[1].defaultWidget().text()
            label = self.toolBar["&S2S"].actions()[0].defaultWidget()
            label.setText('   {} = {}  '.format(alpha, alpha_value))
            # Operations
            self.test()
            self.graph.beginForwardSteps()


            self.graph.setAlpha(float(alpha_value))

            self.graph.makeEverythingSemitransparent()
            self.setCurrentTool(pyHViewTranslationTool(self.getView()))

    def run(self):
        alpha = self.toolBar["&ADTool"].actions()[1].defaultWidget().text()
        if self.graph.hiddenNodes() and ops.is_float(alpha):
            self.actionGroup["&ADTool"].actions()[0].setEnabled(False)
            self.graph.run(alpha)
            self.actionGroup["&ADTool"].actions()[0].setEnabled(True)

    def forward(self):
        self.actionGroup["&S2S"].actions()[0].setEnabled(False)
        self.actionGroup["&S2S"].actions()[3].setEnabled(False)

        self.actionGroup["&S2S"].actions()[1].setEnabled(True)
        self.actionGroup["&S2S"].actions()[4].setEnabled(True)

        self.graph.forward(True)
        self.graph.beginBackwardSteps()


    def backward(self):
        self.actionGroup["&S2S"].actions()[1].setEnabled(False)
        self.actionGroup["&S2S"].actions()[4].setEnabled(False)

        self.graph.backward(True)
        if self.graph.weights():
            self.actionGroup["&S2S"].actions()[2].setEnabled(True)
            self.actionGroup["&S2S"].actions()[5].setEnabled(True)

            self.graph.beginUpdateSteps()
        else:
            self.show_evaluateGraph_View()

    def updateWeights(self):
        a = self.toolBar["&ADTool"].actions()[1].defaultWidget().text()
        if ops.is_float(a):
            alpha = float(a)
            self.graph.updateWeight(alpha, True)
        self.show_evaluateGraph_View()


    def show_evaluateGraph_View(self):
        self.toolBar['&CreateGraph'].setVisible(False)
        self.toolBar["&ADTool"].setVisible(True)
        self.toolBar['&S2S'].setVisible(False)

        self.graph.makeEverythingOpaque()
        self.setCurrentTool(EvaluateGenericTool(self.getView()))

    def forwardStep(self):
        if self.graph.hasForwardInfo():
            self.graph.forwardStep()
        else:
            if self.graph.step_info:
                self.graph.step_info.endStep()
            self.graph.beginBackwardSteps()
            self.graph.makeEverythingSemitransparent()

            self.actionGroup["&S2S"].actions()[0].setEnabled(False)
            self.actionGroup["&S2S"].actions()[3].setEnabled(False)

            self.actionGroup["&S2S"].actions()[1].setEnabled(True)
            self.actionGroup["&S2S"].actions()[4].setEnabled(True)


    def backwardStep(self):
        if self.graph.hasBackwardInfo():
            self.graph.backwardStep()
        else:
            if self.graph.step_info:
                self.graph.step_info.endStep()

            if self.graph.weights():
                self.graph.beginUpdateSteps()
                for figure in self.graph.weights():
                    f_decorated = pyHTransparentDecorator(figure)
                    f_decorated.makeSemitransparent()

                self.actionGroup["&S2S"].actions()[1].setEnabled(False)
                self.actionGroup["&S2S"].actions()[4].setEnabled(False)

                self.actionGroup["&S2S"].actions()[2].setEnabled(True)
                self.actionGroup["&S2S"].actions()[5].setEnabled(True)

            else:
                self.show_evaluateGraph_View()


    def updateWeightStep(self):
        if self.graph.hasUpdateWeightInfo():
            self.graph.updateWeightStep()
        else:
            if self.graph.step_info:
                self.graph.step_info.endStep()
            self.show_evaluateGraph_View()




    def _createToolbar_S2S(self, text):
        self.add_toolbar("&S2S")
        self.toolBar['&S2S'].setVisible(False)
        label = QtWidgets.QLabel()
        label.setStyleSheet('font: 20px;')
        label.setText(text)
        label.setToolTip("Alpha represents the weight update valor")
        self.toolBar["&S2S"].addWidget(label)
        self.toolBar["&S2S"].addSeparator()
        self.addAction("&S2S", IMG_DIR + "/forward_step_n.png", 'For. Step', self, "Ctrl+P", "Forward step",
                       self.forwardStep, True, IMG_DIR + "/forward_step_p.png")
        self.addAction("&S2S", IMG_DIR + "/backward_step_n.png", 'Back. Step', self, "Ctrl+P", "Backward step",
                       self.backwardStep, True, IMG_DIR + "/backward_step_p.png")
        self.addAction("&S2S", IMG_DIR + "/update_step_n.png", 'Upd. Step', self, "Ctrl+P", "Update weights step",
                       self.updateWeightStep, True, IMG_DIR + "/update_step_p.png")
        self.toolBar["&S2S"].addSeparator()
        self.addAction("&S2S", IMG_DIR + "/forward_n.png", 'Forward', self, "Ctrl+P", "Forward",
                       self.forward, True, IMG_DIR + "/forward_p.png")
        self.addAction("&S2S", IMG_DIR + "/backward_n.png", 'Backward', self, "Ctrl+P", "Backward",
                       self.backward, True, IMG_DIR + "/backward_p.png")
        self.addAction("&S2S", IMG_DIR + "/update_n.png", 'Update', self, "Ctrl+P", "Update",
                       self.updateWeights, True, IMG_DIR + "/update_p.png")
        self.actionGroup["&S2S"].actions()[0].setCheckable(False)  # forward step   0
        self.actionGroup["&S2S"].actions()[1].setCheckable(False)  # backward step  1
        self.actionGroup["&S2S"].actions()[2].setCheckable(False)  # update step    2
        self.actionGroup["&S2S"].actions()[3].setCheckable(False)  # forward        3
        self.actionGroup["&S2S"].actions()[4].setCheckable(False)  # backward       4
        self.actionGroup["&S2S"].actions()[5].setCheckable(False)  # update         5


    def _createToolbar_ADTool(self):
        self.add_toolbar("&ADTool")
        self.toolBar['&ADTool'].setVisible(False)
        label = QtWidgets.QLabel()
        alpha = u'\u03B1'
        text = '   {} '.format(alpha)
        label.setStyleSheet('font: 20px;')
        label.setText(text)
        label.setToolTip("Alpha represents the update valor")
        self.toolBar["&ADTool"].addWidget(label)
        textEdit = QtWidgets.QLineEdit()
        textEdit.setMaximumSize(60, 30)
        textEdit.setStyleSheet('border-radius: 6px;'
                               'border: 2px solid #b5b5b5;'
                               'padding: 5px;'
                               'color: #b5b5b5;'
                               'background: #545454;')
        textEdit.setText('0.1')
        textEdit.setValidator(QtGui.QDoubleValidator(textEdit))
        self.toolBar["&ADTool"].addWidget(textEdit)
        self.toolBar["&ADTool"].addSeparator()
        self.addAction("&ADTool", IMG_DIR + "/run_n.png", 'Run', self, "Ctrl+P", "Run",
                       self.run, True, IMG_DIR + "/run_p.png")
        self.addAction("&ADTool", IMG_DIR + "/step_n.png", 'By Steps', self, "Ctrl+P", "Step by Step",
                       self.stepToStepView, True, IMG_DIR + "/step_p.png")
        self.toolBar["&ADTool"].addSeparator()
        self.addAction("&ADTool", IMG_DIR + "/edit_n.png", 'Edit View', self, "Ctrl+P", "Edit View",
                       self.design_graph_view, True, IMG_DIR + "/edit_p.png")
        self.toolBar["&ADTool"].addSeparator()
        self.addAction("&ADTool", IMG_DIR + "/tf_n.png", 'TF Code', self,
                      "Ctrl+T", "Generate a .ipynb document in tensorflow code.",
                      self.save_nb_dialog, True, IMG_DIR + "/tf_p.png")
        self.actionGroup["&ADTool"].actions()[0].setCheckable(False)  # Run
        self.actionGroup["&ADTool"].actions()[1].setCheckable(False)  # Step by step
        self.actionGroup["&ADTool"].actions()[2].setCheckable(False)  # Edit View
        return text


    def _createToolbar_CreateGraph(self):
        self.add_menu("&Menu")
        self.addAction("&Menu", IMG_DIR + "/new2.png", 'New', self,
                       "Ctrl+N", "New document", self.newFile, False,
                       IMG_DIR + "/new3.png", True, False)
        self.addAction("&Menu", IMG_DIR + "/open_n.png", 'Open', self,
                       "Ctrl+O", "Open", self.open_file_dialog, False,
                       IMG_DIR + "/open_p.png", True, False)
        self.addAction("&Menu", IMG_DIR + "/save_n.png", 'Save', self,
                       "Ctrl+S", "Save", self.save_file_dialog, False,
                       IMG_DIR + "/save_p.png", True, False)
        self.addAction("&Menu", IMG_DIR + "/undo.png", 'undo', self,
                       "Ctrl+Z",
                       "New document", self.undo, False,
                       IMG_DIR + "/undo.png", True, False)
        self.addAction("&Menu", IMG_DIR + "/redo.png", 'redo', self,
                       "Ctrl+Y",
                       "New document", self.redo, False,
                       IMG_DIR + "/redo.png", True, False)

        self.add_toolbar("&CreateGraph")
        self.addAction("&CreateGraph", IMG_DIR + "/move_n.png", 'Move View', self, "Ctrl+N",
                       "New document", self.viewTranslate, True, IMG_DIR + "/move_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/mouse_n.png", 'Select', self, "Ctrl+N",
                       "Select figures", self.test, True, IMG_DIR + "/mouse_p.png")
        self.toolBar["&CreateGraph"].addSeparator()
        self.toolBar["&CreateGraph"].addSeparator()
        self.addAction("&CreateGraph", IMG_DIR + "/input_n.png", 'Input', self, "Ctrl+I",
                       "Create Input Node", self.creatingADInputNode, True, IMG_DIR + "/input_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/weight_n.png", 'Variable', self, "Ctrl+W",
                       "Create Weight Node", self.creatingADWeightNode, True, IMG_DIR + "/weight_p.png")
        self.toolBar["&CreateGraph"].addSeparator()
        self.addAction("&CreateGraph", IMG_DIR + "/plus_n.png", 'Add', self, "Ctrl+S",
                       "Create Sum Node", self.creatingADSumNode, True, IMG_DIR + "/plus_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/sub_n.png", 'Sub', self, "Ctrl+S",
                       "Create Sub Node", self.creatingADSubNode, True, IMG_DIR + "/sub_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/mul_n.png", 'Multiply', self, "Ctrl+S",
                       "Create Mul Node", self.creatingADMulNode, True, IMG_DIR + "/mul_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/max_n.png", 'Maximum', self, "Ctrl+S",
                       "Create Max Node", self.creatingADMaxNode, True, IMG_DIR + "/max_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/fc_n.png", 'Fully Con.', self, "Ctrl+S", "Create Fully connected node", self.createFullyConnectNode, True, IMG_DIR + "/fc_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/sigmoid_n.png", 'Sigmoid', self, "Ctrl+S",
                       "Create Sig Node", self.creatingADSigNode, True, IMG_DIR + "/sigmoid_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/sigmoid_n.png", 'tanh',
                       self, "Ctrl+S",
                       "Create Tanh Node", self.creatingADTanhNode, True,
                       IMG_DIR + "/sigmoid_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/relu_n.png", 'Relu', self, "Ctrl+S",
                       "Create Relu", self.creatingADReluNode, True, IMG_DIR + "/relu_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/pow2_n.png", 'SE', self,
                       "Ctrl+S", "Create Square Error node", self.createSENode, True,
                       IMG_DIR + "/pow2_p.png")
        self.addAction("&CreateGraph", IMG_DIR + "/pow2_n.png", 'MSE', self,
                       "Ctrl+S", "Create Mean Square Error node", self.createMSENode, True,
                       IMG_DIR + "/pow2_p.png")
        self.toolBar["&CreateGraph"].addSeparator()
        self.addAction("&CreateGraph", IMG_DIR + "/connector_n.png", 'Connector', self, "Ctrl+S",
                       "Create Node Conection", self.creatingADNodeConnectionTool, True, IMG_DIR + "/connector_p.png")
        self.toolBar["&CreateGraph"].addSeparator()
        self.addAction("&CreateGraph", IMG_DIR + "/add_value_n.png", 'Add Value', self, "Ctrl+S", "Add Value",
                       self.selectingNodes, True, IMG_DIR + "/add_value_p.png")
        self.toolBar["&CreateGraph"].addSeparator()
        self.addAction("&CreateGraph", IMG_DIR + "/evaluate_n.png", 'Evaluate', self, "Ctrl+P", "Crear Grafo",
                       self.evaluateNetworkView, True, IMG_DIR + "/evaluate_p.png")


def main():

    app = QtWidgets.QApplication(sys.argv)
    ex = StandardEditor()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()