#!/usr/bin/python3
# coding: utf-8

import os
from .logger import g_log

def check_file_exist(fpath:str):
    """ @brief check file if exist, throw error if not exist """
    if not os.path.exists(fpath):
        g_log.error(f"File '{fpath}' not exist")
