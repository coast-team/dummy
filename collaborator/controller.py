from collaborator.config_loader import ConfigLoader
from collaborator.dummy_error.configfile_error import ConfigfileError
from collaborator.dummy_error.webdriver_error import WebdriverError
from collaborator.collab_factory import CollaboratorFactory
import sys
import uuid

NOT_INITIALIZED = 'Not yet initialized'
RUNNING = 'Running'
WEBDRIVER_ERROR = 'Webdriver is not available'
COLLABORATOR_INSTANCIATED = 'Collaborator is instanciated'
COLLABORATOR_PROCESSING = 'Collaborator is processing'
COLLABORATOR_BEING_STOP = 'Collaborator is being stoped'
COLLABORATOR_STOP = 'Collaborator has been stoped'
CONFIG_FILE_ERROR = 'File is not well formatted'


class Controller(object):
    """docstring for Controller."""
    def __init__(self, path_to_config):
        self.__path_to_config = path_to_config
        self.__id = str(uuid.uuid4())
        self.__summary = {'status': NOT_INITIALIZED}
        self.__collab_factory = CollaboratorFactory()
        self.__collaborator = None
        self.__config = {}

        try:
            self.__configurationLoader = ConfigLoader(
                path_to_config)
            self.__config = self.__configurationLoader.getDefaultConfig()

            self.__summary['status'] = RUNNING
        except ConfigfileError as e1:
            print("Erreur lors du chargement du fichier de config")
            self.__summary['status'] = CONFIG_FILE_ERROR
            self.__summary['error_msg'] = str(e1)
        except WebdriverError as e2:
            self.__summary['status'] = WEBDRIVER_ERROR
            self.__summary['controller-error'] = str(e1)

    def getConfig(self):
        return self.__config

    def getStatus(self):
        return self.__summary

    def createCollaborator(self, collab_type):
        response = {}
        try:
            self.__collaborator = self.__collab_factory.createCollaborator(
                collab_type,
                self.__path_to_config,
                self.__id)
            self.__summary['status'] = COLLABORATOR_INSTANCIATED

            response = self.__collaborator.getConfig()
        except ConfigfileError as e1:
            self.__collaborator = None
            self.__summary['status'] = CONFIG_FILE_ERROR
            self.__summary['error_msg'] = str(e1)
        except WebdriverError as e2:
            self.__summary['status'] = WEBDRIVER_ERROR
            self.__summary['controller-error'] = str(e2)

            response['status'] = self.__summary['status']
        return response

    def startCollaborator(self, collab_type):
        response = {}
        if self.__summary['status'] != COLLABORATOR_INSTANCIATED:
            response = self.createCollaborator(collab_type)
            if self.__collaborator is None:
                return response
        self.__collaborator.start()
        self.__summary['status'] = COLLABORATOR_PROCESSING
        response['status'] = 'Collaborator is starting'
        response['collaborator-errors'] = self.__collaborator.getErrors()
        return response

    def stopWritingCollaborator(self, collab_type):
        response = {}
        if(self.__collaborator is not None
           and self.__summary['status'] == COLLABORATOR_PROCESSING):
            self.__collaborator.killWriter()
            self.__summary['status'] = COLLABORATOR_BEING_STOP
            response['collaborator-errors'] = self.__collaborator.getErrors()
        else:
            self.__summary['controller-error'] = 'Collaborator is not ready'
            response['controller-error'] = self.__summary['controller-error']

        response['status'] = self.__summary['status']
        return response

    def stopReadingCollaborator(self, collab_type):
        response = {}
        if(self.__collaborator is not None
           and self.__summary['status'] == COLLABORATOR_BEING_STOP):
            self.__collaborator.killReader()
            self.__summary['status'] = COLLABORATOR_STOP
        else:
            self.__summary['controller-error'] = 'Collaborator is not ready'
            response['controller-error'] = self.__summary['controller-error']

        response['status'] = self.__summary['status']

        return response

    def retrieveCollabRecords(self, collab_type):
        response = {}
        response['status'] = self.__summary['status']

        if self.__collaborator is None:
            self.__summary['controller-error'] = 'Collaborator is not ready'
            response['controller-error'] = self.__summary['controller-error']
            return response

        traces_path = self.__collaborator.getTracesPath()
        traces = []

        for path in traces_path:
            with open(path, 'r') as trace:
                lines = [line.strip('\n') for line in trace.readlines()]
                traces.append(lines)
        response['traces'] = traces
        return response
