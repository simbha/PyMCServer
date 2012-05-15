from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pymcserver import utils
import logging
import os

server = None
log = logging.getLogger("PyMCServer")
accesslog = logging.getLogger("WebAccess")
datadir = "data"

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

def initServer():
    global log, accesslog, server
    utils.mkdir(datadir)
    
    # Setup console/file logging
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s"))
    fh = logging.FileHandler(os.path.join(datadir, "webserver.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s"))
    log.setLevel(logging.DEBUG)
    log.addHandler(sh)
    log.addHandler(fh)
    
    # Setup web access.log
    fh = logging.FileHandler(os.path.join(datadir, "access.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    accesslog.addHandler(fh)
    
    log.info("W** SUCKS")
    
    server = WebServer("127.0.0.1", 8099)
    
    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()
    