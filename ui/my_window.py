'''
Simple class that holds main window for this app
'''
# -- importng important libraries --
from classes.multiple_epochs import multiple_epochs_cl
from PySide2 import QtCore, QtWidgets, QtGui
from spot_plot_canvas import mplSpotCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from os import getcwd
import matplotlib
import matplotlib.pyplot as plt
from numpy import searchsorted

matplotlib.use('Qt5Agg')
# ----------------------------------

# -- main UI class --
class my_window_cl(QtWidgets.QMainWindow):
    
    # -- init --
    def __init__(self, list_of_epochs = "None"):
        super().__init__()
        
        # -- declaring necessary widgets --
        self.__declare_necessary_widgets()

        # -- setting central widget -
        self.setCentralWidget(self.window)
        
        # -- connecting to slots --
        self.__connect_to_slots()
        
        if list_of_epochs != "None":
            # -- for accesing data later --
            self.epochlst_obj = list_of_epochs
            if len(self.epochlst_obj.epochs) > 0:
                # -- filling project list --
                self.__fill_list_of_projects(self.epochlst_obj.epochs)
                # -- plotting --
                self.spot_canvas.add_plots_to_canvas(self.epochlst_obj)
                # -- index --
                self.chosen_project_index = 0
                self.projects_list.setCurrentRow(self.chosen_project_index)
                self.plot_map_of_epoch(self.chosen_project_index)

        

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
        
        # ---- setting up diffrent sections ----
        self.__set_up_basic_buttons()
        self.__set_cloudet_part_widget()

        # ----- adding widgets to the grid -----
        self.layout.addWidget(self.buttons_gb, 0, 0)
        #self.layout.addWidget(self.cloudet_bar_gb, 0, 1, 1, 1)
        self.layout.addWidget(self.tab_widget_cl_sp, 0, 1, 2, 1)
        #self.layout.addWidget(self.list_of_cloudets_gb, 1, 1, 1, 1)
        self.layout.addWidget(self.ramka, 1, 0)
        self.layout.addWidget(self.spot_map_widget, 0, 2, 2, 1)

        # -- setting column stretch --
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,1)
        self.layout.setColumnStretch(2,3)

        self.layout.setRowStretch(0,1)
        self.layout.setRowStretch(1,1)

    def __set_up_basic_buttons(self):

        # ------- BASIC BUTTONS ------
        # load data 
        self.load_button = QtWidgets.QPushButton("Load data files")
        self.reload_button = QtWidgets.QPushButton("Reload")
        self.properties_button = QtWidgets.QPushButton("Plot properties")
        self.spot_plot_button = QtWidgets.QPushButton("Spot plot")
        self.proper_motions = QtWidgets.QPushButton("Proper motions")
        self.append_load_button = QtWidgets.QPushButton("Load files (append mode)")

        # sizing
        self.load_button.setMaximumSize(10000, 10000)
        self.load_button.setMinimumSize(0, 0)
        self.append_load_button.setMaximumSize(10000, 10000)
        self.append_load_button.setMinimumSize(0, 0)
        self.reload_button.setMaximumSize(10000, 10000)
        self.reload_button.setMinimumSize(0, 0)
        self.properties_button.setMaximumSize(10000, 10000)
        self.properties_button.setMinimumSize(0, 0)
        self.spot_plot_button.setMaximumSize(10000, 10000)
        self.spot_plot_button.setMinimumSize(0, 0)
        self.proper_motions.setMaximumSize(10000, 10000)
        self.proper_motions.setMinimumSize(0, 0)

        # group box
        self.buttons_gb = QtWidgets.QGroupBox("Actions")
        # layout
        self.buttons_gb_layout = QtWidgets.QVBoxLayout(self.buttons_gb)

        # layout
        self.buttons_gb_layout.addWidget(self.load_button)
        self.buttons_gb_layout.addWidget(self.append_load_button)
        self.buttons_gb_layout.addWidget(self.reload_button)
        self.buttons_gb_layout.addWidget(self.properties_button)
        self.buttons_gb_layout.addWidget(self.spot_plot_button)
        self.buttons_gb_layout.addWidget(self.proper_motions)

        # setting down "spot_plot_button"
        self.spot_plot_button.setDown(True)
        # -----------------------------
    
    # -- setting cloudet part widgets --
    def __set_cloudet_part_widget(self):
        # ------- CLOUDET PART WIDGET ------
        # qtab
        self.tab_widget_cl_sp = QtWidgets.QTabWidget(self.window)
        # adding tabs to Qtab

        # widget over everything
        self.cloudet_bar_widget = QtWidgets.QWidget(self.window)
        # layout
        self.cloudet_bar_widget_vbox = QtWidgets.QVBoxLayout(self.cloudet_bar_widget)

        # groupbox
        self.cloudet_bar_gb = QtWidgets.QGroupBox("Data managing") # group box
        # layout
        self.cloudet_bar_layout = QtWidgets.QVBoxLayout(self.cloudet_bar_gb) # layout of the grpup box

        # checkboxes
        self.show_cloudets = QtWidgets.QCheckBox("Show Cloudets")
        self.show_beam = QtWidgets.QCheckBox("Show Beam")
        self.show_mark_range = QtWidgets.QCheckBox("Show marked range")
        

        # buttons
        self.add_to_cloudets_button = QtWidgets.QPushButton("Add to saved cloudets")
        self.remove_from_cloudets_button = QtWidgets.QPushButton("Remove from saved cloudets")
        self.add_to_cloudets_button.setMaximumSize(10000, 10000)
        self.add_to_cloudets_button.setMinimumSize(0, 0)
        self.remove_from_cloudets_button.setMaximumSize(10000, 10000)
        self.remove_from_cloudets_button.setMinimumSize(0, 0)

        # add to gb layout
        self.cloudet_bar_layout.addWidget(self.show_cloudets)
        self.cloudet_bar_layout.addWidget(self.show_beam)
        self.cloudet_bar_layout.addWidget(self.show_mark_range)
        self.cloudet_bar_layout.addWidget(self.add_to_cloudets_button)
        self.cloudet_bar_layout.addWidget(self.remove_from_cloudets_button)



        # list of cloudets 
        self.list_of_cloudets_gb = QtWidgets.QGroupBox("Cloudets")
        self.list_of_cloudets_gb_layout = QtWidgets.QVBoxLayout(self.list_of_cloudets_gb)
        self.list_of_cloudets = QtWidgets.QListWidget()
        self.list_of_cloudets_gb_layout.addWidget(self.list_of_cloudets)

        # adding both to widget
        self.cloudet_bar_widget_vbox.addWidget(self.cloudet_bar_gb)
        self.cloudet_bar_widget_vbox.addWidget(self.list_of_cloudets_gb)
        # -----------------------------
        
        # ---- SPOT - SHIFTER WIDGET ----
        # --- widget ---
        self.spot_shifter_widget = QtWidgets.QWidget(self.window)
        # layout
        self.spot_shifter_widget_vbox = QtWidgets.QVBoxLayout(self.spot_shifter_widget)
        # first gb - buttons
        self.spot_shifter_buttons = QtWidgets.QGroupBox("Options")
        # layout for gb
        self.spot_shifter_buttons_vbox = QtWidgets.QVBoxLayout(self.spot_shifter_buttons)
        # --- buttons ---
        self.set_as_origin_button = QtWidgets.QPushButton("Set as (0,0)")
        self.unset_origin_button = QtWidgets.QPushButton("Unset (0,0)")
        # sizing of buttons
        self.set_as_origin_button.setMaximumSize(10000, 10000)
        self.set_as_origin_button.setMinimumSize(0, 0)
        self.unset_origin_button.setMaximumSize(10000, 10000)
        self.unset_origin_button.setMinimumSize(0, 0)
        # -- checkboxes --
        self.show_spots = QtWidgets.QCheckBox("Show Spots")
        self.show_channel_label = QtWidgets.QCheckBox("Show channel numbers")
        self.show_selected_spot = QtWidgets.QCheckBox("Show selected spot")
        # adding buttons to the layout
        self.spot_shifter_buttons_vbox.addWidget(self.show_spots)
        self.spot_shifter_buttons_vbox.addWidget(self.show_channel_label)
        self.spot_shifter_buttons_vbox.addWidget(self.show_selected_spot)
        self.spot_shifter_buttons_vbox.addWidget(self.set_as_origin_button)
        self.spot_shifter_buttons_vbox.addWidget(self.unset_origin_button)
        # --- list of spots ---
        # second gb - list of spots
        self.list_of_spots_gb = QtWidgets.QGroupBox("Spots of ")
        # layout
        self.list_of_spots_gb_vbox = QtWidgets.QVBoxLayout(self.list_of_spots_gb)
        # list
        self.list_of_spots = QtWidgets.QListWidget()
        # adding list to gb
        self.list_of_spots_gb_vbox.addWidget(self.list_of_spots)
        # --- adding to main widget --
        self.spot_shifter_widget_vbox.addWidget(self.spot_shifter_buttons)
        self.spot_shifter_widget_vbox.addWidget(self.list_of_spots_gb)

        # making tabs 
        self.tab_widget_cl_sp.addTab(self.cloudet_bar_widget, "Cloudlets")
        self.tab_widget_cl_sp.addTab(self.spot_shifter_widget, "Spots")

        # setting "show spots" to checked
        self.show_spots.setChecked(True)

        
    
    # -- connect widgets (buttons etc. to proper slots)
    def __connect_to_slots(self):
        # project list
        self.projects_list.clicked.connect(self.__plot_on_list_click)
        # spot list
        self.list_of_spots.clicked.connect(self.__mark_spot_on_click)

        # buttons
        self.reload_button.clicked.connect(self.__reload_slot)
        self.load_button.clicked.connect(self.__load_slot)
        self.proper_motions.clicked.connect(self.__resize_plot)
        self.append_load_button.clicked.connect(self.__load_files_append_mode)
        self.set_as_origin_button.clicked.connect(self.__set_new_origin)
        self.unset_origin_button.clicked.connect(self.__unset_new_origin)
        self.add_to_cloudets_button.clicked.connect(self.__append_to_cloudet_list)
        self.remove_from_cloudets_button.clicked.connect(self.__remove_from_saved_cloudets)
        # checkboxes
        self.show_beam.clicked.connect(self.__beam_visible)
        self.show_mark_range.clicked.connect(self.__rectangle_visible)
        self.show_spots.clicked.connect(self.__show_plot_checkbox_slot)
        self.show_channel_label.clicked.connect(self.__show_plot_checkbox_slot)
        self.show_selected_spot.clicked.connect(self.__switch_marked_spot_visibility_slot)



    def plot_map_of_epoch(self, index = 0):
        # -- failsafe, if there are no epochs loaded --
        if len(self.epochlst_obj.epochs) == 0:
            print("----> No maps loaded! Failed, trying to plot...")
            return
        #self.spot_canvas.spot_plotting_wrapper(self.epochlst_obj.epochs[index].dRA, self.epochlst_obj.epochs[index].dDEC, self.epochlst_obj.epochs[index].velocity, self.epochlst_obj.epochs[index].flux_density, label=self.epochlst_obj.epochs[index].project_code)
        self.spot_canvas.set_plot_visible(index, self.show_spots.isChecked(), self.show_channel_label.isChecked())
        
        # -- setting beam width to new --
        self.spot_canvas.beam_ellipse.set_width(self.epochlst_obj.epochs[index].beam_size_ra)
        self.spot_canvas.beam_ellipse.set_height(self.epochlst_obj.epochs[index].beam_size_dec)

        # -- setting label on the group box --
        self.list_of_cloudets_gb.setTitle("Cloudets of " + self.epochlst_obj.epochs[index].project_code)

        # -- setting label on the spot list --
        self.list_of_spots_gb.setTitle("Spots of " + self.epochlst_obj.epochs[index].project_code)
        # filling list of spots
        self.__fill_list_of_spots(index)
        # filling list of cloudets
        self.__fill_list_of_cloudets(index)

    # ====== SLOTS ====== 
    def __plot_on_list_click(self):
        # -- searching of the proper epoch --
        # -- by extracting project code --
        index = self.projects_list.currentRow()
        # -- putting it on the plot --
        #self.spot_canvas.spot_plotting_wrapper(self.epochlst_obj.epochs[index].dRA, self.epochlst_obj.epochs[index].dDEC, self.epochlst_obj.epochs[index].velocity, self.epochlst_obj.epochs[index].flux_density, label=self.epochlst_obj.epochs[index].project_code)
        self.spot_canvas.set_plot_visible(index, self.show_spots.isChecked(), self.show_channel_label.isChecked())
        # -- setting global index number --
        self.chosen_project_index = index

        # -- setting beam width to new value --
        self.spot_canvas.beam_ellipse.set_width(self.epochlst_obj.epochs[index].beam_size_ra)
        self.spot_canvas.beam_ellipse.set_height(self.epochlst_obj.epochs[index].beam_size_dec)

        # -- setting label on the group box --
        self.list_of_cloudets_gb.setTitle("Cloudets of " + self.epochlst_obj.epochs[index].project_code)

        # -- setting label on the spot list --
        self.list_of_spots_gb.setTitle("Spots of " + self.epochlst_obj.epochs[index].project_code)
        # filling list of spots
        self.__fill_list_of_spots(index)
        # filling list of cloudets
        self.__fill_list_of_cloudets(index)

        self.list_of_spots.setCurrentRow(0)
        # -- calling "mark" ---
        self.__mark_spot_on_click()

    # -- slot for reloading --
    def __reload_slot(self):
        # clearing lists
        self.epochlst_obj.epochs = [] # clearing list of "spot class" objects

        # clearing widgets
        self.projects_list.clear()

        # loading data again
        self.epochlst_obj.read_multiple_epochs(self.epochlst_obj.fileslst, reload=True)

        # filling list widget
        self.__fill_list_of_projects(self.epochlst_obj.epochs)

        # plotting first epoch
        self.plot_map_of_epoch(0)

        # printing
        print("----------")
        print("----> Reloaded")

    # - makes spots visible and invisible -
    def __show_plot_checkbox_slot(self):
            self.spot_canvas.set_plot_visible(self.chosen_project_index, self.show_spots.isChecked(), self.show_channel_label.isChecked())
            self.spot_canvas.fig.canvas.draw_idle()

    def __switch_marked_spot_visibility_slot(self):
        self.spot_canvas.spot_marker_sc.set_visible(self.show_selected_spot.isChecked())
        self.spot_canvas.fig.canvas.draw_idle()
    
    def __beam_visible(self):
        # -- connecting canvas to methods --
        if self.show_beam.isChecked() == False:
            self.spot_canvas.beam_ellipse.set_visible(False)
            self.spot_canvas.fig.canvas.mpl_disconnect(self.kk)
        else:
            self.spot_canvas.beam_ellipse.set_visible(True)
            self.kk = self.spot_canvas.fig.canvas.mpl_connect('button_press_event', self.spot_canvas.onclick)
            if self.spot_canvas.selector.active:
                self.spot_canvas.selector.set_active(False)
                self.show_mark_range.setChecked(False)
        self.spot_canvas.fig.canvas.draw_idle()

    def __rectangle_visible(self):
        # setting span selector active / inactive
        if self.show_mark_range.isChecked() == False:
            self.spot_canvas.selector.set_active(False)
        else:
            if self.show_beam.isChecked():
                self.show_beam.setChecked(False)
                self.__beam_visible()
            self.spot_canvas.selector.set_active(True)

        self.spot_canvas.fig.canvas.draw_idle()

    def __load_slot(self):

        # enabling QFileDialog:
        list_of_filenames = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file(s)", getcwd(), "All (*);;.DAT files (*.DAT *.dat)")
        
        # -- if "cancel" was clicked --
        if len(list_of_filenames[0]) == 0:
            return

        # -- if files were chosen... --
        # clearing the lists
        try:
            del self.epochlst_obj # if this was declared previously, no problem
        except(AttributeError):
            pass # but it could not, so we need to override this fact
        
        # clearing widget
        self.projects_list.clear()

        # reading chosen files
        self.epochlst_obj = multiple_epochs_cl()
        self.epochlst_obj.read_multiple_epochs(list_of_filenames[0], reload=False, first_time=True, append=False)

        # filling the widget 
        self.__fill_list_of_projects(self.epochlst_obj.epochs)

        # plotting spot map of the first epoch
        self.spot_canvas.add_plots_to_canvas(self.epochlst_obj)

    def __load_files_append_mode(self):
        # we need failsafe
        # otherwise dumb user will use "append" mode when nothing is loaded
        try:
            if len(self.epochlst_obj.epochs) == 0:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("You cannot load in \"append mode\" when nothing is loaded!")
                msgBox.exec()
                return
        except:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("You cannot load in \"append mode\" when nothing is loaded!")
                msgBox.exec()
                return
        
        # -- actual data loading --
        # enabling QFileDialog:
        list_of_filenames = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file(s) (append mode!)", getcwd(), "All (*);;.DAT files (*.DAT *.dat)")
        # -- if "cancel" was clicked --
        if len(list_of_filenames[0]) == 0:
            return
        
        # clearing widget
        self.projects_list.clear()

        # reading chosen files
        self.epochlst_obj.read_multiple_epochs(list_of_filenames[0], reload=False, first_time=False, append=True)

        # filling the widget 
        self.__fill_list_of_projects(self.epochlst_obj.epochs)
        
        # adding plots to our "spot_plot_canvas_object"
        self.spot_canvas.add_plots_to_canvas(self.epochlst_obj)

    def __mark_spot_on_click(self):

        index = self.list_of_spots.currentRow()

        self.spot_canvas.plot_single_spot_filled(self.epochlst_obj.epochs[self.chosen_project_index].dRA[index], self.epochlst_obj.epochs[self.chosen_project_index].dDEC[index], self.epochlst_obj.epochs[self.chosen_project_index].flux_density[index])
    
    def __resize_plot(self):
        self.spot_canvas.fig.canvas.draw_idle()

    # - sets new origin slot -
    def __set_new_origin(self):
        # getting index of the selected spot
        index = self.list_of_spots.currentRow()
        # getting RA and DEC of selected spot
        spot_ra = self.epochlst_obj.epochs[self.chosen_project_index].dRA[index]
        spot_dec = self.epochlst_obj.epochs[self.chosen_project_index].dDEC[index]
        # shifting spots
        self.epochlst_obj.epochs[self.chosen_project_index].set_as_origin(spot_ra, spot_dec)
        # - updating plot data -
        # creating "offsets" table
        offsets = self.__make_offsets_for_scatter_plot()

        self.spot_canvas.spot_plots_table[self.chosen_project_index].set_offsets( offsets )
        # moving the marker point
        self.spot_canvas.spot_marker_sc.set_offsets([self.epochlst_obj.epochs[self.chosen_project_index].dRA[index], self.epochlst_obj.epochs[self.chosen_project_index].dDEC[index]])
        
        # moving the channel labels
        self.__move_channel_labels(offsets)
        
        # redrawing plot
        self.spot_canvas.fig.canvas.draw_idle()
    
    def __unset_new_origin(self):
        # we need no "index" stuff
        # we just invoke the "unset_as_origin" method
        self.epochlst_obj.epochs[self.chosen_project_index].unset_as_origin()
        
        # and repeat stuff with updating the graph
        # create new offsets
        offsets = self.__make_offsets_for_scatter_plot()
        # update the graph
        self.spot_canvas.spot_plots_table[self.chosen_project_index].set_offsets( offsets )
        # move the marker point
        index = self.list_of_spots.currentRow()
        self.spot_canvas.spot_marker_sc.set_offsets([self.epochlst_obj.epochs[self.chosen_project_index].dRA[index], self.epochlst_obj.epochs[self.chosen_project_index].dDEC[index]])
        # move the channel labels
        self.__move_channel_labels(offsets)
        # redrawing plot
        self.spot_canvas.fig.canvas.draw_idle()

    def __append_to_cloudet_list(self):
        # we need to use marked range
        # so if marking range is inactive, we basically should do nothing
        if self.show_mark_range.isChecked() != True:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Marking spots is inactive, so nothing can be appended to the cloudet list")
                msgBox.exec()
                return
        
        # if it is checked, then we do another failsafe - if the checkbox has been selected, but no range selected yet:
        if self.spot_canvas.selected_range == [0,0,0,0]:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("No range selected yet!")
                msgBox.exec()
                return

        # now we can do funnier stuff
        # we extract the spot parameters from the marked range
        # limits
        limits = self.spot_canvas.selected_range
        # getting params from params range
        channels, velocities, dX, dX_err, dY, dY_err, flux, flux_err = self.epochlst_obj.epochs[self.chosen_project_index].get_spots_params_from_range(limits[0], limits[1], limits[2], limits[3])
        # getting cloudets
        cloudet_vel, cloudet_dRA, cloudet_dRA_err, cloudet_dDEC, cloudet_dDEC_err, cloudet_flux, cloudet_flux_err = self.epochlst_obj.epochs[self.chosen_project_index].calculate_cloudet_params(velocities, dX, dX_err, dY, dY_err, flux, flux_err)
        # adding to list of cloudets
        self.list_of_cloudets.addItem(QtWidgets.QListWidgetItem( "%.3f  %.3f  %.3f  %.3f" % (cloudet_vel, cloudet_flux, cloudet_dRA, cloudet_dDEC ) ) )
        # adding to "cloudet" parameter of the "spots" class
        self.epochlst_obj.epochs[self.chosen_project_index].add_to_cloudets(cloudet_vel, cloudet_flux, cloudet_dRA, cloudet_dRA_err, cloudet_dDEC, cloudet_dDEC_err, save=True)

    def __remove_from_saved_cloudets(self):
        # we need to get index of the chosen cloudet
        index = self.list_of_cloudets.currentRow()

        # and we call "remove_cloudet" method from spot class
        self.epochlst_obj.epochs[self.chosen_project_index].remove_from_cloudets(index, save=True)

        # we remove it from list
        self.list_of_cloudets.removeItemWidget(self.list_of_cloudets.takeItem(index))

    # ====== HELPER PRIVATE METHOODS ====== 
    # -- this is just to avoid spaghetti --
    # calculates offsets to update the scatter plot
    def __make_offsets_for_scatter_plot(self):
        offsets = []
        for i in range(len(self.epochlst_obj.epochs[self.chosen_project_index].dRA)):
            offsets.append( [ self.epochlst_obj.epochs[self.chosen_project_index].dRA[i], self.epochlst_obj.epochs[self.chosen_project_index].dDEC[i] ] )
        
        return offsets
    
    # moves channel labels from "spot_plot" widget
    def __move_channel_labels(self, offsets):
        # only two lines
        # it makes use of the global "self.chosen_project_index"
        for i in range(len(offsets)):
            self.spot_canvas.channel_labels_table[self.chosen_project_index][i].set_position(offsets[i])
    
    # fills project list with proper data
    def __fill_list_of_projects(self, list_of_projects):
            for i in list_of_projects:
                self.projects_list.addItem(QtWidgets.QListWidgetItem(i.project_code + " Date: " + i.time_string + " PI: " + i.project_pi))
    
    # fills list of spots with proper data
    def __fill_list_of_spots(self, index):
        # - clear the previous list -
        self.list_of_spots.clear()
        # - loop to fill it again -
        for i in range(len(self.epochlst_obj.epochs[index].flux_density)):
            self.list_of_spots.addItem(QtWidgets.QListWidgetItem ( "%d   %.2f   %.2f   %.2f" % (self.epochlst_obj.epochs[index].channel[i], self.epochlst_obj.epochs[index].flux_density[i], self.epochlst_obj.epochs[index].dRA[i], self.epochlst_obj.epochs[index].dDEC[i] ) ) )

    def __fill_list_of_cloudets(self, index):
        # - clear the previous list -
        self.list_of_cloudets.clear()
        # if there is no cloudets, do nothing
        if self.epochlst_obj.epochs[index].cloudets_added == False:
            return

        # - loop to fill it actually -
        for i in range(len(self.epochlst_obj.epochs[index].cloudets_VEL)):
            cloudet_vel = self.epochlst_obj.epochs[index].cloudets_VEL[i]
            cloudet_flux = self.epochlst_obj.epochs[index].cloudets_FLUX[i]
            cloudet_dRA = self.epochlst_obj.epochs[index].cloudets_dRA[i]
            cloudet_dDEC = self.epochlst_obj.epochs[index].cloudets_dDEC[i]
            self.list_of_cloudets.addItem(QtWidgets.QListWidgetItem ( "%.3f  %.3f  %.3f  %.3f" % (cloudet_vel, cloudet_flux, cloudet_dRA, cloudet_dDEC ) ) )