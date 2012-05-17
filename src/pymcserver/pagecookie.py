def handlePage(handler, res, path):
    res.code = 200
    res.endHeaders()
    wfile = res.getWFile()