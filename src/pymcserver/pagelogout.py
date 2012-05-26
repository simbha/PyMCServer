def handlePage(handler, res, path):
    if path == "/":
        handler.getSession().user = None
        res.code = 301
        res.headers["Location"] = "/"
        res.endHeaders()
    else:
        res.code = 404
        handler.sendErrorPage(res)