'''
popup window to select an already started project
Here, "project" means "A couple of VLBI projects opened together"
'''
# --- important libraries ---
from PySide2 import QtCore, QtWidgets, QtGui
from os.path import realpath
from os import walk
from classes.multiple_epochs import multiple_epochs_cl
from ui.my_window import my_window_cl
import sys
# - class -
class project_selector_cl(QtWidgets.QWidget):

    # -- init --
    def __init__(self, app):
        super().__init__()

        self.app = app
        # -- main layout --
        self.layout1 = QtWidgets.QVBoxLayout()
        
        # -- list of opened projects --
        # group box
        self.gblist = QtWidgets.QGroupBox("Opened projects:")
        # group box layout
        self.gblist_layout = QtWidgets.QVBoxLayout(self.gblist)
        # opened projects
        self.opened_projects_list = QtWidgets.QListWidget()

        # -- buttons --
        # hbox layout
        self.layout2 = QtWidgets.QHBoxLayout()
        # buttons
        self.choose_project = QtWidgets.QPushButton("Load project")
        self.discard = QtWidgets.QPushButton("Discard")
        
        # -- LAYOUT MANAGING --
        # -- adding to group box layout -- 
        self.gblist_layout.addWidget(self.opened_projects_list)
        # adding buttons to button layout
        self.layout2.addWidget(self.choose_project)
        self.layout2.addWidget(self.discard)
        # adding list and layout to main layout
        self.layout1.addWidget(self.gblist)
        self.layout1.addItem(self.layout2)

        # setting layout
        self.setLayout(self.layout1)

        # ---- finding root directory --
        self.root_directory, self.projs_path = self.__find_root_directory()

        # connecting buttons
        self.__fill_list_with_selected_projects()

        self.choose_project.clicked.connect(self.__load_selected_project)

        self.discard.clicked.connect(self.__discard_loading_project)

        
    def __find_root_directory(self):
        # -- path to file --
        scr_directory = realpath(__file__)
        # -- searching for root directory --
        tmp = scr_directory.split("/")
        root_directory = ""
        for i in range(len(tmp)-2):
            root_directory = root_directory + tmp[i] + "/"
        
        # -- path directory --
        projs_path = root_directory + "data"

        return root_directory, projs_path

    def __fill_list_with_selected_projects(self):

        # -- dirs in path --
        dirs_in_dir = next( walk ( self.projs_path ), (None, None, [] ) ) [1]
        
        # -- fill list --
        for i in range(len(dirs_in_dir)):
            self.opened_projects_list.addItem(QtWidgets.QListWidgetItem(dirs_in_dir[i]))
        
    # -- loads project from selected directory --
    def __load_selected_project(self):
        # -- getting project directory --
        self.selected_project_directory = self.projs_path + "/" + self.opened_projects_list.currentItem().text()
        # -- listing files from it --
        files_in_dir = next( walk ( self.selected_project_directory ), (None, None, [] ) ) [2]
        for i in range(len(files_in_dir)):
            files_in_dir[i] = self.selected_project_directory + "/" + files_in_dir[i]

        # making "multiple files" class
        self.dw = multiple_epochs_cl()
        self.dw.read_multiple_epochs(files_in_dir, reload=False, first_time=False, append=False)


        # making window with these loaded 
        self.main_window = my_window_cl(self.dw)
        self.main_window.resize(1366,720)
        self.main_window.show()
        self.setVisible(False)

    # -- discards loading and starts gui --
    def __discard_loading_project(self):
        self.main_window = my_window_cl()
        self.main_window.resize(1366,720)
        self.main_window.show()
        self.setVisible(False)