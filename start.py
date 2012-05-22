#!/usr/bin/env python2

import sys
import os
import traceback

if sys.version_info[0] != 2:
    print("PyMCServer requires Python 2.x to run.")
    exit(1)

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

os.chdir(os.path.dirname(__file__))
import pymcserver.server
pymcserver.server.initServer()