from pymcserver import utils
def handlePage(handler, res, path):
    if path == "/":
        # If user is logged in, then redirect to /
        if handler.getSession().user:
            res.code = 301
            res.headers["Location"] = "/"
            res.endHeaders()
        else:
            res.code = 200
            res.endHeaders()
            handler.wfile.write(handler.getServer().pageComponents["header"]())
            handler.wfile.write("""<div class="centerBox">
<h2>Log in to PyMCServer</h2>
<form action="action" method="post">
<table>
<tr>
<td width="50%">Username:</td><td width="50%"><input type="text" name="username"></td>
</tr>
<tr>
<td>Password:</td><td><input type="password" name="password"></td>
</tr>
<tr>
<td></td><td style="text-align: right"><input type="submit"></input></td>
</table>
</form>
<p class="small" style="margin-top: 48px">PyMCServer version {0} running on {1}.</p>
""".format(handler.getServer().hostname, utils.getVersion()))
            handler.wfile.write(handler.getServer().pageComponents["footer"]())
    elif path == "/action":
        if handler.command == "POST":
            pass
        else:
            res.code = 405
            handler.sendErrorPage(res)
    else:
        res.code = 404
        handler.sendErrorPage(res)