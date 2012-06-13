import pymcserver

def reloadCommand(args):
    log = pymcserver.server.log
    log.info("Reloading modules...")
    for v in pymcserver.server.server.pageHandlers.itervalues():
        reload(v)
        log.info("Reloaded " + v.__name__)

def shutdownCommand(args):
    pymcserver.server.server.stop()

def startCommand(args):
    if len(args) < 1:
        pymcserver.server.log.info("Usage: start <serverid>")
        return
    
    name = args[0]
    
    if name in pymcserver.server.run.allServers:
        srv = pymcserver.server.run.allServers[name]
        if not srv.isRunning():
            srv.startServer(None)
            pymcserver.server.log.info("Started server '%s'." % name)
        else:
            pymcserver.server.log.error("'%s' is already running." % name)
    else:
        pymcserver.server.log.error("No server named '%s'" % name)