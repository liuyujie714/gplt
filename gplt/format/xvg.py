#!/usr/bin/python3
# coding: utf-8

import re, os
import numpy as np
from utils.logger import g_log
from utils.utils import check_file_exist
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
        check_file_exist(self.fname)
        self._read_header()
        data = []
        g_log.info(f'Loading file: {self.fname}')
        with open(self.fname, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if len(line.strip()) < 1 or line.startswith('@') or line.startswith('#'):
                    continue
                if line.startswith('&'):
                    g_log.error('Have not yet support multi-sets xvg')
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
    
    def write(self, fout:str, additions:str = None) -> None:
        """ @brief Output data to fout file, if fout is None, will set to fname

        Parameters
        ----------
        additions : str, addition context append file
        """
        if fout is None:
            fout = self.fname
        header = """@ view 0.15, 0.15, 0.75, 0.85
@ legend on
@ legend box on
@ legend loctype view
@ legend 0.78, 0.8
@ legend length 2\n"""
        g_log.info(f'Write {fout}')
        with open(fout, 'w') as f:
            f.write('# XVG written by gplt\n')
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
            if additions is not None:
                f.write(additions)

    def _has_legend(self) -> bool:
        """ @brief If has legend in xvg """
        return len(self.legend) > 0
