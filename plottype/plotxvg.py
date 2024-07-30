
import matplotlib.pyplot as plt
from typing import List
from format.xvg import XVGIO
from utils.units import get_unit_frac, get_unit_from_str

class PlotXVG(XVGIO):
    """ @brief Plot xvg data """
    def __init__(self, fname: str, *args, **kwargs) -> None:
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
        # adjust unit of axis
        for key, val in self.kwargs['kwargs']:
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
        keywords = ['legend', 'title', 'xaxis', 'yaxis', 'xlim', 'ylim']
        for key, val in self.kwargs['kwargs']:
            if val != None and key in keywords:
                setattr(self, key, val)

    def plot(self):
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
    def __init__(self, fnames: list, *args, **kwargs) -> None:
        self.fnames = fnames
        self.args = args
        self.kwargs = kwargs
        self.mplot()

    def mplot(self):
        objs: List[PlotXVG] = []
        for f in self.fnames:
            objs.append(PlotXVG(f, kwargs=self.kwargs['kwargs']))

        # set font
        font = {'family': 'Times New Roman',
                'weight': 'regular',
                'size'  : '14'}
        plt.rc('font', **font)

        # plot figure
        plt.figure('XVG Figure', figsize=(8,6))
        legs = []
        is_custom_leg = any(key == 'legend' and value is not None for key, value in self.kwargs['kwargs'])
        for idx, obj in enumerate(objs):
            plt.plot(obj.data[:, 0], obj.data[:, 1:])
            # merge legends
            if not is_custom_leg and len(self.fnames)>1:
                legs.extend([f'{x} of {self.fnames[idx]}' for x in obj.legend])
            else:
                legs = obj.legend

        plt.legend(legs, frameon=False)
        plt.xlabel(objs[0].xaxis)
        plt.ylabel(objs[0].yaxis)
        plt.title(objs[0].title)
        # set range of axis
        if objs[0].xlim != None:
            plt.xlim(objs[0].xlim)
        if objs[0].ylim != None:
            plt.ylim(objs[0].ylim)
        # save png
        for key, value in self.kwargs['kwargs']:
            if key == 'outfile' and value is not None:
                print(f'INFO) Write {value}')
                plt.savefig(value, dpi=600)
                return
        plt.show()
