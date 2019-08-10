from MiniTensorFlow.qt.pyHSetADValueDialog import pyHSetADValueDialog
from pyHotDraw.Core.Exceptions import pyHFigureNotFound
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor
from pyHotDraw.Geom.pyHPoint import pyHPoint
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure

from MiniTensorFlow.qt.AssignValuesDialog import AssignValuesDialog
class pyHADAssignValuesTool(object):
    '''
    classdocs
    '''

    def __init__(self, v):
        '''
        Constructor
        '''
        self.view = v
        self.getView().clearSelectedFigures()

    def getView(self):
        return self.view

    def onMouseDown(self, e):
        pass

    def onMouseUp(self, e):
        pass

    def onMouseMove(self, e):
        pass

    def onMouseDobleClick(self, e):
        if e.isLeftClick():
            actual_value = self.getView()
            p = pyHPoint(e.getX(), e.getY())

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


    def onMouseWheel(self, e):
        pass

    def onKeyPressed(self, e):
        pass