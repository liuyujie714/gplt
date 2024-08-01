#!/usr/bin/python3
# coding: utf-8

import numpy as np
from io import TextIOWrapper
from format.xvg import XVGIO

class XPMIO:
    def __init__(self, fname:str) -> None:
        self.fname = fname
        self.title = ''
        self.xaxis = ''
        self.yaxis = ''
        self.type = 'Continuous' # Continuous or Discrete 
        self.ncode = 1 # 1 or 2 chars of the level
        self.value_list = []
        self.code2value = {}  # code to value
        self.hexcolors = [] # such as #FFFFFF
        self.dim = np.zeros(4, dtype=int) # data shape ncol + nrow + ncolors + ncode
        self.dt = 1  # time interval in ps
        # secondary structure and color rgb
        self.color_map = {
            'Coil': (1, 1, 1), 'B-Sheet': (1, 0, 0), 'B-Bridge': (0, 0, 0),       
            'Bend': (0, 1, 0), 'Turn': (1, 1, 0), 'A-Helix': (0, 0, 1), 
            '5-Helix': (0.7, 0.3, 0.8), '3-Helix': (0.5, 0.5, 0.5), 'PP-Helix' : (0, 1, 1),
            'Chain': (0, 0.5, 0.5)
        }
        # single code to ss name
        self.sscode_map = {
            '~' : 'Coil', 'E' : 'B-Sheet', 'B' : 'B-Bridge' ,
            'S' : 'Bend', 'T' : 'Turn', 'H' : 'A-Helix',
            'I' : '5-Helix', 'G' : '3-Helix', 'P' : 'PP-Helix',
            '=' : 'Chain'
        }
        self.xticks = []
        self.yticks = []
        self.legend = []
        self.data = []  # save or write data
    
    def read(self) -> np.ndarray:
        """ @brief Read xpm file and return data """
        print(f'INFO) Loading file: {self.fname}')
        with open(self.fname, 'r') as f:
            while line:=f.readline().rstrip('\n'):
                if len(line) < 2:
                    continue
                if 'title:' in line:
                    self.title = line.split('"')[1]
                elif 'legend:' in line:
                    self.legend = [line.split('"')[1]]
                elif 'x-label:' in line:
                    self.xaxis = line.split('"')[1]
                elif 'y-label:' in line:
                    self.yaxis = line.split('"')[1]
                elif 'type:' in line:
                    self.type = line.split('"')[1]
                elif 'static char' in line:
                    self.dim = np.array(f.readline().split('"')[1].split(), dtype=int)
                    if self.dim[3] > 1:
                        self.ncode = self.dim[3]
                    for i in range(self.dim[2]):
                        temp = f.readline().rstrip('\n')
                        value = temp.split('"')[-2]
                        if value=="Chain_Separator": # use short name
                            value="Chain"
                        self.value_list.append(value)
                        self.code2value[temp[1:1+self.ncode]] = float(value) if self.type == 'Continuous' else i
                        self.hexcolors.append(temp.split('"')[1].split()[-1])
                elif 'x-axis:' in line:
                    self.xticks.extend(line.split()[2:-1])
                elif 'y-axis:' in line:
                    self.yticks.extend(line.split()[2:-1])
                elif line[0] == '"' and line[self.dim[0]*self.ncode + 1] == '"':
                    # reverse order data use insert
                    self.data.insert(0, [self.code2value[line[j:j+self.ncode]] 
                                      for j in range(1, self.dim[0]*self.ncode + 1, self.ncode)])

        # check dim
        if len(self.xticks) > self.dim[0]:
            print('INFO) Process axis length to match array')
            self.xticks.pop()
            self.yticks.pop()

        self.data = np.asarray(self.data)
        self.xticks = np.asarray(self.xticks, dtype=np.float64)
        self.yticks = np.asarray(self.yticks, dtype=np.float64)
        return self.data
    
    def write(self, fout:str = None, nbins:int = 51) -> None:
        """ Write data to xpm file 
        
        Parameters
        ----------
        fout: the output filename, will use fname prefix if fout is None to write
        """
        if fout is None:
            fout = self.fname
        if fout.split('.')[-1] != 'xpm':
            raise TypeError('Output file must be .xpm!')
        if len(self.data) == 0:
            raise ValueError('Empty data!')
        if not self._has_legend():
            self.legend = ['']
        
        header = """/* XPM */
/* This file is created by gplt */
/* title:   "{}" */
/* legend:  "{}" */
/* x-label: "{}" */
/* y-label: "{}" */
/* type:    "{}" */
static char *gromacs_xpm[] = """

        if 'Secondary' in self.title:
            self.write_ss_xpm(fout, header)
            self.write_ss_xvg()
        else:
            self.write_simple_xpm(fout, header, nbins)

    def write_simple_xpm(self, fout:str, headerfmt:str, nbins:int):
        """ @brief Write simple float xpm, such as densmap.xpm format """
        single_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+{}|;:\',<.>/?'
        # calculate dim from given self.data
        self.dim[0], self.dim[1] = len(self.data[0]), len(self.data) # ncol * nrow
        if nbins > len(single_chars):
            raise ValueError(f'The nbins must be <= {len(single_chars)}')
        self.dim[2] = nbins # how many bins for diving data
        self.dim[3] = 1 # only use one letter
        fmin, fmax = np.min(self.data), np.max(self.data)
        dx = (fmax-fmin)/(nbins-1)
        codes = []
        for i in range(nbins):
            r = int(np.round(255 - (255 * i / (nbins-1))))
            g = int(np.round(255 - (255 * i / (nbins-1))))
            b = int(np.round(255 - (255 * i / (nbins-1))))
            codes.append('#%02X%02X%02X' %(r, g, b))
        #print(codes)

        print(f'INFO) Write {fout}')
        with open(fout, 'w') as w:
            w.writelines(x for x in headerfmt 
                         .format(self.title, self.legend[0], self.xaxis, self.yaxis, self.type)
            )
            w.write('{\n')
            w.write('"%d %d   %d %d"\n' %(self.dim[0],self.dim[1],self.dim[2],self.dim[3]))
            for idx, code in enumerate(codes):
                w.write('"%c%c c %s " /* "%.3g" */,\n' % (
                        single_chars[idx], ' ', code, fmin+dx*idx
                        ))
            # write x-axis
            self._write_axis2(w, 'x', self.xticks)
            # write y-axis
            self._write_axis2(w, 'y', self.yticks)
            # write data matrix in chars
            for idx, i in enumerate(self.data[::-1, :]): # column reverse
                w.write('"')
                for j in i:
                    w.write('%c' %(single_chars[int((j-fmin)/dx)]))
                if idx < len(self.data)-1:
                    w.write('",\n')
                else:
                    w.write('"\n')

    def write_ss_xvg(self):
        """ @brief Write scount.xvg from .dat """
        xvg = XVGIO("scount.xvg")
        xvg.title = 'Secondary Structure'
        xvg.xaxis = 'Frame'
        xvg.yaxis = 'Number of Residues'
        unique_codes = sorted(np.unique(self.data.flatten()), reverse=True)
        xvg.legend = [self.sscode_map[k] for k in unique_codes]
        xvg.data = np.zeros(shape=(self.data.shape[1], len(xvg.legend) + 1))
        xvg.data[:, 0] = [x for x in range(self.data.shape[1])]
        for fr in range(self.data.shape[1]):
            for idx, s in enumerate(unique_codes, 1):
                xvg.data[fr, idx] = np.count_nonzero(self.data[:, fr] == s)
        counts = np.sum(xvg.data[:, 1:], axis=0, dtype=np.int32)
        context =  '# Totals   ' + ''.join('{:>10d} ' .format(x) for x in counts) + '\n'
        context += '# SS pr.   ' + ''.join('{:>10.2f} ' .format(x/np.sum(counts)) for x in counts) + '\n'
        xvg.write(None, context)

    def write_ss_xpm(self, fout:str, headerfmt:str):
        """ @brief Write secondary structure of protein xpm, and count xvg"""
        # calculate dim from given self.data
        self.dim[0], self.dim[1] = len(self.data[0]), len(self.data) # ncol * nrow
        # data use int to represent ss
        breverse = False
        if self.data.dtype == np.int32:
            rev_colors = {v: k for k, v in self.code2value.items()}
            breverse = True
        codes = np.unique(np.array(self.data).flatten()) # unique codes
        self.dim[2] = len(codes)
        self.dim[3] = 1 # one code
        print(f'INFO) Write {fout}')
        with open(fout, 'w') as w:
            w.writelines(x for x in headerfmt 
                         .format(self.title, self.legend[0], self.xaxis, self.yaxis, self.type)
            )
            w.write('{\n')
            w.write('"%d %d   %d %d"\n' %(self.dim[0],self.dim[1],self.dim[2],self.dim[3]))
            for code in codes:
                # "\"%c%c c #%02X%02X%02X \" /* \"%.3g\" */,\n" for simple
                # "\"%c%c c #%02X%02X%02X \" /* \"%3d\" */,\n" for discrete
                # "\"%c%c c #%02X%02X%02X \" /* \"%s\" */,\n" for string value in discrete
                ch = rev_colors[code] if breverse else code
                name = self.sscode_map[ch if breverse else code]
                cls = list(map(lambda x: np.int32(np.round(x * 255)), self.color_map[name]))
                if name == 'Chain':
                    name = 'Chain_Separator'
                w.write('"%c%c c #%02X%02X%02X " /* "%s" */,\n' % (
                    ch, ' ', cls[0], cls[1], cls[2], name
                ))
            # write x-aixs
            self._write_axis(w, 'x', self.dim[0], self.dt)
            # write y-axis
            self._write_axis(w, 'y', self.dim[1], 1, started=1) # residue is continuous
            # wrie characters matrix
            for idx, i in enumerate(self.data[::-1, :]):
                w.write('"')
                for j in i:
                    if isinstance(j, np.integer):
                        w.write(f'{rev_colors[j]}')
                    else:
                        w.write(f'{j}')
                if idx < len(self.data)-1:
                    w.write('",\n')
                else:
                    w.write('"\n')

    def _has_legend(self) -> bool:
        """ @brief If has legend in xpm """
        return len(self.legend) > 0
    
    def _write_axis2(self, w:TextIOWrapper, axis:str, ticks:list):
        """ @brief Write given ticks data to axis """
        # write axis
        for i, val in enumerate(ticks):
            if i%80==0:
                if i: 
                    w.write('*/\n')
                w.write('/* %s-axis:  ' %axis)
            w.write('%g ' %val)
        w.write('*/\n')

    def _write_axis(self, w:TextIOWrapper, axis:str, len:int, dt:float, started:int=0):
        """ @brief  Write continuous data by given parameters"""
        # write axis
        for i in range(len):
            if i%80==0:
                if i: 
                    w.write('*/\n')
                w.write('/* %s-axis:  ' %axis)
            w.write('%g ' %(dt*i+started))
        w.write('*/\n')
