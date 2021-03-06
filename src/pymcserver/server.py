from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pymcserver import cmds, utils, pagecookie, pageresource, pagelogin, \
    pagemanage, pagelogout, runner, pagesettings, pagenew, pageapi, components, \
    pagetest
from pymcserver.utils import Session
import ConfigParser
import Cookie
import logging
import os
import shutil
import socket
import sys
import threading
import time
import traceback
import uuid

server = None
run = None
log = logging.getLogger("PyMCServer")
accesslog = logging.getLogger("WebAccess")
DATADIR = "data"
RESDIR = "res"

_allCommands = {}

allErrors = {
    403: ("Forbidden", "You have no access to go to that page."),
    404: ("Not found", "The page does not exist."),
    405: ("Method not allowed", "Incorrect request method."),
    500: ("Server error", "Something went wrong. Check the PyMCServer logs.")
}

class WebServer():
    def __init__(self, host, port):
        self.httpd = HTTPServer((host, port), MCHTTPRequestHandler)
        self.pageHandlers = {}
        self.allSessions = {}
        self.hostname = socket.gethostname()
        
        self.running = False
    
    def run(self):
        self.running = True
        self.httpd.serve_forever()
    
    def stop(self):
        self.running = False
        log.info("Stopping PyMCServer...")
        self.httpd.shutdown()
        
class MCHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        accesslog.info(fmt % args)
    
    def do_GET(self):
        self.handlePage()
        
    def do_POST(self):
        self.handlePage()
    
    def getResource(self, path):
        '''Get a resource as string'''
        with self.getResourceFP(path) as f:
            return f.read()
    
    def getResourceFP(self, path):
        '''Get a resource as a file pointer'''
        return open(os.path.join(RESDIR, path), "rb")
    
    def putResource(self, path):
        '''Place a resource directly into the page'''
        with self.getResourceFP(path) as f:
            while True:
                buf = f.read(4096)
                if len(buf) == 0:
                    break
                self.wfile.write(buf)
    
    def handlePage(self):
        res = Response(self)
        sessid = None
        
        if "Cookie" in self.headers:
            c = Cookie.SimpleCookie(self.headers["Cookie"])
            if "session" in c:
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
        
        # Special case for /api, do not redirect, send a 403 instead.
        if mod == "api" and not session.user:
            res.code = 403
            res.endHeaders()
            return
        
        # Send client to login page for everything else
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
        
    def getSession(self, sessid=None):
        """if sessid == None:
            if "Cookie" in self.headers:
                c = Cookie.SimpleCookie(self.headers["Cookie"])
                if "session" in c:
                    sessid = c["session"].value
                    if sessid in server.allSessions:
                        return server.allSessions[sessid]
                    else:
                        return None
                else:
                    return None
            else:
                return None"""
        
        if sessid == None:
            return server.allSessions.get(self.cursessid, None)
        
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
        
        self.wfile.write(components.makeHeader())
        self.wfile.write("""<div class="centerBox">
<h2>%s - %s</h2>
<p>%s</p>%s
<p><a href="/">Back to PyMCServer home</a></p>
<p class="small" style="margin-top: 48px">PyMCServer version %s running on %s.</p>
</div>
""" % (res.code,
       allErrors.get(res.code, ("Unknown error"))[0],
       allErrors.get(res.code, (None, "Unknown description."))[1],
       msg,
       utils.getVersion(),
       server.hostname))
        self.wfile.write(components.makeFooter())

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
        
        # Some hack to prevent chrome to screw up redirects
        if self.code == 301:
            self.headers["Cache-Control"] = "no-cache"
        
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
    def __init__(self):
        super(ConsoleHandlerThread, self).__init__()
        self.setName("ConsoleHandlerThread")
        
    def run(self):
        line = raw_input("> ")
        while True:
            try:
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
            except:
                traceback.print_exc()
            if not server.running:
                break
            line = raw_input("> ")

def registerCommand(name, function):
    _allCommands[name] = function

def initServer():
    global log, accesslog, server, run
    startTime = time.time()
    
    # Setup data directory
    utils.mkdir(DATADIR)
    configdir = os.path.join(DATADIR, "config")
    utils.mkdir(configdir)
    serverdir = os.path.join(DATADIR, "servers")
    utils.mkdir(serverdir)
    
    # Setup console/file logging
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    fh = logging.FileHandler(os.path.join(DATADIR, "webserver.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.setLevel(logging.DEBUG)
    log.addHandler(sh)
    log.addHandler(fh)
    log.info("Starting PyMCServer, version " + utils.getVersion())
    
    # Setup user list
    users = os.path.join(configdir, "users.txt")
    if not os.path.exists(users):
        shutil.copyfile(os.path.join(RESDIR, "users.txt"), users)
    
    # Setup config file
    conf = ConfigParser.RawConfigParser()
    conf.read(os.path.join(RESDIR, "config.ini"))
    confpath = os.path.join(configdir, "config.ini")
    
    if os.path.exists(confpath):
        with open(confpath, "r") as fi:
            conf.readfp(fi)
    with open(confpath, "w") as fi:
        conf.write(fi)
    
    # Import readline, if available
    try:
        if not "--noreadline" in sys.argv:
            import readline
            readline.clear_history()
    except ImportError:
        pass
    
    # Setup web access.log
    fh = logging.FileHandler(os.path.join(DATADIR, "access.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    accesslog.setLevel(logging.DEBUG)
    accesslog.addHandler(fh)
    
    # Register console commands
    registerCommand("list", cmds.listCommand)
    registerCommand("reload", cmds.reloadCommand)
    registerCommand("shutdown", cmds.shutdownCommand)
    registerCommand("start", cmds.startCommand)
    registerCommand("stop", cmds.stopCommand)
    
    # Setup server
    server = WebServer(conf.get("web", "listen"), conf.getint("web", "port"))
    
    # Register page handlers
    server.pageHandlers["api"] = pageapi
    server.pageHandlers["cookies"] = pagecookie
    server.pageHandlers["res"] = pageresource
    server.pageHandlers["login"] = pagelogin
    server.pageHandlers["logout"] = pagelogout
    server.pageHandlers["manage"] = pagemanage
    server.pageHandlers["new"] = pagenew
    server.pageHandlers["settings"] = pagesettings
    server.pageHandlers["test"] = pagetest
    
    # Import all the servers
    run = runner.ServerRunner()
    
    for i in os.listdir(serverdir):
        path = os.path.join(serverdir, i)
        if os.path.isdir(path):
            run.allServers[i] = runner.BukkitServer(path)
            log.info("Loaded server '%s'" % i)
    
    # Import extra servers from config.ini
    if conf.has_section("extraservers"):
        sec = dict(conf.items("extraservers"))
        for k, v in sec.iteritems():
            run.allServers[k] = runner.BukkitServer(v)
            log.info("Loaded extra server '%s'" % k)
    
    log.info("Done (%ss)!" % str(round(time.time() - startTime, 2)))
    log.info("The URL is: http://%s:%s" % ("localhost", conf.get("web", "port")))
    log.info("Try 'admin' as user and 'w**SUCKS' as the password.")
    
    # Create console handler
    cons = ConsoleHandlerThread()
    if not "--noconsole" in sys.argv:
        cons.start()
    
    try:
        server.run()
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt detected.")
    except EOFError:
        log.info("EOF from stdin detected.")
    finally:
        # Stop all mc servers
        for k, v in run.allServers.iteritems():
            log.info("Stopping server '%s'" % k)
            v.stopServer()
            
        # Stop the server if its still running
        if server.running:
            server.stop()
