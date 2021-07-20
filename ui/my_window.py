'''
Simple class that holds main window for this app
'''
# -- importng important libraries --
from PySide2 import QtCore, QtWidgets, QtGui
from spot_plot_canvas import mplSpotCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
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
        self.epochlst = list_of_epochs.epochs
        self.epochlst_obj = list_of_epochs

        # -- declaring necessary widgets --
        self.__declare_necessary_widgets()

        # -- setting central widget -
        self.setCentralWidget(self.window)

        # -- filling project list --
        self.__fill_list_of_projects(self.epochlst)
        # -- plotting --
        self.plot_map_of_epoch(0)
        #self.plot_map_of_epoch(1)
        #self.plot_map_of_epoch(4)

        self.connect(self.projects_list, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.__plot_on_list_click)

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

        # -- list of projects --
        self.projects_list = QtWidgets.QListWidget()

        # -- adding list to the group box --
        self.vbox_main.addWidget(self.projects_list)

        # ------- SPOT PLOT -----------
        # -- widget to hold plot widgets --
        self.spot_map_widget = QtWidgets.QWidget(self.window)
        # -- layout for this widget --
        self.spot_map_widget_layout = QtWidgets.QVBoxLayout(self.spot_map_widget)

        # -- declaring canvas --
        self.spot_canvas = mplSpotCanvas(self)
        # -- toolbar --
        self.toolbar_to_spot_canvas = NavigationToolbar(self.spot_canvas, self)
        
        # -- adding theese two to layout --
        self.spot_map_widget_layout.addWidget(self.toolbar_to_spot_canvas)
        self.spot_map_widget_layout.addWidget(self.spot_canvas)
        # ------------------------------

        # ------- BASIC BUTTONS ------
        # load data 
        self.load_button = QtWidgets.QPushButton("Load data files")
        self.reload_button = QtWidgets.QPushButton("Reload")
        self.properties_button = QtWidgets.QPushButton("Plot properties")

        # sizing
        self.load_button.setMaximumSize(10000, 10000)
        self.load_button.setMinimumSize(0, 0)
        self.reload_button.setMaximumSize(10000, 10000)
        self.reload_button.setMinimumSize(0, 0)
        self.properties_button.setMaximumSize(10000, 10000)
        self.properties_button.setMinimumSize(0, 0)

        # group box
        self.buttons_gb = QtWidgets.QGroupBox("Actions")
        # layout
        self.buttons_gb_layout = QtWidgets.QVBoxLayout(self.buttons_gb)

        # layout
        self.buttons_gb_layout.addWidget(self.load_button)
        self.buttons_gb_layout.addWidget(self.reload_button)
        self.buttons_gb_layout.addWidget(self.properties_button)
        # -----------------------------

        # ----- adding widgets to the grid -----
        self.layout.addWidget(self.buttons_gb, 0,0)
        self.layout.addWidget(self.ramka, 1, 0)
        self.layout.addWidget(self.spot_map_widget, 0,1,2,1)

        # -- setting column stretch --
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,3)

        self.layout.setRowStretch(0,3)
        self.layout.setRowStretch(1,1)

    def __plot_on_list_click(self, item):
        # -- searching of the proper epoch --
        # -- by extracting project code --
        txt = item.text()
        tmp = txt.split()
        projcode = tmp[0]
        index = self.epochlst_obj.search_by_proj_code(projcode)

        # -- putting it on the plot --
        self.spot_canvas.spot_plotting_wrapper(self.epochlst[index].dRA, self.epochlst[index].dDEC, self.epochlst[index].velocity, self.epochlst[index].flux_density, label=projcode)


    def plot_map_of_epoch(self, index = 0):
        self.spot_canvas.spot_plotting_wrapper(self.epochlst[index].dRA, self.epochlst[index].dDEC, self.epochlst[index].velocity, self.epochlst[index].flux_density, label=self.epochlst[index].project_code)

    # -- fills project list with proper data --
    def __fill_list_of_projects(self, list_of_projects):
            for i in list_of_projects:
                self.projects_list.addItem(QtWidgets.QListWidgetItem(i.project_code + " Date: " + i.time_string + " PI: " + i.project_pi))