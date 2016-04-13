'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Core.Exceptions import pyHHandleNotFound,pyHFigureNotFound
from pyHotDraw.Tools.pyHAreaSelectionTool import pyHAreaSelectionTool
from pyHotDraw.Tools.pyHAbstractTool import pyHAbstractTool
from pyHotDraw.Tools.pyHFigureMoveTool import pyHFigureMoveTool

class pyHSelectionTool(object):
    '''
    classdocs
    '''
    def __init__(self,v):
        '''
        Constructor
        '''
        self.view=v
    def getView(self):
        return self.view
    def onMouseDown(self,e):
        p=pyHPoint(e.getX(),e.getY())
        try:
            h=self.view.findHandle(p)
            print "handle encontrado"
            self.delegateTool=h
        except (pyHHandleNotFound):
            try:
                f=self.view.findFigure(p)
                if not self.view.isThisFigureInSelectedFigures(f):
                    self.getView().clearSelectedFigures()
                    self.getView().selectFigure(f)
                    print "figura encontrada"
                    self.delegateTool=pyHFigureMoveTool(self.view)
                else:
                    print "figura deseleccionada"
                    self.getView().getSelectionFigure().removeFigure(f)
                    self.delegateTool=pyHAbstractTool(self.view)
            except (pyHFigureNotFound):
                print "seleccionando Area"
                self.delegateTool=pyHAreaSelectionTool(self.view)
        self.delegateTool.onMouseDown(e)
    def onMouseUp(self,e):
        self.delegateTool.onMouseUp(e)
    def onMouseMove(self,e):
        self.delegateTool.onMouseMove(e)
    def onMouseDobleClick(self,e):
        #Not delegation is done
        v=self.getView()
        p=pyHPoint(e.getX(),e.getY())
        try:
            f=v.findFigure(p)
            if not self.view.isThisFigureInSelectedFigures(f):
                r=f.getDisplayBox()
            else:
                r=v.getSelectionFigure().getDisplayBox()
            v.setTransformFitToRectangle(r)
        except (pyHFigureNotFound):
            v.setTransformFitToDrawing()
    def onMouseWheel(self,e):
        self.delegateTool.onMouseWheel(e)
    def onKeyPressed(self,e):
        for f in self.getView().getSelectedFigures():
            self.getView().getDrawing().removeFigure(f)
        self.delegateTool.onKeyPressed(e)