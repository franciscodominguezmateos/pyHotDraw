
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sys

class pyHQTError(QtWidgets.QMessageBox):
    def __init__(self, mensagge=None, description_mensagge=None, detailed_mensagge=None):
        QtWidgets.QMessageBox.__init__(self)

        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.mensagge = str(mensagge) if mensagge else ''
        self.description_mensagge = str(description_mensagge) if description_mensagge else ''
        self.detailed_mensagge = str(detailed_mensagge) if detailed_mensagge else ''
        self.setWindowTitle('Error')
        self.setStyleSheet("QLabel{font: bold 20px;} QPushButton{ width:120px; font-size: 15px; }")

    def showDialog(self):
        if self.mensagge: self.setText(self.mensagge)
        if self.description_mensagge: self.setInformativeText(self.description_mensagge)
        if self.detailed_mensagge: self.setDetailedText(self.detailed_mensagge)
        self.exec()

"""
app = QApplication(sys.argv)
e = pyHQTError('Se produjo un error al generar la información del grafo.',
               detailed_mensagge='- No existe ningún nodo entrada.\n'
                                 '- Existe nodos sin inicializar.\n')
e.showDialog()
sys.exit(app.exec_())
"""