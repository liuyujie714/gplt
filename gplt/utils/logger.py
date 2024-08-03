#!/usr/bin/python3
# coding: utf-8

import logging, sys, time
import inspect
import colorama as clr

class Logger:
    """ @brief A logger class, use g_log in any source file """
    def __init__(self) -> None:
        clr.init(autoreset=True) # inital colorama
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
        frame = inspect.stack()[2]
        return f' <- source file: {frame.filename} (line {frame.lineno})'
    
    def debug(self, msg):
        self.logger.debug(clr.Fore.BLUE + f'{self.curr_time()}\nDEBUG) {msg} {self.caller_info()}')

    def info(self, msg):
        self.logger.info(clr.Fore.YELLOW + f'{self.curr_time()}\nINFO) {msg}')

    def error(self, msg):
        self.logger.error(clr.Fore.RED + clr.Back.YELLOW + f'{self.curr_time()}\nERROR) {msg} {self.caller_info()}')
        sys.exit(1)

    def critical(self, msg):
        self.logger.critical(clr.Fore.RED + clr.Back.WHITE + f'{self.curr_time()}\nCRITICAL) {msg} {self.caller_info()}')
        sys.exit(2)    

g_log = Logger() # the golbal handle of singleton

