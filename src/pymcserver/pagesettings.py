from pymcserver import components
import hashlib
import urlparse

pagecode = """<table style="border-collapse: collapse; height: 100%; padding-top: 28px">
<tr>
<td class="sidebar">{0}</td>
<td class="content">{1}</td>
</tr>
</table>
"""

sidebar = """<h2>Settings</h2>
<ul class="list">
<li><a href="/settings/pass">Change Password</a></li>
<li><a href="/settings/console">Console</a></li>
<li><a href="/settings/about">About PyMCServer</a></li>
</ul>"""

about = """<h1>About PyMCServer</h1>
<p>A web based Minecraft server administration console written in Python.</p>
<p>Note that PyMCServer is in <b>ALPHA</b>, it is unfinished and bugs are everywhere.
It's not recommended for production use.</p>
"""

usersPage = """<h1>Change Password</h1>{err}
<p>Change the admin user's password. (no multi user yet)</p>
<form method="POST">
<table style="width: 320px">
<tr><td>New password:</td><td><input type="password" name="newpass"></td></tr>
<tr><td>Confirm password:</td><td><input type="password" name="confirmpass"></td></tr>
<tr><td></td><td style="text-align: right"><input type="submit"></input>
</table>
</form>
"""

def handlePage(handler, res, path):
    if path == "/":
        res.endHeaders()
        handler.wfile.write(components.makeHeader())
        handler.wfile.write(components.makeMenuBar(handler))
        handler.wfile.write(pagecode.format(sidebar, "<h1>Settings</h1>\n<p>Click on a setting on the sidebar.</p>"))
        handler.wfile.write(components.makeFooter())
    elif path == "/pass":
        error = ""
        if handler.command == "POST":
            try:
                parse = urlparse.parse_qs(handler.rfile.read(int(handler.headers["Content-Length"])))
                newpass = parse["newpass"][0]
                confirmpass = parse["confirmpass"][0]
                if newpass != confirmpass:
                    raise Exception("New passwords don't match.")
                with open("./data/config/users.txt", "wb") as f:
                    f.write("admin:" + hashlib.md5(newpass).hexdigest())
                error = "Password changed."
            except KeyError:
                error = "Form not filled out completely."
            except Exception, e:
                error = e.message
            
        res.code = 200
        res.endHeaders()
        handler.wfile.write(components.makeHeader())
        handler.wfile.write(components.makeMenuBar(handler))
        handler.wfile.write(pagecode.format(sidebar, usersPage.format(err=error and "<p class=\"error\">%s</p>" % error or "")))
        handler.wfile.write(components.makeFooter())
    elif path == "/console":
        res.code = 404
        handler.sendErrorPage(res)
    elif path == "/about":
        res.code = 200
        res.endHeaders()
        handler.wfile.write(components.makeHeader())
        handler.wfile.write(components.makeMenuBar(handler))
        handler.wfile.write(pagecode.format(sidebar, about))
        handler.wfile.write(components.makeFooter())
    else:
        res.code = 404
        handler.sendErrorPage(res)