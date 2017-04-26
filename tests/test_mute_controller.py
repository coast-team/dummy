from collaborator.mute_collaborator.mute_collaborator import MuteCollaborator
from collaborator.controller import Controller
from collaborator.config_loader import ConfigLoader
from mock import Mock
import os
import pytest


path_to_config_suffix = '/config_files/config_test_success.ini'

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


def start_mute():
    pass


def kill_reader_mute():
    pass


def kill_writer_mute():
    pass


"""
Fixtures
"""


@pytest.fixture
def get_path_to_config_file():
    dir_path_prefix = os.getcwd()
    return dir_path_prefix + path_to_config_suffix


@pytest.fixture
def get_mute_collaborator():
    path_to_config = get_path_to_config_file()
    return Mock(spec=MuteCollaborator)


@pytest.fixture
def get_contoroller(monkeypatch, get_mute_collaborator):
    mute_collab = Mock(return_value=get_mute_collaborator)
    monkeypatch.setattr('collaborator.controller.MuteCollaborator',
                        mute_collab)

    get_mute_collaborator.getConfig = get_mute_config
    get_mute_collaborator.start = start_mute

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


def test_createMuteCollaborator(monkeypatch, get_mute_collaborator):
    controller = get_contoroller(monkeypatch, get_mute_collaborator)
    res = controller.createMuteCollaborator()
    assert res['collaborator'] == 'Mute Collaborator'
    assert res['refresh_rate'] == 500
    assert res['url_targeted'] == "http://www.coedit.re/doc/toto"
    assert res['writing_speed'] == 5


def test_startMuteCollaborator(monkeypatch, get_mute_collaborator):
    controller = get_contoroller(monkeypatch, get_mute_collaborator)
    res = controller.startMuteCollaborator()
    assert res['status'] == "Collaborator is starting"

    controller = get_contoroller(monkeypatch, get_mute_collaborator)
    controller.createMuteCollaborator()
    res = controller.startMuteCollaborator()
    assert res['status'] == "Collaborator is starting"


def test_stopWritingMuteCollaborator(monkeypatch, get_mute_collaborator):
    controller = get_contoroller(monkeypatch, get_mute_collaborator)
    controller.startMuteCollaborator()
    res = controller.stopWritingMuteCollaborator()
    assert res['status'] == "Collaborator is being stoped"
