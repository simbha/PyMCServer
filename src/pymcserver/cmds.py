# -*- coding: utf-8 -*-

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
