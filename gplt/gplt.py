#!/usr/bin/python3
# coding: utf-8

import sys, os
from utils.coolstuff import CoolStuff
from utils.logger import g_log

# add path to syspath
gpltpath = os.path.dirname(os.path.realpath(__file__))
if gpltpath not in sys.path:
    sys.path.insert(0, gpltpath)

import argparse
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

    if len(sys.argv) < 3:
        args.print_help()
        args.exit('Error! Missing input options')
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
    except Exception as ex:
        raise ex
    g_log.info('gplt reminds you: ' + CoolStuff().print_choice())

if __name__ == '__main__':
    gplt_command()
