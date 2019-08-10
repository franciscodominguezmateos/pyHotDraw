#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np


class pyHSetADValueDialog(QtWidgets.QDialog):

    def __init__(self, parent, actual_value, actual_label):
        super(pyHSetADValueDialog, self).__init__(parent) #, QtCore.Qt.FramelessWindowHint
        self.info_label = QtWidgets.QLabel(self)
        self.value_label = QtWidgets.QLabel(self)
        self.value_field = QtWidgets.QTextEdit(self)
        self.label_label = QtWidgets.QLabel(self)


        self.label_field = QtWidgets.QLineEdit(self)
        self._value = actual_value
        self._label = actual_label
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Set Node Value')
        self.resize(230, 165)

        p = self.palette()
        p.setColor(QtGui.QPalette().Background, QtGui.QColor(255, 255, 255))
        self.setPalette(p)


        # label Label
        self.label_label.setText("Label")
        self.label_label.move(20, 20)

        # Text Box Label
        self.label_field.resize(110, 32)
        self.label_field.move(90, 15)
        self.label_field.setText(self._label)

        # label Value
        self.value_label.setText("Value")
        self.value_label.move(20, 65)

        self.info_label.setText("(max 3x3)")
        self.info_label.move(20, 90)
        self.info_label.setStyleSheet('font-size: 11px;'
                                      'font-style: italic;')

        # Text Box Value
        self.value_field.resize(110, 90)
        self.value_field.move(90, 60)
        self.value_field.setText(str(self._value))

        self.setWidgetStyle(self.label_label)
        self.setWidgetStyle(self.value_label)

        # Evento Dialog al pulsar "Enter"
        #self.value_field.connect(self.validateText)
        self.label_field.returnPressed.connect(self.validateText)

        # Evento al perder el foco del dialog
        self.installEventFilter(self)

        self.show()


    def eventFilter(self, obj, event):
        """
        Cierra automáticamente la ventana si se pierde el foco.
        """
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.close()
            return True
        return False


    def validateText(self):
        v = str(self.value_field.text())
        l = str(self.label_field.text())
        try:
            self._value = self.accept_value(v)
            self._label = l if l else '\ '
            self.accept()

        except ValueError:
            self.value_field.selectAll()

    def accept_value(self, value):
        try:
            np.array(value, np.float64)
            return value
        except ValueError:
            return None

    def getValue(self):
        return self._value

    def getLabel(self):
        return self._label


    def setWidgetStyle(self, w):
        style = 'font: 18px bold;'
        w.setStyleSheet(style)

"""
app = QtGui.QApplication(sys.argv)
test = pyHSetADValueDialog(None, "x_0", "12")



#l.setCentralWidget(test)

test.show()

sys.exit(app.exec_())
"""
