#!/usr/bin/python3
# coding: utf-8

import re

Time_Units = {'fs' : 1,     
              'ps' : 1E-3, 
              'ns' : 1E-6,  
              'us' : 1E-9, 
              'ms' : 1E-12, 
              's'  : 1E-15
}
Length_Units = {'angstrom' : 1, 
                'nm' : 1E-1, 
                'um' : 1E-4, 
                'mm' : 1E-7, 
                'cm' : 1E-8, 
                'dm' : 1E-9, 
                'm'  : 1E-10
}

def get_unit_from_str(ss:str):
    """ @brief get unit from given string, such as Time (ps) -> ps 

    Return
    ------
    If failed or can not parser unit, return None
    """
    keys = [x for x in Time_Units.keys()]+[x for x in Length_Units.keys()]+['a']
    s = ss.lower()
    pattern = r'\((.*?)\)'
    if match:=re.search(pattern, s):
        if match.group(1) in keys:
            return match.group(1)
    return None

def _get_factor(src:str, desc:str, dic:dict):
    """ @breif return factor if can convert, else return None """
    s = src.lower()
    # unit Angstrom
    if s=='a':
        s = 'angstrom'
    d = desc.lower()
    if d=='a':
        d = 'angstrom'

    a = b = -1
    for unit, frac in dic.items():
        if s==unit:
            a = frac
        if d==unit:
            b = frac
    if a > 0 and b > 0:
        return b/a
    else:
        return None

def get_unit_frac(src:str, desc:str):
    """ @brief get unit factor from src convert to desc """
    ret = _get_factor(src, desc, Time_Units)
    if ret is not None:
        return ret
    ret = _get_factor(src, desc, Length_Units)
    if ret is not None:
        return ret
    raise ValueError(f"Can not convert between '{src}' and '{desc}'")

