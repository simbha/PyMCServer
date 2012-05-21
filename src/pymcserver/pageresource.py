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
        # Get the mime type of the file and set the content type header
        mime = mimetypes.guess_type(filepath)[0]
        res.headers["Content-Type"] = mime
        res.endHeaders()
        
        # Read the file 4 KB at a time and send it
        with open(filepath) as f:
            while True:
                buf = f.read(4096)
                if len(buf) == 0:
                    break
                handler.wfile.write(buf)
            
    except IOError:
        handler.sendErrorPage(res)