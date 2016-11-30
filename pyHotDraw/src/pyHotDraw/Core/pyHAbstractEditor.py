'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHDiamondFigure import pyHDiamondFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Figures.pyHImageFigure import pyHCameraFigure
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Figures.pyHImageFigure import pyHImageFigure
from pyHotDraw.Figures.pyHConnectionFigure import pyHConnectionFigure
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure
from pyHotDraw.Tools.pyHCreationTool import pyHCreationTool
from pyHotDraw.Tools.pyHCreationImageTool import pyHCreationImageTool
from pyHotDraw.Tools.pyHPolylineCreationTool import pyHPolylineCreationTool
from pyHotDraw.Tools.pyHLineCreationTool import pyHLineCreationTool
from pyHotDraw.Tools.pyHSplineCreationTool import pyHSplineCreationTool
from pyHotDraw.Tools.pyHSelectionTool import pyHSelectionTool
from pyHotDraw.Tools.pyHViewTranslationTool import pyHViewTranslationTool
from pyHotDraw.Tools import pyHConnectionImageTool.pyHConnectionTool
from pyHotDraw.Tools.pyHConnectionImageFilterTool import pyHConnectionImageFilterTool

class pyHAbstractEditor(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.menuBar=self.createMenuBar()
        self.menu={}
        self.toolBar={}
        self.actionGroup={}
        self.clipBoard=[]
#Abstract to redefine
    def createMenuBar(self):
        pass
    #Each menu as a associated a toolbar and a name
    def addMenuAndToolBar(self,name):
        pass
    def addAction(self,icon,name,container,sortCut,statustip,connect):
        pass
    def copy(self):
        self.clipBoard=[]
        v=self.getView()
        s=v.getSelectedFigures()
        for f in s:
            self.clipBoard.append(f)
    def cut(self):
        self.copy()
        v=self.getView()
        s=v.getSelectedFigures()
        for f in self.clipBoard:
            s.remove(f)
            v.getDrawing().removeFigure(f)
        v.update()
    def paste(self):
        v=self.getView()
        s=v.getSelectedFigures()
        for f in self.clipBoard:
            v.getDrawing().addFigure(f)
        v.update()
    def setCreationTool(self,t):
        self.currentTool=t
    def setSelectionTool(self,t):
        self.currentTool=t
    def setCurrentTool(self,t):
        self.currentTool=t
    def getCurrentTool(self):
        return self.currentTool
    def setView(self,v):
        self.view=v
    def getView(self):
        return self.view
    
    def jointPolylinesLast(self,f0,f1):
        p1=f1.getPoints()
        f0.getPoints().extend(p1[1:])
    def touches(self,p0,p1):
        return p0.distance(p1)<1.0
    def jointPolyline(self,f0,selectedFigures):
        changed=True
        while changed:
            changed=False
            toRemove=[]
            for f1 in selectedFigures:
                p0f=f0.getFirstPoint()
                p0l=f0.getLastPoint()
                p1f=f1.getFirstPoint()
                p1l=f1.getLastPoint()
                if self.touches(p0l,p1f):
                    self.jointPolylinesLast(f0,f1)
                    toRemove.append(f1)
                    changed=True
                if self.touches(p0f,p1l):
                    f0.reversePoints()
                    f1.reversePoints()
                    self.jointPolylinesLast(f0,f1)
                    toRemove.append(f1)
                    changed=True
                if self.touches(p0l,p1l):
                    f1.reversePoints()
                    self.jointPolylinesLast(f0,f1)
                    toRemove.append(f1)
                    changed=True
                if self.touches(p0f,p1f):
                    f0.reversePoints()
                    self.jointPolylinesLast(f0,f1)
                    toRemove.append(f1)
                    changed=True
            for f in toRemove:
                selectedFigures.remove(f)
                self.getView().getDrawing().removeFigure(f)
    def join(self):
        v=self.getView()
        selectedFigures=v.getSelectedFigures()
        f0=selectedFigures[0]
        selectedFigures.remove(f0)
        self.jointPolyline(f0,selectedFigures)
        selectedFigures.append(f0)
        v.update()
    def selectionGroup(self):
        v=self.getView()
        selectedFigures=v.getSelectedFigures()
        g=pyHCompositeFigure()
        for f in selectedFigures:
            g.addFigure(f)
        for f in g.getFigures():
            v.getDrawing().removeFigure(f)
            selectedFigures.remove(f)
        if g.getFigures():
            v.selectFigure(g)
            v.getDrawing().addFigure(g)
            #v.update()
    def selectionUngroup(self):
        v=self.getView()
        fts=[]
        frs=[]
        selectedF=v.getSelectedFigures()
        for fs in selectedF:
            if isinstance(fs,pyHCompositeFigure):
                for f in fs.getFigures():
                    fts.append(f)
                    v.getDrawing().addFigure(f)
                frs.append(fs)
                v.getDrawing().removeFigure(fs)
        for f in frs:
            selectedF.remove(f)
        for f in fts:
            v.selectFigure(f)
        #v.update()
    def moveFront(self):
        v=self.getView()
        selectedFigures=v.getSelectedFigures()
        for f in selectedFigures:
            v.getDrawing().removeFigure(f)
            v.getDrawing().addFigure(f)
    def moveBack(self):
        v=self.getView()
        selectedFigures=v.getSelectedFigures()
        for f in selectedFigures:
            v.getDrawing().removeFigure(f)
            v.getDrawing().getFigures().insert(0,f)
    def selectingFigures(self):
        self.setCurrentTool(pyHSelectionTool(self.getView()))
    def creatingLineConnection(self):
        self.setCurrentTool(pyHConnectionImageTool(self.getView(),pyHConnectionFigure()))
    def creatingLineImageFilterConnection(self):
        self.setCurrentTool(pyHConnectionImageFilterTool(self.getView(),pyHConnectionFigure()))
    def creatingRectangle(self):
        self.setCurrentTool(pyHCreationTool(self.getView(),pyHRectangleFigure(0,0,2,2)))
    def creatingDiamond(self):
        self.setCurrentTool(pyHCreationTool(self.getView(),pyHDiamondFigure(0,0,2,2)))
    def creatingEllipse(self):
        self.setCurrentTool(pyHCreationTool(self.getView(),pyHEllipseFigure(0,0,2,2)))
    def creatingImage(self):
        self.setCurrentTool(pyHCreationImageTool(self.getView()))
    def creatingCamera(self):
        self.setCurrentTool(pyHCreationTool(self.getView(),pyHCameraFigure(0,0)))
    def creatingPolyline(self):
        self.setCurrentTool(pyHPolylineCreationTool(self.getView()))
    def creatingLine(self):
        self.setCurrentTool(pyHLineCreationTool(self.getView()))
    def creatingSpline(self):
        self.setCurrentTool(pyHSplineCreationTool(self.getView()))
    def viewTranslate(self):
        self.setCurrentTool(pyHViewTranslationTool(self.getView()))

        