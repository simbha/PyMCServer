def handlePage(handler, res, path):
    res.code = 200
    res.headers["Content-Type"] = "text/plain"
    res.endHeaders()
    handler.wfile.write("PINGAS!")