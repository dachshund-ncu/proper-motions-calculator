'''
This class creates simple plot canvas to display spot maps
'''

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy import min, ptp, log
matplotlib.use('Qt5Agg')

class mplSpotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):# width=5, height=4, dpi=100):
        self.fig = Figure()#(figsize=(width, height), dpi=dpi)
        
        self.gs = gridspec.GridSpec(1,2, width_ratios=[30,1], figure=self.fig)
        self.axes = self.fig.add_subplot(self.gs[0,0])
        self.cbax = self.fig.add_subplot(self.gs[0,1])

        super(mplSpotCanvas, self).__init__(self.fig)
    
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
        self.axes.scatter(x, y, s=(flux2)**2.0 * 5, marker="o", facecolor="none", edgecolor=colors)

        # - array for colorbar -
        p = plt.cm.ScalarMappable(cmap=plt.cm.jet)
        p.set_array(vel)
        self.fig.colorbar(p, ax=self.axes, cax=self.cbax)
        self.axes.grid()

        # - setting title -
        self.axes.set_title(label)

        # - making x_axis inverse -
        self.axes.invert_xaxis()

        # - redoing this nice plot -
        self.__make_nice_looking_plot()
        # - re-drawing figure -
        self.fig.canvas.draw_idle()
    
    def __make_nice_looking_plot(self):
        # -- ticks --
        self.axes.xaxis.set_tick_params(direction='in', width=1, length = 3, top = True)
        self.axes.xaxis.set_tick_params(direction='in', width=1, length = 3, which='minor', top = True)
        self.axes.yaxis.set_tick_params(direction='in', width=1, length = 3, right=True)
        self.axes.yaxis.set_tick_params(direction='in', width=1, length = 3, which='minor', right=True)

        self.cbax.yaxis.set_tick_params(direction='in', width=1, length = 3)