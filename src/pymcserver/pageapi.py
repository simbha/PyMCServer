from pymcserver import utils
import os
import pymcserver
def handlePage(handler, res, path):
    res.code = 200
    res.headers["Content-Type"] = "text/plain"
    res.endHeaders()
    # yeah hardcoded
    handler.wfile.write(utils.escape(utils.tail(open(os.path.join(pymcserver.server.run.allServers["server1"].getPath(), "server.log")))))