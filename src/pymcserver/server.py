from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pymcserver import cmds, utils, pagecookie, components, pageresource, \
    pagelogin
from pymcserver.utils import Session
import Cookie
import logging
import os
import readline
import socket
import sys
import threading
import time
import uuid
import shutil

server = None
log = logging.getLogger("PyMCServer")
accesslog = logging.getLogger("WebAccess")
datadir = "data"
active = True

_allCommands = {}

allErrors = {
    403: ("Forbidden", "You have no access to go to that page."),
    404: ("Not found", "The page does not exist."),
    405: ("Method not allowed", "Incorrect request method."),
    500: ("Server error", "Something went wrong. Check the PyMCServer logs.")
}

class WebServer():
    def __init__(self, host, port):        self.httpd = HTTPServer((host, port), MCHTTPRequestHandler)
        self.pageHandlers = {}        self.pageComponents = {}        self.allSessions = {}
        self.hostname = socket.gethostname()
        
        self.running = False
    
    def run(self):
        self.running = True
        self.httpd.serve_forever()
    
    def stop(self):
        self.running = False
        log.info("Stopping PyMCServer...")
        self.httpd.socket.close()
        
class MCHTTPRequestHandler(BaseHTTPRequestHandler):    def log_message(self, fmt, *args):
        accesslog.info(fmt % args)

    def do_GET(self):
        self.handlePage()
        
    def do_POST(self):
        self.handlePage()
    
    def handlePage(self):
        res = Response(self)
        sessid = None
        
        if "Cookie" in self.headers:
            c = Cookie.SimpleCookie(self.headers["Cookie"])            if "session" in c:
                sessid = c["session"].value
                
        self.cursessid = sessid
                
        # Create a session if cookie does not exist or is invalid
        if self.getSession(sessid) == None:
            cookie = Cookie.SimpleCookie()
            
            sessid = str(uuid.uuid4())
            self.cursessid = sessid
            server.allSessions[sessid] = Session()
            
            cookie["session"] = sessid
            cookie["session"]["Path"] = "/"
            
            res.headers["Set-Cookie"] = cookie.output(header="")
        else:
            # If session is valid, update the last visited time
            self.getSession(sessid).time = time.time()
        
        path = str(self.path)
        mod = path.split("/")[1]
        relpath = "/" + "/".join(path.split("/")[2:])
        handled = False
        
        # Prevent exploits
        if "/.." in path:
            res.code = 403
            self.sendErrorPage(res)
            return
        
        # Redirect / to /manage
        if path == "/":
            res.code = 301
            res.headers["Location"] = "/manage"
            res.endHeaders()
            return
        
        # Redirect /favicon.ico to /res/favicon.ico
        if path == "/favicon.ico":
            res.code = 301
            res.headers["Location"] = "/res/favicon.ico"
            res.endHeaders()
            return
        
        # Send client to login page if not logged in.
        session = self.getSession(sessid)
        if not (path == "/" or mod == "res" or mod == "login" or mod == "cookies") and not session.user:
            res.code = 301
            res.headers["Location"] = "/login"
            res.endHeaders()
            return
        
        if mod in server.pageHandlers:
            # Pass request to page handler
            server.pageHandlers[mod].handlePage(self, res, relpath)
            handled = True
        else:
            res.code = 404
            handled = False
        
        if not handled:
            self.sendErrorPage(res)
        
    def getSession(self, sessid=None):        """if sessid == None:
            if "Cookie" in self.headers:
                c = Cookie.SimpleCookie(self.headers["Cookie"])                if "session" in c:
                    sessid = c["session"].value
                    if sessid in server.allSessions:
                        return server.allSessions[sessid]
                    else:
                        return None                else:                    return None
            else:                return None"""
        
        if sessid == None:
            return server.allSessions[self.cursessid]
        
        if sessid in server.allSessions:
            return server.allSessions[sessid]
        else:
            return None
    
    def getServer(self):
        global server
        return server
    
    def sendErrorPage(self, res, message=None):
        self.send_response(res.code)
        for key, value in res.headers.iteritems():
            self.send_header(key, value)
        self.end_headers()
        
        msg = ""
        if message:
            msg = "\n<pre>%s</pre>" % message
        
        self.wfile.write(server.pageComponents["header"]())
        self.wfile.write("""<div class="centerBox">
<h2>%s - %s</h2>
<p>%s</p>%s
<p><a href="/">Back to PyMCServer home</a></p>
<p class="small" style="margin-top: 48px">PyMCServer version %s running on %s.</p>
</div>
""" % (res.code,
       allErrors.get(res.code, ("Unknown error"))[0],
       allErrors.get(res.code, (None, "Unknown description"))[1],
       msg,
       utils.getVersion(),
       server.hostname))
        self.wfile.write(server.pageComponents["footer"]())

class Response:
    def __init__(self, handler):
        self.code = 500
        self.headers = {}
        self.handler = handler
        
        self.headers["Content-Type"] = "text/html"
        
        self.__endheaders = False
        self.__headersStack = []
    
    def endHeaders(self):
        '''Once headers are sent, the page must be sent.'''
        self.handler.send_response(self.code)
        for key, value in self.headers.iteritems():
            self.handler.send_header(key, value)
        self.handler.end_headers()
        #self.__headersStack = traceback.format_stack()
        self.__endheaders = True
    
    def getWFile(self):
        return self.handler.wfile
    
    def getRFile(self):
        return self.handler.rfile
    
    def cancelResponse(self):
        self.__canceled = True

class ConsoleHandlerThread(threading.Thread):
    def run(self):
        #while server.running:
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
            if not server.running:
                break

def registerCommand(name, function):
    _allCommands[name] = function

def initServer():
    global log, accesslog, server
    utils.mkdir(datadir)
    
    configdir = os.path.join(datadir, "config")
    utils.mkdir(configdir)
    
    users = os.path.join(configdir, "users.txt")
    if not os.path.exists(users):
        shutil.copyfile("res/users.txt", users)
    
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
    log.info("Try 'admin' as user and 'w**SUCKS' as the password.")
    
    # Setup web access.log
    fh = logging.FileHandler(os.path.join(datadir, "access.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    accesslog.setLevel(logging.DEBUG)
    accesslog.addHandler(fh)
    
    # Register commands
    registerCommand("test", cmds.testCommand)
    registerCommand("pingas", cmds.testCommand)
    registerCommand("reload", cmds.reloadCommand)
    registerCommand("stop", cmds.stopCommand)
    
    server = WebServer("127.0.0.1", 8099)
    
    # Register page components
    server.pageComponents["header"] = components.makeHeader
    server.pageComponents["footer"] = components.makeFooter
    
    # Register page handlers
    server.pageHandlers["cookies"] = pagecookie
    server.pageHandlers["res"] = pageresource
    server.pageHandlers["login"] = pagelogin
    
    cons = ConsoleHandlerThread()
    if not "--noconsole" in sys.argv:        cons.start()
        
    try:
        server.run()
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt detected.")
    except EOFError:
        log.info("EOF from stdin detected.")
    finally:
        # Stop the server if its still running
        if server.running:
            server.stop()
