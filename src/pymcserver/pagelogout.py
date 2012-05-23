postbox = """<div class="centerBox">
<h2>Logging out...</h2>
<p style="margin-top: 8px">Go <a href="/">here</a> you didn't redirect.</p>
</div>
"""

def handlePage(handler, res, path):
    # Why a meta refresh instead of a redirect. Well, chrome
    # seems to break the "logout" button and instead puts you
    # to the manage page again, instead of logging out, so
    # I used a meta refresh as a hack.
    if path == "/":
        handler.getSession().user = None
        handler.wfile.write(handler.getServer().pageComponents["header"](extraHead="""<meta http-equiv="refresh" content="1; url=/">\n"""))
        handler.wfile.write(postbox)
        handler.wfile.write(handler.getServer().pageComponents["footer"]())
    else:
        res.code = 404
        handler.sendErrorPage(res)