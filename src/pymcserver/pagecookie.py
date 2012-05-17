def handlePage(handler, res, path):
    res.code = 200
    res.headers["Content-Type"] = "text/plain"
    res.endHeaders()
    wfile = res.getWFile()
    wfile.write(handler.headers)
    wfile.write("\n")
    wfile.write(handler.getServer().allSessions)