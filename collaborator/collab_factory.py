from collaborator.mute_collaborator.mute_collaborator import MuteCollaborator
from collaborator.mute_collaborator_cluster.mute_collaborator_cluster import MuteCollaboratorCluseter

class CollaboratorFactory(object):
    """docstring for CollaboratorFactory."""
    def createCollaborator(self, collab_type, path_to_config, collab_id):
        if collab_type == 'mute':
            return MuteCollaborator(path_to_config, collab_id)
        elif collab_type == 'mute-cluster':
            return MuteCollaboratorCluseter(path_to_config, collab_id)

        return MuteCollaborator(path_to_config, collab_id)
