from collaborator.mute_collaborator.mute_collaborator import MuteCollaborator
from collaborator.controller import Controller
from collaborator.config_loader import ConfigLoader
from mock import Mock
import os
import pytest

COLLAB_TYPES = ['mute']

path_to_config_suffix = '/config_files/config_test_success.ini'

"""
Mock : Collaborator
"""
def trivial():
    pass

"""
Mock : Mute Collaborator
"""

@pytest.fixture
def get_mute_config():
    return {
        "collaborator": "Mute Collaborator",
        "refresh_rate": 500,
        "status": "RUNNING",
        "url_targeted": "http://www.coedit.re/doc/toto",
        "writing_speed": 5
        }

"""
Fixtures
"""


@pytest.fixture
def get_path_to_config_file():
    dir_path_prefix = os.getcwd()
    return dir_path_prefix + path_to_config_suffix


@pytest.fixture
def get_mute_collaborator():
    mocked_mute = Mock(spec=MuteCollaborator)
    mocked_mute.getConfig = get_mute_config
    mocked_mute.start = trivial
    mocked_mute.killWriter = trivial
    mocked_mute.killReader = trivial
    return mocked_mute


@pytest.fixture
def get_contoroller(monkeypatch, get_mute_collaborator):
    mute_collab = Mock(return_value=get_mute_collaborator)
    monkeypatch.setattr('collaborator.collab_factory.MuteCollaborator',
                        mute_collab)

    path_to_config = get_path_to_config_file()
    return Controller(path_to_config)


"""
TESTS
"""

def test_controller(monkeypatch, get_mute_collaborator):
    controller = get_contoroller(monkeypatch, get_mute_collaborator)

    config = controller.getConfig()
    assert config['port'] == 8000

    status = controller.getStatus()
    assert status['status'] == 'Running'

@pytest.mark.parametrize("collab_type", COLLAB_TYPES)
def test_createMuteCollaborator(monkeypatch, get_mute_collaborator, collab_type):
    controller = get_contoroller(monkeypatch, get_mute_collaborator)

    if collab_type == 'mute':
        expected = get_mute_config()
    else :
        expected = get_mute_config() #Mute collaborator is the default collaborator

    res = controller.createCollaborator(collab_type)

    assert res['collaborator'] == expected['collaborator']
    assert res['refresh_rate'] == expected['refresh_rate']
    assert res['url_targeted'] == expected['url_targeted']
    assert res['writing_speed'] == expected['writing_speed']

@pytest.mark.parametrize("collab_type", COLLAB_TYPES)
def test_startMuteCollaborator(monkeypatch, get_mute_collaborator, collab_type):
    controller = get_contoroller(monkeypatch, get_mute_collaborator)

    res = controller.startCollaborator(collab_type)
    assert res['status'] == "Collaborator is starting"

    controller = get_contoroller(monkeypatch, get_mute_collaborator)
    controller.createCollaborator(collab_type)
    res = controller.startCollaborator(collab_type)
    assert res['status'] == "Collaborator is starting"

@pytest.mark.parametrize("collab_type", COLLAB_TYPES)
def test_stopWritingMuteCollaborator(monkeypatch, get_mute_collaborator, collab_type):
    controller = get_contoroller(monkeypatch, get_mute_collaborator)
    controller.startCollaborator(collab_type)
    res = controller.stopWritingCollaborator(collab_type)
    assert res['status'] == "Collaborator is being stoped"
