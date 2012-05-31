from pymcserver import utils
import cgi
import os
import pymcserver
import time
import traceback
import urlparse

pagecode = """<table style="border-collapse: collapse; height: 100%; padding-top: 28px">
<tr>
<td class="sidebar">{0}</td>
<td class="content">{1}</td>
</tr>
</table>
"""


content = """<h1>Pingas</h1>{err}
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
    <td style="width: 100%"><input name="command" type="text" id="commandEntry" style="width: 100%"></td>
    <td style="padding-left: 12px"><input type="submit" value="Send"></input></td>
    </tr>
    </table>
    </form>
</td>
<td style="width: 50%; padding-left: 8px">
    <h2>Actions</h2>
    <!--<ul>
    <li><a href="/manage/start">Start server</a></li>
    <li><a href="/manage/stop">Stop server</a></li>
    </ul>-->
    <form method="POST">
    <ul>
    <li><input type="submit" name="startServer" value="Start server"></li>
    <li><input type="submit" name="stopServer" value="Stop server"></li>
    <li><input type="submit" name="killServer" value="Force stop server"></li>
    </ul>
    </form>
</td>
</tr>
</table>
"""

script = """<script type="text/javascript">
function onLoad()
{
    document.getElementById("commandEntry").focus();
}
window.onload = onLoad
</script>
"""

#pagecode = """
#<div style="background: green; min-height: 100%">w** SUCKS
#</div>"""

def handlePage(handler, res, path):
    if path == "/":
        error = ""
        '''if handler.command == "POST":
            parse = urlparse.parse_qs(handler.rfile.read(int(handler.headers["Content-Length"])))
            
            try:
                server = pymcserver.server.run.allServers["server1"]
                if "startServer" in parse:
                    if not server.isRunning():
                        server.startServer(None)
                    else:
                        error = "Server is already running."
                elif "stopServer" in parse:
                    if server.isRunning():
                        server.stopServer()
                    else:
                        error = "Server is already stopped."
                elif "killServer" in parse:
                    if server.isRunning():
                        server.killServer()
                    else:
                        error = "Server is already stopped."
                elif "command" in parse:
                    if server.isRunning():
                        com = parse["command"][0]
                        server.sendCommand(com)
                        time.sleep(1) # PINGAS!
                    else:
                        error = "The server is not running."
                    
                if error:
                    error = """<p class="error">{0}</p>\n""".format(error)
                else:
                    error = ""
            except:
                traceback.print_exc()
            
        res.code = 200
        res.endHeaders()
            
        try:
            log = cgi.escape(utils.tail(open(os.path.join(pymcserver.server.run.allServers["server1"].getPath(), "server.log"))))
        except:
            log = ""
            
        handler.wfile.write(handler.getServer().pageComponents["header"](extraHead=script))
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write(pagecode.format(sidebar, content.format(cons=log, err=error)))
        handler.wfile.write(handler.getServer().pageComponents["footer"]())'''
        
        sidebar = """<h2>Servers</h2>
        <ul class="list">"""
        for k, v in pymcserver.server.run.allServers.iteritems():
            sidebar += '<li><a href="{0}">{1}</a></li>'.format("/manage/" + k, k)
        sidebar += '<li><a href="/new">Create new server</a></li>'
        sidebar += """</ul>"""
        
        content = """<h1>Server list</h1>
        <table>"""
        for k, v in pymcserver.server.run.allServers.iteritems():
            content += "<tr>"
            content += '<td width="120px">{0}</td>'.format(k)
            content += "<td>{0}</td>".format(v.isRunning() and '<span style="color: green">Running</span>' or '<span style="color: red">Stopped</span>')
            content += "</tr>"
        content += "</table>"
        
        handler.wfile.write(handler.getServer().pageComponents["header"](extraHead=script))
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write(pagecode.format(sidebar, content))
        handler.wfile.write(handler.getServer().pageComponents["footer"]())
        
    else:
        res.code = 404
        handler.sendErrorPage(res)
