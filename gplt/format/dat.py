#!/usr/bin/python3
# coding: utf-8

import numpy as np
from format.xpm import XPMIO
from utils.logger import g_log

class DAT2XPM():
    """ @brief Convert dat to xpm file """
    def __init__(self, fdat:str) -> None:
        self.fdat = fdat
        self.xpm = XPMIO(fdat.split('.')[0]+'.xpm')

    def to_xpm(self, nbins:int=51):
        """ @brief Read a .dat file and convert it to out.xpm file """
        # check .dat type
        g_log.info(f'Loading {self.fdat}')
        with open(self.fdat, 'r') as f:
            line = f.readline()
        # is ss dat, such dssp.dat
        if any(ch.isalpha() for ch in line):
            self.to_ss_xpm()
        else:
            self.to_simple_xpm(nbins)
    
    def to_simple_xpm(self, nbins:int):
        """ @brief Read a .dat file and convert it to simple xpm file such as densmap.dat, ..."""
        with open(self.fdat, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.xpm.data.append(list(map(float, line.rstrip('\n').split())))
        self.xpm.data = np.asarray(self.xpm.data)

        # check input .dat format
        if self.xpm.data.shape[1] == 3: # N*3, is x,y,z format
            self.xpm.xticks = np.unique(self.xpm.data[:, 0])
            self.xpm.yticks = np.unique(self.xpm.data[:, 1])
            temp = np.zeros(shape=(len(self.xpm.xticks), len(self.xpm.yticks)))
            for (x, y, z) in self.xpm.data:
                temp[int(x), int(y)] = z
            self.xpm.data = temp.transpose()

        else: # .dat from gromacs output, such as densmap.dat
            # reverse...
            self.xpm.yticks = self.xpm.data[0, 1:]
            self.xpm.xticks = self.xpm.data[1:, 0]
            self.xpm.data   = self.xpm.data[1:, 1:]
            # transpose data
            self.xpm.data   = self.xpm.data.transpose()

        # set title, ...
        self.xpm.title = 'Simple XPM'
        self.xpm.xaxis = 'X-label'
        self.xpm.yaxis = 'Y-label'
        self.xpm.type = 'Continuous'
        # write new xpm file
        self.xpm.write(None, nbins)

    def to_ss_xpm(self):
        """ @brief Read a .dat file and convert it to ss xpm file such as ss.xpm, ..."""
        with open(self.fdat, 'r') as f:
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
        self.xpm.write()
