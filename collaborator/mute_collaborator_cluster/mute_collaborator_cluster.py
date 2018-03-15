from collaborator.collaborator import Collaborator
from collaborator.mute_collaborator.mute_write_component import (
    MuteWriteComponent)
import time

class MuteCollaboratorCluseter(Collaborator):

    def __init__(self, path_to_config, id):
        Collaborator.__init__(self, id, path_to_config)
        self.__config_mute = self._configurationLoader.getMuteConfig()

        self.__config_mute_cluster = self._configurationLoader.getMuteClusterConfig()

        cluster_size = self.__config_mute_cluster['clusterSize']

        drivers = [self.getDriver() for i in range(cluster_size)]
        
        writer_record_path = self.__config_mute['writerRecordPath']

        self.__mute_writers = []
        for i in range(cluster_size):
            
            mute_writer = MuteWriteComponent(self,
                                            drivers[i],
                                            self.__config_mute['splitter'],
                                            writer_record_path,
                                            self.__config_mute[
                                                'writingSpeed'])
            self.__mute_writers.append(mute_writer)
        
    def getConfig(self):
        config = super(MuteCollaboratorCluseter, self).getConfig()

        config['collaborator'] = 'Mute Collaborator'
        config['writing_speed'] = self.__config_mute['writingSpeed']
        config['refresh_rate'] = self.__config_mute['refreshRate']

        return config
        
    def run(self):
        for writer in self.__mute_writers:
            writer.start()

    def killWriter(self):
        for writer in self.__mute_writers:
            writer.kill()
        for writer in self.__mute_writers:
            writer.join()

    def getTracesPath(self):
        traces_path = []
        traces_path.append(self.__config_mute['writerRecordPath'])
        return traces_path

