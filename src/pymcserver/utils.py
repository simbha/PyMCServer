import subprocess
import os
import time

curversion = None
VERSION = "0.1"

class Session:
    def __init__(self):
        self.user = None
        self.time = time.time()

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
def tail(f, window=20):
    BUFSIZ = 2048
    f.seek(0, 2)
    bytes = f.tell()
    size = window
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if (bytes - BUFSIZ > 0):
            # Seek back one whole BUFSIZ
            f.seek(block*BUFSIZ, 2)
            # read BUFFER
            data.append(f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.append(f.read(bytes))
        linesFound = data[-1].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return '\n'.join(''.join(data).splitlines()[-window:])

def getVersion():
    global curversion
    
    if not curversion:
        try:
            com = subprocess.Popen(["git", "describe", "--tags"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            output = com.stdout.readline().rstrip("\n")
            com.wait()
            
            curversion = output
        except:
            curversion = VERSION
    
    return curversion
