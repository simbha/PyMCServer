import pymcserver

def listCommand(args):
    pymcserver.server.log.info("Server list:")
    for k, v in pymcserver.server.run.allServers.iteritems():
        running = v.isRunning() and "running" or "stopped"
        pymcserver.server.log.info("- %s (%s)" % (k, running))

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
        
def stopCommand(args):
    if len(args) < 1:
        pymcserver.server.log.info("Usage: stop <serverid>")
        return
    
    name = args[0]
    
    if name in pymcserver.server.run.allServers:
        srv = pymcserver.server.run.allServers[name]
        if srv.isRunning():
            srv.stopServer()
            pymcserver.server.log.info("Stopped server '%s'." % name)
        else:
            pymcserver.server.log.error("'%s' is already stopped." % name)
    else:
        pymcserver.server.log.error("No server named '%s'" % name)
