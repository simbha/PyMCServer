from pymcserver import utils
import os
import pymcserver
import runner
import urlparse

postbox = """<div class="centerBox">
<h2>Create new Server</h2>{error}
<form method="post">
<table>
<tr><td width="50%">Server name:</td><td width="50%"><input type="text" name="serverName"></td></tr>
<tr><td></td><td><span class="small">Server name must be alphanumeric.</span><td></tr>
<tr><td><div class="formSeperator"></div></td></tr>
<tr><td>Port:</td><td><input type="text" name="port" value="25565"></td></tr>
<tr><td></td><td><span class="small">This doesn't work actually...</span><td></tr>
<tr><td><div class="formSeperator"></div></td></tr>
<tr><td></td><td style="text-align: right"><input type="submit"></td></tr>
</table>
</form>
</div>
"""

def handlePage(handler, res, path):
    if path == "/":
        if handler.command == "GET":
            res.code = 200
            res.endHeaders()
            handler.wfile.write(components.makeHeader())
            handler.wfile.write(components.makeMenuBar(handler))
            handler.wfile.write(postbox.format(error=""))
            handler.wfile.write(components.makeFooter())
        elif handler.command == "POST":
            parse = urlparse.parse_qs(handler.rfile.read(int(handler.headers["Content-Length"])))
            try:
                name = parse["serverName"][0]
                port = parse["port"][0]
                if not name.isalnum():
                    raise Exception("Name isn't alphanumeric.")
                if name in pymcserver.server.run.allServers:
                    raise Exception("There is already a server named '%s'" % name)
                
                utils.logAction(handler, "created a new server called %s." % name)
                pymcserver.server.run.allServers[name] = runner.BukkitServer(os.path.join(pymcserver.server.datadir, "servers", name))
                pymcserver.server.log.info("Created server %s..." % name)
                res.code = 301
                res.headers["Location"] = "/manage"
                res.endHeaders()
            except KeyError:
                res.code = 200
                res.endHeaders()
                handler.wfile.write(components.makeHeader())
                handler.wfile.write(components.makeMenuBar(handler))
                handler.wfile.write(postbox.format(error='<p class="error">Some form entries are missing.</p>'))
                handler.wfile.write(components.makeFooter())
            except Exception, e:
                handler.wfile.write(components.makeHeader())
                handler.wfile.write(components.makeMenuBar(handler))
                handler.wfile.write(postbox.format(error='<p class="error">%s</p>' % utils.escape(e.message)))
                handler.wfile.write(components.makeFooter())
    else:
        res.code = 404
        handler.sendErrorPage(res)
