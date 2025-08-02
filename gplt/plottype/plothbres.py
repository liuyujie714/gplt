#!/usr/bin/python3
# coding: utf-8

from plottype.plotxpm import PlotXPM
from typing import List, Tuple
from utils.logger import g_log
from dataclasses import dataclass
import numpy as np

@dataclass
class AtomInfo:
    name: str
    resid: int
    resname: str

class PlotHBResidue(PlotXPM):
    """ Plot hydrogen bonds residue heat map with residue name and id"""
    def __init__(self, fnames: List[str], **kwargs) -> None:
        self.fnames = fnames
        self.ndx = None
        self.xpm = None
        self.gro = None
        self.check_files()
        super().__init__(self.xpm, **kwargs['kwargs'])
        self.__plot()

    def check_files(self):
        """ Check file list, must has hbond.ndx, hbmap.xpm and md.gro """
        for f in self.fnames:
            if f.endswith('.ndx'):
                self.ndx = f
            elif f.endswith('.xpm'):
                self.xpm = f
            elif f.endswith('.gro'):
                self.gro = f
        if self.ndx is None:
            g_log.error(f'Missing ndx file for hydrogen bonds')
        if self.xpm is None:
            g_log.error(f'Missing xpm file for hydrogen bonds')
        if self.gro is None:
            g_log.error(f'Missing gro file for hydrogen bonds')
            
    def __plot(self):
        """ Read xpm/ndx/gro for hydrogen bonds residue and plot it"""
        # read gro to get residue name, resid, atom name
        resnames, resids, names = [], [], []
        with open(self.gro, 'r') as f:
            lines = f.readlines()
            natoms = int(lines[1])
            for line in lines[2:2+natoms]:
                resids.append(int(line[0:5]))
                resnames.append(line[5:10].strip())
                names.append(line[10:15].strip())

        # read hbond.ndx to get donor-hydrogen-acceptor pairs
        n = self.data.shape[0] # the number of hbond pairs in ndx
        hbpairs : List[Tuple[AtomInfo]] = [] # store donor-hydrogen-acceptor pairs
        with open(self.ndx, 'r') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                if line.startswith("[ hbonds_"):
                    for pair in lines[idx+1:idx+n+1]:
                        # to 0-based index
                        d, h, a = np.asarray(list(map(int, pair.split())))-1
                        hbpairs.append(
                            (AtomInfo(names[d], resids[d], resnames[d]),
                            AtomInfo(names[h], resids[h], resnames[h]),
                            AtomInfo(names[a], resids[a], resnames[a]))
                        )
                    break
        if len(hbpairs) == 0:
            g_log.error(f"Not find '[ hbonds_' line in {self.ndx}")

        # for replace yticks TODO
        self.yticks_str = [ f'{p[0].resname}{p[0].resid}@{p[0].name}-{p[2].resname}{p[2].resid}@{p[2].name}' for p in hbpairs]
        self.plot()
