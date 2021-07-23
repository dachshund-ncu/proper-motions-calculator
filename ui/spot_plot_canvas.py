'''
This class creates simple plot canvas to display spot maps
'''

from classes.multiple_epochs import multiple_epochs_cl
from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Ellipse, Rectangle
from numpy import min, ptp, log
matplotlib.use('Qt5Agg')

class mplSpotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):# width=5, height=4, dpi=100):
        self.fig = Figure()#(figsize=(width, height), dpi=dpi)
        
        self.gs = gridspec.GridSpec(1,2, width_ratios=[30,1], figure=self.fig)
        # axis - scatter plot & cloudlets
        self.axes = self.fig.add_subplot(self.gs[0,0])
        # colorbar
        self.cbax = self.fig.add_subplot(self.gs[0,1])
        # beam plot - ellipse
        self.beam_ellipse = Ellipse([0,0], 4.5, 4.5, angle=0.0, fc='None', ec='black', visible=False)
        # rectangle marker
        self.mark_rect = Rectangle([0,0], 30, 30, fc='grey', ec='black', visible=False)
        # table with existing collection objects (spots)
        self.spot_plots_table = []
        # table with existing collection objects (cloudets)
        self.cloudet_plots_table = []
        # table with existing objects (text)
        self.channel_labels_table = []

        super(mplSpotCanvas, self).__init__(self.fig)

        # -- connecting canvas to methods --
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.axes_cleared = True


    def spot_plotting_wrapper(self, x,y, vel, flux, label=""):
        # -- clearing axes --
        self.axes.clear()
        self.cbax.clear()
        
        # -- doing rest of things --
        flux2 = log(flux * 1000.0)
        # -- creating color table --
        scaled_vel = (vel - vel.min()) / vel.ptp()
        colors = plt.cm.jet(scaled_vel)

        # -- scatter plot --
        self.axes.scatter(x, y, s=(flux2)**2.0 * 5, edgecolor=colors, marker="o", facecolor="none")
        # - array for colorbar -
        p = plt.cm.ScalarMappable(cmap=plt.cm.jet)
        p.set_array(vel)
        self.fig.colorbar(p, ax=self.axes, cax=self.cbax)
        self.cbax.set_ylim(vel.min(), vel.max())
        self.axes.grid()

        # - setting title -
        self.axes.set_title(label)

        # - making x_axis inverse -
        self.axes.invert_xaxis()

        # - redoing this nice plot -
        self.__make_nice_looking_plot()
        
        # - adding ellipse and rectangle -
        self.axes.add_patch(self.beam_ellipse)
        self.axes.add_patch(self.mark_rect)

        # - re-drawing figure -
        self.fig.canvas.draw_idle()
        self.axes_cleared = True
    
    # -- adds new plot (collection etc. to existing axes) --
    def __add_plot(self, x, y, flux, vel, vmin, vrange):
        # scaling flux with log
        flux2 = log(flux * 1000.0)
        # making scaled color-scale
        scaled_vel = (vel - vmin) / vrange
        colors = plt.cm.jet(scaled_vel)

        # making plot
        b = self.axes.scatter(x, y, s=(flux2)**2.0 * 5, edgecolor=colors, marker="o", facecolor="none", visible=False)
        
        return b
        
    # -- adds new channel labels to spots --
    def __add_chennel_labels(self, x,y,channels):
        # adding channel labels to the plot
        channel_labels = []
        for i in range(len(channels)):
            w = self.axes.text(x[i], y[i], str(channels[i]), visible=False)
            channel_labels.append(w)
        
        return channel_labels

    # -- adds cloudet plot to axes --
    def __add_cloudets(self,x,y):
        pass
    
    # -- adds colorbar --
    def __add_colorbar(self, all_vels):
        p = plt.cm.ScalarMappable(cmap=plt.cm.jet)
        p.set_array(all_vels)
        self.fig.colorbar(p, ax=self.axes, cax=self.cbax)
        self.cbax.set_ylim(min(all_vels), max(all_vels))

    # uses all private methods to fill
    # it takes "spot class" object as an argument
    # vmin and vrange are for color-scale
    def __add_new_plot_object(self, epoch, vmin, vrange):
        x = epoch.dRA
        y = epoch.dDEC
        channels = epoch.channel
        velocity = epoch.velocity
        flux = epoch.flux_density
        # adding collection object
        self.spot_plots_table.append(self.__add_plot(x,y,flux,velocity,vmin, vrange))
        # adding cloudet object
        pass
        # addding text objects
        self.channel_labels_table.append(self.__add_chennel_labels(x,y,channels))

    # public method, that makes multiple instances of this "add_new_plot"
    def add_plots_to_canvas(self, multiple_epochs_object):
        # - we clean our tables -
        self.channel_labels_table = []
        self.cloudet_plots_table = []
        self.spot_plots_table = []
        # - we need to extract all velocities possible -
        vels = []
        for i in multiple_epochs_object.epochs:
            vels.extend(i.velocity)
        # we take minimum and maximum value
        vmin = min(vels) # minimum vel
        vmax = max(vels) # maximum vel
        vrange = vmax - vmin # range of the vels

        # - we clear axes - this method should be called once per load
        # so it should be called also when "append load happend"
        # it will completely clear plot canvas
        self.axes.clear()
        self.cbax.clear()
        # setting proper bool
        self.axes_cleared = True

        # - now we can call "add_new_plot" private instance
        for i in multiple_epochs_object.epochs:
            self.__add_new_plot_object(i, vmin, vrange)

        # - and we make colorbar -
        self.__add_colorbar(vels)

        # - and we make marker -
        self.spot_marker_sc = self.axes.scatter(multiple_epochs_object.epochs[0].dRA[0], multiple_epochs_object.epochs[0].dDEC[0], c='black', s = log(multiple_epochs_object.epochs[0].flux_density[0] * 1000.0) **2.0 * 5, alpha=0.5, visible=False)

        # - grid -
        self.axes.grid()
        # - making x_axis inverse -
        self.axes.invert_xaxis()
        # - adding ellipse and rectangle -
        self.axes.add_patch(self.beam_ellipse)
        self.axes.add_patch(self.mark_rect)
        # - at the end - we make nice looking plot -
        self.__make_nice_looking_plot()

        

    def set_plot_visible(self, index, spot_marker=True, channel_marker=True):
        # -- checking, if checkboxes are marked or not --
        # "show spots" checkbox
        if spot_marker == False:
            for i in self.spot_plots_table:
                i.set_visible(False)
        
        # "show channel labels" checkbox
        if channel_marker == False:
            for i in self.channel_labels_table:
                for j in range(len(i)):
                    i[j].set_visible(False)

        # if both are marked, there is nothing more to do
        if spot_marker == False and channel_marker == False:
            return
        
        # if not, we can set something visible or not
        # we set all unvisible, except for the "index" one
        for i in range(len(self.spot_plots_table)):
            # spot plots if/else
            if i == index and spot_marker == True:
                self.spot_plots_table[i].set_visible(True)
            else:
                self.spot_plots_table[i].set_visible(False)
            
            # channel labels if/else
            if i == index and channel_marker == True:
                for j in self.channel_labels_table[i]:
                    j.set_visible(True)
            else:
                for j in self.channel_labels_table[i]:
                    j.set_visible(False)
        
        # redrawing figure
        self.fig.canvas.draw_idle()


    def __make_nice_looking_plot(self):
        # -- ticks --
        self.axes.xaxis.set_tick_params(direction='in', width=1, length = 3, top = True)
        self.axes.xaxis.set_tick_params(direction='in', width=1, length = 3, which='minor', top = True)
        self.axes.yaxis.set_tick_params(direction='in', width=1, length = 3, right=True)
        self.axes.yaxis.set_tick_params(direction='in', width=1, length = 3, which='minor', right=True)

        self.cbax.yaxis.set_tick_params(direction='in', width=1, length = 3)
    
    # -- methood - show beam where clicked --
    def onclick(self, event):
        x,y = event.xdata, event.ydata
        if x == None or y == None:
            #print("----> Tried to draw beam outside plot. Fortunately nothing happened")
            return
        self.beam_ellipse.set_center([x,y])
        self.fig.canvas.draw_idle()
    
    def plot_single_spot_filled(self, dx,dy,flux):
        flux2 = log(flux * 1000.0)
        self.spot_marker_sc.set_offsets([dx,dy])
        self.spot_marker_sc.set_sizes([flux2**2.0 * 5])
        self.fig.canvas.draw_idle()
        '''
        if self.axes_cleared == False:
            flux2 = log(flux * 1000.0)
            self.axes.set_xlim(self.axes.get_xlim())
            self.axes.set_ylim(self.axes.get_ylim())
            self.spot_marker_sc.set_offsets([dx,dy])
            self.spot_marker_sc.set_sizes([flux2**2.0 * 5])
            self.fig.canvas.draw_idle()
        else:
            flux2 = log(flux * 1000.0)
            self.axes.set_xlim(self.axes.get_xlim())
            self.axes.set_ylim(self.axes.get_ylim())
            self.spot_marker_sc = self.axes.scatter(dx,dy,c='black', s=(flux2)**2.0 * 5, alpha=0.5)
            self.fig.canvas.draw_idle()
            self.axes_cleared = False
        '''