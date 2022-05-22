import sys
import argparse
import logging

logger = logging.getLogger('DAQ.util')

def config_args() -> tuple:
    parser = argparse.ArgumentParser(description='DAQ Controller', add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
    parser.add_argument('-ng', '--nogui', action='store_true', help='Run without GUI (still use plotter).')
    parser.add_argument('-np', '--noplot', action='store_true', help='Run without plotter (just record data).')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug settings and logging.')
    parser.add_argument('-l', '--loglevel', type=str, default='warning', help='Set the logging level.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Run with verbose logging to stdout.')
    parser.add_argument('-s', '--simulate', action='store_true', help='Run with simulated input (no Arduino).')
    parser.add_argument('-p', '--port', type=str, default='auto', help='Set path to Arduino port.')
    args = parser.parse_args()

    match args.loglevel.casefold():
        case 'debug':
            args.loglevel = logging.DEBUG
        case 'info':
            args.loglevel = logging.INFO
        case 'warning':
            args.loglevel = logging.WARNING
        case 'error':
            args.loglevel = logging.ERROR
        case 'critical':
            args.loglevel = logging.CRITICAL

    if args.simulate == True:
        args.port = 'sim'
    
    if args.debug == True:
        args.loglevel = logging.DEBUG

    return args.port, args.loglevel, not args.nogui, not args.noplot, args.verbose

def config_logger(log_level: int=logging.INFO, verbose: bool=False):
    FILENAME = 'daq.log'
    LOG_FORMAT = '%(asctime)s %(name)s::%(levelname)s: %(message)s'
    FILE_DATE_FMT =  '%y-%m-%d.%H:%M:%S'
    VERBOSE_DATE_FORMAT = '%H:%M:%S'

    logger = logging.getLogger('DAQ')
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(filename=FILENAME)
    console_handler = logging.StreamHandler(sys.stderr)

    file_handler.setLevel(log_level)

    if verbose == True:
        console_handler.setLevel(log_level)
    else:
        console_handler.setLevel(logging.WARN)

    file_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=FILE_DATE_FMT))
    console_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=VERBOSE_DATE_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)