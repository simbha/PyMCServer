import pymcserver

def makeHeader(extraHead=None, title=None):
    comp = """<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="/res/style.css" />{0}
<title>{1}</title>
</head>
<body>
<div id="wrapper">
"""

    ex = extraHead or ""
    ti = "%s - PyMCServer" % pymcserver.server.server.hostname
    
    return comp.format(ex, ti)

def makeFooter():
    return """</div>
</body>
</html>
"""

def makeMenuBar(handler):
    comp = """<div class="menubar">
<table>
<tr>
<td>
<ul class="menubarItems">
<li><a href="#">w** SUCKS</a></li><li><a href="#">PS3 &gt; w**</a></li>
</ul>
</td>
<td width="180px">
Logged in as: {0}
</td>
<td width="64px">
<a class="menuButton" href="/logout">Log out</a>
</td>
</tr>
</table>
</div>"""

    return comp.format(handler.getSession().user)