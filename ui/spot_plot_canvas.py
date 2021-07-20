'''
This class creates simple plot canvas to display spot maps
'''

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

class mplSpotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):# width=5, height=4, dpi=100):
        
        self.fig = Figure()#(figsize=(width, height), dpi=dpi)
        self.axes=self.fig.add_subplot(111)
        

        super(mplSpotCanvas, self).__init__(self.fig)