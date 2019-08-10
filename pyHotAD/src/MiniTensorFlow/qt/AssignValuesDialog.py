#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from MiniTensorFlow.figures.MathTextFigure import is_math_text
from MiniTensorFlow.microtensorflow.Variable import Variable
import numpy as np
import sys


class AssignValuesDialog(QDialog):
    def __init__(self,
                 parent=None,
                 actual_name='',
                 actual_value='',
                 name_editabe=True):

        super(AssignValuesDialog, self).__init__(
            parent, QtCore.Qt.FramelessWindowHint)

        self._label_name          = QLabel('Label', self)
        self._label_value         = QLabel('Value', self)
        self._label_max_dimension = QLabel('(max 4x4)', self)

        self._name_field    = QLineEdit(actual_name, self)
        self._name_field.setReadOnly(not name_editabe)
        actual_value = self._matrix_to_string(actual_value)
        self._value_field   = QTextEdit(actual_value, self)
        self._accept_button = QPushButton('Accept', self)
        self._cancel_button = QPushButton('Cancel', self)

        self.initUI()

    def initUI(self):
        self._config_labels()
        self._config_fields()
        self._config_buttons()

        self.setContentsMargins(20, 10, 20, -10)
        layout = self._create_layout(self)
        self.setStyleSheet(STYLE)
        self.setLayout(layout)


    def _create_layout(self, parent):
        layout = QVBoxLayout(parent)
        info_layout = self._create_info_layout()
        buttoms_layout = self._create_options_layout()
        layout.addLayout(info_layout, 0)
        layout.addLayout(buttoms_layout, 1)

        return layout

    def _create_info_layout(self):
        grid_layout = QGridLayout()
        grid_layout.addWidget(self._label_name, 0, 0)
        grid_layout.addWidget(self._label_value, 1, 0, QtCore.Qt.AlignBottom)
        grid_layout.addWidget(self._label_max_dimension, 2, 0,
                              QtCore.Qt.AlignTop)
        grid_layout.addWidget(self._name_field, 0, 1)
        grid_layout.addWidget(self._value_field, 1, 1, 2, 1)
        return grid_layout

    def _create_options_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 20, 0, 20)
        layout.addWidget(self._accept_button, 0)
        layout.addSpacing(20)
        layout.addWidget(self._cancel_button, 1)

        return layout



    def _config_labels(self):
        self._label_name.setFixedSize(60, 32)
        self._label_value.setFixedSize(60, 32)
        self._label_max_dimension.setFixedSize(60, 32)

        self._set_font_style(self._label_name)
        self._set_font_style(self._label_value)
        self._label_max_dimension.setStyleSheet(self.styleSheet() +
                                               'font-size: 11px;'
                                               'font-style: italic;')

    def _config_fields(self):
        self._name_field.setFixedSize(122, 32)
        self._value_field.setFixedSize(122, 70)
        self._value_field.setAcceptRichText(False)
        self._value_field.setTabChangesFocus(True)

    def _config_buttons(self):
        self._accept_button.setDefault(True)
        self._accept_button.clicked.connect(self.COMPROBAR_CAMPOS)

        self._cancel_button.clicked.connect(self.reject)

    @staticmethod
    def _set_font_style(widget):
        style = widget.styleSheet()
        style += 'font: 18px bold;'
        widget.setStyleSheet(style)

    # Cerrar el dialog si se pierde el foco
    def eventFilter(self, obj, event):
        """Cierra automáticamente la ventana si se pierde el foco.

        """
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.close()
            self.reject() # ?
            return True
        return False


    def validateText(self):
        v = str(self.leV.text())
        l = str(self.leL.text())
        try:
            if v is not '':
                self.value = float(v)
            else:

                self.value = None
            self.label = l
            self.accept()

        except ValueError:
            self.leV.selectAll()

    @staticmethod
    def _matrix_to_string(value):
        if value is not None and isinstance(value, np.matrix):
            rows, columns = value.shape
            representation = ''
            aux_array = value.A
            for r in range(rows):
                for c in range(columns):
                    element = aux_array[r][c]
                    representation += '{:g}, '.format(element)
                representation = representation[:-2] + ';\n'
            return representation[:-2]
        return ''


    def get_value(self):
        value = self._value_field.toPlainText()
        return value if value else None

    def get_name(self):
        name = str(self._name_field.text())
        return name if name else '\ '

    @staticmethod
    def set_label_style(label):
        style = 'font: 18px bold;'
        label.setStyleSheet(style)


    def COMPROBAR_CAMPOS(self):
        error_in_name = False
        if self._name_field.isModified():
            error_in_name = not self._check_name()
            if error_in_name:
                self._set_error_color(self._label_name)
            else:
                self._set_normal_color(self._label_name)

        error_in_value = False
        if self._value_field.document().isModified():
            error_in_value = not self._check_value()
            if error_in_value:
                self._set_error_color(self._label_value)
            else:
                self._set_normal_color(self._label_value)

        if not error_in_name and not error_in_value:
            return self.accept()


    def _check_name(self):
        name = str(self._name_field.text())
        name_to_math = '$ {} $'.format(name)
        return is_math_text(name_to_math)

    def _check_value(self):
        """
        True-> Ok
        False-> Error
        :return: bool
        """
        value = str(self._value_field.toPlainText())
        if value=='': return True
        ACCEPTABLES_CHARS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                             '.', ',', ';', ' ', '\n', '-')

        for char in value:
            if not char in ACCEPTABLES_CHARS:
                return False
        if Variable.is_acceptable_arg(value):
            rows, columns = np.matrix(value).shape
            return 1 <= rows <= 4 and 1 <= columns <= 4
        else:
            return False

    def _set_error_color(self, label):
        print(label.styleSheet())
        style = label.styleSheet() + 'color: red;'
        label.setStyleSheet(style)

    def _set_normal_color(self, label):
        style = label.styleSheet() + 'color: white;'
        label.setStyleSheet(style)

STYLE = """
/* #b5b5b5 */

QDialog{
   background: #263238;
   color: #fff;}


QPushButton{
    color: #FFFFFF;
    font: bold;
    font-size: 13px;
    border: 2px solid #FFFFFF;
    border-radius: 6px;
    padding: 3px;
    width: 70px;
    height: 25px;}


QPushButton:hover{
    background: #616161;}


QPushButton:checked, QToolButton:pressed{
    background: #262626;}


QLabel{
    font: 14px bold;
    color: #FFFFFF;
}
QLineEdit{
    border-radius: 6px;
    border: 2px solid #FFFFFF;
    padding: 5px;
    color: #FFFFFF;
    /* background: #545454; */
    background: #4F6773;
    font: bold;

}
QTextEdit{
    font: bold;
    border-radius: 6px;
    border: 2px solid #FFFFFF;
    padding: 5px;
    color: #FFFFFF;
    background: #4F6773;
    font-size: 12px;
}
"""




"""
app = QApplication(sys.argv)
test = AssignValuesDialog(None, "x_0")

if test.exec():
    print('accept')
else:
    print('reject')
sys.exit(app.exec_())
"""