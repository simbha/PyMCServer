#!/usr/bin/env python2

import sys
import os
import traceback

if sys.version_info[0] != 2:
    print("PyMCServer requires Python 2.x to run.")
    if sys.platform.startswith("linux"):
        print("Try using 'python2' instead of 'python'.")
    elif sys.platform == "win32":
        raw_input("Press enter to continue.")
    exit(1)

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pymcserver.server
pymcserver.server.initServer()
