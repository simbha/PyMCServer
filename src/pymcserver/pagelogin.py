from pymcserver import utils, components
import hashlib
import os
import pymcserver
import urlparse

postbox = """<div class="centerBox">
<h2>Log in to PyMCServer</h2>
<form method="post">
<table>
<tr>
<td width="50%">Username:</td><td width="50%"><input type="text" name="username"></td>
</tr>
<tr>
<td>Password:</td><td><input type="password" name="password"></td>
</tr>
<tr>
<td></td><td style="text-align: right"><input type="submit"></td>
</tr>
</table>
</form>{0}
<p class="small" style="margin-top: 48px">PyMCServer version {1} running on {2}.</p>
"""

def isAuthorized(user, pasw):
    with open(os.path.join(pymcserver.server.datadir, "config", "users.txt")) as f:
        for line in f:
            spl = line.split(":")
            name = spl[0] # there's a prequel to SPL1? oh no!
            passhash = spl[1].rstrip()
            
            if user == name:
                md5 = hashlib.md5()
                md5.update(pasw)
                if passhash == md5.hexdigest():
                    return True
                else:
                    return False
    return False

def handlePage(handler, res, path):
    if path == "/":
        # If user is logged in, then redirect to /
        if handler.getSession().user:
            res.code = 301
            res.headers["Location"] = "/"
            res.endHeaders()
        else:
            if handler.command == "GET":
                res.code = 200
                res.endHeaders()
                handler.wfile.write(components.makeHeader())
                handler.wfile.write(postbox.format("", utils.getVersion(), handler.getServer().hostname))
                handler.wfile.write(components.makeFooter())
            if handler.command == "POST":
                parse = urlparse.parse_qs(handler.rfile.read(int(handler.headers["Content-Length"])))
                
                try:
                    u = parse["username"][0]
                    p = parse["password"][0]
                except KeyError:
                    res.code = 200
                    res.endHeaders()
                    err = "\n<p class=\"error\">Missing username/password.</p>"
                    
                    handler.wfile.write(components.makeHeader())
                    handler.wfile.write(postbox.format(err, utils.getVersion(), handler.getServer().hostname))
                    handler.wfile.write(components.makeFooter())
                    return
                
                if isAuthorized(u, p):
                    handler.getSession().user = u
                    utils.logAction(handler, "(%s) logged in to PyMCServer." % handler.client_address[0])
                    res.code = 301
                    res.headers["Location"] = "/manage"
                    res.endHeaders()
                else:
                    utils.logAction(handler, "(%s) failed to log in to PyMCServer." % handler.client_address[0])
                    res.code = 200
                    res.endHeaders()
                    err = "\n<p class=\"error\">Username/password not correct.</p>"
                    
                    handler.wfile.write(components.makeHeader())
                    handler.wfile.write(postbox.format(err, utils.getVersion(), handler.getServer().hostname))
                    handler.wfile.write(components.makeFooter())
                    return
    else:
        res.code = 404
        handler.sendErrorPage(res)
