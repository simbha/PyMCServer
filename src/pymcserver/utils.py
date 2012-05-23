import subprocess
import os
import time
from ConfigParser import ConfigParser

curversion = None

class Session:    def __init__(self):
        self.user = None        self.time = time.time()

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getVersion():
    global curversion
    
    if not curversion:
        try:
            com = subprocess.Popen(["git", "describe", "--tags"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = com.stdout.readline().rstrip("\n")
            com.wait()
            
            curversion = output
        except:
            curversion = "UNKNOWNVERSION"
    
    return curversion