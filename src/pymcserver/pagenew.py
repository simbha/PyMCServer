def handlePage(handler, res, path):
    res.code = 404
    handler.sendErrorPage(res)