from collaborator.dummy_error.configfile_error import ConfigfileError
import configparser
import os


class ConfigLoader(object):
    """docstring for CollaboratorConfigLoader."""
    def __init__(self, path_to_config):
        self.__parser = configparser.ConfigParser()
        self.__parser.read(path_to_config)

    def getDefaultConfig(self):
        default_config = {}

        try:
            default_config['port'] = int(self.__parser['DEFAULT']['port'])
            if 'address' in self.__parser['DEFAULT']:
                default_config['address'] = self.__parser['DEFAULT']['address']
            return default_config
        except KeyError:
            print('Une clé est manquante dans le fichier de config')
            print("Une erreur s'est produite dans la section DEFAULT")
            raise ConfigfileError()
        except ValueError:
            print("une valeur est incorrecte")
            print("Une erreur s'est produite dans la section DEFAULT")
            raise ConfigfileError()

    def getCollaboratorConfig(self):
        collab_config = {}

        try:
            collab_config['chromeLocation'] = self.__parser['COLLABORATOR'][
                 'chromeLocation']
            collab_config['noDisplay'] = self.__parser[
                'COLLABORATOR'].getboolean('noDisplay')
            collab_config['chromeDriverLocation'] = self.__parser[
                'COLLABORATOR']['chromeDriverLocation']
            collab_config['waitingTime'] = int(self.__parser['COLLABORATOR'][
                 'waitingTime'])
            collab_config['url'] = self.__parser['COLLABORATOR']['url']
            collab_config['loadingTime'] = int(self.__parser['COLLABORATOR'][
                'loadingTime'])
        except KeyError:
            print('Une clé est manquante dans le fichier de config')
            print("Une erreur s'est produite dans la section COLLABORATOR")
            raise ConfigfileError()
        except ValueError:
            print("une valeur est incorrecte")
            print("Une erreur s'est produite dans la section COLLABORATOR")
            raise ConfigfileError()

        return collab_config

    def getMuteConfig(self):
        mute_config = {}

        try:
            mute_config['refreshRate'] = int(self.__parser['MUTE'][
                'refreshRate'])
            mute_config['isBasicBehavior'] = self.__parser['MUTE'].getboolean(
                'isBasicBehavior')
            mute_config['readerRecordPath'] = self.__parser['MUTE'][
                'readerRecordPath']
            mute_config['writerRecordPath'] = self.__parser['MUTE'][
                'writerRecordPath']
            mute_config['splitter'] = self.__parser['MUTE']['splitter']
            if mute_config['refreshRate']:
                mute_config['writingSpeed'] = int(self.__parser['MUTE']
                                                  ['writingSpeed'])
        except KeyError:
            print('Une clé est manquante dans le fichier de config')
            print("Une erreur s'est produite dans la section MUTE")
            raise ConfigfileError()
        except ValueError:
            print("une valeur est incorrecte")
            print("Une erreur s'est produite dans la section MUTE")
            raise ConfigfileError()

        return mute_config
