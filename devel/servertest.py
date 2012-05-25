import sys
import os
import urllib
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists("server"):
    os.mkdir("server")
    
if not os.path.exists(os.path.join("server", "craftbukkit.jar")):
    print("Dling CB...")
    urllib.urlretrieve("http://cbukk.it/craftbukkit.jar", os.path.join("server", "craftbukkit.jar"))

try:
    print("Starting CB")
    bukkit = subprocess.Popen(["java", "-jar", "craftbukkit.jar", "--nojline"], stdin=subprocess.PIPE, cwd="server")
    bukkit.stdin.write("say PIIIIIIIIIINGGGGGGGGGASSSSSS BOOOM!\n")
    bukkit.stdin.write("stop\n")
    bukkit.wait()
    print("Bukkit stopped")
except KeyboardInterrupt:
    bukkit.send_signal(9)