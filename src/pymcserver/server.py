# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pymcserver import utils
import logging
import os
import threading

server = None
log = logging.getLogger("PyMCServer")
accesslog = logging.getLogger("WebAccess")
datadir = "data"
active = True

_allCommands = {}

class WebServer:
    def __init__(self, host, port):
        self.httpd = HTTPServer((host, port), MCHTTPRequestHandler)
    
    def run(self):
        self.httpd.serve_forever()
    
    def start(self):
        self.run()
    
    def stop(self):
        self.httpd.socket.close()
        

class MCHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        accesslog.info(fmt % args)

    def do_GET(self):
        self.send_response(200);
        self.end_headers();
        self.wfile.write("the w** sucks");

class ConsoleHandlerThread(threading.Thread):
    def run(self):
        while True:
            line = raw_input("> ")
            if line:
                com = line.split()[0]
                if _allCommands.has_key(com):
                    args = line.split()[1:]
                    _allCommands[com](args)
                elif com == "help":
                    log.info("Command list: ")
                    for i in _allCommands.keys():
                        log.info("- %s" % i)
                else:
                    log.error("Unknown command. Type 'help' for command list")

def registerCommand(name, function):
    _allCommands[name] = function
    
def testCommand(args):
    print """
§§§§§__§§__§§§____§§___§§§§___­­­­­­­­­­­___§§______§§§§﻿ ﻿
§§__§§_§§__§§_§§__§§__§§___§§_­­­­­­­­­­­__§§§§___§§§__§§
§§__§§_§§__§§_§§__§§_§§_______­­­­­­­­­­­__§§§§___§§
§§§§§__§§__§§__§§_§§_§§___§§§_­­­­­­­­­­­_§§__§§____§§§
§§_____§§__§§__§§_§§_§§____§§_­­­­­­­­­­­_§§§§§§______§§
§§_____§§__§§__§§_§§__§§__§§§_­­­­­­­­­­­§§____§§_§§§__§§
§§_____§§__§§___§§§§____§§§§__­­­­­­­­­­­§§____§§___§§§§﻿
""".strip()
    print " | ".join(args)

def initServer():
    global log, accesslog, server
    utils.mkdir(datadir)
    
    # Setup console/file logging
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    fh = logging.FileHandler(os.path.join(datadir, "webserver.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.setLevel(logging.DEBUG)
    log.addHandler(sh)
    log.addHandler(fh)
    log.info("W** SUCKS")
    
    # Setup web access.log
    fh = logging.FileHandler(os.path.join(datadir, "access.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    accesslog.addHandler(fh)
    
    # Set up commands
    registerCommand("test", testCommand)
    registerCommand("pingas", testCommand)
    
    server = WebServer("127.0.0.1", 8099)
    ConsoleHandlerThread().start()
    
    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()
    