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