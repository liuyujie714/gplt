#!/usr/bin/python3
# coding: utf-8

import numpy as np
from format.xpm import XPMIO

class DAT2XPM():
    """ @bref Convert dat to xpm file """
    def __init__(self, fname:str) -> None:
        self.fname = fname
        self.xpm = XPMIO('temp')
        self.read()

    def read(self):
        """ @breif Read dssp.dat file and convert it to ss_old.xpm file """
        with open(self.fname, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.xpm.data.append(list(line.rstrip('\n')))
        self.xpm.data = np.asarray(self.xpm.data).transpose() 
        # set title, ...
        self.xpm.title = 'Secondary structure'
        self.xpm.xaxis = 'Frame'
        self.xpm.yaxis = 'Residue'
        self.xpm.type = 'Discrete'
        # write new xpm file
        self.xpm.write('ss_old.xpm')
