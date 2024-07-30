#!/usr/bin/python3
# coding: utf-8

import re
import numpy as np
from .xmgrdecode import XmgrDecode

class XVGIO:
    def __init__(self, fname:str) -> None:
        self.fname = fname
        self.title = ''
        self.xaxis = ''
        self.yaxis = ''
        self.legend = []
        self.data = []  # save or write data

    def read(self) -> np.ndarray:
        """ @brief Read xvg data and return multi-columns data in array """
        self._read_header()
        data = []
        print(f'INFO) Loading file: {self.fname}')
        with open(self.fname, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if len(line.strip()) < 1 or line.startswith('@') or line.startswith('#'):
                    continue
                if line.startswith('&'):
                    raise IOError('Have not yet support multi-sets xvg')
                data.append(list(map(float, line.strip().split())))
        self.data = np.array(data)
        return self.data
    

    def _read_header(self):
        pattern = re.compile('^@ s\d+ legend')
        with open(self.fname, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '@    title' in line:
                    self.title = line.split('"')[1]
                elif '@    xaxis' in line:
                    self.xaxis = line.split('"')[1]
                elif '@    yaxis' in line:
                    self.yaxis = line.split('"')[1]
                elif pattern.match(line):
                    self.legend.append(line.split('"')[1])
        # check legend, if not exit, try use yaxis
        if not self._has_legend() and self.yaxis != '':
            self.legend = [self.yaxis]

        # decoding to python characters
        self.title = XmgrDecode(self.title).decoding()
        self.xaxis = XmgrDecode(self.xaxis).decoding()
        self.yaxis = XmgrDecode(self.yaxis).decoding()
        self.legend = XmgrDecode(self.legend).decoding()
    
    def write(self, fout:str) -> None:
        """ @brief Output data to fout file """
        header = """@ view 0.15, 0.15, 0.75, 0.85
@ legend on
@ legend box on
@ legend loctype view
@ legend 0.78, 0.8
@ legend length 2\n"""
        with open(fout, 'w') as f:
            f.write('# XVG written by glot\n')
            f.write(f'@    title "{self.title}"\n')
            f.write(f'@    xaxis  label "{self.xaxis}"\n')
            f.write(f'@    yaxis  label "{self.yaxis}"\n')
            f.write(f'@TYPE xy\n')
            f.writelines(x for x in header)
            for idx, leg in enumerate(self.legend):
                f.write(f'@ s{idx} legend "{leg}"\n')
            for d in self.data:
                if hasattr(d, '__iter__'):
                    f.writelines(f'{val:10g} ' for val in d)
                else:
                    f.write('{:>10g}' .format(d))
                f.write('\n')

    def _has_legend(self) -> bool:
        """ @brief If has legend in xvg """
        return len(self.legend) > 0
