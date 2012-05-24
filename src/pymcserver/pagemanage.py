pagecode = """<table style="border-collapse: collapse; height: 100%; padding-top: 28px">
<tr>
<td style="background: green; width: 240px">1</td>
<td style="background: black">2</td>
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
        handler.wfile.write(handler.getServer().pageComponents["header"]())
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write(pagecode)
        handler.wfile.write(handler.getServer().pageComponents["footer"]())
    else:
        res.code = 404
        handler.sendErrorPage(res)