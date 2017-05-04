import threading
import utils
HTTP = "http://"
PORT = ":8000"


class Client(object):
    """docstring for Client."""
    def __init__(self, collab_type, path_to_addresses_file):
        self.__collab_type = collab_type
        self.__addresses = self.getAddresses(path_to_addresses_file)

    def getAddresses(self, path_to_addresses_file):
        with open(path_to_addresses_file, 'r') as file:
            ip_addresses = [
                HTTP + line.strip('\n') + PORT for line in file.readlines()]
        return ip_addresses

    def getStatus(self):
        print("=== Get Status ===")

        for address in self.__addresses:
            utils.get_status(address)

    def createCollaborator(self):
        print("=== Creating %s collaborators ===" % self.__collab_type)
        utils.parallelize(utils.create_collab, self.__collab_type,
                          self.__addresses)

    def startCollaborator(self):
        print("=== Starting %s collaborators ===" % self.__collab_type)
        utils.parallelize(utils.start_collab, self.__collab_type,
                          self.__addresses)

    def stopwritingCollaborator(self):
        print("=== Stoping (writers) %s collaborators ==="
              % self.__collab_type)
        utils.parallelize(utils.stopwriting_collab, self.__collab_type,
                          self.__addresses)

    def stopreadingCollaborator(self):
        print("=== Stoping (readers) %s collaborators ==="
              % self.__collab_type)
        utils.parallelize(utils.stopreading_collab, self.__collab_type,
                          self.__addresses)

