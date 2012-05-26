from pymcserver import utils
import cgi
import os
import pymcserver
import time
import urlparse

pagecode = """<table style="border-collapse: collapse; height: 100%; padding-top: 28px">
<tr>
<td class="sidebar" >{0}</td>
<td class="content">{1}</td>
</tr>
</table>
"""

sidebar = """<h2>Servers</h2>
<ul class="list">
<li><a href="#">pingas</a></li>
<li class="listSelected"><a href="#">pingas</a></li>
<li><a href="#">pingas</a></li>
<li><a href="#">pingas</a></li>
</ul>
"""

content = """<h2>Pingas</h2>
<table>
<tr>
<td style="width: 50%; padding-right: 8px">
    <h2>Console</h2>
    <form method="POST">
    <pre style="width: 100%; font-size: 8px; overflow-x: auto">{cons}
    </pre>
    <table>
    <tr>
    <td style="vertical-align: middle; padding-right: 8px">Command:</td>
    <td style="width: 100%"><input name="command" type="text" style="width: 100%"></td>
    <td style="padding-left: 12px"><input type="submit" value="Send"></input></td>
    </tr>
    </table>
    </form>
</td>
<td style="width: 50%; padding-left: 8px">
    <h2>Actions</h2>
    <ul>
    <li><a href="/manage/start">Start server</a></li>
    <li><a href="/manage/stop">Stop server</a></li>
    </ul>
</td>
</tr>
</table>
"""

#pagecode = """
#<div style="background: green; min-height: 100%">w** SUCKS
#</div>"""

def handlePage(handler, res, path):
    if path == "/":
        res.code = 200
        res.endHeaders()
        
        if handler.command == "POST":
            parse = urlparse.parse_qs(handler.rfile.read(int(handler.headers["Content-Length"])))
            com = parse["command"][0]
            pymcserver.server.run.allServers["server1"].sendCommand(com)
            time.sleep(1) # PINGAS!
            
        try:
            log = cgi.escape(utils.tail(open(os.path.join(pymcserver.server.run.allServers["server1"].getPath(), "server.log"))))
        except:
            log = ""
            
        handler.wfile.write(handler.getServer().pageComponents["header"]())
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write(pagecode.format(sidebar, content.format(cons = log)))
        handler.wfile.write(handler.getServer().pageComponents["footer"]())
            
    elif path == "/start":
        res.code = 301
        res.headers["Location"] = "/manage"
        res.endHeaders()
        pymcserver.server.run.allServers["server1"].startServer(None)
        
    elif path == "/stop":
        res.code = 301
        res.headers["Location"] = "/manage"
        res.endHeaders()
        pymcserver.server.run.allServers["server1"].stopServer(None)
    else:
        res.code = 404
        handler.sendErrorPage(res)
