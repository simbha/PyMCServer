import pymcserver
import urlparse

pagecode = """<table style="border-collapse: collapse; height: 100%; padding-top: 28px">
<tr>
<td class="sidebar" >{0}</td>
<td style="background: black">{1}</td>
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
<p><a href="/manage/start">Start server</a></p>
<p><a href="/manage/stop">Stop server</a></p>
<form method="POST">
<p>Command: <input type="text" name="command"> <input type="submit" value="Send"></p>
</form>
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
            
        handler.wfile.write(handler.getServer().pageComponents["header"]())
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write(pagecode.format(sidebar, content))
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
