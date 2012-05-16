from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pymcserver import cmds, utils, hooks
import Cookie
import logging
import os
import readline
import threading
import traceback

server = None
log = logging.getLogger("PyMCServer")
accesslog = logging.getLogger("WebAccess")
datadir = "data"
active = True

_allCommands = {}

class WebServer:
    def __init__(self, host, port):        # That, is HORRIBLE. You can't pass objects to HTTPServer,
        # you have to use a class!
        self.httpd = HTTPServer((host, port), MCHTTPRequestHandler)
        self.preHandleHooks = []        self.allSessions = {}    
    def registerPreHook(self, function):        self.preHandleHooks.append(function)    
    def run(self):
        self.httpd.serve_forever()
    
    def start(self):
        self.run()
    
    def stop(self):
        self.httpd.socket.close()
        
class MCHTTPRequestHandler(BaseHTTPRequestHandler):    def log_message(self, fmt, *args):
        accesslog.info(fmt % args)

    def do_GET(self):
        res = Response()
        
        for hook in server.preHandleHooks:
            hook(self, res)
        
        self.send_response(res.code)
        for key, value in res.headers:
            self.send_header(key, value)
    
    def getSession(self):        if "Cookie" in self.headers:
            c = Cookie.SimpleCookie(self.headers["Cookie"])            if "session" in c:                return c["session"].value            else:                pass
        else:            pass
    
    def getServer(self):
        global server
        return server

class Response:
    def __init__(self, handler):
        self.code = 500
        self.headers = {}
        self.handler = handler
        
        self.headers["Content-Type"] = "text/html"
        
        self.__endheaders = False
        self.__headersStack = []
    
    def endHeaders(self):
        self.handler.end_headers()
        #self.__headersStack = traceback.format_stack()
        self.__endheaders = True
    
    def getWFile(self):
        return self.handler.wfile
    
    def getRFile(self):
        return self.handler.rfile

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
    log.info("Starting PyMCServer, " + utils.getVersion())
    log.info("W** SUCKS")
    
    # Setup web access.log
    fh = logging.FileHandler(os.path.join(datadir, "access.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    accesslog.setLevel(logging.DEBUG)
    accesslog.addHandler(fh)
    
    # Set up commands
    registerCommand("test", cmds.testCommand)
    registerCommand("pingas", cmds.testCommand)
    
    server = WebServer("127.0.0.1", 8099)        server.registerPreHook(hooks.loginCheckHook)
    server.registerPreHook(hooks.cookieHook)
    
    ConsoleHandlerThread().start()
    
    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()
