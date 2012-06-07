# List all cookies, this was used for testing. Should be moved to a server command.
def handlePage(handler, res, path):
    res.code = 404
    res.endHeaders()
    return
    '''res.code = 200
    res.headers["Content-Type"] = "text/plain"
    res.endHeaders()
    wfile = res.getWFile()
    wfile.write(handler.headers)
    wfile.write("\n")
    for key, value in handler.getServer().allSessions.iteritems():
        wfile.write(key + ":\n")
        for k, v in value.__dict__.iteritems():
            wfile.write("    %s: %s\n" % (k, v))'''