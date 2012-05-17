import commands
import os
import time

class Session:
        self.user = None

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getVersion():
    output = commands.getstatusoutput("git describe --tags")
    if output[0] == 0:
        return output[1]
    else:
        return "UNKNOWNVERSION"