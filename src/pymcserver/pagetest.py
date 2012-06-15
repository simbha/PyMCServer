def handlePage(handler, res, path):
    res.code = 200
    res.headers["Content-Type"] = "video/mp4"
    res.endHeaders()
    handler.wfile.write(handler.putResource("genesis.mp4"))