from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

import os, sys

class Window(QDialog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("graphical_panel/Ui_close_popup.ui", self)
        self.setWindowTitle("Input")
        self.success_int = 1
        self.failure_int = 1
        self.note = "def"
        # self.save_and_close_pushButton.clicked.connect(lambda: self.save_and_exit())
        self.save_and_close_pushButton.clicked.connect(self.close)
        self.show()

    def return_strings(self):
        #   Return list of values. It need map with str (self.lineedit.text() will return QString)
        self.success_int = 1 if self.success_radioButton.isChecked() > 0 else 0
        self.failure_int = 1 if self.failure_radioButton.isChecked() > 0 else 0
        return map(str, [str(self.success_int), str(self.failure_int),  self.note_lineEdit.text()])

    @staticmethod
    def get_data():
        dialog = Window()
        dialog.exec_()
        return dialog.return_strings()
