#!/usr/bin/python2

import sys

if sys.version_info.major != 2:
    print("PyMCServer requires Python 2.x to run.")
    exit(1)

#####################################################
#             Python 2.x only code                  #
#####################################################

__server = None
__log = None
__datadir = "data"

from pymcserver.server import WebServer
import logging
import os

def mkdir(path):
    if not os.path.exists(__datadir):
        os.makedirs(__datadir)

def initServer():
    mkdir(__datadir)
    
    # Setup logging
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s"))
    
    fh = logging.FileHandler(os.path.join(__datadir, "webserver.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s"))
    
    __log = logging.getLogger("PyMCServer")
    __log.setLevel(logging.DEBUG)
    __log.addHandler(sh)
    __log.addHandler(fh)
    __log.info("W** SUCKS")
    
    __server = WebServer("127.0.0.1", 8099)
    try:
        __server.run()
    except KeyboardInterrupt:
        __server.stop()

if __name__ == '__main__':
    initServer()