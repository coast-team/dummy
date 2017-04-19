from collaborator.dummy_error.configfile_error import ConfigfileError
import configparser
import os


class CollaboratorConfigLoader(object):
    """docstring for CollaboratorConfigLoader."""
    def __init__(self, path_to_config):
        self.__parser = configparser.ConfigParser()
        self.__parser.read(path_to_config)

    def getDefaultConfig(self):
        default_config = {}

        try:
            default_config['chromeLocation'] = self.__parser['DEFAULT'][
                 'chromeLocation']
            default_config['chromeDriverLocation'] = self.__parser['DEFAULT'][
                 'chromeDriverLocation']
            default_config['waitingTime'] = self.__parser['DEFAULT'][
                 'waitingTime']
            default_config['url'] = self.__parser['DEFAULT']['url']
            return default_config
        except KeyError:
            print("Une erreur s'est produite dans la section DEFAULT")
            raise ConfigfileError()

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
            return mute_config
        except KeyError:
            print("Une erreur s'est produite dans la section MUTE")
            raise ConfigfileError()
