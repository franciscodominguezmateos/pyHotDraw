'''
Created on

@author: javi
'''
from MiniTensorFlow.figures.pyHRemoveFiguresDecorator import pyHRemoveFiguresDecorator
from pyHotDraw.Core.Exceptions import pyHFigureNotFound, pyHHandleNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Tools.pyHAbstractTool import pyHAbstractTool
from pyHotDraw.Tools.pyHAreaSelectionTool import pyHAreaSelectionTool
from pyHotDraw.Tools.pyHFigureMoveTool import pyHFigureMoveTool
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor
from MiniTensorFlow.qt.AssignValuesDialog import AssignValuesDialog


class pyHSelectNodesTool(object):
    '''
    classdocs
    '''
    def __init__(self,v):
        '''
        Constructor
        '''
        self.view=v
        self.delegateTool = pyHAbstractTool(self.view)

    def getView(self):
        return self.view


    def onMouseDown(self,e):
        p=pyHPoint(e.getX(),e.getY())
        try:
            h = self.view.findHandle(p)
            self.delegateTool = h

        except (pyHHandleNotFound):
            try:
                f=self.view.findFigure(p)

                if not self.view.isThisFigureInSelectedFigures(f):
                    self.getView().clearSelectedFigures()
                    self.getView().selectFigure(f)


                self.delegateTool= pyHFigureMoveTool(self.view)

            except pyHFigureNotFound:
                self.getView().clearSelectedFigures()
                self.delegateTool=pyHAreaSelectionTool(self.view)

        self.delegateTool.onMouseDown(e)


    def onMouseUp(self,e):
        self.delegateTool.onMouseUp(e)
        self.delegateTool = pyHAbstractTool(self.view)


    def onMouseMove(self,e):
        self.delegateTool.onMouseMove(e)

    # add
    def onMouseDobleClick(self,e):
        if e.isLeftClick():
            actual_value = self.getView()
            p = pyHPoint(e.getX(), e.getY())
            try:
                h = self.view.findHandle(p)
                self.delegateTool = h

            except (pyHHandleNotFound):
                try:
                    figure = actual_value.findFigure(p)
                    if isinstance(figure, NodeFigure):
                        if figure.is_input():
                            container_figure = figure.figures[0]
                            color = container_figure.getAttribute('COLOR')
                            container_figure.setColor(
                                pyHAttributeColor(90, 90, 90, 255))

                            node = figure.get_node()
                            actual_value = node.getValue() if node else ""
                            dialog = AssignValuesDialog(self.getView(),
                                                        figure.get_text(),
                                                        actual_value)

                            pos = self.getView().cursor().pos()
                            dialog.move(pos.x() + 30, pos.y() - 70)

                            if dialog.exec():
                                actual_value = dialog.get_value()
                                if actual_value:
                                    figure.setValue(actual_value)

                                figure.set_text(dialog.get_name())

                            container_figure.setColor(color)


                except pyHFigureNotFound:
                    pass
            self.delegateTool.onMouseDobleClick(e)

    def onMouseWheel(self,e):
        self.delegateTool.onMouseWheel(e)

    def onKeyPressed(self,e):
        if e.isDelKey():
            drawing = self.getView().getDrawing()

            selected_figures = self.getView().getSelectedFigures()
            remove_tool = pyHRemoveFiguresDecorator(drawing, selected_figures)
            remove_tool.removeFigures()

            self.getView().clearSelectedFigures()
            self.delegateTool.onKeyPressed(e)
