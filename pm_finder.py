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
from multiple_epochs import multiple_epochs_cl
from my_window import my_window_cl
# --------------------------

# -- creating list of files --
spots_path = scr_directory + "examples/CepA/"

files_in_dir = next( walk( spots_path ), ( None, None, [] ) ) [2]
for i in range(len(files_in_dir)):
    files_in_dir[i] = spots_path + files_in_dir[i]


# -- creating multiple epochs --
dw = multiple_epochs_cl()
dw.read_multiple_epochs(files_in_dir)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = my_window_cl(dw)
    widget.resize(1366,720)
    widget.show()

    sys.exit(app.exec_())