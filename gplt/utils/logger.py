#!/usr/bin/python3
# coding: utf-8

import logging, sys, time
import inspect
import colorama as clr

class _Logger:
    """ @brief A private logger class, please use g_log in any source file """
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
        """@brief throw all debug msg, only used when level <= logging.INFO """
        self.logger.debug(clr.Fore.BLUE + f'{self.curr_time()}\nDEBUG) {msg} {self.caller_info()}')

    def info(self, msg):
        """@brief throw normal msg """
        self.logger.info(clr.Fore.YELLOW + f'{self.curr_time()}\nINFO) {msg}')

    def warn(self, msg):
        """@brief throw warning msg """
        self.logger.warning(clr.Fore.MAGENTA + f'{self.curr_time()}\nWARNING) {msg}')

    def error(self, msg):
        """@brief throw error msg and exit with code 1"""
        self.logger.error(clr.Fore.RED + clr.Back.BLACK + f'{self.curr_time()}\nERROR) {msg} {self.caller_info()}')
        sys.exit(1)

    def critical(self, msg):
        """@brief throw fatal error msg and exit with code 2 """
        self.logger.critical(clr.Fore.RED + clr.Back.WHITE + f'{self.curr_time()}\nCRITICAL) {msg} {self.caller_info()}')
        sys.exit(2)    

g_log = _Logger() # the golbal handle of singleton

