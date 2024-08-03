#!/usr/bin/python3
# coding: utf-8

import sys, os

# add path to syspath
gpltpath = os.path.dirname(os.path.realpath(__file__))
if gpltpath not in sys.path:
    sys.path.insert(0, gpltpath)


import argparse
from utils.coolstuff import CoolStuff
from utils.logger import g_log
from plottype.plotxvg import PlotMultiXVG
from plottype.plotxpm import PlotMultiXPM, MultiDAT2XPM

def parser_opt():
    args = argparse.ArgumentParser(
        description='A program for plotting gromacs data'
    )
    gp1 = args.add_argument_group('Options to specify input files')
    gp1.add_argument('-f', '--file', type=str, default=None, nargs='*',
                      help='A gromacs data files, such as xvg, xpm, dat'
    )

    gp2 = args.add_argument_group('Options to specify output files:')
    gp2.add_argument('-o', '--outfile', type=str, default=None, 
                      help='Save figure to file, such as png, jpg with 600 dpi, or pdf')
    
    gp3 = args.add_argument_group('Other options:')
    gp3.add_argument('-title', '--title', type=str, default=None, 
                      help='Set title of figure')
    gp3.add_argument('-legend', '--legend', type=str, default=None, nargs='*',
                      help='Set legends of figure')
    gp3.add_argument('-xlim', '--xlim', type=float, default=None, nargs=2,
                      help='Set limits of xaxis')
    gp3.add_argument('-ylim', '--ylim', type=float, default=None, nargs=2,
                      help='Set limits of yaxis')
    gp3.add_argument('-xprec', '--xprec', type=int, default=None,
                      help='Set the precision of xtick')
    gp3.add_argument('-yprec', '--yprec', type=int, default=None,
                      help='Set the precision of ytick')
    gp3.add_argument('-zprec', '--zprec', type=int, default=None,
                      help='Set the precision of ztick if available')
    gp3.add_argument('-xaxis', '--xaxis', type=str, default=None,
                      help='Set X axis label')
    gp3.add_argument('-yaxis', '--yaxis', type=str, default=None,
                      help='Set y axis label')
    gp3.add_argument('-ux', '--unitx', type=str, default=None, 
                     help='The unit for x axis')
    gp3.add_argument('-uy', '--unity', type=str, default=None, 
                     help='The unit for y axis')
    gp3.add_argument('-style', '--mplstyle', type=str, default=None, 
                     help='The matplotlib style file for plotting')
    gp3.add_argument('-u', '--using', type=str, default=None, 
                     help='Use the selection columns to plot. 1-3 represents 1,2,3 column, 1,2 represent 1 and 2 column. ' \
                     '1,2:2 represents 1 and 2 column for file 1, 2 column for file2, ...(: represents multi-files)'  )

    if len(sys.argv) < 3:
        args.print_help()
        g_log.error('Missing input options')
    return args.parse_args()

def gplt_command():
    opts = parser_opt()
    suffix = opts.file[0].split('.')[-1]
    func_call = {
        'xvg' : PlotMultiXVG,
        'xpm' : PlotMultiXPM,
        'dat' : MultiDAT2XPM
    }
    try:
        func_call[suffix](opts.file, kwargs=opts._get_kwargs())
    except KeyError:
        g_log.error(f'Have not yet support "{suffix}" format')
    g_log.info('GPLT reminds you: ' + CoolStuff().print_choice())

if __name__ == '__main__':
    gplt_command()
