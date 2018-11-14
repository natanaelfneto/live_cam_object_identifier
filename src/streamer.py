#!/usr/bin/env python
# identifier.py

# project name
__project__ = "streamer.py"

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
import cv2
import getpass
import logging
import numpy as np
import os
import sys
import time
# 
from queue import Queue
from threading import Thread
from imutils.video import FPS

from win32api import GetSystemMetrics

# 
class VideoStream:

    # 
    def __init__(self, source, queue_size):
        '''
            Initiate an instance of the class
        '''

        # get loggert on a self instance
        self.logger = logger.adapter

        # 
        self.stream = cv2.VideoCapture(source)

        # 
        self.Q = Queue(maxsize=queue_size)

    # 
    def start(self):
        '''
        '''

        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()

        # 
        return self

    # 
    def update(self):
        '''
        '''

        while True:
            (grabbed, frame) = self.stream.read()
            self.Q.put(frame)

    # 
    def read(self):
        '''
        '''

        # 
        return self.Q.get()

    # 
    def more(self):
        '''
        '''

        # 
        return self.Q.qsize() > 0

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
        nargs="+",
        help='source to have objects identified', 
        default=None
    )

    # debug flag argument parser
    parser.add_argument(
        '-q','--queue-size',
        type=int, 
        help='set queue maximum size for frames [default=60]',
        default=60,
        required=False
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
        queue_size=args.queue_size
    )

# run funtion for module
def run(debug=False, sources=None, queue_size=None):

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

    if len(sources) >= 12:
        logger.adapter.info('In this version, the maximum number of screen is fixed in 12. Sorry :(')
        sys.exit()

    streams = {}
    for index, source in enumerate(sources):
        stream = VideoStream(source, queue_size).start()
        fps = FPS().start()

        streams[index] = {
            "stream": stream,
            "fps": fps
        }

    # 
    time.sleep(1.0)
    
    # 
    while True:

        # aux variables
        text_color = (0, 255, 0)

        screen_height, screen_width = GetSystemMetrics(1), GetSystemMetrics(0)

        row = screen_height / 3 
        col = screen_width / 4
    
        output_top = "press 'Q' to quit application"
        title = '{0}-{1} @ {2}'.format(__project__, __version__, __author__)

        resized = []
        for index in streams:
            stream = streams[index]["stream"]

            if not stream.more():
                break

            frame = stream.read()
            loss = 1 - (stream.Q.qsize() / stream.Q.maxsize)
            frames_ratio = '{0}/{1}'.format(stream.Q.qsize(), stream.Q.maxsize)
            height, width, depth = frame.shape
            output_bottom = "queue ratio: {0}, server delay correction: {1:.2f} ms".format(frames_ratio, loss)

            resized_height, resized_width = row, col
            
            cv2.putText(frame, output_bottom, (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
            resized.append(
                cv2.resize(
                    frame,
                    ( int(resized_width), int(resized_height) )
                )
            )

        container = np.concatenate(resized, axis=1)

        # add context to the frame
        cv2.putText(container, output_top, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        
        # 
        cv2.imshow(title, container)

        # server delay correction
        time.sleep(loss)

        # check if 'Q' key for 'application exit' was pressed
        if cv2.waitKey(22) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            sys.exit()

        # 
        for index in streams:
            fps = streams[index]["fps"]
            fps.update()

# run function on command call
if __name__ == "__main__":
    args(sys.argv[1:])
# end of code