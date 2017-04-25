#!/usr/bin/env python3
from collaborator.http_server.http_server import entryPoint
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) < 2:
        path_to_config = os.getenv('CONFIG_PATH', './config_files/example.ini')
    else:
        path_to_config = sys.argv[1]

    if not os.path.exists(path_to_config):
        sys.exit("Path to config file : %s doesn't exist" % path_to_config)
    entryPoint(path_to_config)
