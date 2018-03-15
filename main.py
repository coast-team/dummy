#!/usr/bin/env python3
from collaborator.http_server.http_server import entryPoint
from collaborator.controller import Controller
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) < 2:
        cwd = os.getcwd()
        path_to_config = os.getenv('CONFIG_PATH',
                                   cwd + '/config_files/example_mac.ini')
    else:
        path_to_config = sys.argv[1]

    if not os.path.exists(path_to_config):
        sys.exit("Path to config file : %s doesn't exist" % path_to_config)

    print("Loading from %s" % path_to_config)

    controller = Controller(path_to_config)
    entryPoint(controller)
