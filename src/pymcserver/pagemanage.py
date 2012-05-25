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

#pagecode = """
#<div style="background: green; min-height: 100%">w** SUCKS
#</div>"""

def handlePage(handler, res, path):
    if path == "/":
        res.code = 200
        res.endHeaders()
        handler.wfile.write(handler.getServer().pageComponents["header"]())
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write(pagecode.format(sidebar, "pingas"))
        handler.wfile.write(handler.getServer().pageComponents["footer"]())
    else:
        res.code = 404
        handler.sendErrorPage(res)