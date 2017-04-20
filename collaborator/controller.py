from collaborator.collaborator_config_loader import CollaboratorConfigLoader
from collaborator.dummy_error.configfile_error import ConfigfileError
from collaborator.mute_collaborator.mute_collaborator import MuteCollaborator
import sys
import uuid

NOT_INITIALIZED = 'Not yet initialized'
RUNNING = 'Running'
COLLABORATOR_INSTANCIATED = 'Collaborator is instanciated'
COLLABORATOR_PROCESSING = 'Collaborator is processing'
COLLABORATOR_BEING_STOP = 'Collaborator is being stoped'
CONFIG_FILE_ERROR = 'File is not well formatted'


class Controller(object):
    """docstring for Controller."""
    def __init__(self, path_to_config):
        self.__path_to_config = path_to_config
        self.__id = str(uuid.uuid4())
        self.__summary = {'status': NOT_INITIALIZED}
        self.__collaborator = None
        self.__config = {}
        try:
            self.__configurationLoader = CollaboratorConfigLoader(
                path_to_config)
            self.__config = self.__configurationLoader.getDefaultConfig()

            self.__summary['status'] = RUNNING
        except ConfigfileError as e:
            print("Erreur lors du chargement du fichier de config")
            self.__summary['status'] = CONFIG_FILE_ERROR
            self.__summary['error_msg'] = str(e)

    def getConfig(self):
        return self.__config

    def getStatus(self):
        return self.__summary

    """
    MUTE Collaborator interactions
    """

    def createMuteCollaborator(self):
        response = {}

        try:
            self.__collaborator = MuteCollaborator(self.__path_to_config,
                                                   self.__id)
            self.__summary['status'] = COLLABORATOR_INSTANCIATED

            response = self.__collaborator.getConfig()
        except ConfigfileError:
            self.__collaborator = None
            self.__summary['status'] = CONFIG_FILE_ERROR

            response['status'] = self.__summary['status']
        return response

    def startMuteCollaborator(self):
        response = {}
        if self.__summary['status'] != COLLABORATOR_INSTANCIATED:
            response = self.createMuteCollaborator
            if self.__collaborator is None:
                return response
        self.__collaborator.start()
        self.__summary['status'] = COLLABORATOR_PROCESSING
        response['status'] = 'Collaborator is starting'
        return response

    def stopWritingMuteCollaborator(self):
        response = {}
        if(self.__collaborator is not None
           and self.__summary['status'] == COLLABORATOR_PROCESSING):
            self.__collaborator.killWriter()
            self.__summary['status'] = COLLABORATOR_BEING_STOP
        else:
            response['error'] = 'Collaborator is not ready'

        response['status'] = self.__summary['status']

        return response

    def stopReadingMuteCollaborator(self):
        response = {}
        if(self.__collaborator is not None
           and self.__summary['status'] == COLLABORATOR_BEING_STOP):
            self.__collaborator.killReader()
            self.__summary['status'] = COLLABORATOR_BEING_STOP
        else:
            response['error'] = 'Collaborator is not ready yet'

        response['status'] = self.__summary['status']

        return response

    def retrieveMuteCollabRecords(self):
        response = {}
        pass