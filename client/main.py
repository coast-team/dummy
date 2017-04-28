from client import Client
import os
import sys
import time

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("[Usage] %s path_to_ip_file" % sys.argv[0])

    path_to_config = sys.argv[1]

    if not os.path.exists(path_to_config):
        sys.exit("Path to config file : %s doesn't exist" % path_to_config)

    client = Client('mute', path_to_config)
    client.getStatus()
    client.createCollaborator()
    client.startCollaborator()
    print('sleeping...')
    time.sleep(10)
    client.stopwritingCollaborator()
    client.stopreadingCollaborator()
