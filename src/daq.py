# import daq_cli as cli
# import daq_gui as gui
import daq_util as util
import time
import sys
import logging
import atexit
import numpy as np

# def dbg_print(string: str, *argv):
#     if (debug_mode): print(string, *argv)
logger = logging.getLogger('DAQ')

def exit_monitor():
    return # do nothing

def main(port:str = 'auto', gui:bool=True, plot:bool=True, debug:bool=True, start_time:float=time.time()):
    if gui == False:
        None # do nothing at the moment TODO
    else:
        None # do nothing at the moment

if __name__ == '__main__':
    port, loglevel, gui, plot, verbose = util.config_args()
    util.config_logger(loglevel, verbose)
    main(gui, plot, debug)