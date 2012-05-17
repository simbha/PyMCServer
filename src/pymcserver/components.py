def makeHeader(extraHead=None):
    comp = """<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="/res/style.css" />{0}
</head>
<body>
"""
    
    if extraHead:
        return comp.format(extraHead)
    else:
        return comp.format("")

def makeFooter():
    return """</body>
</html>
"""