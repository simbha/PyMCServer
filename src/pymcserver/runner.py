import os
import subprocess
import urllib

class ServerRunner():
    def __init__(self):
        self.allServers = {}

class BaseServer(object):
    def isRunning(self):
        raise NotImplementedError()
    
    def downloadServer(self):
        raise NotImplementedError()
    
    def getPath(self):
        raise NotImplementedError()
    
    def killServer(self, args):
        raise NotImplementedError()
        
    def startServer(self, args):
        raise NotImplementedError()
    
    def stopServer(self, args):
        raise NotImplementedError()
    
    def sendCommand(self, command):
        raise NotImplementedError()
    
class BukkitServer(BaseServer):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(path)
        
    def downloadServer(self):
        urllib.urlretrieve("http://cbukk.it/craftbukkit.jar", os.path.join(self.path, "craftbukkit.jar"))
    
    def getPath(self):
        return self.path
        
    def sendCommand(self, command):
        self.serverThread.stdin.write(command + os.linesep)
         
    def startServer(self, args):
        if not os.path.exists(os.path.join(self.path, "craftbukkit.jar")):
            self.downloadServer()
            
        self.serverThread = subprocess.Popen(["java", "-jar", "craftbukkit.jar", "--nojline"], stdin=subprocess.PIPE, cwd=self.path)
    
    def stopServer(self, args):
        self.serverThread.stdin.write("stop" + os.linesep)
        self.serverThread.wait()
        
    def killServer(self, args):
        self.serverThread.kill()