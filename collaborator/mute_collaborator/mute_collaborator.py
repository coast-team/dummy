from collaborator.collaborator import Collaborator
from collaborator.mute_collaborator.mute_read_component import (
    MuteReadComponent)
from collaborator.mute_collaborator.mute_write_component import (
    MuteWriteComponent)
import time


class MuteCollaborator(Collaborator):
    """docstring for MuteCollaborator."""
    def __init__(self, path_to_config, id):
        Collaborator.__init__(self, id, path_to_config)
        self.__config_mute = self._configurationLoader.getMuteConfig()

        reader_driver = self.getDriver()
        writer_driver = self.getDriver()

        reader_record_path = self.__config_mute['readerRecordPath'] + str(id)
        writer_record_path = self.__config_mute['writerRecordPath'] + str(id)

        self.__mute_reader = MuteReadComponent(
            self.__config_mute['refreshRate'],
            reader_driver,
            self.__config_mute['splitter'],
            reader_record_path)

        self.__mute_writer = MuteWriteComponent(writer_driver,
                                                self.__config_mute['splitter'],
                                                writer_record_path,
                                                self.__config_mute[
                                                    'writingSpeed'])

    def getConfig(self):
        config = super(MuteCollaborator, self).getConfig()

        config['collaborator'] = 'Mute Collaborator'
        config['writing_speed'] = self.__config_mute['writingSpeed']
        config['refresh_rate'] = self.__config_mute['refreshRate']

        return config

    def run(self):
        self.__mute_reader.start()
        self.__mute_writer.start()

    def killWriter(self):
        self.__mute_writer.kill()
        self.__mute_writer.join()

    def killReader(self):
        time.sleep(self._config['waitingTime'])
        self.__mute_reader.kill()
        self.__mute_reader.join()
