#!/usr/bin/python3
# coding: utf-8

from format.xpm import XPMIO
from format.dat import DAT2XPM
from utils.units import get_unit_frac, get_unit_from_str
import matplotlib.pyplot as plt
import matplotlib.colors as set_colors
import numpy as np


class PlotXPM(XPMIO):
    """ @brief A class to plot xpm """
    def __init__(self, fname: list, *args, **kwargs) -> None:
        super().__init__(fname)
        self.args = args
        self.kwargs = kwargs
        self.xlim = None
        self.ylim = None

        self.read() # read data
        self._set_display()   
        #self.plot() 

    def _set_display(self):
        """ @brief Set up figure display, such label, title, legend, ... """

        """ @brief Set up figure display, such label, title, legend, ... """
        # adjust unit of axis
        for key, val in self.kwargs['kwargs']:
            if val is None:
                continue
            if key=='unitx':
                ret = get_unit_from_str(self.xaxis)
                if ret is not None:
                    frac = get_unit_frac(ret, val)
                    # scale x data
                    self.xticks *= frac
                    # set new xlabel use unit val
                    self.xaxis = self.xaxis.replace(ret, val)
            elif key=='unity':
                ret = get_unit_from_str(self.yaxis)
                if ret is not None:
                    frac = get_unit_frac(ret, val)
                    # scale y data
                    self.yticks *= frac
                    # set new xlabel use unit val
                    self.yaxis = self.yaxis.replace(ret, val)

        keywords = ['legend', 'xaxis', 'yaxis', 'xlim', 'ylim']
        # SS can not modify title
        if 'Secondary' not in self.title:
            keywords += ['title']
        for key, val in self.kwargs['kwargs']:
            if val != None and key in keywords:
                setattr(self, key, val)

    def plot(self):
        """ @brief Plot XPM figure """

        # set font
        font = {'family': 'Times New Roman',
                'weight': 'regular',
                'size'  : '14'}
        plt.rc('font', **font)

        plt.figure('XPM Figure', figsize=(8, 6))
        X, Y = np.meshgrid(self.xticks, self.yticks)
        Z = np.array(self.data, dtype=float)

        # hb xpm
        if "Hydrogen" in self.yaxis:
            h = plt.contourf(X, Y, Z, np.linspace(0, 1, 3), colors=['white', 'red'])
            cb = plt.colorbar(h, orientation='horizontal', fraction=0.03)
            cb.set_ticks([0.25, 0.75])
            cb.set_ticklabels(['None', 'Present'])
        # ss xpm
        elif 'Secondary' in self.title:
            # fix plot bug, we should use pcolormesh
            cmap = set_colors.ListedColormap([self.color_map[i] for i in self.value_list])
            boundaries = list(self.colors.values())
            boundaries.append(len(boundaries))
            norm = set_colors.BoundaryNorm(boundaries, cmap.N)
            h = plt.pcolormesh(X, Y, Z, cmap=cmap, norm=norm, shading='nearest')
            cb = plt.colorbar(h, orientation='horizontal')
            cb.set_ticks(np.array(boundaries[:-1]) + 0.5)
            cb.set_ticklabels(self.value_list)
        # other
        else:
            h = plt.contourf(X, Y, Z, np.linspace(min(self.colors.values()), max(self.colors.values()), 9), cmap="jet")
            cb = plt.colorbar(h)
        if self._has_legend(): 
            cb.set_label(self.legend[0])

        plt.xlabel(self.xaxis)
        plt.ylabel(self.yaxis)
        plt.title(self.title)
        # set range
        if self.xlim != None:
            plt.xlim(self.xlim)
        if self.ylim != None:
            plt.ylim(self.ylim)

        # save png
        for key, value in self.kwargs['kwargs']:
            if key == 'outfile' and value is not None:
                print(f'INFO) Write {value}')
                plt.savefig(value, dpi=600)
                return
        plt.show()

class PlotMultiXPM():
    def __init__(self, fnames: list, *args, **kwargs) -> None:
        self.fnames = fnames
        self.kwargs = kwargs
        self.mplot()

    def mplot(self):
        for f in self.fnames:
            obj = PlotXPM(f, kwargs=self.kwargs['kwargs'])
            obj.plot()

class PlotDat(DAT2XPM):
    def __init__(self, fname: list, *args, **kwargs) -> None:
        super().__init__(fname[0])
    
    def plot(self):
        pass