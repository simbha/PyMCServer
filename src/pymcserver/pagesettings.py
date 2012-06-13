pagecode = """<table style="border-collapse: collapse; height: 100%; padding-top: 28px">
<tr>
<td class="sidebar">{0}</td>
<td class="content">{1}</td>
</tr>
</table>
"""

sidebar = """<h2>Settings</h2>
<ul class="list">
<li><a href="/settings/users">Users</a></li>
<li><a href="/settings/console">PyMCServer Console</a></li>
</ul>"""

def handlePage(handler, res, path):
    res.code = 200
    
    if path == "/":
        res.endHeaders()
        handler.wfile.write(handler.getServer().pageComponents["header"]())
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write(pagecode.format(sidebar, "a pingas"))
        handler.wfile.write(handler.getServer().pageComponents["footer"]())
    else:
        res.code = 404
        handler.sendErrorPage(res)