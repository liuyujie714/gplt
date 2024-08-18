#!/usr/bin/python3
# coding: utf-8

from format.xpm import XPMIO
from format.dat import DAT2XPM
from utils.units import get_unit_frac, get_unit_from_str
from utils.logger import g_log
import matplotlib.pyplot as plt
import matplotlib.colors as set_colors
from matplotlib.ticker import FormatStrFormatter
import numpy as np

class PlotXPM(XPMIO):
    """ @brief A class to plot xpm """
    def __init__(self, fname: list, **kwargs) -> None:
        super().__init__(fname)
        self.kwargs = kwargs
        self.xlim = None
        self.ylim = None
        self.xprec = None
        self.yprec = None
        self.zprec = None
        self.mplstyle = None
        self.d3 = False # if show 3D surface, such as FEL.xpm

        self.read() # read data
        self._set_display()   
        #self.plot() 

    def _set_display(self):
        """ @brief Set up figure display, such label, title, legend, ... """

        """ @brief Set up figure display, such label, title, legend, ... """
        # adjust unit of axis
        unitx = self.kwargs['unitx']
        if unitx is not None:
            ret = get_unit_from_str(self.xaxis)
            if ret is not None:
                frac = get_unit_frac(ret, unitx)
                # scale x data
                self.xticks *= frac
                # set new xlabel use unit val
                self.xaxis = self.xaxis.replace(ret, unitx)
        unity = self.kwargs['unity']
        if unity is not None:
            ret = get_unit_from_str(self.yaxis)
            if ret is not None:
                frac = get_unit_frac(ret, unity)
                # scale y data
                self.yticks *= frac
                # set new xlabel use unit val
                self.yaxis = self.yaxis.replace(ret, unity)

        # scale axis
        if self.kwargs['scalex'] is not None:
            self.xticks *= self.kwargs['scalex']
        if self.kwargs['scaley'] is not None:
            self.yticks *= self.kwargs['scaley']
        if self.kwargs['scalez'] is not None:
            self.data *= self.kwargs['scalez']

        # only set label
        keywords = ['legend', 'xaxis', 'yaxis', 'zaxis', 'xlim', 'ylim', 'title', 'mplstyle', 
                    'xprec', 'yprec', 'zprec', 'd3']
        for key in keywords:
            if self.kwargs[key] is not None:
                setattr(self, key, self.kwargs[key]) # self.key = val

    def plot(self):
        """ @brief Plot XPM figure """

        # set font
        font = {'family': 'Times New Roman',
                'weight': 'regular',
                'size'  : '14'}
        plt.rc('font', **font)
        if self.mplstyle is not None:
            plt.style.use(self.mplstyle)

        fig = plt.figure(figsize=(8,6))
        fig.canvas.manager.set_window_title('XPM Figure')
        ax = fig.add_subplot(projection='3d' if self.d3 else None)
        X, Y = np.meshgrid(self.xticks, self.yticks)
        Z = np.array(self.data, dtype=float)

        # hb, ss xpm with Discrete data
        if self.type == 'Discrete':
            # fix plot bug, we should use pcolormesh
            cmap = set_colors.ListedColormap(self.hexcolors)
            boundaries = list(self.code2value.values())
            boundaries.append(len(boundaries))
            norm = set_colors.BoundaryNorm(boundaries, cmap.N)
            h = plt.pcolormesh(X, Y, Z, cmap=cmap, norm=norm, shading='nearest')
            fraction = 0.15 if len(self.hexcolors) > 3 else 0.03
            cb = plt.colorbar(h, orientation='horizontal', fraction=fraction)
            cb.set_ticks(np.array(boundaries[:-1]) + 0.5)
            cb.set_ticklabels(self.value_list)
        # continuous data
        else:
            if self.d3:
                ax.plot_surface(X, Y, Z, cmap='jet')
                if self.zaxis == '' and self._has_legend():
                    self.zaxis = self.legend[0]
                ax.set_zlabel(self.zaxis)
                h = plt.contourf(X, Y, Z, list(self.code2value.values()), offset=np.min(self.data), cmap="jet")
                cb = plt.colorbar(h, location='left', shrink=0.6)
            else:
                h = plt.contourf(X, Y, Z, list(self.code2value.values()), cmap="jet")
                cb = plt.colorbar(h)
        if self._has_legend(): 
            cb.set_label(self.legend[0])

        ax.set_xlabel(self.xaxis, labelpad=10 if self.d3 else None)
        ax.set_ylabel(self.yaxis, labelpad=10 if self.d3 else None)
        ax.set_title(self.title)
        # set range
        if self.xlim is not None:
            ax.set_xlim(self.xlim)
        if self.ylim is not None:
            ax.set_ylim(self.ylim)
        
        # set precision of ticks
        if self.xprec is not None:
            ax.xaxis.set_major_formatter(FormatStrFormatter(f'%.{self.xprec}f'))
        if self.yprec is not None:
            ax.yaxis.set_major_formatter(FormatStrFormatter(f'%.{self.yprec}f'))
        if self.zprec is not None:
            cb.formatter = FormatStrFormatter(f'%.{self.zprec}f')
            cb.update_ticks()

        # save png
        fout = self.kwargs['outfile']
        if fout is not None:
            g_log.info(f'Write {fout}')
            plt.savefig(fout, dpi=600 if self.mplstyle is None else plt.rcParams['savefig.dpi'])
        else:
            plt.show()

class PlotMultiXPM():
    def __init__(self, fnames: list, **kwargs) -> None:
        self.fnames = fnames
        self.kwargs = kwargs['kwargs']
        self.mplot()

    def mplot(self):
        for f in self.fnames:
            obj = PlotXPM(f, **self.kwargs)
            obj.plot()

class MultiDAT2XPM():
    """ @ batch convert dat to xpm files """
    def __init__(self, fnames: list, **kwargs) -> None:
        self.fnames = fnames
        self.batch()
    
    def batch(self):
        for f in self.fnames:
            obj = DAT2XPM(f)
            obj.to_xpm(51)
