import requests
import sys

if len(sys.argv) < 2:
    sys.exit('Usage: %s host-address' % sys.argv[0])

host = sys.argv[1]

print("TEST ---- Status")
addr1 = host + '/get/status'
print(addr1)
r1 = requests.get(addr1)
print(r1.text)

print("TEST ---- Create a collaborator")
addr2 = host + '/create/mute/collaborator'
print(addr2)
r2 = requests.post(addr2)
print(r2.text)

print("TEST ---- Start a collaborator")
addr3 = host + '/start/mute/collaborator'
print(addr3)
r3 = requests.put(addr3)
print(r3.text)

print("TEST ---- stop a collaborator")
addr4 = host + '/stop-writing/mute/collaborator'
print(addr4)
r4 = requests.put(addr4)
print(r4.text)

addr5 = host + '/stop-reading/mute/collaborator'
print(addr5)
r5 = requests.put(addr5)
print(r5.text)
