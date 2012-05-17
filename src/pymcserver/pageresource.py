# This module handles everything on /res
import os
import mimetypes

__RESDIR="./res"

def handlePage(handler, res, path):
    """Open a resouce, find its mime type and send it."""
    res.code = 200
    
    if path == "/":
        res.code = 403
        handler.sendErrorPage(res)
        return
    
    # No need to handle parent directory exploit pingas, because
    # the web server pre-handles that.
    
    filepath = os.path.join(__RESDIR, path.lstrip("/"))
    
    try:
        mime = mimetypes.guess_type(filepath)[0]
        res.headers["Content-Type"] = mime
        res.endHeaders()
        
        f = open(filepath)
        while True:
            buffer = f.read(4096)
            if len(buffer) == 0:
                break # eof 
            handler.wfile.write(buffer)
            
    except IOError:
        handler.sendErrorPage(res)