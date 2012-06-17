from pymcserver import utils, components
import os
import pymcserver
import traceback
import urlparse

pagecode = """<table style="border-collapse: collapse; height: 100%; padding-top: 28px">
<tr>
<td class="sidebar">{0}</td>
<td class="content">{1}</td>
</tr>
</table>
"""

content = """<h1>{serverName}</h1>{err}
<table>
<tr>
<td style="width: 50%; padding-right: 8px">
    <h2>Console</h2>
    <form method="POST">
    <pre id="consoleLog" style="width: 100%; font-size: 8px; overflow-x: auto">{cons}</pre>
    <table>
    <tr>
    <td style="vertical-align: middle; padding-right: 8px">Command:</td>
    <td style="width: 100%"><input name="command" type="text" id="commandEntry" style="width: 100%" autocomplete="off"></td>
    <td style="padding-left: 12px"><input type="submit" value="Send"></td>
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
var xmlhttp = new XMLHttpRequest();
var sName = '%s';

function onLoad()
{
    document.getElementById("commandEntry").focus();
    setInterval(updateConsole, 1000);
    xmlhttp.onreadystatechange = onStateChanged;
}

function onStateChanged()
{
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
    {
        document.getElementById("consoleLog").innerHTML = xmlhttp.responseText;
    }
}

function updateConsole()
{
    xmlhttp.open("GET", "/api/" + sName + "/console", true);
    xmlhttp.send()
}

window.onload = onLoad;
</script>
"""

def handlePage(handler, res, path):
    # Parse URL
    split = path.split("/")
    sName = len(split) >= 2 and split[1] or None
    sAction = len(split) >= 3 and split[2] or None
    
    # Sidebar
    sidebar = """<h2>Servers</h2>
    <ul class="list">"""
    for k, v in pymcserver.server.run.allServers.iteritems():
        sidebar += '<li><a href="{0}">{1}</a></li>'.format("/manage/" + k, k)
    sidebar += '<li><a href="/new">Create new server</a></li>'
    sidebar += """</ul>"""
    if sName:
        sidebar += """<h2 style="margin-top: 96px">{0}</h2>
<ul class="list">
<li><a href="/manage/{0}/console">Console</a></li>
<li><a href="/manage/{0}/settings">Settings</a></li>
</ul>""".format(sName)
    
    if path == "/":
        res.code = 200
        res.endHeaders()
        
        # Server list content
        li = """<h1>Server list</h1>
        <table>"""
        for k, v in pymcserver.server.run.allServers.iteritems():
            li += "<tr>"
            li += '<td width="120px">{0}</td>'.format(k)
            li += "<td>{0}</td>".format(v.isRunning() and '<span style="color: green">Running</span>' or '<span style="color: red">Stopped</span>')
            li += "</tr>"
        li += "</table>"
        
        handler.wfile.write(components.makeHeader())
        handler.wfile.write(components.makeMenuBar(handler))
        handler.wfile.write(pagecode.format(sidebar, li))
        handler.wfile.write(components.makeFooter())
        
    elif sName != None:
        # Check to make sure the server exists
        if not (sName in pymcserver.server.run.allServers):
            res.code = 404
            handler.sendErrorPage(res)
            return
        
        if sAction == None:
            error = ""
            if handler.command == "POST":
                parse = urlparse.parse_qs(handler.rfile.read(int(handler.headers["Content-Length"])))
                
                try:
                    server = pymcserver.server.run.allServers[sName]
                    if "startServer" in parse:
                        if not server.isRunning():
                            server.startServer(None)
                            # Really stupid hack to get chrome on windows to prevent it from being
                            # stuck at loading the page.
                            res.code = 301
                            res.headers["Location"] = "/manage/%s" % sName
                            res.endHeaders()
                            return
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
                            utils.logAction(handler, "sent command %s" % com, sName)
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
                with pymcserver.server.run.allServers[sName].getLogFP() as f:
                    log = utils.escape(utils.tail(f))
            except:
                log = ""
                
            handler.wfile.write(components.makeHeader(extraHead=script % sName))
            handler.wfile.write(components.makeMenuBar(handler))
            handler.wfile.write(pagecode.format(sidebar, content.format(serverName=sName, cons=log, err=error)))
            handler.wfile.write(components.makeFooter())
        elif sAction == "settings":
            res.code = 200
            res.endHeaders()
            handler.wfile.write(components.makeHeader(extraHead=script % sName))
            handler.wfile.write(components.makeMenuBar(handler))
            handler.wfile.write(pagecode.format(sidebar, "Nothing yet..."))
            handler.wfile.write(components.makeFooter())
        else:
            res.code = 404
            handler.sendErrorPage(res)
    else:
        res.code = 404
        handler.sendErrorPage(res)
