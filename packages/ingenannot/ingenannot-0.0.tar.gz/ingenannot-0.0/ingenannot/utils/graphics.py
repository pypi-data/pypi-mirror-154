#!/usr/bin/env python3

import math
import numpy as np
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
#from matplotlib import gridspec

from upsetplot import plot

class Graphics(object):


    lColors = ['palevioletred','darkorchid','royalblue','darkturquoise','mediumspringgreen','olivedrab','gold','sandybrown','red','silver','m','blue','lightseagreen','chartreuse','darkkhaki','bisque','sienna','firebrick','gray','plum','darkcyan','darkgreen','orange','lightcoral','yellow']


    @staticmethod
    def plotDistribution(lXs, lYs, out="", title="", xax="", yax="", color="blue", legend="", grid=[]):
        """Draw a simple Distribution"""

        fig = plt.Figure(figsize=(20,20))
        fig.suptitle(title, fontsize=32)
        ax = fig.add_subplot(111)
        ax.plot(lXs,lYs, color=color)
        if legend:
            ax.legend(legend, fontsize=22)
        for line in grid:
            ax.axvline(x=line, linestyle='dashed', linewidth=1, color='black')
        axis_font = {'size':'28'}
        ax.set_xlabel(xax, **axis_font)
        ax.set_ylabel(yax, **axis_font)
        ax.tick_params(labelsize=20)
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)


    @staticmethod
    def plotUpsetPlot(counts,out="",title=""):
        ''' plot UpSet plot'''

        plot(counts, show_counts=True, subset_size="count")
        plt.title(title, fontsize=10)
        plt.savefig(out)
