def handlePage(handler, res, path):
    if path == "/":
        # If user is logged in, then redirect to /
        if handler.getSession().user:
            res.code = 301
            res.headers["Location"] = "/"
            res.end_headers()
        else:
            res.code = 200
            res.end_headers()
    elif path == "/action":
        if handler.command == "POST":
            pass
        else:
            res.code = 405
            handler.sendErrorPage(res)
    else:
        res.code = 404
        handler.sendErrorPage(res)