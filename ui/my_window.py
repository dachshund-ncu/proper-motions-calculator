'''
Simple class that holds main window for this app
'''
# -- importng important libraries --
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
# ----------------------------------

# -- main UI class --
class my_window_cl(QtWidgets.QWidget):
    
    # -- init --
    def __init__(self, list_of_epochs):
        super().__init__()

        self.buttons = []
        
        for i in list_of_epochs:
            self.buttons.append(QtWidgets.QPushButton(str(i.mjd)))

        self.layout = QtWidgets.QVBoxLayout(self)

        for i in self.buttons:
            self.layout.addWidget(i)