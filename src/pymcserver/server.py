'''
Created on May 14, 2012

@author: administrator
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

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
    def do_GET(self):
        self.send_response(200);
        self.end_headers();
        self.wfile.write("the w** sucks");