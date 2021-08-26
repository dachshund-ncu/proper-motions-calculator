#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------
# -- importing important libraries --
# --- STANDARD LIBRARIES ---
import sys
from numpy import loadtxt
from os import walk, getcwd
from os.path import realpath
from PySide2 import QtCore, QtWidgets, QtGui
# --------------------------

# --------------------------
# --- CUSTOM CLASSES ---
# -- finding absolute path of the script --
scr_directory = realpath(__file__)
tmp = scr_directory.split("/")
scr_directory = ""
for i in range(len(tmp)-1):
    scr_directory = scr_directory + tmp[i] + "/"
# -- adding directories to path --
sys.path.append(scr_directory + 'classes')
sys.path.append(scr_directory + 'ui')
# -- importing my super classes --
from project_selector import project_selector_cl
# --------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget2 = project_selector_cl(app)
    widget2.resize(800,600)
    widget2.show()
    
    app.exec_()