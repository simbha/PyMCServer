import pymcserver
import os
import subprocess
import time
import urllib

FNULL = open(os.devnull, "wb")

class ServerRunner():
    def __init__(self):
        self.allServers = {}

class BaseServer(object):
    def downloadServer(self):
        raise NotImplementedError()
    
    def getPath(self):
        raise NotImplementedError()
    
    def isRunning(self):
        raise NotImplementedError()
    
    def killServer(self):
        raise NotImplementedError()
        
    def startServer(self, args):
        raise NotImplementedError()
    
    def stopServer(self):
        raise NotImplementedError()
    
    def sendCommand(self, command):
        raise NotImplementedError()

# The stock MC server...
class StockServer(BaseServer):
    def __init__(self, path):
        self.path = path
        self.serverThread = None
        
        if not os.path.exists(self.path):
            os.makedirs(path)
    
    def getPath(self):
        return self.path
    
    def isRunning(self):
        if not (self.serverThread == None):
            return self.serverThread.poll() == None and True or False
        else:
            return False
        
    def sendCommand(self, command):
        self.serverThread.stdin.write(command + os.linesep)
         
    def startServer(self, args):
        if self.isRunning():
            return
        
        if not os.path.exists(os.path.join(self.path, "minecraft_server.jar")):
            raise RuntimeError
            
        self.serverThread = subprocess.Popen(["java", "-jar", "minecraft_server.jar", "nogui"], stdin=subprocess.PIPE, stdout=FNULL, stderr=FNULL, cwd=self.path)
    
    def stopServer(self):
        if not self.isRunning():
            return
        
        self.serverThread.stdin.write("stop" + os.linesep)
        
    def killServer(self):
        if not self.isRunning():
            return
        
        self.serverThread.kill()
    
class BukkitServer(StockServer):
    def __init__(self, path):
        super(BukkitServer, self).__init__(path)
        self.__dllasttime = time.time()
        
    def _reportHook(self, bn, bs, size):
        # Show download progress but only output to the console every second
        if time.time() - self.__dllasttime > 1:
            self.__dllasttime = time.time()
            totalblocks = size / bs
            dledblocks = bn
            progress = int((float(dledblocks) / float(totalblocks)) * 100)
            pymcserver.server.log.info("Downloading craftbukkit.jar... %s%%" % progress)
            
    def downloadServer(self):
        pymcserver.server.log.info("Downloading craftbukkit.jar...")
        urllib.urlretrieve("http://cbukk.it/craftbukkit.jar", os.path.join(self.path, "craftbukkit.jar"), self._reportHook)
        
    def startServer(self, args):
        if self.isRunning():
            return
        
        if not os.path.exists(os.path.join(self.path, "craftbukkit.jar")):
            self.downloadServer()
            
        self.serverThread = subprocess.Popen(["java", "-jar", "craftbukkit.jar", "--nojline"], stdin=subprocess.PIPE, stdout=FNULL, stderr=FNULL, cwd=self.path)