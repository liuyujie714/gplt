#!/usr/bin/python3
# coding: utf-8

import logging, sys, time
import inspect
from termcolor import colored

class Logger:
    """ @brief A logger class, use g_log in any source file """
    def __init__(self) -> None:
        logging.basicConfig(
            format='%(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        self.info('Initial logger')

    @staticmethod
    def curr_time():
        """ @brief return current time in str"""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    @staticmethod
    def caller_info():
        """ @brief get caller source filename and line number"""
        frame = inspect.stack()[2]  # 调用方是栈的第三个元素
        module = inspect.getmodule(frame[0])
        filename = module.__file__ if module else "unknown"
        lineno = frame.lineno
        return f'in {filename} (line {lineno})'
    
    def debug(self, msg):
        self.logger.debug(colored(f'{self.curr_time()}\nDEBUG) {msg} {self.caller_info()}', 'blue'))

    def info(self, msg):
        self.logger.info(colored(f'{self.curr_time()}\nINFO) {msg}', 'yellow'))

    def error(self, msg):
        self.logger.error(colored(f'{self.curr_time()}\nERROR) {msg} {self.caller_info()}', 'red', 'on_yellow'))
        sys.exit(1)

    def critical(self, msg):
        self.logger.critical(colored(f'{self.curr_time()}\nCRITICAL) {msg} {self.caller_info()}', 'red', 'on_white', ['bold']))
        sys.exit(2)    

g_log = Logger() # the golbal handle of singleton
