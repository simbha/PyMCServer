def handlePage(handler, res, path):
    if path == "/":
        res.code = 200
        res.endHeaders()
        handler.wfile.write(handler.getServer().pageComponents["header"]())
        handler.wfile.write(handler.getServer().pageComponents["menubar"](handler))
        handler.wfile.write("<p>w** SUCKS</p>")
        handler.wfile.write(handler.getServer().pageComponents["footer"]())
    else:
        res.code = 404
        handler.sendErrorPage(res)