'''
Simple class that holds main window for this app
'''
# -- importng important libraries --
import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui

from spot_plot_canvas import mplSpotCanvas

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
# ----------------------------------

# -- main UI class --
class my_window_cl(QtWidgets.QMainWindow):
    
    # -- init --
    def __init__(self, list_of_epochs):
        super().__init__()

        # -- for accesing data later --
        self.epochlst = list_of_epochs

        # -- declaring necessary widgets --
        self.__declare_necessary_widgets()

        # -- setting central widget -
        self.setCentralWidget(self.window)

        # -- plotting --
        self.plot_map_of_epoch(0)
        #self.plot_map_of_epoch(1)
        #self.plot_map_of_epoch(4)

        self.projects_list.itemClicked.connect(self.__plot_on_list_click)

    def __declare_necessary_widgets(self):
        # -- main widget --
        self.window = QtWidgets.QWidget(self)
        # -- its layout --
        self.layout = QtWidgets.QGridLayout(self.window)

        # -- left-hand vertical layout --
        self.vbox_main = QtWidgets.QVBoxLayout()
        # -- group box for this --
        self.ramka = QtWidgets.QGroupBox("Projects loaded")
        # -- setting layout for group box --
        self.ramka.setLayout(self.vbox_main)
        # -- adding group box to the main layout --
        self.layout.addWidget(self.ramka, 0, 0)
        # -- list of projects --
        self.projects_list = QtWidgets.QListWidget()
        for i in self.epochlst:
            self.projects_list.addItem(QtWidgets.QListWidgetItem(i.project_code + " Date: " + i.time_string + " PI: " + i.project_pi))

        # -- adding list to the group box --
        self.vbox_main.addWidget(self.projects_list)

        # -- declaring canvas --
        self.spot_canvas = mplSpotCanvas(self)
        # -- adding spot canvas to the grid --
        self.layout.addWidget(self.spot_canvas, 0,1)

        # -- setting column stretch --
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,2)

    def __plot_on_list_click(self):
        print("AESAAAASE")


    def plot_map_of_epoch(self, index = 0):
        self.spot_canvas.axes.clear()
        self.spot_canvas.axes.plot(self.epochlst[index].dRA, self.epochlst[index].dDEC, ls="", marker="o", c='red')

    