# This module handles everything on /res
import os
import mimetypes

__CONTENTDIR = "content"

def handlePage(handler, res, path):
    """Open a resource, find its mime type and send it."""
    res.code = 200
    
    if path == "/":
        res.code = 403
        handler.sendErrorPage(res)
        return
    
    # No need to handle parent directory exploit pingas, because
    # the web server pre-handles that.
    
    filepath = os.path.join(__CONTENTDIR, path.lstrip("/"))
    
    try:
        if os.path.isdir(filepath):
            res.code = 403
            handler.sendErrorPage(res)
            return
            
        # Read the file 4 KB at a time and send it
        with open(filepath, "rb") as f:
            # Get the mime type of the file and set the content type header
            mime = mimetypes.guess_type(filepath)[0]
            res.headers["Content-Type"] = mime
            res.endHeaders()
            
            while True:
                buf = f.read(4096)
                if len(buf) == 0:
                    break
                handler.wfile.write(buf)
    except IOError:
        res.code = 404
        handler.sendErrorPage(res)
