#!/usr/bin/python3
# coding: utf-8

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from typing import List
from format.xvg import XVGIO
from utils.units import get_unit_frac, get_unit_from_str
from utils.logger import g_log
import pandas as pd
import numpy as np

class PlotXVG(XVGIO):
    """ @brief Plot xvg data """
    def __init__(self, fname: str, **kwargs) -> None:
        super().__init__(fname)
        self.kwargs = kwargs
        self.xlim = None
        self.ylim = None
        self.xprec = None
        self.yprec = None
        self.using = None #  use fixed columns to plot
        self.mplstyle = None # matplotlib style

        self.read() # read data
        self._set_display()
        #self.plot()

    def _set_display(self):
        """ @brief Set up figure display, such label, title, legend, ... """
        # adjust unit of axis
        for key, val in self.kwargs.items():
            if val is None:
                continue
            if key=='unitx':
                ret = get_unit_from_str(self.xaxis)
                if ret is not None:
                    frac = get_unit_frac(ret, val)
                    # scale x data
                    self.data[:, 0] *= frac
                    # set new xlabel use unit val
                    self.xaxis = self.xaxis.replace(ret, val)
            elif key=='unity':
                ret = get_unit_from_str(self.yaxis)
                if ret is not None:
                    frac = get_unit_frac(ret, val)
                    # scale y data
                    self.data[:, 1:] *= frac
                    # set new xlabel use unit val
                    self.yaxis = self.yaxis.replace(ret, val)

        # only set label
        keywords = ['legend', 'title', 'xaxis', 'yaxis', 'xlim', 'ylim', 'mplstyle',
                    'xprec', 'yprec', 'using']
        for key, val in self.kwargs.items():
            if val != None and key in keywords:
                setattr(self, key, val) # self.key = val

    def _plot(self):
        """ @brief Plot figure """
        plt.figure(figsize=(8,6))
        plt.plot(self.data[:, 0], self.data[:, 1:])
        plt.xlabel(self.xaxis)
        plt.ylabel(self.yaxis)
        plt.title(self.title)
        if self._has_legend(): 
            plt.legend(self.legend, frameon=False)
        # set range
        if self.xlim != None:
            plt.xlim(self.xlim)
        if self.ylim != None:
            plt.ylim(self.ylim)
        plt.show()

class PlotMultiXVG():
    """ @brief Plot mulit-files xvg """
    def __init__(self, fnames: list, **kwargs) -> None:
        self.fnames = fnames
        self.kwargs = kwargs['kwargs']
        self.mplot()

    def parser_using(self, string:str):
        """ @brief parser input '-u' option from command 

        Parameters
        ----------
        string: input string, such as 1,2:3:4

        Return
        ------
        return None if string is empty list [], else return a list that includes these columns to ploting,
        """ 
        if string is None:
            return []
        groups = string.split(':')
        if len(groups) != len(self.fnames):
            g_log.error(f'The number of grous ({len(groups)}) from -u is not equal to total input files ({len(self.fnames)})')
        plist = []
        for g in groups:
            g1 = []
            # 1-3 
            if len(g.split(',')) >= 1 :
                for j in g.split(','):
                    sp = j.split('-')
                    if len(sp) == 1:
                        g1.extend([int(sp[0])])
                    else:
                        g1.extend([x for x in range(int(sp[0]), int(sp[1])+1)])
            plist.append(sorted(list(set(g1))))
        return plist

    def mplot(self):
        """ @brief Plot Multi-sets on one figure """
        objs: List[PlotXVG] = []
        for f in self.fnames:
            objs.append(PlotXVG(f, **self.kwargs))

        # set font
        font = {'family': 'Times New Roman',
                'weight': 'regular',
                'size'  : '14'}
        plt.rc('font', **font)
        # set style if has mplstyle
        if objs[0].mplstyle is not None:
            plt.style.use(objs[0].mplstyle)

        # plot figure
        fig, ax = plt.subplots(figsize=(8,6))
        fig.canvas.manager.set_window_title('XVG Figure')
        legs = []
        
        # parser -using
        #print('input: ', objs[0].using) 
        grps = self.parser_using(objs[0].using)
        if len(grps) > 0:
            xcol = grps[0][0] - 1
            if xcol < 0:
                g_log.error('Input -u must b > 1')
            grps[0] = grps[0][1:] # drop the first column

        for idx, obj in enumerate(objs):
            if len(grps) > 0:
                for g in range(len(grps[idx])):
                    plt.plot(obj.data[:, xcol], obj.data[:, grps[idx][g]-1])
            else:
                plt.plot(obj.data[:, 0], obj.data[:, 1:])
            # merge legends
            if (self.kwargs['legend'] is None) and len(self.fnames)>1:
                legs.extend([f'{x} of {self.fnames[idx]}' for x in obj.legend])
            else:
                legs = obj.legend

        # set show
        ax.legend(legs, frameon=False)
        ax.set_xlabel(objs[0].xaxis)
        ax.set_ylabel(objs[0].yaxis)
        ax.set_title(objs[0].title)
        
        # set range of axis
        if objs[0].xlim != None:
            ax.set_xlim(objs[0].xlim)
        if objs[0].ylim != None:
            ax.set_ylim(objs[0].ylim)

        # set precision of ticks
        if objs[0].xprec is not None:
            ax.xaxis.set_major_formatter(FormatStrFormatter(f'%.{objs[0].xprec}f'))
        if objs[0].yprec is not None:
            ax.yaxis.set_major_formatter(FormatStrFormatter(f'%.{objs[0].yprec}f'))

        # save png or plot
        fout = self.kwargs['outfile']
        if fout is not None:
            g_log.info(f'Write {fout}')
            # write excel table
            if '.xlsx' in fout:
                mergedata = [objs[0].data[:, 0]] # x axis
                # all y axises
                for obj in objs:
                    mergedata.extend(obj.data[:, col] for col in range(1, obj.data[:, 1:].shape[1] + 1))
                cols = [objs[0].xaxis] + legs
                cols = [cols[i].replace('$', '') for i in range(len(cols))] # remove latex
                df = pd.DataFrame(np.array(mergedata).T, columns=cols)
                df.to_excel(fout, index=False)
            else:
                plt.savefig(fout, dpi=600 if objs[0].mplstyle is None else plt.rcParams['savefig.dpi'])
        else:
            plt.show()
