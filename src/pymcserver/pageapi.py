from pymcserver import utils
import os
import pymcserver

def handlePage(handler, res, path):
    res.headers["Content-Type"] = "text/plain"
    
    split = path.split("/")
    if len(split) < 3:
        res.code = 404
        res.endHeaders()
        return
    
    sName = split[1]
    action = split[2]
    
    # Check if server exists
    if not (sName in pymcserver.server.run.allServers):
        res.code = 404
        res.endHeaders()
        return
    server = pymcserver.server.run.allServers[sName]
    
    if action == "console":
        res.code = 200
        res.endHeaders()
        # yeah hardcoded
        handler.wfile.write(utils.escape(utils.tail(open(os.path.join(server.getPath(), "server.log")))))
    else:
        res.code = 404
        res.endHeaders()
