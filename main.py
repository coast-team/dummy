from collaborator.mute_collaborator.mute_collaborator import MuteCollaborator
from collaborator.network_tracker.network_tracker import NetworkTracker
from collaborator.dummy_error.configfile_error import ConfigfileError
import time
import sys

t = []
print("Test Network")
network_tracker = NetworkTracker("./test")
network_tracker.start()
for n in range(3):
    try:
        t.append(MuteCollaborator('./example.ini', n))
    except ConfigfileError:
        sys.exit(1)
print("Start")
for c in t:
    c.start()
print("Pending ...")
time.sleep(60)
print("ending ...")
for c in t:
    c.killWriter()

for c in t:
    c.killReader()

for c in t:
    c.join()

network_tracker.kill()
network_tracker.join()
