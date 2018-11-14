#!/usr/bin/env python
# identifier.py

# project name
__project__ = "object_identifier"

# project version
__version__ = "0.1"

# prohect author
__author__ = "natanaelfneto"
__authoremail__ = "natanaelfneto@outlook.com"

# project source code
__source__ = "https://github.com/natanaelfneto/???"

# project general description
__description__ = '''???'''

# project short description
short_description = "???"


# third party imports
import argparse
import getpass
import logging
import os
import sys
import time


# class for logger instancies and configurations
class Logger(object):

    # path validity init
    def __init__(self, folder=None, format=None, extra=None, debug_flag=False):
        ''' 
            Initiate a Logger instance.
            Argument:
                logger: a logging instance for output and log
        '''

        # 
        log = {
            # setup of log folder
            'folder': folder,
            # set logging basic config variables
            'level': 'INFO',
            # 
            'date_format': '%Y-%m-%d %H:%M:%S',
            # 
            'filepath': folder+'/'+__project__+'.log',
            #
            'format': format,
            # extra data into log formatter
            'extra': extra
        }

        # set log name
        logger = logging.getLogger(__project__+'-'+__version__)

        # set formatter
        formatter = logging.Formatter(log['format'])

        # check debug flag
        if debug_flag:
            logger.setLevel('DEBUG')
        else:
            logger.setLevel('INFO')

        # check if log folder exists
        if not os.path.exists(log['folder']):
            print("Log folder: {0} not found".format(log['folder']))
            try:
                os.makedirs(log['folder'])
                print("Log folder: {0} created".format(log['folder']))
            except Exception  as e:
                print("Log folder: {0} could not be created, error: {1}".format(log['folder'], e))
                sys.exit()

        # setup of file handler
        file_handler = logging.FileHandler(log['filepath'])     
        file_handler.setFormatter(formatter)

        # setup of stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # add handler to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        # update logger to receive formatter within extra data
        logger = logging.LoggerAdapter(logger, log['extra'])

        self.adapter = logger

# command line argument parser
def args(args):
    '''
        Main function for terminal call of library
        Arguments:
            args: receive all passed arguments and filter them using
                the argparser library
    '''

    # argparser init
    parser = argparse.ArgumentParser(description=short_description)

    # prevent follow and lines flag to be setted at the same time
    group = parser.add_mutually_exclusive_group(required=False)

    # files with limited lines
    parser.add_argument(
        'sources',
        nargs='+',
        help='sources to have objects identified', 
        default=[]
    )

    # debug flag argument parser
    parser.add_argument(
        '-d','--debug',
        action='store_true', 
        help='process debug flag',
        default=False,
        required=False
    )

    # version output argument parser
    parser.add_argument(
        '-v','--version',
        action='version',
        help='output software version',
        default=False,
        version=(__project__+"-"+__version__)
    )

    # passing filtered arguments as array
    args = parser.parse_args(args)
    
    # call tail sources function
    run(
        debug=args.debug,
        sources=args.sources,
    )

# run funtion for module
def run(debug=False, sources=[]):

    # normalizing debug variable
    global debug_flag
    debug_flag = debug

    # standard log folder
    log_folder = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log/'))

    # standard log format
    log_format = '%(asctime)-8s %(levelname)-5s [%(project)s-%(version)s] user: %(user)s LOG: %(message)s'

    # creates a logger instance from class Logger within:
    # an adapter (the logging library Logger Adapter) and the verbose flag
    global logger
    logger = Logger(
        folder = log_folder,
        format = log_format,
        debug_flag = debug_flag,
        extra = {
            'project':  __project__,
            'version':  __version__,
            'user':     getpass.getuser()
        },
    )

    # debug flag variable
    logger.adapter.debug('DEBUG flags was setted as: {0}'.format(debug))

# run function on command call
if __name__ == "__main__":
    args(sys.argv[1:])
# end of code