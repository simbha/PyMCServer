# -*- coding: utf-8 -*-
import pymcserver

def testCommand(args):
    print """
§§§§§__§§__§§§____§§___§§§§______§§______§§§§
§§__§§_§§__§§_§§__§§__§§___§§___§§§§___§§§__§§
§§__§§_§§__§§_§§__§§_§§_________§§§§___§§
§§§§§__§§__§§__§§_§§_§§___§§§__§§__§§____§§§
§§_____§§__§§__§§_§§_§§____§§__§§§§§§______§§
§§_____§§__§§__§§_§§__§§__§§§_§§____§§_§§§__§§
§§_____§§__§§___§§§§____§§§§__§§____§§___§§§§
""".strip()
    print " | ".join(args)

def reloadCommand(args):
    log = pymcserver.server.log
    log.info("Reloading modules...")
    for v in pymcserver.server.server.pageHandlers.itervalues():
        reload(v)
        log.info("Reloaded " + v.__name__)

def shutdownCommand(args):
    pymcserver.server.log.warning("Shutdown command is glitchy, yeah threading is hard...")
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