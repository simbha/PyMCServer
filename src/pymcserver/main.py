#!/usr/bin/python2

import sys

if sys.version_info.major != 2:
    print("PyMCServer requires Python 2.x to run.")
    exit(1)

#####################################################
#             Python 2.x only code                  #
#####################################################

from pymcserver import server

if __name__ == '__main__':
    server.initServer()