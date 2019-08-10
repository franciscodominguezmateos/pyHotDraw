#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/03/2013

@author: paco
'''

import pickle
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from MiniTensorFlow.Tools.pyHADAssignValuesTool import pyHADAssignValuesTool
from pyHotDraw.Core.Qt.pyHStandardView import pyHStandardView
from pyHotDraw.Core.pyHAbstractEditor import pyHAbstractEditor


class pyHStandardEditor(QtWidgets.QMainWindow,pyHAbstractEditor):
    def __init__(self):
        super(pyHStandardEditor, self).__init__()
        pyHAbstractEditor.__init__(self)
        self.initActionMenuToolBars()
        self.statusBar()
        self.initUI()



    # Redefinning abstract method
    def _createMenuBar(self):
        return QtWidgets.QMainWindow.menuBar(self)


    def addMenuAndToolBar(self, name):
        self.menu[name] = self.menuBar.addMenu(name)
        self.toolBar[name] = self.addToolBar(name)
        self.actionGroup[name] = QtGui.QActionGroup(self)



    def addAction(self,
                  menuName,
                  icon_n,
                  name,
                  container,
                  sortCut,
                  statusTip,
                  connect,
                  addToActionGroup,
                  icon_s,
                  add_to_menu=False,
                  add_to_toolbar=True):
        a = QtWidgets.QAction(name, container)
        # a.setText(name)
        a.setObjectName(name)
        a.setShortcut(sortCut)
        a.setToolTip(statusTip)
        a.triggered.connect(connect)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_n), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        if icon_s:
            selected_icon = QtGui.QPixmap(icon_s)
            icon.addPixmap(selected_icon, QtGui.QIcon.Selected)
            icon.addPixmap(selected_icon, QtGui.QIcon.Normal, QtGui.QIcon.On)
            icon.addPixmap(selected_icon, QtGui.QIcon.Active)

        a.setIcon(icon)

        if addToActionGroup:
            a.setCheckable(True)
            self.actionGroup[menuName].addAction(a)

        if add_to_menu:
            self.menu[menuName].addAction(a)
        if add_to_toolbar:
            self.toolBar[menuName].addAction(a)




    def initActionMenuToolBars(self):
        pass



    def onScaleChanged(self, index):
        s = float(index)
        t = self.getView().getTransform()
        t.sx = s + 0.50
        t.sy = s + 0.50
        self.getView().update()

    def newFile(self):
        self.getView().getDrawing().clearFigures()
        self.getView().clearSelectedFigures()
        self.getView().update()

    def openFile(self):
        self.getView().getDrawing().clearFigures()
        fileNames = QtGui.QFileDialog.getOpenFileName(self, ("Open Image"), QtCore.QDir.currentPath(),
                                                      ("Image Files (*.dxf)"))
        if not fileNames:
            fileName = "C:\\Users\\paco\\Desktop\\a4x2laser.dxf"
        else:
            fileName = fileNames[0]
        self.openDXF(fileName)
        self.getView().update()

    def initUI(self):
        self.setGeometry(300, 30, 100, 100)
        self.setWindowTitle('pyHotDraw')
        self.sb = QtWidgets.QLabel(self)
        self.sb.setText("x=0,y=0")
        self.statusBar().addPermanentWidget(self.sb)
        # self.sb1=QtGui.QLabel(self)


        self.setView(pyHStandardView(self))

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(self.getView())

        self.setCentralWidget(self.getView())
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = pyHStandardEditor()

    # ex.timeElapsed = dt.datetime.now()
    # ex.openDXF("a4x2laser.dxf")
    # puertos_disponibles=scan(num_ports=20,verbose=True)
    # ex.openPLT("a4x2laser.plt")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()